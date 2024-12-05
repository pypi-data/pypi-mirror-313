# Copyright 2023-2024, Quantum Computing Incorporated
"""Client for QCi's optimization API."""

import concurrent.futures
import time
from typing import Optional, Union
import warnings

import requests
from requests.adapters import HTTPAdapter, Retry
from requests.compat import urljoin
from requests_futures.sessions import FuturesSession

from qci_client.utilities import log_to_console, now_utc_ms
import qci_client.auth.client
from qci_client.optimization import utilities
from qci_client.optimization.data_converter import data_to_json
from qci_client.optimization import enum
from qci_client.utilities import raise_for_status

RESULTS_CHECK_INTERVAL_S = 2.5
# We are uploading files we want to retry when we receive certain error codes.
RETRY_TOTAL = 7
BACKOFF_FACTOR = 2
STATUS_FORCELIST = [502, 503, 504]


class OptimizationClient:  # pylint: disable=too-many-public-methods
    """Used to run optimization jobs against QCi hardware."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        *,
        url: Optional[str] = None,
        api_token: Optional[str] = None,
        timeout: Optional[float] = None,
        max_workers: int = 8,
        compress: bool = False,
    ):
        """
        Provides access to QCi's public API for running optimization problems on Dirac
        devices, including file uploads/downloads and submitting/retrieving entire jobs.

        :param url: url basepath to API endpoint, including scheme, if None, then falls
            back to QCI_API_URL environment variable
        :param api_token: refresh token for authenticating to API, if None, then falls
            back to QCI_TOKEN environment variable
        :param timeout: number of seconds before timing out requests, None waits
            indefinitely
        :param max_workers: number of threads for concurrent file download calls
        :param compress: compress file metadata and parts before uploading
        """
        # The optimization client defers to auth client for url, api_token, and timeout.
        self._auth_client = qci_client.auth.client.AuthClient(
            url=url, api_token=api_token, timeout=timeout
        )

        self._max_workers = max_workers
        self._compress = compress

        # Session usage can improve performance. Used in non-concurrent situations.
        self._session = requests.Session()
        self._session.mount(
            "https://",
            HTTPAdapter(
                max_retries=Retry(
                    total=RETRY_TOTAL,
                    backoff_factor=BACKOFF_FACTOR,
                    status_forcelist=STATUS_FORCELIST,
                )
            ),
        )

    @property
    def url(self) -> str:
        """Return API URL."""
        return self._auth_client.url

    @property
    def api_token(self) -> str:
        """Return API token."""
        return self._auth_client.api_token

    @property
    def timeout(self) -> Optional[float]:
        """Return timeout setting."""
        return self._auth_client.timeout

    @property
    def max_workers(self) -> int:
        """Return maximum number of concurrent workers for file operations."""
        return self._max_workers

    @property
    def compress(self) -> bool:
        """Return file compression usage flag."""
        return self._compress

    @property
    def jobs_url(self):
        """Get jobs URL."""
        return urljoin(self.url, "optimization/v1/jobs")

    def get_job_id_url(self, *, job_id: str) -> str:
        """Get job URL with job ID."""
        return f"{self.jobs_url}/{job_id}"

    def get_job_status_url(self, *, job_id: str) -> str:
        """Get job-status URL using job ID."""
        return f"{self.get_job_id_url(job_id=job_id)}/status"

    def get_job_metrics_url(self, job_id: str) -> str:
        """Get legacy job-metrics URL using job ID."""
        return f"{self.get_job_id_url(job_id=job_id)}/metrics"

    def get_job_metrics_v1_url(self, job_id: str) -> str:
        """Get v1 job-metrics URL using job ID."""
        return f"{self.get_job_id_url(job_id=job_id)}/metrics/v1"

    def get_job_metrics_v2_url(self, job_id: str) -> str:
        """Get v2 job-metrics URL using job ID."""
        return f"{self.get_job_id_url(job_id=job_id)}/metrics/v2"

    def get_job_allocations_url(self) -> str:
        """Get job-allocations URL."""
        return f"{self.jobs_url}/allocations"

    @property
    def files_url(self):
        """Get files URL."""
        return urljoin(self.url, "optimization/v1/files")

    def get_file_id_url(self, *, file_id: str) -> str:
        """Get file URL with file ID."""
        return f"{self.files_url}/{file_id}"

    def get_file_contents_url(self, *, file_id: str, part_number: int) -> str:
        """Get file contents URL with file ID and file part number."""
        return f"{self.get_file_id_url(file_id=file_id)}/contents/{str(part_number)}"

    def upload_file(self, *, file: dict) -> dict:
        """
        Upload file (metadata and then parts concurrently). Returns dict with file ID.
        """
        # Use session with maintained connection and multipart concurrency for
        # efficiency.
        file = data_to_json(file=file)

        with FuturesSession(max_workers=self.max_workers) as session:
            session.mount(
                "https://",
                HTTPAdapter(
                    max_retries=Retry(
                        total=RETRY_TOTAL,
                        backoff_factor=BACKOFF_FACTOR,
                        status_forcelist=STATUS_FORCELIST,
                    )
                ),
            )

            post_response_future = session.post(
                self.files_url,
                headers=self._auth_client.headers_without_connection_close,
                timeout=self.timeout,
                json=utilities.get_post_request_body(file=file),
            )

            for response_future in concurrent.futures.as_completed(
                [post_response_future], self.timeout
            ):
                response = response_future.result()
                raise_for_status(response=response)

            file_id = response.json()["file_id"]
            file_part_generator = utilities.file_part_generator(
                file=file, compress=self.compress
            )
            patch_response_futures = []

            if self.compress:
                for part_body, part_number in file_part_generator:
                    patch_response_futures.append(
                        session.patch(
                            self.get_file_contents_url(
                                file_id=file_id, part_number=part_number
                            ),
                            headers=self._auth_client.headers_without_connection_close,
                            timeout=self.timeout,
                            data=utilities.zip_payload(
                                payload=utilities.get_patch_request_body(file=part_body)
                            ),
                        )
                    )
            else:
                for part_body, part_number in file_part_generator:
                    patch_response_futures.append(
                        session.patch(
                            self.get_file_contents_url(
                                file_id=file_id, part_number=part_number
                            ),
                            headers=self._auth_client.headers_without_connection_close,
                            timeout=self.timeout,
                            json=utilities.get_patch_request_body(file=part_body),
                        )
                    )

            # Due to timeout in underlying PATCH, this should not hang despite no
            # timeout.
            for response_future in concurrent.futures.as_completed(
                patch_response_futures
            ):
                raise_for_status(response=response_future.result())

        return {"file_id": file_id}

    def download_file(self, *, file_id: str) -> dict:
        """Download file (metadata and then parts concurrently)."""
        # Use session with maintained connection and multipart concurrency for
        # efficiency.
        with FuturesSession(max_workers=self.max_workers) as session:
            session.mount(
                "https://",
                HTTPAdapter(
                    max_retries=Retry(
                        total=RETRY_TOTAL,
                        backoff_factor=BACKOFF_FACTOR,
                        status_forcelist=STATUS_FORCELIST,
                    )
                ),
            )

            get_response_future = session.get(
                self.get_file_id_url(file_id=file_id),
                headers=self._auth_client.headers_without_connection_close,
                timeout=self.timeout,
            )

            for response_future in concurrent.futures.as_completed(
                [get_response_future], self.timeout
            ):
                response = response_future.result()
                raise_for_status(response=response_future.result())

            # File metadata is base for returned fully assembled file.
            file = {**response.json()}

            # Remove metadata fields that are not well-defined for fully assembled file.
            file.pop("last_accessed_rfc3339")
            file.pop("upload_date_rfc3339")

            get_response_futures = [
                session.get(
                    self.get_file_contents_url(
                        file_id=file_id, part_number=part_number
                    ),
                    headers=self._auth_client.headers_without_connection_close,
                    timeout=self.timeout,
                )
                for part_number in range(1, file["num_parts"] + 1)
            ]

            # Due to timeout in underlying GET, this should not hang despite no timeout.
            for response_future in concurrent.futures.as_completed(
                get_response_futures
            ):
                raise_for_status(response=response_future.result())

            # Unpack in order.
            for response_future in get_response_futures:
                file_part = response_future.result().json()
                # Append to all array fields.
                for file_type, file_type_config in file_part["file_config"].items():
                    if file_type not in file["file_config"]:
                        file["file_config"][file_type] = {}

                    for key, value in file_type_config.items():
                        if key not in file["file_config"][file_type]:
                            file["file_config"][file_type][key] = []

                        file["file_config"][file_type][key] += value

        return file

    def submit_job(self, *, job_body: dict) -> dict:
        """
        Submit a job via a request to QCi's optimization API.

        Args:
            job_body: formatted json body that includes all parameters for the job

        Returns:
            Response from POST call to API (see :meth:`get_job_results`)
        """
        response = self._session.post(
            self.jobs_url,
            json=job_body,
            headers=self._auth_client.headers_without_connection_close,
            timeout=self.timeout,
        )
        raise_for_status(response=response)

        return response.json()

    def cancel_job(self, *, job_id: str) -> dict:
        """
        Cancel a job via a PATCH request to QCi's optimization API.

        Only SUBMITTED, QUEUED, and RUNNING jobs will be successfully cancelled, raising
        an exception otherwise.

        Args:
            job_id: ID of job

        Returns:
            Response from PATCH call to API
        """
        response = self._session.patch(
            self.get_job_id_url(job_id=job_id),
            json={
                "job_status": {
                    "cancelled_at_rfc3339nano": now_utc_ms(),
                },
            },
            headers=self._auth_client.headers_without_connection_close,
            timeout=self.timeout,
        )
        raise_for_status(response=response)

        return response.json()

    def get_job_results(self, *, job_id: str) -> dict:
        """
        Get job_info, status, and results of a (possibly uncompleted) job by its ID.

        Args:
            job_id: ID of job

        Returns:
            Dictionary with latest job_info, status, and results.
        """
        job_info = self.get_job_response(job_id=job_id)
        status = enum.JobStatus(self.get_job_status(job_id=job_id)["status"])

        if status == enum.JobStatus.COMPLETED:
            # Simplify file results for users who wait for known results.
            file = self.download_file(file_id=job_info["job_result"]["file_id"])
            results = utilities.get_file_config(file=file)[0]
        else:
            results = None

        return {"job_info": job_info, "status": status.value, "results": results}

    def get_job_status(self, *, job_id: str) -> dict:
        """
        Get the status of a job by its ID.

        Args:
            job_id: ID of job

        Returns:
            Response from GET call to API
        """
        response = self._session.get(
            self.get_job_status_url(job_id=job_id),
            headers=self._auth_client.headers_without_connection_close,
            timeout=self.timeout,
        )
        raise_for_status(response=response)

        return response.json()

    def get_job_metrics(self, *, job_id: str) -> dict:
        """
        Get the metrics for a job by its ID. v2 metrics are tried first, then
        legacy/v1 metrics.

        Args:
            job_id: ID of job

        Returns:
            Response from GET call to API
        """
        # Try for v2 metrics first.
        response = self._session.get(
            self.get_job_metrics_v2_url(job_id=job_id),
            headers=self._auth_client.headers_without_connection_close,
            timeout=self.timeout,
        )

        # If the metrics endpoint is missing, then try the legacy/v1 metrics endpoint.
        if response.status_code == requests.codes["not_found"]:
            response = self._session.get(
                self.get_job_metrics_url(job_id=job_id),  # Equivalent to v1 metrics.
                headers=self._auth_client.headers_without_connection_close,
                timeout=self.timeout,
            )

        raise_for_status(response=response)

        # If the job metrics are missing in the response, then also try the legacy/v1
        # endpoint. (It's possible that the job simply has not completed, but in this
        # case all endpoints return the same response without any job_metrics field.)
        if response.json().get("job_metrics") is None:
            response = self._session.get(
                self.get_job_metrics_url(job_id=job_id),  # Equivalent to v1 metrics.
                headers=self._auth_client.headers_without_connection_close,
                timeout=self.timeout,
            )

            raise_for_status(response=response)

        return response.json()

    def get_job_response(self, *, job_id: str) -> dict:
        """
        Get a response for a job by id, which may/may not be finished.

        :param job_id: ID of job

        :return dict: json response
        """
        response = self._session.get(
            self.get_job_id_url(job_id=job_id),
            headers=self._auth_client.headers_without_connection_close,
            timeout=self.timeout,
        )
        raise_for_status(response=response)

        return response.json()

    def get_allocations(self) -> dict:
        """
        Get allocations for running jobs on different device classes.

        :return dict: json response
        """
        response = self._session.get(
            self.get_job_allocations_url(),
            headers=self._auth_client.headers_without_connection_close,
            timeout=self.timeout,
        )
        raise_for_status(response=response)

        return response.json()

    def build_job_body(  # pylint: disable=too-many-arguments,too-many-locals,too-many-branches,too-many-statements
        self,
        *,
        job_type: Union[enum.JobType, str],
        job_params: dict,
        qubo_file_id: Optional[str] = None,
        graph_file_id: Optional[str] = None,
        hamiltonian_file_id: Optional[str] = None,
        objective_file_id: Optional[str] = None,
        constraints_file_id: Optional[str] = None,
        polynomial_file_id: Optional[str] = None,
        job_name: Optional[str] = None,
        job_tags: Optional[list] = None,
    ) -> dict:
        """
        Constructs body for job submission requests.

        Args:
            job_type: an enum.JobType or one of the string values defined in enum.JobType
            job_params: dict of params to be passed to job submission in "params" key
            qubo_file_id: file id from files API for uploaded qubo
            graph_file_id: file id from files API for uploaded graph
            hamiltonian_file_id: file id from files API for uploaded hamiltonian
            objective_file_id: file id from files API for uploaded objective
            constraints_file_id: file id from files API for uploaded constraints
            polynomial_file_id: file id from files API for uploaded polynomial
            job_name: user specified name for job submission
            job_tags: user specified labels for classifying and filtering user jobs after submission

        Returns:
            None
        """
        problem_config = {}
        device_config = {}

        # This validates input and works even when job_type is already an enum.JobType.
        job_type = enum.JobType(job_type)

        device_type_param = job_params.get("device_type")

        if device_type_param is None:
            if "sampler_type" in job_params:
                warnings.warn(
                    "the 'sampler_type' key is deprecated, please update your usage to "
                    "'device_type'"
                )
                device_type_param = job_params["sampler_type"]

        if device_type_param is None:
            raise ValueError(
                "no 'device_type' specified in job_params, must be one of "
                f"{enum.DEVICE_TYPES_SORTED}"
            )

        # This works even when device_type_param is already an enum.DeviceType.
        device_type = enum.DeviceType(device_type_param)

        num_samples = job_params.get("num_samples")

        if num_samples is None:
            # Fallback to checking deprecated fields.
            if "n_samples" in job_params:
                warnings.warn(
                    "the 'n_samples' key is deprecated, please update your usage to "
                    "'num_samples'"
                )
                num_samples = job_params["n_samples"]
            elif "nsamples" in job_params:
                warnings.warn(
                    "the 'nsamples' key is deprecated, please update your usage to "
                    "'num_samples'"
                )
                num_samples = job_params["nsamples"]
            elif "num_solutions" in job_params:
                warnings.warn(
                    "the 'num_solutions' key is deprecated, please update your usage "
                    "to 'num_samples'"
                )
                num_samples = job_params["num_solutions"]

        if num_samples is not None:
            # Optional parameter.
            device_config["num_samples"] = num_samples

        if job_type == enum.JobType.GRAPH_PARTITIONING:
            if device_type not in enum.DEVICE_TYPES_QUBIT:
                raise ValueError(
                    f"{job_type.value} not supported on {device_type.value}"
                )

            problem_type = enum.ProblemType.GP

            if not graph_file_id:
                raise AssertionError(
                    "graph_file_id must be specified for the given job_type "
                    f"'{job_type.value}'"
                )

            problem_config["graph_file_id"] = graph_file_id

            if "num_paritions" in job_params:
                # Optional parameter.
                problem_config["num_paritions"] = job_params["num_paritions"]

            if "alpha" in job_params:
                # Optional parameter.
                problem_config["alpha"] = job_params["alpha"]

            if "gamma" in job_params:
                # Optional parameter when num_paritions > 2.
                problem_config["gamma"] = job_params["gamma"]
        elif job_type == enum.JobType.SAMPLE_CONTRAINT:
            if device_type not in enum.DEVICE_TYPES_QUBIT:
                raise ValueError(
                    f"{job_type.value} not supported on {device_type.value}"
                )

            problem_type = enum.ProblemType.QLCBO

            if not constraints_file_id:
                raise AssertionError(
                    "At least constraints_file_id must be specified for job_type "
                    f"'{job_type.value}'"
                )

            problem_config["constraints_file_id"] = constraints_file_id
            problem_config["objective_file_id"] = objective_file_id  # May be None.

            if "alpha" in job_params:
                # Optional parameter.
                problem_config["alpha"] = job_params["alpha"]

            if "atol" in job_params:
                # Optional parameter.
                problem_config["atol"] = job_params["atol"]
        elif job_type == enum.JobType.SAMPLE_HAMILTONIAN:
            if device_type not in enum.DEVICE_TYPES_NORMALIZED_QUDIT:
                raise ValueError(
                    f"{job_type.value} not supported on {device_type.value}"
                )

            if device_type == enum.DeviceType.DIRAC2:
                if job_params.get("solution_precision") != 1:
                    problem_type = enum.ProblemType.NQHO_CONTINUOUS
                else:
                    problem_type = enum.ProblemType.NQHO_INTEGER
            else:
                problem_type = enum.ProblemType.NQHO
                # Ensure device type is mapped to API-accepted value.
                device_type = enum.DeviceType.DIRAC3_NORMALIZED_QUDIT

                if "relaxation_schedule" in job_params:
                    # Optional parameter.
                    device_config["relaxation_schedule"] = job_params[
                        "relaxation_schedule"
                    ]

                if "solution_precision" in job_params:
                    # Optional parameter.
                    device_config["solution_precision"] = job_params[
                        "solution_precision"
                    ]

                if "sum_constraint" in job_params:
                    # Optional parameter.
                    device_config["sum_constraint"] = job_params["sum_constraint"]

                if "mean_photon_number" in job_params:
                    # Optional parameter.
                    device_config["mean_photon_number"] = job_params[
                        "mean_photon_number"
                    ]

                normalized_loss_rate = job_params.get("normalized_loss_rate")

                if normalized_loss_rate is not None:
                    warnings.warn(
                        "the 'normalized_loss_rate' key is deprecated, please update your usage to "
                        "'quantum_fluctuation_coefficient'"
                    )
                    device_config["quantum_fluctuation_coefficient"] = (
                        normalized_loss_rate
                    )

                if "quantum_fluctuation_coefficient" in job_params:
                    device_config["quantum_fluctuation_coefficient"] = job_params[
                        "quantum_fluctuation_coefficient"
                    ]

            if (not hamiltonian_file_id and not polynomial_file_id) or (
                hamiltonian_file_id and polynomial_file_id
            ):
                raise AssertionError(
                    "exactly one of hamiltonian_file_id or polynomial_file_id must be "
                    f"specified for job_type='{job_type.value}'"
                )

            if hamiltonian_file_id:
                problem_config["hamiltonian_file_id"] = (
                    hamiltonian_file_id  # Deprecated.
                )
            else:
                problem_config["polynomial_file_id"] = polynomial_file_id
        elif job_type == enum.JobType.SAMPLE_HAMILTONIAN_INTEGER:
            if device_type not in enum.DEVICE_TYPES_QUDIT:
                raise ValueError(
                    f"{job_type.value} not supported on {device_type.value}"
                )

            problem_type = enum.ProblemType.QHO
            # Ensure device type is mapped to API-accepted value.
            device_type = enum.DeviceType.DIRAC3_QUDIT

            if "num_levels" not in job_params and "domain_max" not in job_params:
                raise AssertionError("num_levels is a required field")

            domain_max = job_params.get("domain_max")

            if domain_max is not None:
                warnings.warn(
                    "the 'domain_max' key is deprecated, please update your usage to "
                    "'num_levels'"
                )
                device_config["num_levels"] = domain_max

            device_config["num_levels"] = job_params["num_levels"]

            if "mean_photon_number" in job_params:
                # Optional parameter.
                device_config["mean_photon_number"] = job_params["mean_photon_number"]

            normalized_loss_rate = job_params.get("normalized_loss_rate")

            if normalized_loss_rate is not None:
                warnings.warn(
                    "the 'normalized_loss_rate' key is deprecated, please update your usage to "
                    "'quantum_fluctuation_coefficient'"
                )
                device_config["quantum_fluctuation_coefficient"] = normalized_loss_rate

            if "quantum_fluctuation_coefficient" in job_params:
                device_config["quantum_fluctuation_coefficient"] = job_params[
                    "quantum_fluctuation_coefficient"
                ]

            if "relaxation_schedule" in job_params:
                # Optional parameter.
                device_config["relaxation_schedule"] = job_params["relaxation_schedule"]

            if (not hamiltonian_file_id and not polynomial_file_id) or (
                hamiltonian_file_id and polynomial_file_id
            ):
                raise AssertionError(
                    "exactly one of hamiltonian_file_id or polynomial_file_id must be "
                    f"specified for job_type='{job_type.value}'"
                )

            if hamiltonian_file_id:
                problem_config["hamiltonian_file_id"] = (
                    hamiltonian_file_id  # Deprecated.
                )
            else:
                problem_config["polynomial_file_id"] = polynomial_file_id
        elif job_type == enum.JobType.SAMPLE_HAMILTONIAN_ISING:
            if device_type not in enum.DEVICE_TYPES_QUBIT:
                raise ValueError(
                    f"{job_type.value} not supported on {device_type.value}"
                )

            problem_type = enum.ProblemType.IHO

            if (not hamiltonian_file_id and not polynomial_file_id) or (
                hamiltonian_file_id and polynomial_file_id
            ):
                raise AssertionError(
                    "exactly one of hamiltonian_file_id or polynomial_file_id must be "
                    f"specified for job_type='{job_type.value}'"
                )

            if hamiltonian_file_id:
                problem_config["hamiltonian_file_id"] = (
                    hamiltonian_file_id  # Deprecated.
                )
            else:
                problem_config["polynomial_file_id"] = polynomial_file_id
        elif job_type == enum.JobType.SAMPLE_QUBO:
            if device_type not in enum.DEVICE_TYPES_QUBIT:
                raise ValueError(
                    f"{job_type.value} not supported on {device_type.value}"
                )

            problem_type = enum.ProblemType.QUBO

            if not qubo_file_id:
                raise AssertionError(
                    f"qubo_file_id must be specified for job_type '{job_type.value}'"
                )

            problem_config["qubo_file_id"] = qubo_file_id
        else:
            raise ValueError(f"unsupported job_type '{job_type.value}'")

        job_submission: dict = {
            "problem_config": {problem_type.value: problem_config},
            "device_config": {device_type.value: device_config},
        }

        if job_name is not None:
            # Optional field.
            job_submission["job_name"] = job_name

        if job_tags is not None:
            # Optional field.
            job_submission["job_tags"] = job_tags

        return {"job_submission": job_submission}

    def process_job(
        self, *, job_body: dict, wait: bool = True, verbose: bool = True
    ) -> dict:
        """
        :param job_body: formatted json dict for body of job submission request
        :param wait: wait synchronously for job to complete
        :param verbose: track operations' progress using timestamped console logs

        :return:
            if wait is True, then dict with job_info, status, and results and results
                fields (results is None if job is not successfully COMPLETED)
            if wait is False, then response dict from submitted job, which includes
                job_id for subsequent retrieval (see :meth:`get_job_results`)
        """
        dirac_allocation = self.get_allocations()["allocations"]["dirac"]
        dirac_allocation_s = dirac_allocation["seconds"]

        log = f"Dirac allocation balance = {dirac_allocation_s} s"

        if not dirac_allocation["metered"]:
            log += " (unmetered)"

        log_to_console(log=log, verbose=verbose)

        submit_job_response = self.submit_job(job_body=job_body)
        job_id = submit_job_response["job_id"]

        log_to_console(log=f"Job submitted: job_id='{job_id}'", verbose=verbose)

        if wait:
            status = enum.JobStatus.SUBMITTED
            while status not in enum.JOB_STATUSES_FINAL:
                latest_status = enum.JobStatus(
                    self.get_job_status(job_id=job_id)["status"]
                )

                if latest_status != status:
                    status = latest_status
                    log_to_console(log=status.value, verbose=verbose)

                time.sleep(RESULTS_CHECK_INTERVAL_S)

            dirac_allocation = self.get_allocations()["allocations"]["dirac"]
            dirac_allocation_s = dirac_allocation["seconds"]

            log = f"Dirac allocation balance = {dirac_allocation_s} s"

            if not dirac_allocation["metered"]:
                log += " (unmetered)"

            log_to_console(log=log, verbose=verbose)

            return self.get_job_results(job_id=job_id)

        return submit_job_response

    def list_files(self) -> dict:
        """
        List files (metadata only).

        :return: dict containing list of files
        """
        response = self._session.get(
            self.files_url,
            headers=self._auth_client.headers_without_connection_close,
            timeout=self.timeout,
        )
        raise_for_status(response=response)

        return response.json()
