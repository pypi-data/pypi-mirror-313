from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_deployment_history_event import AgentDeploymentHistoryEvent


T = TypeVar("T", bound="AgentDeploymentHistory")


@_attrs_define
class AgentDeploymentHistory:
    """Agent deployment history

    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        created_by (Union[Unset, str]): The user or service account who created the resource
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        updated_by (Union[Unset, str]): The user or service account who updated the resource
        agent (Union[Unset, str]): Agent name
        end (Union[Unset, str]): End time
        environment (Union[Unset, str]): Environment name
        events (Union[Unset, List['AgentDeploymentHistoryEvent']]): Events
        request_id (Union[Unset, str]): Request ID
        start (Union[Unset, str]): Start time
        status (Union[Unset, str]): Status, eg: running, success, failed
        took (Union[Unset, int]): Number of milliseconds it took to complete the event
        workspace (Union[Unset, str]): The workspace the agent deployment belongs to
    """

    created_at: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    updated_at: Union[Unset, str] = UNSET
    updated_by: Union[Unset, str] = UNSET
    agent: Union[Unset, str] = UNSET
    end: Union[Unset, str] = UNSET
    environment: Union[Unset, str] = UNSET
    events: Union[Unset, List["AgentDeploymentHistoryEvent"]] = UNSET
    request_id: Union[Unset, str] = UNSET
    start: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    took: Union[Unset, int] = UNSET
    workspace: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        created_by = self.created_by

        updated_at = self.updated_at

        updated_by = self.updated_by

        agent = self.agent

        end = self.end

        environment = self.environment

        events: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.events, Unset):
            events = []
            for events_item_data in self.events:
                events_item = events_item_data.to_dict()
                events.append(events_item)

        request_id = self.request_id

        start = self.start

        status = self.status

        took = self.took

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
        if end is not UNSET:
            field_dict["end"] = end
        if environment is not UNSET:
            field_dict["environment"] = environment
        if events is not UNSET:
            field_dict["events"] = events
        if request_id is not UNSET:
            field_dict["request_id"] = request_id
        if start is not UNSET:
            field_dict["start"] = start
        if status is not UNSET:
            field_dict["status"] = status
        if took is not UNSET:
            field_dict["took"] = took
        if workspace is not UNSET:
            field_dict["workspace"] = workspace

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: dict[str, Any]) -> T:
        from ..models.agent_deployment_history_event import AgentDeploymentHistoryEvent

        d = src_dict.copy()
        created_at = d.pop("created_at", UNSET)

        created_by = d.pop("created_by", UNSET)

        updated_at = d.pop("updated_at", UNSET)

        updated_by = d.pop("updated_by", UNSET)

        agent = d.pop("agent", UNSET)

        end = d.pop("end", UNSET)

        environment = d.pop("environment", UNSET)

        events = []
        _events = d.pop("events", UNSET)
        for events_item_data in _events or []:
            events_item = AgentDeploymentHistoryEvent.from_dict(events_item_data)

            events.append(events_item)

        request_id = d.pop("request_id", UNSET)

        start = d.pop("start", UNSET)

        status = d.pop("status", UNSET)

        took = d.pop("took", UNSET)

        workspace = d.pop("workspace", UNSET)

        agent_deployment_history = cls(
            created_at=created_at,
            created_by=created_by,
            updated_at=updated_at,
            updated_by=updated_by,
            agent=agent,
            end=end,
            environment=environment,
            events=events,
            request_id=request_id,
            start=start,
            status=status,
            took=took,
            workspace=workspace,
        )

        agent_deployment_history.additional_properties = d
        return agent_deployment_history

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
