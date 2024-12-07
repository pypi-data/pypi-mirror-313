import random
from collections import defaultdict
from typing import Optional

import numpy as np
from planqk.client.client import _PlanqkClient
from planqk.client.job_dtos import JobDto
from planqk.qiskit import PlanqkQiskitJob
from qiskit.providers import Backend, JobStatus
from qiskit.result.models import ExperimentResult


class PlanqkAzureQiskitJob(PlanqkQiskitJob):

    def __init__(self, backend: Optional[Backend], job_id: Optional[str] = None, job_details: Optional[JobDto] = None,
                 planqk_client: Optional[_PlanqkClient] = None):

        super().__init__(backend, job_id, job_details, planqk_client)

    def _create_experiment_result(self, provider_result: dict) -> ExperimentResult:
        """
        Transform the Azure IonQ simulator result to Qiskit result format.

        Adapted from Azure Quantum Qiskit SDK's job.py module.

        Original source:
        Azure Quantum SDK (MIT License)
        GitHub Repository: https://github.com/microsoft/azure-quantum-python/blob/main/azure-quantum/azure/quantum/qiskit/job.py
        """
        job_result = {"data": self._format_ionq_results(provider_result),
                      "success": True,
                      "header": {},
                      "status": JobStatus.DONE.name,
                      "shots": self.shots}

        return ExperimentResult.from_dict(job_result)

    def _format_ionq_results(self, provider_result: dict) -> dict:
        num_qubits_str = self._job_details.input_params.get("qubits")
        if not num_qubits_str:
            raise KeyError(f"Job with ID {self.id()} does not have the required metadata (num_qubits) to format IonQ results.")

        num_qubits = int(num_qubits_str)

        if not 'histogram' in provider_result:
            raise KeyError("Histogram missing in IonQ Job results")

        counts = defaultdict(int)
        probabilities = defaultdict(int)
        for key, value in provider_result['histogram'].items():
            bitstring = self._to_bitstring(key, num_qubits)
            probabilities[bitstring] += value

        if self.backend().configuration().simulator:
            counts = self._draw_random_sample(probabilities, self.shots)
        else:
            counts = {bitstring: np.round(self.shots * value) for bitstring, value in probabilities.items()}

        self._job_details.input_params.get("memory")

        memory = []
        memory_param = self._job_details.input_params.get("memory")
        if memory_param is not None and memory_param.lower() == "true":
            # Azure Ionq simulator does not support memory natively, hence, it is randomly created. Memory is required for supporting pennylane
            memory = self._generate_random_memory(counts, self.shots)

        return {"counts": counts, "probabilities": probabilities, "memory": memory}

    @staticmethod
    def _to_bitstring(k: str, num_qubits):
        # flip bitstring to convert to little Endian
        return format(int(k), f"0{num_qubits}b")[::-1]

    def _draw_random_sample(self, probabilities, shots):
        _norm = sum(probabilities.values())
        if _norm != 1:
            if np.isclose(_norm, 1.0, rtol=1e-4):
                probabilities = {k: v / _norm for k, v in probabilities.items()}
            else:
                raise ValueError(f"Probabilities do not add up to 1: {probabilities}")

        import hashlib
        id = self.job_id()
        sampler_seed = int(hashlib.sha256(id.encode('utf-8')).hexdigest(), 16) % (2 ** 32 - 1)

        rand = np.random.RandomState(sampler_seed)
        rand_values = rand.choice(list(probabilities.keys()), shots, p=list(probabilities.values()))
        return dict(zip(*np.unique(rand_values, return_counts=True)))

    def _generate_random_memory(self, counts: dict, shots: int):
        return random.choices(list(counts.keys()), weights=counts.values(), k=shots)
