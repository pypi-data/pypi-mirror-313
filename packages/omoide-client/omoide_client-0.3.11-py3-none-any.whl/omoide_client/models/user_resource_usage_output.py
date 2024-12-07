from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UserResourceUsageOutput")


@_attrs_define
class UserResourceUsageOutput:
    """Total resource usage for specific user.

    Attributes:
        user_uuid (str):
        total_items (int):
        total_collections (int):
        content_bytes (int):
        content_hr (str):
        preview_bytes (int):
        preview_hr (str):
        thumbnail_bytes (int):
        thumbnail_hr (str):
    """

    user_uuid: str
    total_items: int
    total_collections: int
    content_bytes: int
    content_hr: str
    preview_bytes: int
    preview_hr: str
    thumbnail_bytes: int
    thumbnail_hr: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user_uuid = self.user_uuid

        total_items = self.total_items

        total_collections = self.total_collections

        content_bytes = self.content_bytes

        content_hr = self.content_hr

        preview_bytes = self.preview_bytes

        preview_hr = self.preview_hr

        thumbnail_bytes = self.thumbnail_bytes

        thumbnail_hr = self.thumbnail_hr

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user_uuid": user_uuid,
                "total_items": total_items,
                "total_collections": total_collections,
                "content_bytes": content_bytes,
                "content_hr": content_hr,
                "preview_bytes": preview_bytes,
                "preview_hr": preview_hr,
                "thumbnail_bytes": thumbnail_bytes,
                "thumbnail_hr": thumbnail_hr,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user_uuid = d.pop("user_uuid")

        total_items = d.pop("total_items")

        total_collections = d.pop("total_collections")

        content_bytes = d.pop("content_bytes")

        content_hr = d.pop("content_hr")

        preview_bytes = d.pop("preview_bytes")

        preview_hr = d.pop("preview_hr")

        thumbnail_bytes = d.pop("thumbnail_bytes")

        thumbnail_hr = d.pop("thumbnail_hr")

        user_resource_usage_output = cls(
            user_uuid=user_uuid,
            total_items=total_items,
            total_collections=total_collections,
            content_bytes=content_bytes,
            content_hr=content_hr,
            preview_bytes=preview_bytes,
            preview_hr=preview_hr,
            thumbnail_bytes=thumbnail_bytes,
            thumbnail_hr=thumbnail_hr,
        )

        user_resource_usage_output.additional_properties = d
        return user_resource_usage_output

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
