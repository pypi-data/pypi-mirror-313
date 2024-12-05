# Copyright 2023-2024, Quantum Computing Incorporated
"""Types."""

from typing import Dict, List, TypedDict, Union


class ConstraintsMetadata(TypedDict):
    """Constraints file metadata."""

    num_constraints: int
    num_variables: int


class ConstraintsMetadataConfig(TypedDict):
    """Constraints file metadata configuration."""

    constraints: ConstraintsMetadata


class GraphMetadata(TypedDict):
    """Graph file metadata."""

    directed: bool
    multigraph: bool
    graph: Dict[str, str]
    num_edges: int
    num_nodes: int


class GraphMetadataConfig(TypedDict):
    """Graph file metadata configuration."""

    graph: GraphMetadata


class HamiltonianMetadata(TypedDict):
    """Hamiltonian file metadata."""

    num_variables: int


class HamiltonianMetadataConfig(TypedDict):
    """Hamiltonian file metadata configuration."""

    hamiltonian: HamiltonianMetadata


class ObjectiveMetadata(TypedDict):
    """Objective file metadata."""

    num_variables: int


class ObjectiveMetadataConfig(TypedDict):
    """Objective file metadata configuration."""

    objective: ObjectiveMetadata


class PolynomialMetadata(TypedDict):
    """Polynomial file metadata."""

    min_degree: int
    max_degree: int
    num_variables: int


class PolynomialMetadataConfig(TypedDict):
    """Polynomial file metadata configuration."""

    polynomial: PolynomialMetadata


class QuboMetadata(TypedDict):
    """QUBO file metadata."""

    num_variables: int


class QuboMetadataConfig(TypedDict):
    """QUBO file metadata configuration."""

    qubo: QuboMetadata


class GpResultsMetadata(TypedDict):
    """Graph Partitioning (GP) results file metadata."""


class GpResultsMetadataConfig(TypedDict):
    """Graph Partitioning (GP)  results file metadata configuration."""

    graph_partitioning_results: GpResultsMetadata


class IhoResultsMetadata(TypedDict):
    """Ising Hamiltonian Optimization (IHO) results file metadata."""


class IhoResultsMetadataConfig(TypedDict):
    """Ising Hamiltonian Optimization (IHO) results file metadata configuration."""

    ising_hamiltonian_optimization_results: IhoResultsMetadata


class NqhoContinuousResultsMetadata(TypedDict):
    """
    Continuous normalized-Qudit Hamiltonian Optimization (NQHO) results file metadata.
    """


class NqhoContinuousResultsMetadataConfig(TypedDict):
    """
    Continuous Normalized-Qudit Hamiltonian Optimization (NQHO) results file metadata
    configuration.
    """

    normalized_qudit_hamiltonian_optimization_continuous_results: (
        NqhoContinuousResultsMetadata  # pylint: disable=line-too-long
    )


class NqhoIntegerResultsMetadata(TypedDict):
    """
    Integer normalized-Qudit Hamiltonian Optimization (NQHO) results file metadata.
    """


class NqhoIntegerResultsMetadataConfig(TypedDict):
    """
    Integer Normalized-Qudit Hamiltonian Optimization (NQHO) results file metadata
    configuration.
    """

    normalized_qudit_hamiltonian_optimization_integer_results: (
        NqhoIntegerResultsMetadata  # pylint: disable=line-too-long
    )


class NqhoResultsMetadata(TypedDict):
    """Normalized-Qudit Hamiltonian Optimization (NQHO) results file metadata."""


class NqhoResultsMetadataConfig(TypedDict):
    """
    Normalized-Qudit Hamiltonian Optimization (NQHO) results file metadata
    configuration.
    """

    normalized_qudit_hamiltonian_optimization_results: NqhoResultsMetadata


class QlcboResultsMetadata(TypedDict):
    """
    Quadratic Linearly Constrained Binary Optimization (QLCBO) results file metadata.
    """


