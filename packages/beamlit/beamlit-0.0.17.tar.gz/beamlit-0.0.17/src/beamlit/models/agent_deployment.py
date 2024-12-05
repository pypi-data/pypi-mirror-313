from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_chain import AgentChain
    from ..models.agent_deployment_configuration import AgentDeploymentConfiguration
    from ..models.agent_deployment_pod_template import AgentDeploymentPodTemplate
    from ..models.deployment_serverless_config import DeploymentServerlessConfig
    from ..models.flavor import Flavor
    from ..models.labels_type_0 import LabelsType0
    from ..models.runtime import Runtime


T = TypeVar("T", bound="AgentDeployment")


@_attrs_define
class AgentDeployment:
    """Agent deployment configuration

    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        created_by (Union[Unset, str]): The user or service account who created the resource
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        updated_by (Union[Unset, str]): The user or service account who updated the resource
        agent (Union[Unset, str]): The name of the agent
        agent_chain (Union[Unset, List['AgentChain']]): Agent chaining configuration
        configuration (Union[Unset, AgentDeploymentConfiguration]): Agent configuration, this is a key value storage. In
            your agent you can retrieve the value with config[key]
        description (Union[Unset, str]): Agent description, very important to have a clear description for your agent if
            you want to make it work with agent chaining
        enabled (Union[Unset, bool]): Whether the agent deployment is enabled
        environment (Union[Unset, str]): The name of the environment
        flavors (Union[Unset, List['Flavor']]): Types of hardware available for deployments
        functions (Union[Unset, List[str]]): Functions used by the agent, those functions needs to be created before
            setting it here
        labels (Union['LabelsType0', None, Unset]): Labels
        llm (Union[Unset, str]): LLM to use for agent, it should be compatible with function calling
        pod_template (Union[Unset, AgentDeploymentPodTemplate]): The pod template, should be a valid Kubernetes pod
            template
        policies (Union[Unset, List[str]]):
        runtime (Union[Unset, Runtime]): Set of configurations for a deployment
        serverless_config (Union[Unset, DeploymentServerlessConfig]): Configuration for a serverless deployment
        store_id (Union[Unset, str]): Create from a store registered function
        workspace (Union[Unset, str]): The workspace the agent deployment belongs to
    """

    created_at: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    updated_at: Union[Unset, str] = UNSET
    updated_by: Union[Unset, str] = UNSET
    agent: Union[Unset, str] = UNSET
    agent_chain: Union[Unset, List["AgentChain"]] = UNSET
    configuration: Union[Unset, "AgentDeploymentConfiguration"] = UNSET
    description: Union[Unset, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    environment: Union[Unset, str] = UNSET
    flavors: Union[Unset, List["Flavor"]] = UNSET
    functions: Union[Unset, List[str]] = UNSET
    labels: Union["LabelsType0", None, Unset] = UNSET
    llm: Union[Unset, str] = UNSET
    pod_template: Union[Unset, "AgentDeploymentPodTemplate"] = UNSET
    policies: Union[Unset, List[str]] = UNSET
    runtime: Union[Unset, "Runtime"] = UNSET
    serverless_config: Union[Unset, "DeploymentServerlessConfig"] = UNSET
    store_id: Union[Unset, str] = UNSET
    workspace: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.labels_type_0 import LabelsType0

        created_at = self.created_at

        created_by = self.created_by

        updated_at = self.updated_at

        updated_by = self.updated_by

        agent = self.agent

        agent_chain: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.agent_chain, Unset):
            agent_chain = []
            for agent_chain_item_data in self.agent_chain:
                agent_chain_item = agent_chain_item_data.to_dict()
                agent_chain.append(agent_chain_item)

        configuration: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.configuration, Unset):
            configuration = self.configuration.to_dict()

        description = self.description

        enabled = self.enabled

        environment = self.environment

        flavors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.flavors, Unset):
            flavors = []
            for componentsschemas_flavors_item_data in self.flavors:
                componentsschemas_flavors_item = componentsschemas_flavors_item_data.to_dict()
                flavors.append(componentsschemas_flavors_item)

        functions: Union[Unset, List[str]] = UNSET
        if not isinstance(self.functions, Unset):
            functions = self.functions

        labels: Union[Dict[str, Any], None, Unset]
        if isinstance(self.labels, Unset):
            labels = UNSET
        elif isinstance(self.labels, LabelsType0):
            labels = self.labels.to_dict()
        else:
            labels = self.labels

        llm = self.llm

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

        store_id = self.store_id

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
        if agent is not UNSET:
            field_dict["agent"] = agent
        if agent_chain is not UNSET:
            field_dict["agent_chain"] = agent_chain
        if configuration is not UNSET:
            field_dict["configuration"] = configuration
        if description is not UNSET:
            field_dict["description"] = description
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if environment is not UNSET:
            field_dict["environment"] = environment
        if flavors is not UNSET:
            field_dict["flavors"] = flavors
        if functions is not UNSET:
            field_dict["functions"] = functions
        if labels is not UNSET:
            field_dict["labels"] = labels
        if llm is not UNSET:
            field_dict["llm"] = llm
        if pod_template is not UNSET:
            field_dict["pod_template"] = pod_template
        if policies is not UNSET:
            field_dict["policies"] = policies
        if runtime is not UNSET:
            field_dict["runtime"] = runtime
        if serverless_config is not UNSET:
            field_dict["serverless_config"] = serverless_config
        if store_id is not UNSET:
            field_dict["store_id"] = store_id
        if workspace is not UNSET:
            field_dict["workspace"] = workspace

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: dict[str, Any]) -> T:
        from ..models.agent_chain import AgentChain
        from ..models.agent_deployment_configuration import AgentDeploymentConfiguration
        from ..models.agent_deployment_pod_template import AgentDeploymentPodTemplate
        from ..models.deployment_serverless_config import DeploymentServerlessConfig
        from ..models.flavor import Flavor
        from ..models.labels_type_0 import LabelsType0
        from ..models.runtime import Runtime

        d = src_dict.copy()
        created_at = d.pop("created_at", UNSET)

        created_by = d.pop("created_by", UNSET)

        updated_at = d.pop("updated_at", UNSET)

        updated_by = d.pop("updated_by", UNSET)

        agent = d.pop("agent", UNSET)

        agent_chain = []
        _agent_chain = d.pop("agent_chain", UNSET)
        for agent_chain_item_data in _agent_chain or []:
            agent_chain_item = AgentChain.from_dict(agent_chain_item_data)

            agent_chain.append(agent_chain_item)

        _configuration = d.pop("configuration", UNSET)
        configuration: Union[Unset, AgentDeploymentConfiguration]
        if isinstance(_configuration, Unset):
            configuration = UNSET
        else:
            configuration = AgentDeploymentConfiguration.from_dict(_configuration)

        description = d.pop("description", UNSET)

        enabled = d.pop("enabled", UNSET)

        environment = d.pop("environment", UNSET)

        flavors = []
        _flavors = d.pop("flavors", UNSET)
        for componentsschemas_flavors_item_data in _flavors or []:
            componentsschemas_flavors_item = Flavor.from_dict(componentsschemas_flavors_item_data)

            flavors.append(componentsschemas_flavors_item)

        functions = cast(List[str], d.pop("functions", UNSET))

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

        llm = d.pop("llm", UNSET)

        _pod_template = d.pop("pod_template", UNSET)
        pod_template: Union[Unset, AgentDeploymentPodTemplate]
        if isinstance(_pod_template, Unset):
            pod_template = UNSET
        else:
            pod_template = AgentDeploymentPodTemplate.from_dict(_pod_template)

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

        store_id = d.pop("store_id", UNSET)

        workspace = d.pop("workspace", UNSET)

        agent_deployment = cls(
            created_at=created_at,
            created_by=created_by,
            updated_at=updated_at,
            updated_by=updated_by,
            agent=agent,
            agent_chain=agent_chain,
            configuration=configuration,
            description=description,
            enabled=enabled,
            environment=environment,
            flavors=flavors,
            functions=functions,
            labels=labels,
            llm=llm,
            pod_template=pod_template,
            policies=policies,
            runtime=runtime,
            serverless_config=serverless_config,
            store_id=store_id,
            workspace=workspace,
        )

        agent_deployment.additional_properties = d
        return agent_deployment

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
