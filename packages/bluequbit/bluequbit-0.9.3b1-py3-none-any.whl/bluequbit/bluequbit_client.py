from __future__ import annotations

import contextlib
import logging
import os
import time
from typing import TYPE_CHECKING, Any, Callable, Union

from . import job_metadata_constants
from .api import jobs
from .backend_connection import BackendConnection
from .check_version import check_version
from .circuit_serialization import isa_qiskit_circuit
from .computation_local import run_circuit_cirq, run_circuit_qiskit
from .estimate_result import EstimateResult
from .exceptions import (
    BQBatchJobsLimitExceededError,
    BQCPUJobsLimitExceededError,
    BQJobCouldNotCancelError,
    BQJobInvalidDeviceTypeError,
    BQJobNotCompleteError,
    BQJobsLimitExceededError,
    BQJobsMalformedShotsError,
    BQSDKUsageError,
)
from .job_result import JobResult
from .version import __version__

if TYPE_CHECKING:
    import datetime

# TODO this requires imports of actual quantum libraries for proper type
# checking.
CircuitT = Any

PauliSumT = Union[list[tuple[str, float]], str]

logger = logging.getLogger("bluequbit-python-sdk")


_SHOTS_LIMIT_NON_QPU = 131072


def _run_circuits_local(circuits, shots, backend_connection):
    created_on = time.time()

    def _format_result(r, num_qubits):
        def to_str_time(x):
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x))

        r["created_on"] = to_str_time(created_on)
        r["run_start"] = to_str_time(r["run_start"])
        r["run_end"] = to_str_time(r["run_end"])
        # Rename counts to top_100k
        r["top_100k"] = r["counts"]
        del r["counts"]
        r["has_statevector"] = "state_vector" in r
        r["num_qubits"] = num_qubits
        r["run_status"] = "COMPLETED"
        return JobResult(r, backend_connection)

    first_circuit = circuits[0] if isinstance(circuits, list) else circuits
    try:
        from deqart_internal.circuit_info import get_num_qubits
        from deqart_internal.computation import run_circuit_object

        try:
            import cuquantum  # noqa: F401

            device_type = "gpu"
        except ImportError:
            # Not in a cuQuantum Appliance
            device_type = "cpu"
        print(f"Using cuQuantum cuStateVec with device type {device_type}")

        def _run_and_format_result(circuit):
            r = run_circuit_object(circuit, device_type, shots=shots)
            num_qubits = get_num_qubits(circuit)
            return _format_result(r, num_qubits)

        if isinstance(circuits, list):
            return [_run_and_format_result(c) for c in circuits]
        return _run_and_format_result(circuits)
    except (ImportError, ModuleNotFoundError):
        fn: Callable
        if isa_qiskit_circuit(first_circuit):
            fn = run_circuit_qiskit
        elif str(type(first_circuit)) == "<class 'cirq.circuits.circuit.Circuit'>":
            fn = run_circuit_cirq
        else:
            error_msg = f"Circuit type not yet supported for {first_circuit}"
            raise BQSDKUsageError(error_msg) from None

        if isinstance(circuits, list):
            return [_format_result(fn(c, shots=shots), len(c.qubits)) for c in circuits]
        return _format_result(fn(circuits, shots=shots), len(circuits.qubits))


