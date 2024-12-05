# Copyright 2023-2024, Quantum Computing Incorporated
"""Functions for data conversion."""

import logging
import time

import networkx as nx
import numpy as np
import scipy.sparse as sp

from qci_client.optimization import utilities
from qci_client.optimization import enum

# We want to limit the memory size of each uploaded chunk to be safely below the max of 15 * MebiByte (~15MB).
# See https://git.qci-dev.com/qci-dev/qphoton-files-api/-/blob/main/service/files.go#L32.
MEMORY_MAX: int = 8 * 1000000  # 8MB


def data_to_json(*, file: dict) -> dict:  # pylint: disable=too-many-branches
    """
    Converts data in file input into JSON-serializable dictionary that can be passed to Qatalyst REST API

    Args:
        file: file dictionary whose data of type numpy.ndarray, scipy.sparse.spmatrix, or networkx.Graph is to be converted

    Returns:
        file dictionary with JSON-serializable data
    """
    start_time_s = time.perf_counter()

    file_config, file_type = utilities.get_file_config(file=file)

    if file_type not in enum.FILE_TYPES_JOB_INPUTS:
        input_file_types = [
            input_file_type.value for input_file_type in enum.FILE_TYPES_JOB_INPUTS
        ]
        input_file_types.sort()
        raise AssertionError(
            f"unsupported file type, must be one of {input_file_types}"
        )

    data = file["file_config"][file_type.value]["data"]

    if file_type == enum.FileType.GRAPH:
        if not isinstance(data, nx.Graph):
            raise AssertionError(
                f"file type '{file_type.value}' data must be type networkx.Graph"
            )

        file_config = {
            **nx.node_link_data(data),
            "num_edges": data.number_of_edges(),
            "num_nodes": data.number_of_nodes(),
        }
    elif file_type in enum.FILE_TYPES_JOB_INPUTS_MATRIX:
        if isinstance(data, nx.Graph):
            raise AssertionError(
                f"file type '{file_type.value}' does not support networkx.Graph data"
            )

        data_ls = []

        if sp.isspmatrix_dok(data):
            for idx, val in zip(data.keys(), data.values()):
                # dok type has trouble subsequently serializing to json without type
                # casts. For example, uint16 and float32 cause problems.
                data_ls.append({"i": int(idx[0]), "j": int(idx[1]), "val": float(val)})
        elif sp.isspmatrix(data) or isinstance(data, np.ndarray):
            data = sp.coo_matrix(data)

            for i, j, val in zip(
                data.row.tolist(), data.col.tolist(), data.data.tolist()
            ):
                data_ls.append({"i": i, "j": j, "val": val})
        else:
            raise ValueError(
                f"file type '{file_type.value}' only supports numpy.ndarray and "
                f"scipy.sparse.spmatrix data types, got '{type(data)}'"
            )

        file_config = {"data": data_ls}
        rows, cols = data.get_shape()

        if file_type == enum.FileType.CONSTRAINTS:
            # Constraints matrix is [A | -b]
            file_config.update({"num_constraints": rows, "num_variables": cols - 1})
        else:
            # This works for hamiltonians, qubos, and objectives.
            file_config["num_variables"] = rows
    else:
        # Polynomial file types do not require translation.
        file_config = file["file_config"][file_type.value]

    logging.debug(
        "Time to convert data to json: %s s.", time.perf_counter() - start_time_s
    )

    return {
        "file_name": file.get("file_name", f"{file_type.value}.json"),
        "file_config": {file_type.value: file_config},
    }
