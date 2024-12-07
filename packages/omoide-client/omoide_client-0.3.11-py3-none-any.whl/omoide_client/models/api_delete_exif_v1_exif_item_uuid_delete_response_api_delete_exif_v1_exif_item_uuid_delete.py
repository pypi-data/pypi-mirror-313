from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ApiDeleteExifV1ExifItemUuidDeleteResponseApiDeleteExifV1ExifItemUuidDelete")


@_attrs_define
class ApiDeleteExifV1ExifItemUuidDeleteResponseApiDeleteExifV1ExifItemUuidDelete:
    """ """

    additional_properties: Dict[str, str] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        api_delete_exif_v1_exif_item_uuid_delete_response_api_delete_exif_v1_exif_item_uuid_delete = cls()

        api_delete_exif_v1_exif_item_uuid_delete_response_api_delete_exif_v1_exif_item_uuid_delete.additional_properties = d
        return api_delete_exif_v1_exif_item_uuid_delete_response_api_delete_exif_v1_exif_item_uuid_delete

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
