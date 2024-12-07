from typing import Optional

from qiskit.circuit import Gate
from qiskit_ionq.helpers import qiskit_circ_to_ionq_circ

from planqk.client.model_enums import Job_Input_Format
from planqk.qiskit import PlanqkQiskitBackend


class PlanqkAzureQiskitBackend(PlanqkQiskitBackend):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _to_gate(self, name: str) -> Optional[Gate]:
        name = name.lower()
        return Gate(name, 0, [])

    def _get_single_qubit_gate_properties(self) -> dict:
        return {None: None}

    def _get_multi_qubit_gate_properties(self) -> dict:
        return {None: None}

    def _convert_to_job_input(self, job_input, options=None):
        gateset = options.get("gateset", "qis")
        ionq_circ, _, _ = qiskit_circ_to_ionq_circ(job_input, gateset=gateset)
        return {
            "gateset": gateset,
            "qubits": job_input.num_qubits,
            "circuit": ionq_circ,
        }

    def _get_job_input_format(self) -> Job_Input_Format:
        return Job_Input_Format.IONQ_CIRCUIT_V1