class QlcboResultsMetadataConfig(TypedDict):
    """
    Quadratic Linearly Constrained Binary Optimization (QLCBO) results file metadata
    configuration.
    """

    quadratic_linearly_constrained_binary_optimization_results: QlcboResultsMetadata


class QuboResultsMetadata(TypedDict):
    """Quadratic Unconstrained Binary Optimization (QUBO) results file metadata."""


class QuboResultsMetadataConfig(TypedDict):
    """
    Quadratic Unconstrained Binary Optimization (QUBO) results file metadata
    configuration.
    """

    quadratic_unconstrained_binary_optimization_results: QuboResultsMetadata


class MetadataOptionalPostRequestBody(TypedDict, total=False):
    """Optional file metadata."""

    file_name: str


class MetadataPostRequestBody(MetadataOptionalPostRequestBody):
    """Request body for POSTing (input) file metadata."""

    file_config: Union[
        ConstraintsMetadataConfig,
        GraphMetadataConfig,
        HamiltonianMetadataConfig,
        ObjectiveMetadataConfig,
        PolynomialMetadataConfig,
        QuboMetadataConfig,
    ]


class MetadataPostResponseBody(TypedDict):
    """File metadata POST response body."""

    file_id: str


class MatrixElement(TypedDict):
    """Matrix element dictionary."""

    i: int
    j: int
    val: float


class ConstraintsPart(TypedDict):
    """Constraints file part."""

    data: List[MatrixElement]


class ConstraintsPartConfig(TypedDict):
    """Constraints file part configuration."""

    constraints: ConstraintsPart


class NodeDict(TypedDict):
    """Dictionary elements of nodes array."""

    id: int


class LinkDictOptional(TypedDict, total=False):
    """Optional fields of dictionary elements of links array."""

    weight: float


class LinkDict(LinkDictOptional):
    """Dictionary elements of links array."""

    source: int
    target: int


class GraphPart(TypedDict):
    """Graph file part."""

    nodes: List[NodeDict]
    links: List[LinkDict]


class GraphPartConfig(TypedDict):
    """Graph file part configuration."""

    graph: GraphPart


class HamiltonianPart(TypedDict):
    """Hamiltonian file part."""

    data: List[MatrixElement]


class HamiltonianPartConfig(TypedDict):
    """Hamiltonian file part configuration."""

    hamiltonian: HamiltonianPart


class ObjectivePart(TypedDict):
    """Objective file part."""

    data: List[MatrixElement]


class ObjectivePartConfig(TypedDict):
    """Objective file part configuration."""

    objective: ObjectivePart


class PolynomialElement(TypedDict):
    """Polynomial element dictionary."""

    idx: List[int]
    val: float


class PolynomialPart(TypedDict):
    """Polynomial file part."""

    data: List[PolynomialElement]


class PolynomialPartConfig(TypedDict):
    """Polynomial file part configuration."""

    polynomial: PolynomialPart


class QuboPart(TypedDict):
    """QUBO file part."""

    data: List[MatrixElement]


class QuboPartConfig(TypedDict):
    """QUBO file part configuration."""

    qubo: QuboPart


class GpResultsPart(TypedDict):
    """GP results file part."""

    balances: List[float]
    counts: List[int]
    cut_sizes: List[float]
    energies: List[float]
    feasibilities: List[bool]
    partitions: List[List[List[int]]]
    solutions: List[List[int]]


class GpResultsPartConfig(TypedDict):
    """GP results file part configuration."""

    graph_partitioning_results: GpResultsPart


class IhoResultsPart(TypedDict):
    """IHO results file part."""

    counts: List[int]
    energies: List[float]
    solutions: List[List[int]]


class IhoResultsPartConfig(TypedDict):
    """IHO results file part configuration."""

    ising_hamiltonian_optimization_results: IhoResultsPart


class NqhoContinuousResultsPart(TypedDict):
    """Continuous NQHO results file part."""

    counts: List[int]
    energies: List[float]
    solutions: List[List[float]]


