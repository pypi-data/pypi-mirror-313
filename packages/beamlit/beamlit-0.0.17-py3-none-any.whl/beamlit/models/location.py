from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.flavor import Flavor


T = TypeVar("T", bound="Location")


@_attrs_define
class Location:
    """Location availability for policies

    Attributes:
        continent (Union[Unset, str]): Location continent
        country (Union[Unset, str]): Location country
        flavors (Union[Unset, List['Flavor']]): Location flavors
        location (Union[Unset, str]): Location name
        name (Union[Unset, str]): Location name
        status (Union[Unset, str]): Location status
    """

    continent: Union[Unset, str] = UNSET
    country: Union[Unset, str] = UNSET
    flavors: Union[Unset, List["Flavor"]] = UNSET
    location: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        continent = self.continent

        country = self.country

        flavors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.flavors, Unset):
            flavors = []
            for flavors_item_data in self.flavors:
                flavors_item = flavors_item_data.to_dict()
                flavors.append(flavors_item)

        location = self.location

        name = self.name

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if continent is not UNSET:
            field_dict["continent"] = continent
        if country is not UNSET:
            field_dict["country"] = country
        if flavors is not UNSET:
            field_dict["flavors"] = flavors
        if location is not UNSET:
            field_dict["location"] = location
        if name is not UNSET:
            field_dict["name"] = name
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: dict[str, Any]) -> T:
        from ..models.flavor import Flavor

        d = src_dict.copy()
        continent = d.pop("continent", UNSET)

        country = d.pop("country", UNSET)

        flavors = []
        _flavors = d.pop("flavors", UNSET)
        for flavors_item_data in _flavors or []:
            flavors_item = Flavor.from_dict(flavors_item_data)

            flavors.append(flavors_item)

        location = d.pop("location", UNSET)

        name = d.pop("name", UNSET)

        status = d.pop("status", UNSET)

        location = cls(
            continent=continent,
            country=country,
            flavors=flavors,
            location=location,
            name=name,
            status=status,
        )

        location.additional_properties = d
        return location

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
