# Copyright 2023-2024, Quantum Computing Incorporated
"""Test enum module."""

import unittest

import pytest

from qci_client.optimization import enum


@pytest.mark.offline
class TestEnums(unittest.TestCase):
    """enum-related test suite."""

    def test_job_type(self):
        """Test all job types."""
        self.assertEqual(enum.JobType.SAMPLE_QUBO.value, "sample-qubo")
        self.assertEqual(enum.JobType.GRAPH_PARTITIONING.value, "graph-partitioning")
        self.assertEqual(enum.JobType.SAMPLE_CONTRAINT.value, "sample-constraint")
        self.assertEqual(enum.JobType.SAMPLE_HAMILTONIAN.value, "sample-hamiltonian")
        self.assertEqual(
            enum.JobType.SAMPLE_HAMILTONIAN_INTEGER.value, "sample-hamiltonian-integer"
        )
        self.assertEqual(
            enum.JobType.SAMPLE_HAMILTONIAN_ISING.value, "sample-hamiltonian-ising"
        )
        self.assertEqual(
            enum.JOB_TYPES,
            frozenset(
                (
                    enum.JobType.SAMPLE_QUBO,
                    enum.JobType.GRAPH_PARTITIONING,
                    enum.JobType.SAMPLE_CONTRAINT,
                    enum.JobType.SAMPLE_HAMILTONIAN,
                    enum.JobType.SAMPLE_HAMILTONIAN_INTEGER,
                    enum.JobType.SAMPLE_HAMILTONIAN_ISING,
                )
            ),
        )

    def test_problem_type(self):
        """Test all problem types."""
        self.assertEqual(enum.ProblemType.GP.value, "graph_partitioning")
        self.assertEqual(enum.ProblemType.IHO.value, "ising_hamiltonian_optimization")
        self.assertEqual(
            enum.ProblemType.NQHO.value, "normalized_qudit_hamiltonian_optimization"
        )
        self.assertEqual(
            enum.ProblemType.NQHO_CONTINUOUS.value,
            "normalized_qudit_hamiltonian_optimization_continuous",
        )
        self.assertEqual(
            enum.ProblemType.NQHO_INTEGER.value,
            "normalized_qudit_hamiltonian_optimization_integer",
        )
        self.assertEqual(
            enum.ProblemType.QLCBO.value,
            "quadratic_linearly_constrained_binary_optimization",
        )
        self.assertEqual(
            enum.ProblemType.QUBO.value, "quadratic_unconstrained_binary_optimization"
        )
        self.assertEqual(
            enum.PROBLEM_TYPES,
            frozenset(
                (
                    enum.ProblemType.GP,
                    enum.ProblemType.IHO,
                    enum.ProblemType.NQHO,
                    enum.ProblemType.NQHO_CONTINUOUS,
                    enum.ProblemType.NQHO_INTEGER,
                    enum.ProblemType.QHO,
                    enum.ProblemType.QLCBO,
                    enum.ProblemType.QUBO,
                )
            ),
        )

    def test_device_type(self):
        """Test all device types."""
        self.assertEqual(enum.DeviceType.DIRAC1.value, "dirac-1")
        self.assertEqual(enum.DeviceType.DIRAC2.value, "dirac-2")
        self.assertEqual(enum.DeviceType.DIRAC3.value, "dirac-3")
        self.assertEqual(
            enum.DeviceType.DIRAC3_NORMALIZED_QUDIT.value, "dirac-3_normalized_qudit"
        )
        self.assertEqual(enum.DeviceType.DIRAC3_QUDIT.value, "dirac-3_qudit")
        self.assertEqual(
            enum.DEVICE_TYPES,
            frozenset(
                (
                    enum.DeviceType.DIRAC1,
                    enum.DeviceType.DIRAC2,
                    enum.DeviceType.DIRAC3,
                    enum.DeviceType.DIRAC3_NORMALIZED_QUDIT,
                    enum.DeviceType.DIRAC3_QUDIT,
                )
            ),
        )
        self.assertEqual(enum.DEVICE_TYPES_QUBIT, frozenset((enum.DeviceType.DIRAC1,)))
        self.assertEqual(
            enum.DEVICE_TYPES_NORMALIZED_QUDIT,
            frozenset(
                (
                    enum.DeviceType.DIRAC2,
                    enum.DeviceType.DIRAC3,
                    enum.DeviceType.DIRAC3_NORMALIZED_QUDIT,
                )
            ),
        )
        self.assertEqual(
            enum.DEVICE_TYPES_QUDIT,
            frozenset((enum.DeviceType.DIRAC3, enum.DeviceType.DIRAC3_QUDIT)),
        )
        self.assertEqual(
            enum.DEVICE_TYPES_SORTED,
            (
                "dirac-1",
                "dirac-2",
                "dirac-3",
                "dirac-3_normalized_qudit",
                "dirac-3_qudit",
            ),
        )

    def test_job_status(self):
        """Test all job statuses."""
        self.assertEqual(enum.JobStatus.SUBMITTED.value, "SUBMITTED")
        self.assertEqual(enum.JobStatus.QUEUED.value, "QUEUED")
        self.assertEqual(enum.JobStatus.RUNNING.value, "RUNNING")
        self.assertEqual(enum.JobStatus.COMPLETED.value, "COMPLETED")
        self.assertEqual(enum.JobStatus.ERRORED.value, "ERRORED")
        self.assertEqual(enum.JobStatus.CANCELLED.value, "CANCELLED")
        self.assertEqual(
            enum.JOB_STATUSES,
            frozenset(
                (
                    enum.JobStatus.SUBMITTED,
                    enum.JobStatus.QUEUED,
                    enum.JobStatus.RUNNING,
                    enum.JobStatus.COMPLETED,
                    enum.JobStatus.ERRORED,
                    enum.JobStatus.CANCELLED,
                )
            ),
        )
        self.assertEqual(
            enum.JOB_STATUSES_FINAL,
            frozenset(
                (
                    enum.JobStatus.COMPLETED,
                    enum.JobStatus.ERRORED,
                    enum.JobStatus.CANCELLED,
                )
            ),
        )

    def test_file_type(self):
        """Test all file types."""
        self.assertEqual(enum.FileType.CONSTRAINTS.value, "constraints")
        self.assertEqual(enum.FileType.GRAPH.value, "graph")
        self.assertEqual(enum.FileType.HAMILTONIAN.value, "hamiltonian")
        self.assertEqual(enum.FileType.OBJECTIVE.value, "objective")
        self.assertEqual(enum.FileType.POLYNOMIAL.value, "polynomial")
        self.assertEqual(enum.FileType.QUBO.value, "qubo")
        self.assertEqual(enum.FileType.GP_RESULTS.value, "graph_partitioning_results")
        self.assertEqual(
            enum.FileType.IHO_RESULTS.value, "ising_hamiltonian_optimization_results"
        )
        self.assertEqual(
            enum.FileType.NQHO_CONTINUOUS_RESULTS.value,
            "normalized_qudit_hamiltonian_optimization_continuous_results",
        )
        self.assertEqual(
            enum.FileType.NQHO_INTEGER_RESULTS.value,
            "normalized_qudit_hamiltonian_optimization_integer_results",
        )
        self.assertEqual(
            enum.FileType.NQHO_RESULTS.value,
            "normalized_qudit_hamiltonian_optimization_results",
        )
        self.assertEqual(
            enum.FileType.QLCBO_RESULTS.value,
            "quadratic_linearly_constrained_binary_optimization_results",
        )
        self.assertEqual(
            enum.FileType.QUBO_RESULTS.value,
            "quadratic_unconstrained_binary_optimization_results",
        )
        self.assertEqual(
            enum.FILE_TYPES,
            frozenset(
                (
                    enum.FileType.CONSTRAINTS,
                    enum.FileType.GRAPH,
                    enum.FileType.HAMILTONIAN,
                    enum.FileType.OBJECTIVE,
                    enum.FileType.POLYNOMIAL,
                    enum.FileType.QUBO,
                    enum.FileType.GP_RESULTS,
                    enum.FileType.IHO_RESULTS,
                    enum.FileType.NQHO_CONTINUOUS_RESULTS,
                    enum.FileType.NQHO_INTEGER_RESULTS,
                    enum.FileType.NQHO_RESULTS,
                    enum.FileType.QHO_RESULTS,
                    enum.FileType.QLCBO_RESULTS,
                    enum.FileType.QUBO_RESULTS,
                )
            ),
        )
        self.assertEqual(
            enum.FILE_TYPES_JOB_INPUTS,
            frozenset(
                (
                    enum.FileType.CONSTRAINTS,
                    enum.FileType.GRAPH,
                    enum.FileType.HAMILTONIAN,
                    enum.FileType.OBJECTIVE,
                    enum.FileType.POLYNOMIAL,
                    enum.FileType.QUBO,
                )
            ),
        )
        self.assertEqual(
            enum.FILE_TYPES_JOB_INPUTS_MATRIX,
            frozenset(
                (
                    enum.FileType.CONSTRAINTS,
                    enum.FileType.HAMILTONIAN,
                    enum.FileType.OBJECTIVE,
                    enum.FileType.QUBO,
                )
            ),
        )
        self.assertEqual(
            enum.FILE_TYPES_JOB_INPUTS_NON_GRAPH,
            frozenset(
                (
                    enum.FileType.CONSTRAINTS,
                    enum.FileType.HAMILTONIAN,
                    enum.FileType.OBJECTIVE,
                    enum.FileType.POLYNOMIAL,
                    enum.FileType.QUBO,
                )
            ),
        )
        self.assertEqual(
            enum.FILE_TYPES_JOB_RESULTS,
            frozenset(
                (
                    enum.FileType.GP_RESULTS,
                    enum.FileType.IHO_RESULTS,
                    enum.FileType.NQHO_CONTINUOUS_RESULTS,
                    enum.FileType.NQHO_INTEGER_RESULTS,
                    enum.FileType.NQHO_RESULTS,
                    enum.FileType.QHO_RESULTS,
                    enum.FileType.QLCBO_RESULTS,
                    enum.FileType.QUBO_RESULTS,
                )
            ),
        )
