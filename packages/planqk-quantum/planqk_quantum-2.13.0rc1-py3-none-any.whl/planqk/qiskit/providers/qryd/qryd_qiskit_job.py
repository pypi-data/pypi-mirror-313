from typing import Optional

from planqk.client.client import _PlanqkClient
from planqk.client.job_dtos import JobDto
from planqk.qiskit import PlanqkQiskitJob
from qiskit.providers import Backend, JobStatus
from qiskit.result.models import ExperimentResult, ExperimentResultData


class PlanqkQrydQiskitJob(PlanqkQiskitJob):

    def __init__(self, backend: Optional[Backend], job_id: Optional[str] = None, job_details: Optional[JobDto] = None,
                 planqk_client: Optional[_PlanqkClient] = None):

        super().__init__(backend, job_id, job_details, planqk_client)

    def _create_experiment_result(self, provider_result: dict) -> ExperimentResult:

        if "data" not in provider_result:
            raise KeyError("The expected key 'data' was not found in Qryd job result")

        if "counts" not in provider_result["data"]:
            raise KeyError("The expected key 'counts' was not found in Qryd job result ['data']")

        if "num_qubits" not in provider_result:
            raise KeyError("The expected key 'num_qubits' was not found in Qryd job result")

        num_qubits = provider_result["num_qubits"]
        counts = {self._to_bitstring(hex_str, num_qubits): count for hex_str, count in provider_result["data"]["counts"].items()}

        return ExperimentResult(
            shots=self.shots,
            success=True,
            status=JobStatus.DONE.name,
            data=ExperimentResultData(
                counts=counts,
                memory=[]
            ),
        )

    @staticmethod
    def _to_bitstring(hex_str: str, num_qubits):
        int_value = int(hex_str, 16)
        # flip bitstring to convert to little Endian
        return format(int(int_value), f"0{num_qubits}b")[::-1]