from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import (
    define as _attrs_define,
    field as _attrs_field,
)

from ..models.acceleration import Acceleration
from ..models.architecture import Architecture
from ..models.framework import Framework
from ..models.python_version import PythonVersion
from ..types import UNSET, Unset

T = TypeVar("T", bound="Conversion")


@_attrs_define
class Conversion:
    """
    Attributes:
        framework (Framework):
        requirements (List[str]):
        accel (Union[Acceleration, None, Unset]):
        arch (Union[Architecture, None, Unset]):
        python_version (Union[Unset, PythonVersion]):
    """

    framework: Framework
    requirements: List[str]
    accel: Union[Acceleration, None, Unset] = UNSET
    arch: Union[Architecture, None, Unset] = UNSET
    python_version: Union[Unset, PythonVersion] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        framework = self.framework.value

        requirements = self.requirements

        accel: Union[None, Unset, str]
        if isinstance(self.accel, Unset):
            accel = UNSET
        elif isinstance(self.accel, Acceleration):
            accel = self.accel.value
        else:
            accel = self.accel

        arch: Union[None, Unset, str]
        if isinstance(self.arch, Unset):
            arch = UNSET
        elif isinstance(self.arch, Architecture):
            arch = self.arch.value
        else:
            arch = self.arch

        python_version: Union[Unset, str] = UNSET
        if not isinstance(self.python_version, Unset):
            python_version = self.python_version.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "framework": framework,
                "requirements": requirements,
            }
        )
        if accel is not UNSET:
            field_dict["accel"] = accel
        if arch is not UNSET:
            field_dict["arch"] = arch
        if python_version is not UNSET:
            field_dict["python_version"] = python_version

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        framework = Framework(d.pop("framework"))

        requirements = cast(List[str], d.pop("requirements"))

        def _parse_accel(data: object) -> Union[Acceleration, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                accel_type_1 = Acceleration(data)

                return accel_type_1
            except:  # noqa: E722
                pass
            return cast(Union[Acceleration, None, Unset], data)

        accel = _parse_accel(d.pop("accel", UNSET))

        def _parse_arch(data: object) -> Union[Architecture, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                arch_type_1 = Architecture(data)

                return arch_type_1
            except:  # noqa: E722
                pass
            return cast(Union[Architecture, None, Unset], data)

        arch = _parse_arch(d.pop("arch", UNSET))

        _python_version = d.pop("python_version", UNSET)
        python_version: Union[Unset, PythonVersion]
        if isinstance(_python_version, Unset):
            python_version = UNSET
        else:
            python_version = PythonVersion(_python_version)

        conversion = cls(
            framework=framework,
            requirements=requirements,
            accel=accel,
            arch=arch,
            python_version=python_version,
        )

        conversion.additional_properties = d
        return conversion

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
