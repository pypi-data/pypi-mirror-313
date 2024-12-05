# Copyright 2023-2024, Quantum Computing Incorporated
"""Utilities, especially for creating request bodies."""

import gzip
from io import BytesIO
import json
from math import floor
import sys
from typing import Generator, Tuple

from qci_client.optimization import types
from qci_client.optimization import enum

# We want to limit the memory size of each uploaded chunk to be safely below the max of
# 15 * MebiByte (~15MB). See https://git.qci-dev.com/qci-dev/optimization-files-api/.
MEMORY_MAX: int = 8 * 1000000  # 8MB


def get_file_type(*, file: dict) -> enum.FileType:
    """Get file type from a file."""
    file_config_keys = list(file["file_config"].keys())

    if len(file_config_keys) != 1:
        raise ValueError(
            "improper number of files specified in file_config (should be exactly one)"
        )

    return enum.FileType(file_config_keys[0])


def get_file_config(*, file: dict) -> Tuple[dict, enum.FileType]:
    """Get file configuration and file type from a file."""
    file_type = get_file_type(file=file)

    return file["file_config"][file_type.value], file_type


def get_post_request_body(*, file: dict) -> types.MetadataPostRequestBody:
    """Format metadata body."""
    file_config, file_type = get_file_config(file=file)
    optional_fields = {}

    if "file_name" in file:
        optional_fields["file_name"] = file["file_name"]

    if file_type == enum.FileType.CONSTRAINTS:
        return types.MetadataPostRequestBody(
            **optional_fields,
            file_config=types.ConstraintsMetadataConfig(
                constraints=types.ConstraintsMetadata(
                    num_constraints=file_config["num_constraints"],
                    num_variables=file_config["num_variables"],
                )
            ),
        )

    if file_type == enum.FileType.GRAPH:
        if "directed" in file_config:
            optional_fields["directed"] = file_config["directed"]

        if "multigraph" in file_config:
            optional_fields["multigraph"] = file_config["multigraph"]

        if "graph" in file_config:
            optional_fields["graph"] = file_config["graph"]

        return types.MetadataPostRequestBody(
            **optional_fields,
            file_config=types.GraphMetadataConfig(
                graph=types.GraphMetadata(
                    **optional_fields,
                    num_edges=file_config["num_edges"],
                    num_nodes=file_config["num_nodes"],
                )
            ),
        )

    if file_type == enum.FileType.HAMILTONIAN:
        return types.MetadataPostRequestBody(
            **optional_fields,
            file_config=types.HamiltonianMetadataConfig(
                hamiltonian=types.HamiltonianMetadata(
                    num_variables=file_config["num_variables"],
                )
            ),
        )

    if file_type == enum.FileType.OBJECTIVE:
        return types.MetadataPostRequestBody(
            **optional_fields,
            file_config=types.ObjectiveMetadataConfig(
                objective=types.ObjectiveMetadata(
                    num_variables=file_config["num_variables"],
                )
            ),
        )

    if file_type == enum.FileType.POLYNOMIAL:
        return types.MetadataPostRequestBody(
            **optional_fields,
            file_config=types.PolynomialMetadataConfig(
                polynomial=types.PolynomialMetadata(
                    min_degree=file_config["min_degree"],
                    max_degree=file_config["max_degree"],
                    num_variables=file_config["num_variables"],
                )
            ),
        )

    if file_type == enum.FileType.QUBO:
        return types.MetadataPostRequestBody(
            **optional_fields,
            file_config=types.QuboMetadataConfig(
                qubo=types.QuboMetadata(
                    num_variables=file_config["num_variables"],
                )
            ),
        )

    raise ValueError(f"unsupported/non-input file type: '{file_type.value}'")


def get_patch_request_body(*, file: dict) -> types.PartPatchRequestBody:
    """Format part body."""
    file_config, file_type = get_file_config(file=file)

    if file_type == enum.FileType.CONSTRAINTS:
        return types.PartPatchRequestBody(
            file_config=types.ConstraintsPartConfig(
                constraints=types.ConstraintsPart(data=file_config["data"])
            ),
        )

    if file_type == enum.FileType.GRAPH:
        return types.PartPatchRequestBody(
            file_config=types.GraphPartConfig(
                graph=types.GraphPart(
                    links=file_config["links"],
                    nodes=file_config["nodes"],
                )
            ),
        )

    if file_type == enum.FileType.HAMILTONIAN:
        return types.PartPatchRequestBody(
            file_config=types.HamiltonianPartConfig(
                hamiltonian=types.HamiltonianPart(data=file_config["data"])
            ),
        )

    if file_type == enum.FileType.OBJECTIVE:
        return types.PartPatchRequestBody(
            file_config=types.ObjectivePartConfig(
                objective=types.ObjectivePart(data=file_config["data"])
            ),
        )

    if file_type == enum.FileType.POLYNOMIAL:
        return types.PartPatchRequestBody(
            file_config=types.PolynomialPartConfig(
                polynomial=types.PolynomialPart(data=file_config["data"])
            ),
        )

    if file_type == enum.FileType.QUBO:
        return types.PartPatchRequestBody(
            file_config=types.QuboPartConfig(
                qubo=types.QuboPart(data=file_config["data"])
            ),
        )

    raise ValueError(f"unsupported/non-input file type: '{file_type.value}'")


