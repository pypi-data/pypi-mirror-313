import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metainfo_input_extras import MetainfoInputExtras


T = TypeVar("T", bound="MetainfoInput")


@_attrs_define
class MetainfoInput:
    """Metainfo for item.

    Attributes:
        user_time (Union[None, Unset, datetime.datetime]):
        content_type (Union[None, Unset, str]):
        extras (Union[Unset, MetainfoInputExtras]):
    """

    user_time: Union[None, Unset, datetime.datetime] = UNSET
    content_type: Union[None, Unset, str] = UNSET
    extras: Union[Unset, "MetainfoInputExtras"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user_time: Union[None, Unset, str]
        if isinstance(self.user_time, Unset):
            user_time = UNSET
        elif isinstance(self.user_time, datetime.datetime):
            user_time = self.user_time.isoformat()
        else:
            user_time = self.user_time

        content_type: Union[None, Unset, str]
        if isinstance(self.content_type, Unset):
            content_type = UNSET
        else:
            content_type = self.content_type

        extras: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.extras, Unset):
            extras = self.extras.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if user_time is not UNSET:
            field_dict["user_time"] = user_time
        if content_type is not UNSET:
            field_dict["content_type"] = content_type
        if extras is not UNSET:
            field_dict["extras"] = extras

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.metainfo_input_extras import MetainfoInputExtras

        d = src_dict.copy()

        def _parse_user_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                user_time_type_0 = isoparse(data)

                return user_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        user_time = _parse_user_time(d.pop("user_time", UNSET))

        def _parse_content_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        content_type = _parse_content_type(d.pop("content_type", UNSET))

        _extras = d.pop("extras", UNSET)
        extras: Union[Unset, MetainfoInputExtras]
        if isinstance(_extras, Unset):
            extras = UNSET
        else:
            extras = MetainfoInputExtras.from_dict(_extras)

        metainfo_input = cls(
            user_time=user_time,
            content_type=content_type,
            extras=extras,
        )

        metainfo_input.additional_properties = d
        return metainfo_input

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
