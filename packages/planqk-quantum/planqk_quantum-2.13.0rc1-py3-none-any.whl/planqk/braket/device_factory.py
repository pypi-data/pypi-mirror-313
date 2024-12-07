from typing import Dict, Type

from planqk.braket.aws_device import PlanqkAwsDevice
from planqk.exceptions import BackendNotFoundError


class DeviceFactory:
    _device_mapping: Dict[str, Type['PlanqkAwsDevice']] = {}

    @classmethod
    def register_device(cls, device_id: str):
        def decorator(device_cls: Type[PlanqkAwsDevice]):
            cls._device_mapping[device_id] = device_cls
            return device_cls
        return decorator

    @classmethod
    def get_device(cls, **fields) -> 'PlanqkAwsDevice':
        backend_dto = fields.get("backend_info", None)
        if backend_dto is None:
            raise RuntimeError("backend_info must not be None")

        device_class = cls._device_mapping.get(backend_dto.id)
        if device_class:
            return device_class(**fields)
        else:
            raise BackendNotFoundError(f"Device '{backend_dto.id}' is not supported by the PlanQK Braket SDK.")