def zip_payload(*, payload: types.PartPatchRequestBody) -> bytes:
    """
    :param payload: str - json contents of file to be zipped

    :return: zipped request_body
    """
    with BytesIO() as fileobj:
        with gzip.GzipFile(fileobj=fileobj, mode="w", compresslevel=6) as file:
            file.write(json.dumps(payload).encode("utf-8"))

        return fileobj.getvalue()


def file_part_generator(*, file: dict, compress: bool) -> Generator:
    """
    Break file-to-upload's data dictionary into chunks, formatting correctly with each
    returned chunk.

    :param file: file to break up into file parts
    :param compress: whether or not file parts are to be compressed

    :return: generator of (part_body, part_number) tuples
    """
    if compress:
        # The user has chosen to compress their files for upload we want a large
        # chunksize to try to maximize compression for each of the chunks.
        # Prior to merged stack, this value was 200000, which was too big in unit tests.
        data_chunk_size_max = 20000
    else:
        # We are using the multipart upload as a validated sharding system that is
        # similar to Mongo GridFS. Mongo recommends 256KB for that system, this value
        # keeps uploaded chunks below this value. After some testing, we decided to
        # limit this to chunks of 10000 elements for performance reasons.
        data_chunk_size_max = 10000

    file_config, file_type = get_file_config(file=file)

    if file_type in enum.FILE_TYPES_JOB_INPUTS_NON_GRAPH:
        return _data_generator(
            file_type=file_type,
            file_config=file_config,
            step_length=data_chunk_size_max,
        )

    if file_type == enum.FileType.GRAPH:
        return _graph_generator(
            file_type=file_type,
            file_config=file_config,
            step_length=data_chunk_size_max,
        )

    # For results data, the n^2 sized data is in the solutions field so chunk it up.
    if file_type in enum.FILE_TYPES_JOB_RESULTS:
        return _results_generator(
            file_type=file_type,
            file_config=file_config,
            step_length=_compute_results_step_len(data=file_config["solutions"][0]),
        )

    raise ValueError(f"unsupported file type: {file_type.value}")


def _get_size(*, obj, seen=None) -> int:
    """
    Recursively finds size of objects

    :param obj: data object to recursively compute size of
    :param seen: takes a set and is used in the recursive step only to record whether an
        object has been counted yet.

    :return int:
    """
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum(_get_size(obj=v, seen=seen) for v in obj.values())
        size += sum(_get_size(obj=k, seen=seen) for k in obj.keys())
    elif hasattr(obj, "__dict__"):
        size += _get_size(obj=obj.__dict__, seen=seen)
    elif hasattr(obj, "__iter__") and not isinstance(obj, (str, bytes, bytearray)):
        size += sum(_get_size(obj=i, seen=seen) for i in obj)
    return size


def _get_soln_size(*, soln):
    # Check whether first entry is a graph node/class assignment, e.g.,
    # {'id': 4, 'class': 2}.
    if isinstance(soln[0], dict):
        return _get_size(obj=soln)

    return sys.getsizeof(soln[0]) * len(soln)


def _compute_results_step_len(*, data: list) -> int:
    """
    Compute the step length for "chunking" the provided data.

    Args:
        data: A list of data

    Returns:
        The step length for "chunking" the data
    """
    # total mem size of soln vector
    soln_mem = _get_soln_size(soln=data)
    # num_vars * step_len < 30k => step_len < 30k/num_vars
    chunk_ratio = MEMORY_MAX / soln_mem
    step_len = max(floor(chunk_ratio), 1)

    return step_len


def _data_generator(
    *, file_type: enum.FileType, file_config: dict, step_length: int
) -> Generator:
    # data may be empty, so use max against 1.
    for part_number, i in enumerate(
        range(0, max(1, len(file_config["data"])), step_length)
    ):
        chunk = {
            "file_config": {
                file_type.value: {
                    "data": file_config["data"][i : i + step_length],
                }
            }
        }

        yield chunk, part_number + 1  #  content endpoint has 1-based uploads


def _graph_generator(
    *, file_type: enum.FileType, file_config: dict, step_length: int
) -> Generator:
    # links and nodes may both be empty, so use max against 1.
    for part_number, i in enumerate(
        range(
            0,
            max(1, len(file_config["links"]), len(file_config["nodes"])),
            step_length,
        )
    ):
        chunk = {
            "file_config": {
                file_type.value: {
                    "links": file_config["links"][i : i + step_length],
                    "nodes": file_config["nodes"][i : i + step_length],
                }
            }
        }

        yield chunk, part_number + 1  #  content endpoint has 1-based uploads


def _results_generator(
    *, file_type: enum.FileType, file_config: dict, step_length: int
) -> Generator:
    for part_number, i in enumerate(
        range(0, max(1, len(file_config["solutions"])), step_length)
    ):
        chunk = {"file_config": {file_type.value: {}}}

        for key, value in file_config.items():
            chunk["file_config"][file_type.value][key] = value[i : i + step_length]

        yield chunk, part_number + 1  #  content endpoint has 1-based uploads
