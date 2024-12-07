from qiskit import QuantumCircuit

from planqk.qiskit.options import OptionsV2
from planqk.qiskit.providers.azure.azure_backend import PlanqkAzureQiskitBackend


class PlanqkAzureIonqBackend(PlanqkAzureQiskitBackend):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def _default_options(cls):
        return OptionsV2(
            gateset="qis",
            memory=False
        )

    def _convert_to_job_params(self, job_input: QuantumCircuit = None, options=None) -> dict:
        memory_option = options.get("memory", None)
        return {"memory": memory_option} if memory_option is not None else {}
