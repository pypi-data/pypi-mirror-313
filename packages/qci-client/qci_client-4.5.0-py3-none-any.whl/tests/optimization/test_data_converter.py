# Copyright 2023-2024, Quantum Computing Incorporated
"""Test for data conversion functions."""

import time
import unittest

import networkx as nx
import numpy as np
import pytest
import scipy.sparse as sp

from qci_client.optimization.data_converter import data_to_json


@pytest.mark.offline
class TestDataToJson(unittest.TestCase):
    """Test suite for data conversion to JSON."""

    def test_file_type_assert(self):
        """Test file generation for bad file type."""
        # test file_type assertion
        with self.assertRaises(AssertionError) as context:
            data_to_json(
                file={"file_config": {"graph_partitioning_results": {"data": []}}}
            )

        self.assertEqual(
            str(context.exception),
            "unsupported file type, must be one of ['constraints', 'graph', "
            "'hamiltonian', 'objective', 'polynomial', 'qubo']",
        )

    def test_graph_file_body(self):
        """Test file generation for graph data."""
        graph_file = {
            "file_name": "graph.json",
            "file_config": {"graph": {"data": nx.Graph((((1, 2), (1, 3))))}},
        }
        expected = {
            "file_name": "graph.json",
            "file_config": {
                "graph": {
                    "num_edges": 2,
                    "num_nodes": 3,
                    "directed": False,
                    "multigraph": False,
                    "graph": {},
                    "nodes": [{"id": 1}, {"id": 2}, {"id": 3}],
                    "links": [{"source": 1, "target": 2}, {"source": 1, "target": 3}],
                },
            },
        }
        got = data_to_json(file=graph_file)
        self.assertDictEqual(got, expected)

        graph_file["file_config"]["graph"]["data"] = []

        with self.assertRaises(AssertionError) as context:
            data_to_json(file=graph_file)

        self.assertEqual(
            str(context.exception), "file type 'graph' data must be type networkx.Graph"
        )

    @pytest.mark.timing
    def test_large_data_conversion(self):
        """Test file generation for large data is sufficiently fast."""
        large_qubo = np.random.normal(size=(3000, 3000))
        large_qubo = large_qubo + large_qubo.T
        start = time.perf_counter()
        data_to_json(file={"file_config": {"qubo": {"data": large_qubo}}})
        end = time.perf_counter()
        conversion_time = end - start

        self.assertTrue(
            conversion_time < 5,
            msg=f"Matrix conversion to JSON took too long: 5s <= {conversion_time}s.",
        )

    def test_type_not_graph_check(self):
        """Test file generation for mismatched data and problem types."""
        bad_hamiltonian_file = {
            "file_config": {
                "hamiltonian": {
                    "num_variables": 3,
                    "data": nx.Graph((((1, 2), (1, 3)))),
                }
            }
        }

        with self.assertRaises(AssertionError) as context:
            data_to_json(file=bad_hamiltonian_file)

        self.assertEqual(
            str(context.exception),
            "file type 'hamiltonian' does not support networkx.Graph data",
        )

    def test_assert_type_not_list(self):
        """Test file generation for improperly formatted qubo data."""
        bad_qubo_file = {
            "file_config": {
                "qubo": {
                    "num_variables": 3,
                    "data": [[1, -1], [-1, 1]],
                }
            }
        }

        with self.assertRaises(ValueError) as context:
            data_to_json(file=bad_qubo_file)

        self.assertEqual(
            str(context.exception),
            "file type 'qubo' only supports numpy.ndarray and scipy.sparse.spmatrix "
            "data types, got '<class 'list'>'",
        )

    def test_hamiltonian_file_body(self):
        """Test file generation for a hamiltonian matrix."""
        expected = {
            "file_name": "hamiltonian.json",
            "file_config": {
                "hamiltonian": {
                    "num_variables": 2,
                    "data": [
                        {"i": 0, "j": 0, "val": -1.0},
                        {"i": 0, "j": 1, "val": 1.0},
                        {"i": 0, "j": 2, "val": 1.0},
                        {"i": 1, "j": 0, "val": 1.0},
                        {"i": 1, "j": 1, "val": -1.0},
                        {"i": 1, "j": 2, "val": 1.0},
                    ],
                }
            },
        }

        ham_np = np.array([[-1, 1, 1], [1, -1, 1]])

        file = {
            "file_name": "hamiltonian.json",
            "file_config": {"hamiltonian": {"data": ham_np}},
        }
        self.assertDictEqual(data_to_json(file=file), expected)

        file = {
            "file_name": "hamiltonian.json",
            "file_config": {"hamiltonian": {"data": sp.dok_matrix(ham_np)}},
        }
        self.assertDictEqual(data_to_json(file=file), expected)

    def test_qubo_file_body(self):
        """Test file generation for a qubo matrix."""
        expected = {
            "file_name": "qubo.json",
            "file_config": {
                "qubo": {
                    "num_variables": 2,
                    "data": [
                        {"i": 0, "j": 0, "val": -1.0},
                        {"i": 0, "j": 1, "val": 1.0},
                        {"i": 1, "j": 0, "val": 1.0},
                        {"i": 1, "j": 1, "val": -1.0},
                    ],
                }
            },
        }

        q_obj_np = np.array([[-1.0, 1.0], [1.0, -1.0]])

        file = {"file_name": "qubo.json", "file_config": {"qubo": {"data": q_obj_np}}}
        self.assertDictEqual(data_to_json(file=file), expected)

        file = {
            "file_name": "qubo.json",
            "file_config": {"qubo": {"data": sp.dok_matrix(q_obj_np)}},
        }
        self.assertDictEqual(data_to_json(file=file), expected)

    def test_objective_file_body(self):
        """Test file generation for an objective matrix."""
        expected = {
            "file_name": "objective.json",
            "file_config": {
                "objective": {
                    "num_variables": 2,
                    "data": [
                        {"i": 0, "j": 0, "val": -1.0},
                        {"i": 0, "j": 1, "val": 1.0},
                        {"i": 1, "j": 0, "val": 1.0},
                        {"i": 1, "j": 1, "val": -1.0},
                    ],
                }
            },
        }

        obj_np = np.array([[-1.0, 1.0], [1.0, -1.0]])

        file = {
            "file_name": "objective.json",
            "file_config": {"objective": {"data": obj_np}},
        }
        self.assertDictEqual(data_to_json(file=file), expected)

        file = {
            "file_name": "objective.json",
            "file_config": {"objective": {"data": sp.dok_matrix(obj_np)}},
        }
        self.assertDictEqual(data_to_json(file=file), expected)

    def test_constraints_file_body(self):
        """Test file generation for a constraints matrix."""
        expected = {
            "file_name": "constraints.json",
            "file_config": {
                "constraints": {
                    "num_constraints": 1,
                    "num_variables": 2,
                    "data": [
                        {"i": 0, "j": 0, "val": 1.0},
                        {"i": 0, "j": 1, "val": 1.0},
                        {"i": 0, "j": 2, "val": -2.0},
                    ],
                }
            },
        }

        con_np = np.array([[1.0, 1.0, -2.0]])

        file = {
            "file_name": "constraints.json",
            "file_config": {"constraints": {"data": con_np}},
        }
        self.assertDictEqual(data_to_json(file=file), expected)

        file = {
            "file_name": "constraints.json",
            "file_config": {"constraints": {"data": sp.dok_matrix(con_np)}},
        }
        self.assertDictEqual(data_to_json(file=file), expected)

    def test_polynomial_file_body(self):
        """Test file generation for a polynomial."""
        data = [
            {"idx": [0, 0, 0], "val": 1.0},
            {"idx": [0, 0, 1], "val": 2.0},
            {"idx": [0, 0, 2], "val": 3.0},
            {"idx": [0, 1, 1], "val": 4.0},
            {"idx": [0, 1, 2], "val": 5.0},
            {"idx": [0, 2, 2], "val": 6.0},
            {"idx": [1, 1, 1], "val": 7.0},
            {"idx": [1, 1, 2], "val": 8.0},
            {"idx": [1, 2, 2], "val": 9.0},
            {"idx": [2, 2, 2], "val": 10.0},
        ]

        expected = {
            "file_name": "polynomial.json",
            "file_config": {
                "polynomial": {
                    "min_degree": 0,
                    "max_degree": 3,
                    "num_variables": 2,
                    "data": data,
                }
            },
        }

        file = {
            "file_name": "polynomial.json",
            "file_config": {
                "polynomial": {
                    "min_degree": 0,
                    "max_degree": 3,
                    "num_variables": 2,
                    "data": data,
                }
            },
        }
        self.assertDictEqual(data_to_json(file=file), expected)
