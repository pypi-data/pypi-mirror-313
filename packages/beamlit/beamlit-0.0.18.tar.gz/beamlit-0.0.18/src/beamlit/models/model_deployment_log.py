from typing import Any, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelDeploymentLog")


@_attrs_define
class ModelDeploymentLog:
    """Log for a model deployment

    Attributes:
        message (Union[Unset, str]): Content of the log
        timestamp (Union[Unset, str]): The timestamp of the log
    """

    message: Union[Unset, str] = UNSET
    timestamp: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        timestamp = self.timestamp

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if message is not UNSET:
            field_dict["message"] = message
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        message = d.pop("message", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        model_deployment_log = cls(
            message=message,
            timestamp=timestamp,
        )

        model_deployment_log.additional_properties = d
        return model_deployment_log

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
