from typing import Optional

from qiskit.providers import JobV1, JobStatus, Backend
from qiskit.qobj import QobjExperimentHeader
from qiskit.result import Result
from qiskit.result.models import ExperimentResult, ExperimentResultData

from planqk.client.client import _PlanqkClient
from planqk.client.job_dtos import JobDto
from planqk.job import PlanqkBaseJob

JobStatusMap = {
    "CREATED": JobStatus.INITIALIZING,
    "PENDING": JobStatus.QUEUED,
    "RUNNING": JobStatus.RUNNING,
    "COMPLETED": JobStatus.DONE,
    "FAILED": JobStatus.ERROR,
    "CANCELLING": JobStatus.RUNNING,
    "CANCELLED": JobStatus.CANCELLED,
    "UNKNOWN": JobStatus.INITIALIZING,
}


class PlanqkQiskitJob(PlanqkBaseJob, JobV1):
    def __init__(self, backend: Optional[Backend], job_id: Optional[str] = None, job_details: Optional[JobDto] = None,
                 planqk_client: Optional[_PlanqkClient] = None):
        """
        Constructor for internal use only. This constructor initializes a PlanqkQiskitJob object and should not be used
        directly to create a job. Instead, use the appropriate methods provided by qiskit.providers.Backend or
        provider.PlanqkQuantumProvider to create or retrieve jobs
        """

        PlanqkBaseJob.__init__(self, backend=backend, job_id=job_id, job_details=job_details, planqk_client=planqk_client)
        JobV1.__init__(self, backend=backend, job_id=job_id, shots=self._job_details.shots)

    def submit(self):
        super()._submit()

    def _create_experiment_result(self, provider_result: dict) -> ExperimentResult:
        return ExperimentResult(
            shots=self.shots,
            success=True,
            status=JobStatus.DONE.name,
            data=ExperimentResultData(
                counts=provider_result.get("counts") or {},
                memory=provider_result.get("memory") or []
            ),
        )

    def result(self) -> Result:
        """
        Return the result of the job.
        """
        provider_result_data = super()._result()

        experiment_result = self._create_experiment_result(provider_result_data)

        # Header required for PennyLane-Qiskit Plugin as it identifies the result based on the circuit name which is always "circ0"
        experiment_result.header = QobjExperimentHeader(name="circ0")

        result = Result(
            backend_name=self._backend.name,
            backend_version=self._backend.version,
            job_id=self._job_id,
            qobj_id=0,
            success=True,
            results=[experiment_result],
            status=JobStatus.DONE,
            date=self._job_details.ended_at,
        )

        return result

    def status(self) -> JobStatus:
        """
        Return the status of the job.
        """
        status = super()._update_state()
        return JobStatusMap[status]

    def to_dict(self) -> dict:
        """
        Return a dictionary representation of the job.
        """
        return {key: value for key, value in vars(self).items() if not key.startswith('_')}

    def backend(self) -> Backend:
        """Return the backend where this job was executed."""
        if self._backend is None:
            from planqk.qiskit import PlanqkQiskitBackend
            self._backend = PlanqkQiskitBackend(self._job_details.backend_id, planqk_client=self._client)
        return self._backend

    def queue_position(self):
        """
        Return the position of the job in the server queue.
        """
        return None


# Keep for backward compatibility reasons
PlanqkJob = PlanqkQiskitJob
