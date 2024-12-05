from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.qps import QPS


T = TypeVar("T", bound="ModelDeploymentMetricsQueryPerSecondPerRegionPerCode")


@_attrs_define
class ModelDeploymentMetricsQueryPerSecondPerRegionPerCode:
    """RPS value (in last 24 hours) per response status code per location, for the model deployment

    Attributes:
        region (Union[Unset, QPS]): Query per second per element, can be per response status code (e.g. 200, 400) or per
            location
    """

    region: Union[Unset, "QPS"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        region: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.region, Unset):
            region = self.region.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if region is not UNSET:
            field_dict["region"] = region

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: dict[str, Any]) -> T:
        from ..models.qps import QPS

        d = src_dict.copy()
        _region = d.pop("region", UNSET)
        region: Union[Unset, QPS]
        if isinstance(_region, Unset):
            region = UNSET
        else:
            region = QPS.from_dict(_region)

        model_deployment_metrics_query_per_second_per_region_per_code = cls(
            region=region,
        )

        model_deployment_metrics_query_per_second_per_region_per_code.additional_properties = d
        return model_deployment_metrics_query_per_second_per_region_per_code

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
