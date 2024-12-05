from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metric import Metric


T = TypeVar("T", bound="Metrics")


@_attrs_define
class Metrics:
    """Metrics for resources

    Attributes:
        agents (Union[Unset, Any]): Metrics for agents
        functions (Union[Unset, Any]): Metrics for functions
        inference_per_second_global (Union[Unset, List['Metric']]): Array of metrics
        models (Union[Unset, Any]): Metrics for models
        query_per_second (Union[Unset, float]): RPS value (in last 24 hours) per location, for all resources globally
    """

    agents: Union[Unset, Any] = UNSET
    functions: Union[Unset, Any] = UNSET
    inference_per_second_global: Union[Unset, List["Metric"]] = UNSET
    models: Union[Unset, Any] = UNSET
    query_per_second: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        agents = self.agents

        functions = self.functions

        inference_per_second_global: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.inference_per_second_global, Unset):
            inference_per_second_global = []
            for componentsschemas_array_metric_item_data in self.inference_per_second_global:
                componentsschemas_array_metric_item = componentsschemas_array_metric_item_data.to_dict()
                inference_per_second_global.append(componentsschemas_array_metric_item)

        models = self.models

        query_per_second = self.query_per_second

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agents is not UNSET:
            field_dict["agents"] = agents
        if functions is not UNSET:
            field_dict["functions"] = functions
        if inference_per_second_global is not UNSET:
            field_dict["inference_per_second_global"] = inference_per_second_global
        if models is not UNSET:
            field_dict["models"] = models
        if query_per_second is not UNSET:
            field_dict["query_per_second"] = query_per_second

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: dict[str, Any]) -> T:
        from ..models.metric import Metric

        d = src_dict.copy()
        agents = d.pop("agents", UNSET)

        functions = d.pop("functions", UNSET)

        inference_per_second_global = []
        _inference_per_second_global = d.pop("inference_per_second_global", UNSET)
        for componentsschemas_array_metric_item_data in _inference_per_second_global or []:
            componentsschemas_array_metric_item = Metric.from_dict(componentsschemas_array_metric_item_data)

            inference_per_second_global.append(componentsschemas_array_metric_item)

        models = d.pop("models", UNSET)

        query_per_second = d.pop("query_per_second", UNSET)

        metrics = cls(
            agents=agents,
            functions=functions,
            inference_per_second_global=inference_per_second_global,
            models=models,
            query_per_second=query_per_second,
        )

        metrics.additional_properties = d
        return metrics

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
