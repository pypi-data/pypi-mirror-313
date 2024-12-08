# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from collections.abc import Iterable
import zaber_bson
from .can_set_state_axis_response import CanSetStateAxisResponse


@dataclass
class CanSetStateDeviceResponse:
    """
    An object containing any setup issues that will prevent setting a state to a given device.
    """

    axis_errors: List[CanSetStateAxisResponse]
    """
    A list of errors that block setting state of device's axes.
    """

    error: Optional[str] = None
    """
    The error blocking applying this state to the given device.
    """

    @staticmethod
    def zero_values() -> 'CanSetStateDeviceResponse':
        return CanSetStateDeviceResponse(
            error=None,
            axis_errors=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'CanSetStateDeviceResponse':
        """" Deserialize a binary representation of this class. """
        data = zaber_bson.loads(data_bytes)  # type: Dict[str, Any]
        return CanSetStateDeviceResponse.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return zaber_bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'error': str(self.error) if self.error is not None else None,
            'axisErrors': [item.to_dict() for item in self.axis_errors] if self.axis_errors is not None else [],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'CanSetStateDeviceResponse':
        return CanSetStateDeviceResponse(
            error=data.get('error'),  # type: ignore
            axis_errors=[CanSetStateAxisResponse.from_dict(item) for item in data.get('axisErrors')],  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.error is not None:
            if not isinstance(self.error, str):
                raise ValueError(f'Property "Error" of "CanSetStateDeviceResponse" is not a string.')

        if self.axis_errors is not None:
            if not isinstance(self.axis_errors, Iterable):
                raise ValueError('Property "AxisErrors" of "CanSetStateDeviceResponse" is not iterable.')

            for i, axis_errors_item in enumerate(self.axis_errors):
                if axis_errors_item is None:
                    raise ValueError(f'Item {i} in property "AxisErrors" of "CanSetStateDeviceResponse" is None.')

                if not isinstance(axis_errors_item, CanSetStateAxisResponse):
                    raise ValueError(f'Item {i} in property "AxisErrors" of "CanSetStateDeviceResponse" is not an instance of "CanSetStateAxisResponse".')

                axis_errors_item.validate()
