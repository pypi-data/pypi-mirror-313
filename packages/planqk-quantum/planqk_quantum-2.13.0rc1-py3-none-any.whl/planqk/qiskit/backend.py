from abc import abstractmethod, ABC
from typing import Optional, Union

from qiskit.circuit import Instruction as QiskitInstruction, Delay, Parameter
from qiskit.circuit import Measure
from qiskit.providers import BackendV2
from qiskit.providers.models import QasmBackendConfiguration, GateConfig
from qiskit.transpiler import Target

from planqk.backend import PlanqkBackend
from planqk.client.backend_dtos import ConfigurationDto, BackendDto
from planqk.client.job_dtos import JobDto
from planqk.client.model_enums import BackendType
from .job import PlanqkQiskitJob
from .options import OptionsV2
from ..client.client import _PlanqkClient


class PlanqkQiskitBackend(PlanqkBackend, BackendV2, ABC):

    def __init__(  # pylint: disable=too-many-arguments
            self,
            planqk_client: _PlanqkClient,
            backend_info: BackendDto,
            **fields,
    ):
        """PlanqkBackend for executing Qiskit circuits against PlanQK devices.

        Example:
            provider = PlanqkQuantumProvider()
            actual = provider.get_backend("azure.ionq.simulator")
            transpiled_circuit = transpile(circuit, actual=actual)
            actual.run(transpiled_circuit, shots=10).result().get_counts()
            {"100": 10, "001": 10}

        Args:
            backend_info: PlanQK actual infos
            provider: Qiskit provider for this actual
            name: name of actual
            description: description of actual
            online_date: online date
            backend_version: actual version
            **fields: other arguments
        """

        PlanqkBackend.__init__(self, planqk_client=planqk_client, backend_info=backend_info)
        BackendV2.__init__(self,
                           provider=backend_info.provider.name,
                           name=backend_info.id,
                           description=f"PlanQK Backend: {backend_info.hardware_provider.name} {backend_info.id}.",
                           online_date=backend_info.updated_at,
                           backend_version="2",
                           **fields)

        self._normalize_qubit_indices()
        self._target = self._planqk_backend_to_target()
        self._configuration = self._planqk_backend_dto_to_configuration()
        self._instance = None

    @abstractmethod
    def _to_gate(self, name: str):
        pass

    @abstractmethod
    def _get_single_qubit_gate_properties(self):
        pass

    @abstractmethod
    def _get_multi_qubit_gate_properties(self):
        pass

    non_gate_instr_mapping = {
        "delay": Delay(Parameter("t")),
        "measure": Measure(),
    }

    def _normalize_qubit_indices(self):
        pass

    @property
    def is_simulator(self):
        return self.backend_info.type == BackendType.SIMULATOR

    def _to_non_gate_instruction(self, name: str) -> Optional[QiskitInstruction]:
        instr = self.non_gate_instr_mapping.get(name, None)
        if instr is not None:
            instr.has_single_gate_props = True
            return instr
        return None


    class PlanqkQiskitTarget(Target):
        def __init__(self, configuration: ConfigurationDto, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._configuration= configuration

        @property
        def physical_qubits(self):
            return sorted(int(qubit.id) for qubit in self._configuration.qubits)

        @property
        def num_qubits(self):
            return self._configuration.qubit_count

        @num_qubits.setter
        def num_qubits(self, value):
            """
            Ignore any attempts to modify num_qubits as always the number of qubits of the configuration must be returned
            """
            pass


    def _planqk_backend_to_target(self) -> Target:
        """Converts properties of a PlanQK actual into Qiskit Target object.

        Returns:
            target for Qiskit actual
        """

        configuration: ConfigurationDto = self.backend_info.configuration
        qubit_count: int = configuration.qubit_count
        target = self.PlanqkQiskitTarget(configuration=configuration, description=f"Target for PlanQK actual {self.name}", num_qubits=qubit_count)

        single_qubit_props = self._get_single_qubit_gate_properties()
        multi_qubit_props = self._get_multi_qubit_gate_properties()
        gates_names = {gate.name.lower() for gate in configuration.gates}

        for gate in gates_names:
            gate = self._to_gate(gate)

            if gate is None:
                continue

            if gate.num_qubits == 1:
                target.add_instruction(instruction=gate, properties=single_qubit_props)
            elif gate.num_qubits > 1:
                target.add_instruction(instruction=gate, properties=multi_qubit_props)
            elif gate.num_qubits == 0 and single_qubit_props == {None: None}:
                # For gates without qubit number qargs can not be determined
                target.add_instruction(instruction=gate, properties={None: None})

        target.add_instruction(Measure(), single_qubit_props)

        non_gate_instructions = set(configuration.instructions).difference(gates_names).difference({'measure'})
        for non_gate_instruction_name in non_gate_instructions:
            instruction = self._to_non_gate_instruction(non_gate_instruction_name)
            if instruction is not None:
                if instruction.has_single_gate_props:
                    target.add_instruction(instruction, single_qubit_props)
                else:
                    target.add_instruction(instruction=instruction, name=non_gate_instruction_name)

        return target

    def _planqk_backend_dto_to_configuration(self) -> QasmBackendConfiguration:
        basis_gates = [self._get_gate_config_from_target(basis_gate.name)
                       for basis_gate in self.backend_info.configuration.gates if basis_gate.native_gate
                       and self._get_gate_config_from_target(basis_gate.name) is not None]
        gates = [self._get_gate_config_from_target(gate.name)
                 for gate in self.backend_info.configuration.gates if not gate.native_gate
                 and self._get_gate_config_from_target(gate.name) is not None]

        return QasmBackendConfiguration(
            backend_name=self.name,
            backend_version=self.backend_version,
            n_qubits=self.backend_info.configuration.qubit_count,
            basis_gates=basis_gates,
            gates=gates,
            local=False,
            simulator=self.backend_info.type == BackendType.SIMULATOR,
            conditional=False,
            open_pulse=False,
            memory=self.backend_info.configuration.memory_result_supported,
            max_shots=self.backend_info.configuration.shots_range.max,
            coupling_map=self.coupling_map,
            supported_instructions=self._target.instructions,
            max_experiments=self.backend_info.configuration.shots_range.max,  # Only one circuit is supported per job
            description=self.backend_info.documentation.description,
            min_shots=self.backend_info.configuration.shots_range.min,
            online_date=self.backend_info.updated_at  # TODO replace with online date
        )

    def _get_gate_config_from_target(self, name) -> GateConfig:
        operations = [operation for operation in self._target.operations
                      if isinstance(operation.name, str)  # Filters out the IBM conditional instructions having no name
                      and operation.name.casefold() == name.casefold()]
        if len(operations) == 1:
            operation = operations[0]
            return GateConfig(
                name=name,
                parameters=operation.params,
                qasm_def='',
            )

    @property
    def target(self):
        return self._target

    @property
    def max_circuits(self):
        return None

    @classmethod
    def _default_options(cls):
        return OptionsV2()

    def _run_job(self, job_request: JobDto) -> Union[PlanqkQiskitJob]:
        from planqk.qiskit.job_factory import PlanqkQiskitJobFactory
        return PlanqkQiskitJobFactory.create_job(backend=self, job_details=job_request, planqk_client=self._planqk_client)

    def retrieve_job(self, job_id: str) -> PlanqkQiskitJob:
        """Return a single job.

        Args:
            job_id: id of the job to retrieve.

        Returns:
            The job with the given id.
        """
        from planqk.qiskit.job_factory import PlanqkQiskitJobFactory
        return PlanqkQiskitJobFactory.create_job(backend=self, job_id=job_id, planqk_client=self._planqk_client)

    def configuration(self) -> QasmBackendConfiguration:
        """Return the actual configuration.

        Returns:
            QasmBackendConfiguration: the configuration for the actual.
        """
        return self._configuration


