# pylint: disable=too-many-lines
# Copyright 2023-2024, Quantum Computing Incorporated
"""Test client for QCi's optimization API."""

from itertools import product
import unittest
import unittest.mock

import networkx as nx
import numpy as np
import pytest
import requests
import scipy.sparse as sp

import qci_client


@pytest.mark.offline
class TestClientOffline(unittest.TestCase):
    """Jobs-API-related test suite that can be run without backend."""

    def setUp(self):
        with pytest.MonkeyPatch().context() as mp:
            mp.setenv("QCI_TOKEN", "test_api_token")
            mp.setenv("QCI_API_URL", "test_url")
            self.client = qci_client.QciClient()
        self.job_id = "63b717a22da68618ec444eac"
        self.file_id = "73b717a22da68618ec444eab"

    def test_jobs_url(self) -> None:
        """Test getting jobs URL."""
        self.assertEqual(self.client.jobs_url, "test_url/optimization/v1/jobs")

    def test_get_job_id_url(self) -> None:
        """Test getting jobs URL for given job ID."""
        self.assertEqual(
            self.client.get_job_id_url(job_id=self.job_id),
            f"test_url/optimization/v1/jobs/{self.job_id}",
        )

    def test_get_job_status_url(self) -> None:
        """Test getting jobs-status URL for given job ID."""
        self.assertEqual(
            self.client.get_job_status_url(job_id=self.job_id),
            f"test_url/optimization/v1/jobs/{self.job_id}/status",
        )

    def test_get_job_metrics_url(self) -> None:
        """Test getting legacy jobs-metrics URL for given job ID."""
        self.assertEqual(
            self.client.get_job_metrics_url(job_id=self.job_id),
            f"test_url/optimization/v1/jobs/{self.job_id}/metrics",
        )

    def test_get_job_metrics_v1_url(self) -> None:
        """Test getting v1 jobs-metrics URL for given job ID."""
        self.assertEqual(
            self.client.get_job_metrics_v1_url(job_id=self.job_id),
            f"test_url/optimization/v1/jobs/{self.job_id}/metrics/v1",
        )

    def test_get_job_metrics_v2_url(self) -> None:
        """Test getting v2 jobs-metrics URL for given job ID."""
        self.assertEqual(
            self.client.get_job_metrics_v2_url(job_id=self.job_id),
            f"test_url/optimization/v1/jobs/{self.job_id}/metrics/v2",
        )

    def test_get_job_allocations_url(self) -> None:
        """Test getting jobs-allocations URL."""
        self.assertEqual(
            self.client.get_job_allocations_url(),
            "test_url/optimization/v1/jobs/allocations",
        )

    def test_files_url(self) -> None:
        """Test getting files URL."""
        self.assertEqual(self.client.files_url, "test_url/optimization/v1/files")

    def test_get_file_id_url(self) -> None:
        """Test getting files URL for given file ID."""
        self.assertEqual(
            self.client.get_file_id_url(file_id=self.file_id),
            f"test_url/optimization/v1/files/{self.file_id}",
        )

    def test_get_file_contents_url(self) -> None:
        """Test getting files contents URL for given file ID."""
        self.assertEqual(
            self.client.get_file_contents_url(file_id=self.file_id, part_number=24),
            f"test_url/optimization/v1/files/{self.file_id}/contents/24",
        )

    def test_build_job_body(self):
        """Test building of various jobs' request bodies."""

        with self.assertRaises(ValueError) as context:
            self.client.build_job_body(
                job_type="sample-qubo",
                job_params={},
                qubo_file_id="qubo_file_id",
            )

        self.assertEqual(
            str(context.exception),
            "no 'device_type' specified in job_params, must be one of "
            "('dirac-1', 'dirac-2', 'dirac-3', 'dirac-3_normalized_qudit', "
            "'dirac-3_qudit')",
        )

        with self.assertRaises(ValueError) as context:
            self.client.build_job_body(
                job_type="sample-hamiltonian-integer",
                job_params={"device_type": "dirac-3_normalized_qudit"},
                polynomial_file_id="polynomial_file_id",
            )

        self.assertEqual(
            str(context.exception),
            "sample-hamiltonian-integer not supported on dirac-3_normalized_qudit",
        )

        with self.assertRaises(ValueError) as context:
            self.client.build_job_body(
                job_type="sample-hamiltonian",
                job_params={"device_type": "dirac-3_qudit"},
                polynomial_file_id="polynomial_file_id",
            )

        self.assertEqual(
            str(context.exception),
            "sample-hamiltonian not supported on dirac-3_qudit",
        )

        constraint_body = self.client.build_job_body(
            job_type="sample-constraint",
            job_params={
                "device_type": "dirac-1",
                "alpha": 5.0,
            },
            objective_file_id="obj_fid",
            constraints_file_id="cons_fid",
            job_name="foobar_name",
            job_tags=["foobar_tag1", "foobar_tag2"],
        )

        self.assertDictEqual(
            constraint_body,
            {
                "job_submission": {
                    "job_name": "foobar_name",
                    "job_tags": ["foobar_tag1", "foobar_tag2"],
                    "problem_config": {
                        "quadratic_linearly_constrained_binary_optimization": {
                            "objective_file_id": "obj_fid",
                            "constraints_file_id": "cons_fid",
                            "alpha": 5.0,
                        }
                    },
                    "device_config": {"dirac-1": {}},
                }
            },
        )

        qubo_body = self.client.build_job_body(
            job_type="sample-qubo",
            job_params={
                "num_samples": 24,
                "device_type": "dirac-1",
            },
            qubo_file_id="qubo_fid",
            job_name="foobar_name",
        )

        self.assertDictEqual(
            qubo_body,
            {
                "job_submission": {
                    "job_name": "foobar_name",
                    "problem_config": {
                        "quadratic_unconstrained_binary_optimization": {
                            "qubo_file_id": "qubo_fid",
                        }
                    },
                    "device_config": {"dirac-1": {"num_samples": 24}},
                }
            },
        )

        hamiltonian_body = self.client.build_job_body(
            job_type="sample-hamiltonian",
            job_params={
                "num_samples": 24,
                "device_type": "dirac-3",
                "sum_constraint": 200,
                "solution_precision": 1,
            },
            hamiltonian_file_id="hamiltonian_fid",
            job_tags=["foobar_tag1", "foobar_tag2"],
        )

        self.assertDictEqual(
            hamiltonian_body,
            {
                "job_submission": {
                    "job_tags": ["foobar_tag1", "foobar_tag2"],
                    "problem_config": {
                        "normalized_qudit_hamiltonian_optimization": {
                            "hamiltonian_file_id": "hamiltonian_fid",
                        }
                    },
                    "device_config": {
                        "dirac-3_normalized_qudit": {
                            "num_samples": 24,
                            "sum_constraint": 200,
                            "solution_precision": 1,
                        }
                    },
                }
            },
        )

        hamiltonian_body = self.client.build_job_body(
            job_type="sample-hamiltonian",
            job_params={
                "device_type": "dirac-3",
                "sum_constraint": 200,
                "solution_precision": 1,
                "mean_photon_number": 1.4,
                "quantum_fluctuation_coefficient": 24,
            },
            polynomial_file_id="polynomial_fid",
        )

        self.assertDictEqual(
            hamiltonian_body,
            {
                "job_submission": {
                    "problem_config": {
                        "normalized_qudit_hamiltonian_optimization": {
                            "polynomial_file_id": "polynomial_fid",
                        }
                    },
                    "device_config": {
                        "dirac-3_normalized_qudit": {
                            "sum_constraint": 200,
                            "solution_precision": 1,
                            "mean_photon_number": 1.4,
                            "quantum_fluctuation_coefficient": 24,
                        }
                    },
                }
            },
        )

        hamiltonian_body = self.client.build_job_body(
            job_type="sample-hamiltonian",
            job_params={"device_type": "dirac-3", "sum_constraint": 2.4},
            polynomial_file_id="polynomial_fid",
        )

        self.assertDictEqual(
            hamiltonian_body,
            {
                "job_submission": {
                    "problem_config": {
                        "normalized_qudit_hamiltonian_optimization": {
                            "polynomial_file_id": "polynomial_fid",
                        }
                    },
                    "device_config": {
                        "dirac-3_normalized_qudit": {
                            "sum_constraint": 2.4,
                        }
                    },
                }
            },
        )

        hamiltonian_body = self.client.build_job_body(
            job_type="sample-hamiltonian",
            job_params={
                "device_type": "dirac-3",
                "sum_constraint": 2.4,
                "solution_precision": 0.1,
            },
            hamiltonian_file_id="hamiltonian_fid",
        )

        self.assertDictEqual(
            hamiltonian_body,
            {
                "job_submission": {
                    "problem_config": {
                        "normalized_qudit_hamiltonian_optimization": {
                            "hamiltonian_file_id": "hamiltonian_fid",
                        }
                    },
                    "device_config": {
                        "dirac-3_normalized_qudit": {
                            "sum_constraint": 2.4,
                            "solution_precision": 0.1,
                        }
                    },
                }
            },
        )

        hamiltonian_body = self.client.build_job_body(
            job_type="sample-hamiltonian",
            job_params={
                "device_type": "dirac-3_normalized_qudit",
                "sum_constraint": 2.4,
                "solution_precision": 0.1,
            },
            hamiltonian_file_id="hamiltonian_fid",
        )

        self.assertDictEqual(
            hamiltonian_body,
            {
                "job_submission": {
                    "problem_config": {
                        "normalized_qudit_hamiltonian_optimization": {
                            "hamiltonian_file_id": "hamiltonian_fid",
                        }
                    },
                    "device_config": {
                        "dirac-3_normalized_qudit": {
                            "sum_constraint": 2.4,
                            "solution_precision": 0.1,
                        }
                    },
                }
            },
        )

        hamiltonian_integer_body = self.client.build_job_body(
            job_type="sample-hamiltonian-integer",
            job_params={
                "device_type": "dirac-3",
                "num_levels": [2],
            },
            hamiltonian_file_id="hamiltonian_fid",
        )

        self.assertDictEqual(
            hamiltonian_integer_body,
            {
                "job_submission": {
                    "problem_config": {
                        "qudit_hamiltonian_optimization": {
                            "hamiltonian_file_id": "hamiltonian_fid",
                        }
                    },
                    "device_config": {"dirac-3_qudit": {"num_levels": [2]}},
                }
            },
        )

        hamiltonian_integer_body = self.client.build_job_body(
            job_type="sample-hamiltonian-integer",
            job_params={
                "device_type": "dirac-3_qudit",
                "num_samples": 2,
                "num_levels": [2, 3, 4, 5],
                "relaxation_schedule": 1,
                "mean_photon_number": 1.1,
                "quantum_fluctuation_coefficient": 25,
            },
            hamiltonian_file_id="hamiltonian_fid",
        )

        self.assertDictEqual(
            hamiltonian_integer_body,
            {
                "job_submission": {
                    "problem_config": {
                        "qudit_hamiltonian_optimization": {
                            "hamiltonian_file_id": "hamiltonian_fid",
                        }
                    },
                    "device_config": {
                        "dirac-3_qudit": {
                            "num_samples": 2,
                            "num_levels": [2, 3, 4, 5],
                            "relaxation_schedule": 1,
                            "mean_photon_number": 1.1,
                            "quantum_fluctuation_coefficient": 25,
                        }
                    },
                }
            },
        )

        graph_body = self.client.build_job_body(
            job_type="graph-partitioning",
            job_params={
                "device_type": "dirac-1",
                "num_samples": 42,
            },
            graph_file_id="graph_fid",
        )

        self.assertDictEqual(
            graph_body,
            {
                "job_submission": {
                    "problem_config": {
                        "graph_partitioning": {
                            "graph_file_id": "graph_fid",
                        }
                    },
                    "device_config": {
                        "dirac-1": {
                            "num_samples": 42,
                        }
                    },
                }
            },
        )


