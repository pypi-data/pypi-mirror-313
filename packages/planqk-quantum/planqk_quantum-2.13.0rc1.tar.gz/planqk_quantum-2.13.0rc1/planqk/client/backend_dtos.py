from datetime import time, date
from typing import Dict
from typing import List
from typing import Optional

from planqk.client.dto_utils import init_with_defined_params
from planqk.client.model_enums import Provider, BackendType, Hardware_Provider, BackendStatus, Job_Input_Format
from pydantic import BaseModel


class DocumentationDto(BaseModel):
    description: Optional[str] = None
    url: Optional[str] = None
    # status_url: Optional[str] = None
    location: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict):  # TODO das auf alle inits anwenden
        return init_with_defined_params(cls, data)


class QubitDto(BaseModel):
    id: str

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**data)


class GateDto(BaseModel):
    name: str
    native_gate: bool

    @classmethod
    def from_dict(cls, data: Dict):
        return init_with_defined_params(cls, data)


class ConnectivityDto(BaseModel):
    fully_connected: bool
    graph: Optional[Dict[str, List[str]]] = None

    @classmethod
    def from_dict(cls, data: Dict):
        return init_with_defined_params(cls, data)


class ShotsRangeDto(BaseModel):
    min: int
    max: int

    @classmethod
    def from_dict(cls, data: Dict):
        return init_with_defined_params(cls, data)


class ConfigurationDto(BaseModel):
    gates: List[GateDto]
    instructions: List[str]
    qubits: Optional[List[QubitDto]] = None
    qubit_count: int
    connectivity: Optional[ConnectivityDto] = None
    supported_input_formats: List[Job_Input_Format]
    shots_range: ShotsRangeDto
    memory_result_supported: Optional[bool] = False
    options: Optional[Dict] = None

    def __post_init__(self):
        self.gates = [GateDto.from_dict(gate) for gate in self.gates]
        self.qubits = [QubitDto.from_dict(qubit) for qubit in self.qubits]
        self.connectivity = ConnectivityDto.from_dict(self.connectivity)
        self.supported_input_formats = [Job_Input_Format(input_format) for input_format in self.supported_input_formats]
        self.shots_range = ShotsRangeDto.from_dict(self.shots_range)

    @classmethod
    def from_dict(cls, data: Dict):
        return init_with_defined_params(cls, data)


class AvailabilityTimesDto(BaseModel):
    granularity: str
    start: time
    end: time

    @classmethod
    def from_dict(cls, data: Dict):
        return init_with_defined_params(cls, data)


class CostDto(BaseModel):
    granularity: str
    currency: str
    value: float

    @classmethod
    def from_dict(cls, data: Dict):
        return init_with_defined_params(cls, data)


class BackendStateInfosDto(BaseModel):
    status: BackendStatus
    queue_avg_time: Optional[int] = None
    queue_size: Optional[int] = None
    provider_token_valid: Optional[bool] = None

    def __post_init__(self):
        self.status = BackendStatus(self.status) if self.status else None

    @classmethod
    def from_dict(cls, data: Dict):
        return init_with_defined_params(cls, data)


class BackendDto(BaseModel):
    id: str
    provider: Provider
    internal_id: Optional[str] = None
    hardware_provider: Optional[Hardware_Provider] = None
    name: Optional[str] = None
    documentation: Optional[DocumentationDto] = None
    configuration: Optional[ConfigurationDto] = None
    type: Optional[BackendType] = None
    status: Optional[BackendStatus] = None
    availability: Optional[List[AvailabilityTimesDto]] = None
    costs: Optional[List[CostDto]] = None
    updated_at: Optional[date] = None
    avg_queue_time: Optional[int] = None
