from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.deployment_serverless_config import DeploymentServerlessConfig
    from ..models.flavor import Flavor
    from ..models.labels_type_0 import LabelsType0
    from ..models.model_deployment_pod_template import ModelDeploymentPodTemplate
    from ..models.model_provider_ref import ModelProviderRef
    from ..models.runtime import Runtime


T = TypeVar("T", bound="ModelDeployment")


@_attrs_define
class ModelDeployment:
    """An instance of a model, deployed in a specific environment

    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        created_by (Union[Unset, str]): The user or service account who created the resource
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        updated_by (Union[Unset, str]): The user or service account who updated the resource
        enabled (Union[Unset, bool]): If false, the model deployment will not be active nor serve requests
        environment (Union[Unset, str]): The name of the environment in which the model deployment is deployed
        flavors (Union[Unset, List['Flavor']]): Types of hardware available for deployments
        labels (Union['LabelsType0', None, Unset]): Labels
        metric_port (Union[Unset, int]): The port to serve the metrics on
        model (Union[Unset, str]): The name of the parent model
        model_provider_ref (Union[Unset, ModelProviderRef]): Reference to a model provider
        pod_template (Union[Unset, ModelDeploymentPodTemplate]): The pod template for the deployment. Should be a
            Kubernetes PodTemplateSpec
        policies (Union[Unset, List[str]]):
        runtime (Union[Unset, Runtime]): Set of configurations for a deployment
        serverless_config (Union[Unset, DeploymentServerlessConfig]): Configuration for a serverless deployment
        serving_port (Union[Unset, int]): The port to serve the model on
        workspace (Union[Unset, str]): The workspace the model deployment belongs to
    """

    created_at: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    updated_at: Union[Unset, str] = UNSET
    updated_by: Union[Unset, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    environment: Union[Unset, str] = UNSET
    flavors: Union[Unset, List["Flavor"]] = UNSET
    labels: Union["LabelsType0", None, Unset] = UNSET
    metric_port: Union[Unset, int] = UNSET
    model: Union[Unset, str] = UNSET
    model_provider_ref: Union[Unset, "ModelProviderRef"] = UNSET
    pod_template: Union[Unset, "ModelDeploymentPodTemplate"] = UNSET
    policies: Union[Unset, List[str]] = UNSET
    runtime: Union[Unset, "Runtime"] = UNSET
    serverless_config: Union[Unset, "DeploymentServerlessConfig"] = UNSET
    serving_port: Union[Unset, int] = UNSET
    workspace: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.labels_type_0 import LabelsType0

        created_at = self.created_at

        created_by = self.created_by

        updated_at = self.updated_at

        updated_by = self.updated_by

        enabled = self.enabled

        environment = self.environment

        flavors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.flavors, Unset):
            flavors = []
            for componentsschemas_flavors_item_data in self.flavors:
                componentsschemas_flavors_item = componentsschemas_flavors_item_data.to_dict()
                flavors.append(componentsschemas_flavors_item)

        labels: Union[Dict[str, Any], None, Unset]
        if isinstance(self.labels, Unset):
            labels = UNSET
        elif isinstance(self.labels, LabelsType0):
            labels = self.labels.to_dict()
        else:
            labels = self.labels

        metric_port = self.metric_port

        model = self.model

        model_provider_ref: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.model_provider_ref, Unset):
            model_provider_ref = self.model_provider_ref.to_dict()

        pod_template: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pod_template, Unset):
            pod_template = self.pod_template.to_dict()

        policies: Union[Unset, List[str]] = UNSET
        if not isinstance(self.policies, Unset):
            policies = self.policies

        runtime: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.runtime, Unset):
            runtime = self.runtime.to_dict()

        serverless_config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.serverless_config, Unset):
            serverless_config = self.serverless_config.to_dict()

        serving_port = self.serving_port

        workspace = self.workspace

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if updated_by is not UNSET:
            field_dict["updated_by"] = updated_by
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if environment is not UNSET:
            field_dict["environment"] = environment
        if flavors is not UNSET:
            field_dict["flavors"] = flavors
        if labels is not UNSET:
            field_dict["labels"] = labels
        if metric_port is not UNSET:
            field_dict["metric_port"] = metric_port
        if model is not UNSET:
            field_dict["model"] = model
        if model_provider_ref is not UNSET:
            field_dict["model_provider_ref"] = model_provider_ref
        if pod_template is not UNSET:
            field_dict["pod_template"] = pod_template
        if policies is not UNSET:
            field_dict["policies"] = policies
        if runtime is not UNSET:
            field_dict["runtime"] = runtime
        if serverless_config is not UNSET:
            field_dict["serverless_config"] = serverless_config
        if serving_port is not UNSET:
            field_dict["serving_port"] = serving_port
        if workspace is not UNSET:
            field_dict["workspace"] = workspace

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: dict[str, Any]) -> T:
        from ..models.deployment_serverless_config import DeploymentServerlessConfig
        from ..models.flavor import Flavor
        from ..models.labels_type_0 import LabelsType0
        from ..models.model_deployment_pod_template import ModelDeploymentPodTemplate
        from ..models.model_provider_ref import ModelProviderRef
        from ..models.runtime import Runtime

        d = src_dict.copy()
        created_at = d.pop("created_at", UNSET)

        created_by = d.pop("created_by", UNSET)

        updated_at = d.pop("updated_at", UNSET)

        updated_by = d.pop("updated_by", UNSET)

        enabled = d.pop("enabled", UNSET)

        environment = d.pop("environment", UNSET)

        flavors = []
        _flavors = d.pop("flavors", UNSET)
        for componentsschemas_flavors_item_data in _flavors or []:
            componentsschemas_flavors_item = Flavor.from_dict(componentsschemas_flavors_item_data)

            flavors.append(componentsschemas_flavors_item)

        def _parse_labels(data: object) -> Union["LabelsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_labels_type_0 = LabelsType0.from_dict(data)

                return componentsschemas_labels_type_0
            except:  # noqa: E722
                pass
            return cast(Union["LabelsType0", None, Unset], data)

        labels = _parse_labels(d.pop("labels", UNSET))

        metric_port = d.pop("metric_port", UNSET)

        model = d.pop("model", UNSET)

        _model_provider_ref = d.pop("model_provider_ref", UNSET)
        model_provider_ref: Union[Unset, ModelProviderRef]
        if isinstance(_model_provider_ref, Unset):
            model_provider_ref = UNSET
        else:
            model_provider_ref = ModelProviderRef.from_dict(_model_provider_ref)

        _pod_template = d.pop("pod_template", UNSET)
        pod_template: Union[Unset, ModelDeploymentPodTemplate]
        if isinstance(_pod_template, Unset):
            pod_template = UNSET
        else:
            pod_template = ModelDeploymentPodTemplate.from_dict(_pod_template)

        policies = cast(List[str], d.pop("policies", UNSET))

        _runtime = d.pop("runtime", UNSET)
        runtime: Union[Unset, Runtime]
        if isinstance(_runtime, Unset):
            runtime = UNSET
        else:
            runtime = Runtime.from_dict(_runtime)

        _serverless_config = d.pop("serverless_config", UNSET)
        serverless_config: Union[Unset, DeploymentServerlessConfig]
        if isinstance(_serverless_config, Unset):
            serverless_config = UNSET
        else:
            serverless_config = DeploymentServerlessConfig.from_dict(_serverless_config)

        serving_port = d.pop("serving_port", UNSET)

        workspace = d.pop("workspace", UNSET)

        model_deployment = cls(
            created_at=created_at,
            created_by=created_by,
            updated_at=updated_at,
            updated_by=updated_by,
            enabled=enabled,
            environment=environment,
            flavors=flavors,
            labels=labels,
            metric_port=metric_port,
            model=model,
            model_provider_ref=model_provider_ref,
            pod_template=pod_template,
            policies=policies,
            runtime=runtime,
            serverless_config=serverless_config,
            serving_port=serving_port,
            workspace=workspace,
        )

        model_deployment.additional_properties = d
        return model_deployment

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
