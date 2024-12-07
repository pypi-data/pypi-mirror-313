from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MetainfoOutput")


@_attrs_define
class MetainfoOutput:
    """Metainfo for item.

    Attributes:
        created_at (str):
        updated_at (str):
        deleted_at (Union[None, Unset, str]):
        user_time (Union[None, Unset, str]):
        content_type (Union[None, Unset, str]):
        content_size (Union[None, Unset, int]):
        preview_size (Union[None, Unset, int]):
        thumbnail_size (Union[None, Unset, int]):
        content_width (Union[None, Unset, int]):
        content_height (Union[None, Unset, int]):
        preview_width (Union[None, Unset, int]):
        preview_height (Union[None, Unset, int]):
        thumbnail_width (Union[None, Unset, int]):
        thumbnail_height (Union[None, Unset, int]):
    """

    created_at: str
    updated_at: str
    deleted_at: Union[None, Unset, str] = UNSET
    user_time: Union[None, Unset, str] = UNSET
    content_type: Union[None, Unset, str] = UNSET
    content_size: Union[None, Unset, int] = UNSET
    preview_size: Union[None, Unset, int] = UNSET
    thumbnail_size: Union[None, Unset, int] = UNSET
    content_width: Union[None, Unset, int] = UNSET
    content_height: Union[None, Unset, int] = UNSET
    preview_width: Union[None, Unset, int] = UNSET
    preview_height: Union[None, Unset, int] = UNSET
    thumbnail_width: Union[None, Unset, int] = UNSET
    thumbnail_height: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        created_at = self.created_at

        updated_at = self.updated_at

        deleted_at: Union[None, Unset, str]
        if isinstance(self.deleted_at, Unset):
            deleted_at = UNSET
        else:
            deleted_at = self.deleted_at

        user_time: Union[None, Unset, str]
        if isinstance(self.user_time, Unset):
            user_time = UNSET
        else:
            user_time = self.user_time

        content_type: Union[None, Unset, str]
        if isinstance(self.content_type, Unset):
            content_type = UNSET
        else:
            content_type = self.content_type

        content_size: Union[None, Unset, int]
        if isinstance(self.content_size, Unset):
            content_size = UNSET
        else:
            content_size = self.content_size

        preview_size: Union[None, Unset, int]
        if isinstance(self.preview_size, Unset):
            preview_size = UNSET
        else:
            preview_size = self.preview_size

        thumbnail_size: Union[None, Unset, int]
        if isinstance(self.thumbnail_size, Unset):
            thumbnail_size = UNSET
        else:
            thumbnail_size = self.thumbnail_size

        content_width: Union[None, Unset, int]
        if isinstance(self.content_width, Unset):
            content_width = UNSET
        else:
            content_width = self.content_width

        content_height: Union[None, Unset, int]
        if isinstance(self.content_height, Unset):
            content_height = UNSET
        else:
            content_height = self.content_height

        preview_width: Union[None, Unset, int]
        if isinstance(self.preview_width, Unset):
            preview_width = UNSET
        else:
            preview_width = self.preview_width

        preview_height: Union[None, Unset, int]
        if isinstance(self.preview_height, Unset):
            preview_height = UNSET
        else:
            preview_height = self.preview_height

        thumbnail_width: Union[None, Unset, int]
        if isinstance(self.thumbnail_width, Unset):
            thumbnail_width = UNSET
        else:
            thumbnail_width = self.thumbnail_width

        thumbnail_height: Union[None, Unset, int]
        if isinstance(self.thumbnail_height, Unset):
            thumbnail_height = UNSET
        else:
            thumbnail_height = self.thumbnail_height

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if deleted_at is not UNSET:
            field_dict["deleted_at"] = deleted_at
        if user_time is not UNSET:
            field_dict["user_time"] = user_time
        if content_type is not UNSET:
            field_dict["content_type"] = content_type
        if content_size is not UNSET:
            field_dict["content_size"] = content_size
        if preview_size is not UNSET:
            field_dict["preview_size"] = preview_size
        if thumbnail_size is not UNSET:
            field_dict["thumbnail_size"] = thumbnail_size
        if content_width is not UNSET:
            field_dict["content_width"] = content_width
        if content_height is not UNSET:
            field_dict["content_height"] = content_height
        if preview_width is not UNSET:
            field_dict["preview_width"] = preview_width
        if preview_height is not UNSET:
            field_dict["preview_height"] = preview_height
        if thumbnail_width is not UNSET:
            field_dict["thumbnail_width"] = thumbnail_width
        if thumbnail_height is not UNSET:
            field_dict["thumbnail_height"] = thumbnail_height

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        def _parse_deleted_at(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        deleted_at = _parse_deleted_at(d.pop("deleted_at", UNSET))

        def _parse_user_time(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user_time = _parse_user_time(d.pop("user_time", UNSET))

        def _parse_content_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        content_type = _parse_content_type(d.pop("content_type", UNSET))

        def _parse_content_size(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        content_size = _parse_content_size(d.pop("content_size", UNSET))

        def _parse_preview_size(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        preview_size = _parse_preview_size(d.pop("preview_size", UNSET))

        def _parse_thumbnail_size(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        thumbnail_size = _parse_thumbnail_size(d.pop("thumbnail_size", UNSET))

        def _parse_content_width(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        content_width = _parse_content_width(d.pop("content_width", UNSET))

        def _parse_content_height(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        content_height = _parse_content_height(d.pop("content_height", UNSET))

        def _parse_preview_width(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        preview_width = _parse_preview_width(d.pop("preview_width", UNSET))

        def _parse_preview_height(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        preview_height = _parse_preview_height(d.pop("preview_height", UNSET))

        def _parse_thumbnail_width(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        thumbnail_width = _parse_thumbnail_width(d.pop("thumbnail_width", UNSET))

        def _parse_thumbnail_height(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        thumbnail_height = _parse_thumbnail_height(d.pop("thumbnail_height", UNSET))

        metainfo_output = cls(
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            user_time=user_time,
            content_type=content_type,
            content_size=content_size,
            preview_size=preview_size,
            thumbnail_size=thumbnail_size,
            content_width=content_width,
            content_height=content_height,
            preview_width=preview_width,
            preview_height=preview_height,
            thumbnail_width=thumbnail_width,
            thumbnail_height=thumbnail_height,
        )

        metainfo_output.additional_properties = d
        return metainfo_output

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