class TestClient(unittest.TestCase):  # pylint: disable=too-many-public-methods
    """Collection of tests for file uploads and jobs with results downloads."""

    @classmethod
    def setUpClass(cls):
        cls.client = qci_client.QciClient()
        cls.graph_dict_input = {
            "file_name": "graph.json",
            "file_config": {"graph": {"data": nx.Graph(((1, 2), (1, 3)))}},
        }

        cls.qubo_dict_input = {
            "file_name": "qubo.json",
            "file_config": {
                "qubo": {"data": sp.csr_matrix([[-1.0, 1.0], [1.0, -1.0]])}
            },
        }

        cls.objective_dict_input = {
            "file_name": "objective.json",
            "file_config": {
                "objective": {"data": sp.csc_matrix([[-1.0, 1.0], [1.0, -1.0]])}
            },
        }

        cls.constraint_dict_input = {
            "file_name": "constraints.json",
            "file_config": {
                "constraints": {
                    "data": sp.coo_matrix(
                        [
                            [-1.0, 1.0, 1.0],
                        ]
                    )
                }
            },
        }

        cls.hamiltonian_dict_input = {
            "file_name": "hamiltonian.json",
            "file_config": {
                "hamiltonian": {"data": np.array([[1.0, 1.0, 0.0], [2.0, 0.0, 1.0]])}
            },
        }

        cls.polynomial_dict_hamiltonian_input = {
            "file_name": "polynomial-hamiltonian.json",
            "file_config": {
                "polynomial": {
                    "min_degree": 1,
                    "max_degree": 2,
                    "num_variables": 2,
                    "data": [
                        {"idx": [0, 1], "val": 1.0},
                        {"idx": [1, 1], "val": -2.0},
                        {"idx": [1, 2], "val": 1.0},
                        {"idx": [2, 2], "val": -1.0},
                    ],
                }
            },
        }

        cls.polynomial_dict_input = {
            "file_name": "polynomial.json",
            "file_config": {
                "polynomial": {
                    "min_degree": 2,
                    "max_degree": 4,
                    "num_variables": 2,
                    "data": [
                        {"idx": [0, 0, 1, 1], "val": 1.0},
                        {"idx": [0, 1, 1, 1], "val": -2.0},
                        {"idx": [1, 1, 1, 1], "val": 1.0},
                    ],
                }
            },
        }

        cls.graph_file_id = cls.client.upload_file(file=cls.graph_dict_input)["file_id"]
        cls.qubo_file_id = cls.client.upload_file(file=cls.qubo_dict_input)["file_id"]
        cls.objective_file_id = cls.client.upload_file(file=cls.objective_dict_input)[
            "file_id"
        ]
        cls.constraints_file_id = cls.client.upload_file(
            file=cls.constraint_dict_input
        )["file_id"]
        cls.hamiltonian_file_id = cls.client.upload_file(
            file=cls.hamiltonian_dict_input
        )["file_id"]
        cls.polynomial_hamiltonian_file_id = cls.client.upload_file(
            file=cls.polynomial_dict_hamiltonian_input
        )["file_id"]
        cls.polynomial_min_degree_2_max_degree_4_file_id = cls.client.upload_file(
            file=cls.polynomial_dict_input
        )["file_id"]

        cls.job_info = set(("job_info", "results", "status"))

        cls.graph_job_body = {
            "job_submission": {
                "job_name": "job_0",
                "problem_config": {
                    "graph_partitioning": {"graph_file_id": cls.graph_file_id},
                },
                "device_config": {"dirac-1": {}},
            }
        }

        cls.qubo_job_body = {
            "job_submission": {
                "job_name": "job_0",
                "problem_config": {
                    "quadratic_unconstrained_binary_optimization": {
                        "qubo_file_id": cls.qubo_file_id
                    },
                },
                "device_config": {"dirac-1": {}},
            }
        }

        cls.constraint_job_body = {
            "job_submission": {
                "job_name": "job_0",
                "problem_config": {
                    "quadratic_linearly_constrained_binary_optimization": {
                        "objective_file_id": cls.objective_file_id,
                        "constraints_file_id": cls.constraints_file_id,
                    }
                },
                "device_config": {"dirac-1": {}},
            }
        }

        cls.hamiltonian_job_body_ising_dirac1 = {
            "job_submission": {
                "job_name": "dirac-1",
                "problem_config": {
                    "ising_hamiltonian_optimization": {
                        "hamiltonian_file_id": cls.hamiltonian_file_id
                    },
                },
                "device_config": {
                    "dirac-1": {
                        "num_samples": 2,
                    }
                },
            }
        }

        cls.polynomial_job_body_ising_dirac1 = {
            "job_submission": {
                "job_name": "dirac-1",
                "problem_config": {
                    "ising_hamiltonian_optimization": {
                        "polynomial_file_id": cls.polynomial_hamiltonian_file_id
                    },
                },
                "device_config": {"dirac-1": {}},
            }
        }

        cls.hamiltonian_job_body_continous_dirac2 = {
            "job_submission": {
                "job_name": "dirac-2",
                "problem_config": {
                    "normalized_qudit_hamiltonian_optimization_continuous": {
                        "hamiltonian_file_id": cls.hamiltonian_file_id
                    }
                },
                "device_config": {"dirac-2": {}},
            }
        }

        cls.hamiltonian_job_body_integer_dirac2 = {
            "job_submission": {
                "job_name": "dirac-2",
                "problem_config": {
                    "normalized_qudit_hamiltonian_optimization_integer": {
                        "hamiltonian_file_id": cls.hamiltonian_file_id
                    },
                },
                "device_config": {"dirac-2": {}},
            }
        }

        cls.polynomial_job_body_hamiltonian_continuous_dirac2 = {
            "job_submission": {
                "job_name": "dirac-2",
                "problem_config": {
                    "normalized_qudit_hamiltonian_optimization_continuous": {
                        "polynomial_file_id": cls.polynomial_hamiltonian_file_id
                    },
                },
                "device_config": {"dirac-2": {}},
            }
        }

        cls.polynomial_job_body_hamiltonian_integer_dirac2 = {
            "job_submission": {
                "job_name": "dirac-2",
                "problem_config": {
                    "normalized_qudit_hamiltonian_optimization_integer": {
                        "polynomial_file_id": cls.polynomial_hamiltonian_file_id
                    },
                },
                "device_config": {
                    "dirac-2": {
                        "num_samples": 2,
                    }
                },
            }
        }

        cls.hamiltonian_job_body_undistilled_dirac3 = {
            "job_submission": {
                "job_name": "dirac-3",
                "problem_config": {
                    "normalized_qudit_hamiltonian_optimization": {
                        "hamiltonian_file_id": cls.hamiltonian_file_id
                    }
                },
                "device_config": {
                    "dirac-3": {
                        "relaxation_parameter": 1,
                        "sum_constraint": 2.4,
                    }
                },
            }
        }

        cls.hamiltonian_job_body_distilled_continuous_dirac3 = {
            "job_submission": {
                "job_name": "dirac-3",
                "problem_config": {
                    "normalized_qudit_hamiltonian_optimization": {
                        "hamiltonian_file_id": cls.hamiltonian_file_id
                    }
                },
                "device_config": {
                    "dirac-3": {
                        "relaxation_parameter": 1,
                        "sum_constraint": 2.4,
                        "solution_precision": 0.1,
                    }
                },
            }
        }

        cls.hamiltonian_job_body_distilled_integer_dirac3 = {
            "job_submission": {
                "job_name": "dirac-3",
                "problem_config": {
                    "normalized_qudit_hamiltonian_optimization": {
                        "hamiltonian_file_id": cls.hamiltonian_file_id
                    }
                },
                "device_config": {
                    "dirac-3": {
                        "relaxation_parameter": 1,
                        "solution_precision": 1,
                    }
                },
            }
        }

        cls.polynomial_min_degree_2_max_degree_4_job_body_distilled_continuous_dirac3 = {
            "job_submission": {
                "job_name": "dirac-3",
                "problem_config": {
                    "normalized_qudit_hamiltonian_optimization": {
                        "polynomial_file_id": cls.polynomial_min_degree_2_max_degree_4_file_id
                    },
                },
                "device_config": {
                    "dirac-3": {
                        "relaxation_parameter": 2,
                        "sum_constraint": 2.4,
                        "solution_precision": 0.1,
                    }
                },
            }
        }

        cls.hamiltonian_job_body_dirac3_qudit = {
            "job_submission": {
                "job_name": "hamiltonian_dirac-3_qudit",
                "problem_config": {
                    "qudit_hamiltonian_optimization": {
                        "hamiltonian_file_id": cls.hamiltonian_file_id
                    }
                },
                "device_config": {
                    "dirac-3_qudit": {
                        "num_levels": [2, 3],
                    }
                },
            }
        }

        cls.polynomial_min_degree_2_max_degree_4_job_body_dirac3_qudit = {
            "job_submission": {
                "job_name": "polynomial_dirac-3_qudit",
                "problem_config": {
                    "qudit_hamiltonian_optimization": {
                        "polynomial_file_id": cls.polynomial_min_degree_2_max_degree_4_file_id
                    }
                },
                "device_config": {
                    "dirac-3_qudit": {
                        "num_levels": [3, 4],
                        "relaxation_schedule": 2,
                        "mean_photon_number": 1.1,
                        "quantum_fluctuation_coefficient": 25,
                    }
                },
            }
        }

    # Files tests.

    def test_upload_file_error(self):
        """Test uploading improperly formatted file."""
        with self.assertRaises(AssertionError):
            bad_file = {
                "file_name": "qubo.json",
                "file_config": {
                    "graph": {
                        "data": [
                            {"i": 0, "j": 0, "val": -1.0},
                            {"i": 0, "j": 1, "val": 1.0},
                            {"i": 1, "j": 0, "val": 1.0},
                            {"i": 1, "j": 1, "val": -1.0},
                        ],
                        "num_variables": 2,
                    }
                },
            }
            self.client.upload_file(file=bad_file)

    def test_upload_file(self):
        """Test uploading of various file types."""
        graph_upload = self.client.upload_file(file=self.graph_dict_input)
        self.assertIn("file_id", graph_upload)
        self.assertIsInstance(graph_upload["file_id"], str)

        qubo_upload = self.client.upload_file(file=self.qubo_dict_input)
        self.assertIn("file_id", qubo_upload)
        self.assertIsInstance(qubo_upload["file_id"], str)

        objective_upload = self.client.upload_file(file=self.objective_dict_input)
        self.assertIn("file_id", objective_upload)
        self.assertIsInstance(objective_upload["file_id"], str)

        constraint_upload = self.client.upload_file(file=self.constraint_dict_input)
        self.assertIn("file_id", constraint_upload)
        self.assertIsInstance(constraint_upload["file_id"], str)

        hamiltonian_upload = self.client.upload_file(file=self.hamiltonian_dict_input)
        self.assertIn("file_id", hamiltonian_upload)
        self.assertIsInstance(hamiltonian_upload["file_id"], str)

    def test_upload_download_file_hamiltonian_matrix_multipart(self):
        """Test uploading and downloading a larger multipart file for square matrix."""
        num_parts_expected = 2
        num_variables = 150
        density = 0.5
        format_ = "dok"
        dtype = np.float32
        J = sp.random(  # pylint: disable=invalid-name
            num_variables, num_variables, density=density, format=format_, dtype=dtype
        )
        J = (J + J.T) / 2  # pylint: disable=invalid-name
        h = sp.random(num_variables, 1, density=density, format=format_, dtype=dtype)
        matrix_upload = sp.hstack((h, J), format=format_, dtype=dtype)

        file_upload = {
            "file_name": "multipart-matrix-upload-download-test",
            "file_config": {
                "hamiltonian": {
                    "num_variables": num_variables,
                    "data": matrix_upload,
                },
            },
        }

        upload_response = self.client.upload_file(file=file_upload)
        download_response = self.client.download_file(
            file_id=upload_response["file_id"]
        )

        if download_response["num_parts"] != num_parts_expected:
            pytest.fail(
                f"num_parts {download_response['num_parts']} in downloaded file does "
                f"not equal {num_parts_expected}"
            )

        matrix_download = sp.dok_matrix(
            (
                download_response["file_config"]["hamiltonian"]["num_variables"],
                download_response["file_config"]["hamiltonian"]["num_variables"] + 1,
            ),
            dtype=dtype,
        )

        for datum in download_response["file_config"]["hamiltonian"]["data"]:
            matrix_download[datum["i"], datum["j"]] = datum["val"]

        if (matrix_download != matrix_upload).nnz != 0:
            pytest.fail(
                "sparse matrix in downloaded file does not equal sparse matrix in "
                "uploaded file"
            )

    def test_upload_download_file_polynomial_multipart(self):
        """Test uploading and downloading a larger multipart file for square matrix."""
        num_parts_expected = 2
        num_variables = 40
        min_degree = 0
        max_degree = 3
        idx_list = list(range(num_variables + 1))  # Include constant index.

        polynomial_upload = []

        for idx in product(idx_list, idx_list, idx_list):
            # Ensure non-decreasing indices.
            if idx[0] > idx[1] or idx[1] > idx[2]:
                continue

            polynomial_upload.append(
                {
                    "idx": list(idx),
                    "val": np.random.uniform(low=-3.14, high=3.14),
                }
            )

        file_upload = {
            "file_name": "multipart-polynomial-upload-download-test",
            "file_config": {
                "polynomial": {
                    "num_variables": num_variables,
                    "min_degree": min_degree,
                    "max_degree": max_degree,
                    "data": polynomial_upload,
                },
            },
        }

        upload_response = self.client.upload_file(file=file_upload)
        download_response = self.client.download_file(
            file_id=upload_response["file_id"]
        )

        if download_response["num_parts"] != num_parts_expected:
            pytest.fail(
                f"num_parts {download_response['num_parts']} in downloaded file does "
                f"not equal {num_parts_expected}"
            )

        polynomial_download = download_response["file_config"]["polynomial"]["data"]

        self.assertEqual(len(polynomial_download), len(polynomial_upload))

        for download_datum, upload_datum in zip(polynomial_download, polynomial_upload):
            self.assertDictEqual(download_datum, upload_datum)

    # Jobs tests, which refer back to some of the above files.

    def run_end_end(self, job_body: dict):
        """
        Utility function for testing end to end pipeline.
        :param job_body: a validate job request
        Testing each in series:
            - submit_job
            - get_job_status (repeating until job finished)
            - get_job_results
            - download_file (compares file_config to results from previous step)
        """

        job_id = self.client.submit_job(job_body=job_body)

        self.assertIn("job_id", job_id)
        self.assertIsInstance(job_id["job_id"], str)

        status = qci_client.JobStatus.SUBMITTED
        while status not in qci_client.JOB_STATUSES_FINAL:
            status = qci_client.JobStatus(
                self.client.get_job_status(job_id=job_id["job_id"])["status"]
            )
        self.assertEqual(status, qci_client.JobStatus.COMPLETED)

        response = self.client.get_job_results(job_id=job_id["job_id"])
        self.assertEqual(self.job_info, set(response.keys()))

        metrics = self.client.get_job_metrics(job_id=job_id["job_id"])
        self.assertEqual(metrics["job_id"], job_id["job_id"])
        self.assertIn("job_metrics", metrics)

        result = self.client.download_file(
            file_id=response["job_info"]["job_result"]["file_id"]
        )
        file_type_expected = (
            list(job_body["job_submission"]["problem_config"].keys())[0] + "_results"
        )
        self.assertDictEqual(
            response["results"], result["file_config"][file_type_expected]
        )

    def process_job_check(self, job_body) -> str:
        """Utility function for checking job types."""
        process_key = ["job_info", "status", "results"]
        job_output = self.client.process_job(job_body=job_body, wait=True)
        self.assertTrue(all(key in process_key for key in list(job_output.keys())))
        job_id = job_output["job_info"]["job_id"]
        self.assertEqual(job_output, self.client.get_job_results(job_id=job_id))
        return job_id

    def test_large_job(self):
        """Test large sample-qubo job."""
        num_variables = 1000
        large_qubo = sp.random(
            num_variables, num_variables, density=0.5, format="dok", dtype=np.float32
        )
        large_qubo = (large_qubo + large_qubo.T) / 2
        large_qubo_dict = {
            "file_name": "test_large_qubo",
            "file_config": {"qubo": {"data": large_qubo}},
        }
        large_file_id = self.client.upload_file(file=large_qubo_dict)["file_id"]
        print("LARGE FILE ID", large_file_id)
        large_job_body = {
            "job_submission": {
                "job_name": "large_qubo_test_job",
                "problem_config": {
                    "quadratic_unconstrained_binary_optimization": {
                        "qubo_file_id": large_file_id
                    }
                },
                "device_config": {"dirac-1": {}},
            }
        }

        self.process_job_check(job_body=large_job_body)

    def test_process_qubo(self):
        """Test that sample-qubo job process can be checked."""
        job_id = self.process_job_check(job_body=self.qubo_job_body)

        # Job already COMPLETED, so cancelling should raise.
        with self.assertRaises(
            requests.HTTPError, msg="400 Client Error: Bad Request for "
        ):
            self.client.cancel_job(job_id=job_id)

    def test_process_constraint(self):
        """Test that sample-constraint job process can be checked."""
        self.process_job_check(job_body=self.constraint_job_body)

    def test_process_hamiltonian_ising_dirac1(self):
        """Test that sample-hamiltonian-ising process job on dirac-1 can be checked."""
        self.process_job_check(job_body=self.hamiltonian_job_body_ising_dirac1)

    def test_process_hamiltonian_dirac2(self):
        """Test that integer sample-hamiltonian process job on dirac-2 can be checked."""
        self.process_job_check(job_body=self.hamiltonian_job_body_integer_dirac2)

    def test_process_hamiltonian_dirac3(self):
        """
        Test that undistilled sample-hamiltonian process on dirac-3 job can be checked.
        """
        self.process_job_check(job_body=self.hamiltonian_job_body_undistilled_dirac3)

    def test_graph_partitioning(self):
        """Test graph-partitioning job."""
        self.run_end_end(job_body=self.graph_job_body)

    def test_sample_qubo(self):
        """Test sample-qubo job."""
        self.run_end_end(job_body=self.qubo_job_body)

    def test_sample_constraint(self):
        """Test sample-constraint job."""
        self.run_end_end(job_body=self.constraint_job_body)

    def test_sample_hamiltonian_ising_polynomial_dirac1(self):
        """Test sample-hamiltonian-ising job using polynomial on dirac-1."""
        self.run_end_end(job_body=self.polynomial_job_body_ising_dirac1)

    def test_sample_hamiltonian_ising_hamiltonian_dirac1(self):
        """Test sample-hamiltonian-ising job using hamiltonian matrix on dirac-1."""
        self.run_end_end(job_body=self.hamiltonian_job_body_ising_dirac1)

    def test_sample_hamiltonian_polynomial_continuous_dirac2(self):
        """Test sample-hamiltonian continuous job using polynomial on dirac-2."""
        self.run_end_end(
            job_body=self.polynomial_job_body_hamiltonian_continuous_dirac2
        )

    def test_sample_hamiltonian_polynomial_integer_dirac2(self):
        """Test sample-hamiltonian integer job using polynomial on dirac-2."""
        self.run_end_end(job_body=self.polynomial_job_body_hamiltonian_integer_dirac2)

    def test_sample_hamiltonian_continuous_dirac2(self):
        """Test continuous sample-hamiltonian job on dirac-2."""
        self.run_end_end(job_body=self.hamiltonian_job_body_continous_dirac2)

    def test_sample_hamiltonian_integer_dirac2(self):
        """Test integer sample-hamiltonian job on dirac-2."""
        self.run_end_end(job_body=self.hamiltonian_job_body_integer_dirac2)

    def test_sample_hamiltonian_polynomial_distilled_continuous_dirac3_normalized_qudit(
        self,
    ):
        """
        Test distilled-to-continuous sample-hamiltonian job using polynomial on dirac-3.
        """
        self.run_end_end(
            job_body=self.polynomial_min_degree_2_max_degree_4_job_body_distilled_continuous_dirac3
        )

    def test_sample_hamiltonian_undistilled_dirac3_normalized_qudit(self):
        """Test undistilled sample-hamiltonian job on dirac-3."""
        self.run_end_end(job_body=self.hamiltonian_job_body_undistilled_dirac3)

    def test_sample_hamiltonian_distilled_continuous_dirac3_normalized_qudit(self):
        """Test distilled-to-continuous sample-hamiltonian job on dirac-3."""
        self.run_end_end(job_body=self.hamiltonian_job_body_distilled_continuous_dirac3)

    def test_sample_hamiltonian_distilled_integer_dirac3_normalized_qudit(self):
        """Test distilled-to-integer sample-hamiltonian job on dirac-3."""
        self.run_end_end(job_body=self.hamiltonian_job_body_distilled_integer_dirac3)

    def test_sample_hamiltonian_integer_hamiltonian_dirac3_qudit(self):
        """
        Test distilled-to-continuous sample-hamiltonian job using polynomial on dirac-3.
        """
        self.run_end_end(job_body=self.hamiltonian_job_body_dirac3_qudit)

    def test_sample_hamiltonian_integer_polynomial_dirac3_qudit(self):
        """
        Test distilled-to-continuous sample-hamiltonian job using polynomial on dirac-3.
        """
        self.run_end_end(
            job_body=self.polynomial_min_degree_2_max_degree_4_job_body_dirac3_qudit
        )


