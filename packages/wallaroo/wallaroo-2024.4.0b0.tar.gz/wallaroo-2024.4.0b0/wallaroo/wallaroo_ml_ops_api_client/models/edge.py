from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import (
    define as _attrs_define,
    field as _attrs_field,
)

from ..models.app_version import AppVersion
from ..types import UNSET, Unset

T = TypeVar("T", bound="Edge")


@_attrs_define
class Edge:
    """The Edge

    Attributes:
        cpus (float): Number of CPUs
        id (str): ID
        memory (str): Amount of memory (in k8s format)
        name (str): User-given name
        tags (List[str]): Edge tags
        created_on_version (Union[Unset, AppVersion]):
        should_run_publish (Union[None, Unset, int]): The pipeline publish ID this edge is supposed to run
        spiffe_id (Union[None, Unset, str]): Spiffe ID
    """

    cpus: float
    id: str
    memory: str
    name: str
    tags: List[str]
    created_on_version: Union[Unset, AppVersion] = UNSET
    should_run_publish: Union[None, Unset, int] = UNSET
    spiffe_id: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cpus = self.cpus

        id = self.id

        memory = self.memory

        name = self.name

        tags = self.tags

        created_on_version: Union[Unset, str] = UNSET
        if not isinstance(self.created_on_version, Unset):
            created_on_version = self.created_on_version.value

        should_run_publish: Union[None, Unset, int]
        if isinstance(self.should_run_publish, Unset):
            should_run_publish = UNSET
        else:
            should_run_publish = self.should_run_publish

        spiffe_id: Union[None, Unset, str]
        if isinstance(self.spiffe_id, Unset):
            spiffe_id = UNSET
        else:
            spiffe_id = self.spiffe_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cpus": cpus,
                "id": id,
                "memory": memory,
                "name": name,
                "tags": tags,
            }
        )
        if created_on_version is not UNSET:
            field_dict["created_on_version"] = created_on_version
        if should_run_publish is not UNSET:
            field_dict["should_run_publish"] = should_run_publish
        if spiffe_id is not UNSET:
            field_dict["spiffe_id"] = spiffe_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        cpus = d.pop("cpus")

        id = d.pop("id")

        memory = d.pop("memory")

        name = d.pop("name")

        tags = cast(List[str], d.pop("tags"))

        _created_on_version = d.pop("created_on_version", UNSET)
        created_on_version: Union[Unset, AppVersion]
        if isinstance(_created_on_version, Unset):
            created_on_version = UNSET
        else:
            created_on_version = AppVersion(_created_on_version)

        def _parse_should_run_publish(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        should_run_publish = _parse_should_run_publish(
            d.pop("should_run_publish", UNSET)
        )

        def _parse_spiffe_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        spiffe_id = _parse_spiffe_id(d.pop("spiffe_id", UNSET))

        edge = cls(
            cpus=cpus,
            id=id,
            memory=memory,
            name=name,
            tags=tags,
            created_on_version=created_on_version,
            should_run_publish=should_run_publish,
            spiffe_id=spiffe_id,
        )

        edge.additional_properties = d
        return edge

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
