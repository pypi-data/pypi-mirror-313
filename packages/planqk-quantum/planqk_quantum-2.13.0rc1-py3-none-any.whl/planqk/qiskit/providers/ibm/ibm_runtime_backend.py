from planqk.qiskit.providers.ibm.ibm_backend import PlanqkIbmQiskitBackend


class PlanqkIbmRuntimeBackend(PlanqkIbmQiskitBackend):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
