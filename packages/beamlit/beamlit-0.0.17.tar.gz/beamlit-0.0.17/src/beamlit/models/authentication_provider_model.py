from typing import Any, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AuthenticationProviderModel")


@_attrs_define
class AuthenticationProviderModel:
    """Model obtained from an external authentication provider, such as HuggingFace, OpenAI, etc...

    Attributes:
        created_at (Union[Unset, str]): Provider model created at
        downloads (Union[Unset, int]): Provider model downloads
        id (Union[Unset, str]): Provider model ID
        library_name (Union[Unset, str]): Provider model library name
        likes (Union[Unset, int]): Provider model likes
        name (Union[Unset, str]): Provider model name
        pipeline_tag (Union[Unset, str]): Provider model pipeline tag
        private (Union[Unset, bool]): Provider model private
        tags (Union[Unset, List[str]]): Provider model tags
        trending_score (Union[Unset, int]): Provider model trending score
    """

    created_at: Union[Unset, str] = UNSET
    downloads: Union[Unset, int] = UNSET
    id: Union[Unset, str] = UNSET
    library_name: Union[Unset, str] = UNSET
    likes: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    pipeline_tag: Union[Unset, str] = UNSET
    private: Union[Unset, bool] = UNSET
    tags: Union[Unset, List[str]] = UNSET
    trending_score: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        downloads = self.downloads

        id = self.id

        library_name = self.library_name

        likes = self.likes

        name = self.name

        pipeline_tag = self.pipeline_tag

        private = self.private

        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        trending_score = self.trending_score

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if downloads is not UNSET:
            field_dict["downloads"] = downloads
        if id is not UNSET:
            field_dict["id"] = id
        if library_name is not UNSET:
            field_dict["library_name"] = library_name
        if likes is not UNSET:
            field_dict["likes"] = likes
        if name is not UNSET:
            field_dict["name"] = name
        if pipeline_tag is not UNSET:
            field_dict["pipeline_tag"] = pipeline_tag
        if private is not UNSET:
            field_dict["private"] = private
        if tags is not UNSET:
            field_dict["tags"] = tags
        if trending_score is not UNSET:
            field_dict["trending_score"] = trending_score

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        created_at = d.pop("created_at", UNSET)

        downloads = d.pop("downloads", UNSET)

        id = d.pop("id", UNSET)

        library_name = d.pop("library_name", UNSET)

        likes = d.pop("likes", UNSET)

        name = d.pop("name", UNSET)

        pipeline_tag = d.pop("pipeline_tag", UNSET)

        private = d.pop("private", UNSET)

        tags = cast(List[str], d.pop("tags", UNSET))

        trending_score = d.pop("trending_score", UNSET)

        authentication_provider_model = cls(
            created_at=created_at,
            downloads=downloads,
            id=id,
            library_name=library_name,
            likes=likes,
            name=name,
            pipeline_tag=pipeline_tag,
            private=private,
            tags=tags,
            trending_score=trending_score,
        )

        authentication_provider_model.additional_properties = d
        return authentication_provider_model

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