class BQClient:
    """Client for managing jobs on BlueQubit platform.

    :param api_token: API token of the user. If ``None``, the token will be looked
                      in the environment variable BLUEQUBIT_API_TOKEN.
    """

    _job_name_prefix_cls: str | None = None

    def __init__(self, api_token: str | None = None):
        super().__init__()
        if os.environ.get("BLUEQUBIT_TESTING") is None:
            with contextlib.suppress(Exception):
                check_version(__version__)

        self._backend_connection = BackendConnection(api_token)

        self.job_name_prefix: str | None = BQClient._job_name_prefix_cls

    def name(self):
        return "BlueQubit"

    def validate_device(self, device):
        if not isinstance(device, str):
            raise BQJobInvalidDeviceTypeError(device)
        converted_device = device.lower()
        if converted_device not in job_metadata_constants.DEVICE_TYPES:
            raise BQJobInvalidDeviceTypeError(device)
        return converted_device

    @staticmethod
    def validate_batch(batch):
        if not isinstance(batch, list):
            return False
        if len(batch) > job_metadata_constants.MAXIMUM_NUMBER_OF_BATCH_JOBS:
            raise BQBatchJobsLimitExceededError(len(batch))
        return True

    @staticmethod
    def validate_batch_for_run(batch, device):
        if not BQClient.validate_batch(batch):
            return
        if len(batch) > job_metadata_constants.MAXIMUM_NUMBER_OF_JOBS_FOR_RUN:
            raise BQJobsLimitExceededError(len(batch))
        if (
            "cpu" in device
            and len(batch) > job_metadata_constants.QUEUED_CPU_JOBS_LIMIT
        ):
            raise BQCPUJobsLimitExceededError(len(batch))

    def estimate(
        self, circuits: CircuitT | list[CircuitT], device: str = "cpu"
    ) -> EstimateResult | list[EstimateResult]:
        """Estimate job runtime

        :param circuits: quantum circuit or circuits
        :type circuits: Cirq, Qiskit, list
        :param device: device for which to estimate the circuit. Can be one of
                       ``"cpu"`` | ``"gpu"`` | ``"quantum"``
        :return: result or results estimate metadata
        """
        device = self.validate_device(device)
        self.validate_batch(circuits)
        response = jobs.submit_jobs(
            self._backend_connection, circuits, device, estimate_only=True
        )
        if isinstance(circuits, list):
            return [EstimateResult(data) for data in response]
        return EstimateResult(response)

    def run(
        self,
        circuits: CircuitT | list[CircuitT],
        device: str = "cpu",
        asynchronous: bool = False,
        job_name: str | None = None,
        shots: int | None = None,
        pauli_sum: PauliSumT | list[PauliSumT] | None = None,
    ) -> JobResult | list[JobResult]:
        """Submit a job to run on BlueQubit platform

        :param circuits: quantum circuit or list of circuits
        :type circuits: Cirq, Qiskit, list
        :param device: device on which to run the circuit. Can be one of
                       ``"cpu"`` | ``"gpu"`` | ``"quantum"`` | ``"local"``
        :param asynchronous: if set to ``False``, wait for job completion before
                             returning. If set to ``True``, return immediately
        :param job_name: customizable job name
        :param shots: number of shots to run. If device is quantum and shots is None then
                      it is set to 1000. For non quantum devices, if None, full
                      probability distribution will be returned. For non quantum
                      devices it is limited to 131072
        :param pauli_sum: The Pauli sum or a list of Pauli sum which
                          expectation value is the computation result
        :return: job or jobs metadata
        """
        device = self.validate_device(device)
        self.validate_batch_for_run(circuits, device)
        if device == "quantum" and shots is None:
            shots = 1000
        if shots is not None and (
            not isinstance(shots, int)
            or shots > job_metadata_constants.MAXIMUM_NUMBER_OF_SHOTS
        ):
            raise BQJobsMalformedShotsError(shots)
        if device == "local":
            return _run_circuits_local(circuits, shots, self._backend_connection)
        response = jobs.submit_jobs(
            self._backend_connection,
            circuits,
            device,
            (
                job_name
                if self.job_name_prefix is None
                else self.job_name_prefix + str(job_name)
            ),
            shots=shots,
            asynchronous=asynchronous,
            pauli_sum=pauli_sum,
        )
        if isinstance(circuits, list):
            logger.info(
                "Submitted %s jobs. Batch ID %s", len(response), response[0]["batch_id"]
            )

            def add_circuit_to_all(job_results, circuits):
                for job_result, circuit in zip(job_results, circuits):
                    job_result.circuit = circuit

            job_results = [
                JobResult(data, self._backend_connection) for data in response
            ]
            if not asynchronous:
                if self._check_all_in_terminal_states(job_results):
                    add_circuit_to_all(job_results, circuits)
                    return job_results

                waited_job_results = self.wait(job_results)
                add_circuit_to_all(waited_job_results, circuits)
                return waited_job_results
                # if job_results[0].batch_id is not None:
                #     return self.wait(batch_id=job_results[0].batch_id)
                # else:
            add_circuit_to_all(job_results, circuits)
            return job_results
        submitted_job = JobResult(response, self._backend_connection)
        if (
            submitted_job.run_status
            in job_metadata_constants.JOB_NO_RESULT_TERMINAL_STATES
        ):
            raise BQJobNotCompleteError(
                submitted_job.job_id,
                submitted_job.run_status,
                submitted_job.error_message,
            )
        logger.info("Submitted: %s", submitted_job)
        if (
            not asynchronous
            and submitted_job.run_status
            not in job_metadata_constants.JOB_TERMINAL_STATES
        ):
            jr = self.wait(submitted_job.job_id)
            assert isinstance(jr, JobResult)
            jr.circuit = circuits
            return jr
        submitted_job.circuit = circuits
        return submitted_job

    @staticmethod
    def _check_all_in_terminal_states(job_results):
        if not isinstance(job_results, list):
            return job_results.run_status in job_metadata_constants.JOB_TERMINAL_STATES
        return all(
            job_result.run_status in job_metadata_constants.JOB_TERMINAL_STATES
            for job_result in job_results
        )

    def wait(
        self, job_ids: str | list[str] | JobResult | list[JobResult]
    ) -> JobResult | list[JobResult]:
        """Wait for job completion

        :param job_ids: job IDs that can be found as property of :class:`JobResult` metadata
                        of :func:`~run` method, or `JobResult` instances from which job IDs
                        will be extracted
        :return: job metadata
        """
        self.validate_batch(job_ids)
        while True:
            job_results = self._get(job_ids, need_qc_unprocessed=False)
            if self._check_all_in_terminal_states(job_results):
                if not isinstance(job_ids, list):
                    assert isinstance(job_results, JobResult)
                    if (
                        job_results.run_status
                        in job_metadata_constants.JOB_NO_RESULT_TERMINAL_STATES
                    ):
                        raise BQJobNotCompleteError(
                            job_ids, job_results.run_status, job_results.error_message
                        )
                return job_results
            time.sleep(1.0)

    def get(
        self,
        job_ids: str | list[str] | JobResult | list[JobResult],
    ) -> JobResult | list[JobResult]:
        """Get current metadata of jobs

        :param job_ids: job IDs that can be found as property of :class:`JobResult` metadata
                        of :func:`~run` method
        :return: jobs metadata
        """
        return self._get(job_ids)

    def _get(
        self,
        job_ids: str | list[str] | JobResult | list[JobResult],
        need_qc_unprocessed=True,
    ) -> JobResult | list[JobResult]:
        self.validate_batch(job_ids)
        job_ids_list = job_ids if isinstance(job_ids, list) else [job_ids]
        if isinstance(job_ids_list[0], JobResult):
            job_ids_list = [jr.job_id for jr in job_ids_list]  # type: ignore[union-attr]
        job_results = jobs.search_jobs(
            self._backend_connection,
            job_ids=job_ids_list,
            need_qc_unprocessed=need_qc_unprocessed,
        )
        job_results = [
            JobResult(r, self._backend_connection) for r in job_results["data"]
        ]
        if isinstance(job_ids, list):
            return job_results
        return job_results[0]

    def cancel(
        self, job_ids: str | list[str] | JobResult | list[JobResult]
    ) -> JobResult | list[JobResult]:
        """Submit jobs cancel request

        :param job_ids: job IDs that can be found as property of :class:`JobResult` metadata
                        of :func:`run` method
        :return: job or jobs metadata
        """
        self.validate_batch(job_ids)
        if isinstance(job_ids, JobResult):
            job_ids = job_ids.job_id
        elif isinstance(job_ids, list) and isinstance(job_ids[0], JobResult):
            job_ids = [jr.job_id for jr in job_ids]  # type: ignore[union-attr]
        responses = jobs.cancel_jobs(self._backend_connection, job_ids)
        if isinstance(job_ids, list):
            for response in responses:
                if response["ret"] == "FAILED":
                    logger.warning(response["error_message"])
        try:
            self.wait(job_ids)
        except BQJobNotCompleteError as e:
            if not e.run_status == "CANCELED":
                raise BQJobCouldNotCancelError(
                    e.job_id, e.run_status, e.error_message
                ) from None
        return self.get(job_ids)

    def search(
        self,
        run_status: str | None = None,
        created_later_than: str | datetime.datetime | None = None,
        batch_id: str | None = None,
    ) -> list[JobResult]:
        """Search jobs

        :param run_status: if not ``None``, run status of jobs to filter.
                           Can be one of ``"FAILED_VALIDATION"`` | ``"PENDING"`` |
                           ``"QUEUED"`` | ``"RUNNING"`` | ``"TERMINATED"`` | ``"CANCELED"`` |
                           ``"NOT_ENOUGH_FUNDS"`` | ``"COMPLETED"``

        :param created_later_than: if not ``None``, filter by latest job creation datetime.
                                   Please add timezone for clarity, otherwise UTC
                                   will be assumed

        :param batch_id: if not ``None``, filter by batch ID

        :return: metadata of jobs
        """
        job_results = jobs.search_jobs(
            self._backend_connection, run_status, created_later_than, batch_id=batch_id
        )
        return [JobResult(r, self._backend_connection) for r in job_results["data"]]