class NqhoContinuousResultsPartConfig(TypedDict):
    """Continuous NQHO results file part configuration."""

    normalized_qudit_hamiltonian_optimization_continuous_results: (
        NqhoContinuousResultsPart  # pylint: disable=line-too-long
    )


class NqhoIntegerResultsPart(TypedDict):
    """Integer NQHO results file part."""

    counts: List[int]
    energies: List[float]
    solutions: List[List[int]]


class NqhoIntegerResultsPartConfig(TypedDict):
    """Integer NQHO results file part configuration."""

    normalized_qudit_hamiltonian_optimization_integer_results: NqhoIntegerResultsPart


class NqhoResultsPartWithoutDistilled(TypedDict):
    """NQHO results file part without distilled solution results."""

    counts: List[int]
    energies: List[float]
    solutions: List[List[int]]


class NqhoResultsPartWithDistilled(NqhoResultsPartWithoutDistilled):
    """NQHO results file part with distilled solution results."""

    distilled_energies: List[float]
    distilled_solutions: List[List[int]]


class NqhoResultsPartConfig(TypedDict):
    """NQHO results file part configuration."""

    normalized_qudit_hamiltonian_optimization_results: Union[
        NqhoResultsPartWithoutDistilled,
        NqhoResultsPartWithDistilled,
    ]


class QlcboResultsPart(TypedDict):
    """QLCBO results file part."""

    counts: List[int]
    energies: List[float]
    feasibilities: List[bool]
    objective_values: List[float]
    solutions: List[List[int]]


class QlcboResultsPartConfig(TypedDict):
    """QLCBO results file part configuration."""

    quadratic_linearly_constrained_binary_optimization_results: QlcboResultsPart


class QuboResultsPart(TypedDict):
    """QUBO results file part."""

    counts: List[int]
    energies: List[float]
    solutions: List[List[int]]


class QuboResultsPartConfig(TypedDict):
    """QUBO results file part configuration."""

    quadratic_unconstrained_binary_optimization_results: QuboResultsPart


class PartPatchRequestBody(TypedDict):
    """The request body for PATCHing (input) file parts."""

    file_config: Union[
        ConstraintsPartConfig,
        GraphPartConfig,
        HamiltonianPartConfig,
        ObjectivePartConfig,
        PolynomialPartConfig,
        QuboPartConfig,
    ]


class PartPatchResponseBody(TypedDict):
    """File part PATCH response body."""

    file_id: str


class MetadataOptionalGetResponseBody(TypedDict, total=False):
    """Optional fields for file metadata GET responses."""

    organization_id: str
    user_id: str
    file_name: str


class MetadataGetResponseBody(MetadataOptionalGetResponseBody):
    """GET file metatada response body."""

    file_id: str
    upload_date_rfc3339: str
    last_accessed_rfc3339: str
    num_parts: int
    num_bytes: int
    file_config: Union[
        ConstraintsMetadataConfig,
        GraphMetadataConfig,
        HamiltonianMetadataConfig,
        ObjectiveMetadataConfig,
        QuboMetadataConfig,
        GpResultsMetadataConfig,
        IhoResultsMetadataConfig,
        NqhoContinuousResultsMetadataConfig,
        NqhoIntegerResultsMetadataConfig,
        NqhoResultsMetadataConfig,
        QlcboResultsMetadataConfig,
        QuboResultsMetadataConfig,
    ]


class GetResponseBody(TypedDict):
    """Fields for GET file metadata responses."""

    files: List[MetadataGetResponseBody]


class PartGetResponseBody(TypedDict):
    """GET file part response body."""

    file_id: str
    part_number: int
    upload_date_rfc3339: str
    file_config: Union[
        ConstraintsPartConfig,
        GraphPartConfig,
        HamiltonianPartConfig,
        ObjectivePartConfig,
        QuboPartConfig,
        GpResultsPartConfig,
        IhoResultsPartConfig,
        NqhoContinuousResultsPartConfig,
        NqhoIntegerResultsPartConfig,
        NqhoResultsPartConfig,
        QlcboResultsPartConfig,
        QuboResultsPartConfig,
    ]
