from typing import Any, Dict, List, Type, TypeVar

from attrs import (
    define as _attrs_define,
    field as _attrs_field,
)

from ..models.auto_scale_config_type_0_type import AutoScaleConfigType0Type

T = TypeVar("T", bound="AutoScaleConfigType0")


@_attrs_define
class AutoScaleConfigType0:
    """
    Attributes:
        type (AutoScaleConfigType0Type):
    """

    type: AutoScaleConfigType0Type
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = AutoScaleConfigType0Type(d.pop("type"))

        auto_scale_config_type_0 = cls(
            type=type,
        )

        auto_scale_config_type_0.additional_properties = d
        return auto_scale_config_type_0

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
