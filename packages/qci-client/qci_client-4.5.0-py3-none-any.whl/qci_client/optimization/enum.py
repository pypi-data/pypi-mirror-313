# Copyright 2023-2024, Quantum Computing Incorporated
"""Enumerations."""

from enum import Enum


class JobType(Enum):
    """Enumeration of all job types, which are specific to qci-client."""

    SAMPLE_QUBO = "sample-qubo"
    """"""
    GRAPH_PARTITIONING = "graph-partitioning"
    """"""
    SAMPLE_CONTRAINT = "sample-constraint"
    """"""
    SAMPLE_HAMILTONIAN = "sample-hamiltonian"
    """"""
    SAMPLE_HAMILTONIAN_INTEGER = "sample-hamiltonian-integer"
    """"""
    SAMPLE_HAMILTONIAN_ISING = "sample-hamiltonian-ising"
    """"""


JOB_TYPES = frozenset(type for type in JobType)


class ProblemType(Enum):
    """Enumeration of all problem types, where values match jobs API values."""

    GP = "graph_partitioning"
    """"""
    IHO = "ising_hamiltonian_optimization"
    """"""
    NQHO = "normalized_qudit_hamiltonian_optimization"
    """"""
    NQHO_CONTINUOUS = "normalized_qudit_hamiltonian_optimization_continuous"
    """"""
    NQHO_INTEGER = "normalized_qudit_hamiltonian_optimization_integer"
    """"""
    QHO = "qudit_hamiltonian_optimization"
    """"""
    QLCBO = "quadratic_linearly_constrained_binary_optimization"
    """"""
    QUBO = "quadratic_unconstrained_binary_optimization"
    """"""


PROBLEM_TYPES = frozenset(type for type in ProblemType)


class DeviceType(Enum):
    """Enumeration of all device types, where values match jobs API values."""

    DIRAC1 = "dirac-1"
    """"""
    DIRAC2 = "dirac-2"
    """"""
    DIRAC3 = "dirac-3"  # Legacy, but still accepted here for ease of use.
    """"""
    DIRAC3_NORMALIZED_QUDIT = "dirac-3_normalized_qudit"
    """"""
    DIRAC3_QUDIT = "dirac-3_qudit"
    """"""


DEVICE_TYPES = frozenset(type for type in DeviceType)
DEVICE_TYPES_QUBIT = frozenset((DeviceType.DIRAC1,))
DEVICE_TYPES_NORMALIZED_QUDIT = frozenset(
    (
        DeviceType.DIRAC2,
        DeviceType.DIRAC3,  # Simplifies user interface in job_params.
        DeviceType.DIRAC3_NORMALIZED_QUDIT,
    )
)
DEVICE_TYPES_QUDIT = frozenset(
    (
        DeviceType.DIRAC3,  # Simplifies user interface in job_params.
        DeviceType.DIRAC3_QUDIT,
    )
)
DEVICE_TYPES_SORTED = [type.value for type in DEVICE_TYPES]
DEVICE_TYPES_SORTED.sort()
DEVICE_TYPES_SORTED = tuple(DEVICE_TYPES_SORTED)


class JobStatus(Enum):
    """Enumeration of all jobs statuses, where values match jobs API values."""

    SUBMITTED = "SUBMITTED"
    """"""
    QUEUED = "QUEUED"
    """"""
    RUNNING = "RUNNING"
    """"""
    COMPLETED = "COMPLETED"
    """"""
    ERRORED = "ERRORED"
    """"""
    CANCELLED = "CANCELLED"
    """"""


JOB_STATUSES = frozenset(status for status in JobStatus)
JOB_STATUSES_FINAL = frozenset(
    (JobStatus.COMPLETED, JobStatus.ERRORED, JobStatus.CANCELLED)
)


class FileType(Enum):
    """Enumeration of all file types, where values match files API values."""

    CONSTRAINTS = "constraints"
    """"""
    GRAPH = "graph"
    """"""
    HAMILTONIAN = "hamiltonian"
    """"""
    OBJECTIVE = "objective"
    """"""
    POLYNOMIAL = "polynomial"
    """"""
    QUBO = "qubo"
    """"""
    GP_RESULTS = "graph_partitioning_results"
    """"""
    IHO_RESULTS = "ising_hamiltonian_optimization_results"
    """"""
    NQHO_CONTINUOUS_RESULTS = (
        "normalized_qudit_hamiltonian_optimization_continuous_results"
    )
    """"""
    NQHO_INTEGER_RESULTS = "normalized_qudit_hamiltonian_optimization_integer_results"
    """"""
    NQHO_RESULTS = "normalized_qudit_hamiltonian_optimization_results"
    """"""
    QHO_RESULTS = "qudit_hamiltonian_optimization_results"
    """"""
    QLCBO_RESULTS = "quadratic_linearly_constrained_binary_optimization_results"
    """"""
    QUBO_RESULTS = "quadratic_unconstrained_binary_optimization_results"
    """"""


FILE_TYPES = frozenset(type for type in FileType)
FILE_TYPES_JOB_INPUTS = frozenset(
    type for type in FileType if "results" not in type.value
)
FILE_TYPES_JOB_INPUTS_MATRIX = FILE_TYPES_JOB_INPUTS - frozenset(
    [FileType.GRAPH, FileType.POLYNOMIAL]
)
FILE_TYPES_JOB_INPUTS_NON_GRAPH = FILE_TYPES_JOB_INPUTS - frozenset([FileType.GRAPH])
FILE_TYPES_JOB_RESULTS = frozenset(type for type in FileType if "results" in type.value)


def get_file_type(*, file: dict) -> FileType:
    """Get file type from a file."""
    file_config_keys = list(file["file_config"].keys())

    if len(file_config_keys) != 1:
        raise ValueError(
            "improper number of files specified in file_config (should be exactly one)"
        )

    return FileType(file_config_keys[0])