class TestMultipartUploadDownload(unittest.TestCase):
    """Multipart-file upload/download test suite."""

    @classmethod
    def setUpClass(cls):
        cls.client = qci_client.QciClient()

    def test_multipart_upload_download_hamiltonian(self):
        """Test uploading/downloading multipart hamiltonian matrix file."""
        # num_variables = 1700

        # resdata = {
        #     "file_name": "test-file.json",
        #     "file_type": "job_results_sample_qubo",
        #     "organization_id": "5ddf5db3fed87d53b6bf392a",
        #     "username": "test_user",
        #     "counts": counts.flatten().tolist(),
        #     "energies": energies.flatten().tolist(),
        #     "samples": samples.tolist(),
        # }

        # resp = self.client.upload_file(file=resdata)
        # meta = self.client.get_file_metadata(file_id=resp["file_id"], is_results_file=is_results_file)
        # self.assertEqual(meta["num_parts"], expected_parts)

        # test_res_whole = self.client.get_file_whole(file_id=resp["file_id"], is_results_file=is_results_file)
        # self.assertEqual(len(test_res_whole["counts"]), counts.shape[0])
        # self.assertEqual(len(test_res_whole["energies"]), energies.shape[0])
        # self.assertEqual(len(test_res_whole["samples"]), samples.shape[0])
        # self.assertEqual(len(test_res_whole["samples"][0]), samples.shape[1])

        # del_resp = self.client.delete_file(resp["file_id"])
        # assert del_resp["num_deleted"] == 1

    def test_multipart_upload_download_polynomial(self):
        """Test uploading/downloading multipart polynomial file."""
        # Tests float uploads, so we use Hamiltonian job type so the API can handle floats
        # num_variables = 20000

        # resdata = {
        #     "file_name": "test-file.json",
        #     "file_type": "job_results_sample_hamiltonian",
        #     "organization_id": "5ddf5db3fed87d53b6bf392a",
        #     "username": "test_user",
        #     # "solution_type": "continuous",
        #     "counts": counts.flatten().tolist(),
        #     "energies": energies.flatten().tolist(),
        #     "samples": samples.tolist(),
        # }

        # resp = self.client.upload_file(file=resdata)
        # meta = self.client.get_file_metadata(file_id=resp["file_id"], is_results_file=is_results_file)
        # self.assertEqual(meta["num_parts"], expected_parts)

        # test_res_whole = self.client.get_file_whole(file_id=resp["file_id"], is_results_file=is_results_file)
        # self.assertEqual(len(test_res_whole["counts"]), len(test_vec_int))
        # self.assertEqual(len(test_res_whole["energies"]), test_vec.shape[0])
        # self.assertEqual(len(test_res_whole["samples"]), num_samples)
        # self.assertEqual(len(test_res_whole["samples"][0]), num_nodes)

        # del_resp = self.client.delete_file(resp["file_id"])
        # assert del_resp["num_deleted"] == 1
