from typing import Any, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="StoreAgentConfiguration")


@_attrs_define
class StoreAgentConfiguration:
    """Store agent configuration used to configure your agent directly from beamlit interface

    Attributes:
        description (Union[Unset, str]): Store function configuration description
        if_ (Union[Unset, str]): Conditional rendering for the configuration, example: provider === 'openai'
        name (Union[Unset, str]): Store function configuration name
        required (Union[Unset, bool]): Store function configuration required
        secret (Union[Unset, bool]): Store function configuration secret
    """

    description: Union[Unset, str] = UNSET
    if_: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    required: Union[Unset, bool] = UNSET
    secret: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        if_ = self.if_

        name = self.name

        required = self.required

        secret = self.secret

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if if_ is not UNSET:
            field_dict["if"] = if_
        if name is not UNSET:
            field_dict["name"] = name
        if required is not UNSET:
            field_dict["required"] = required
        if secret is not UNSET:
            field_dict["secret"] = secret

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        if_ = d.pop("if", UNSET)

        name = d.pop("name", UNSET)

        required = d.pop("required", UNSET)

        secret = d.pop("secret", UNSET)

        store_agent_configuration = cls(
            description=description,
            if_=if_,
            name=name,
            required=required,
            secret=secret,
        )

        store_agent_configuration.additional_properties = d
        return store_agent_configuration

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
