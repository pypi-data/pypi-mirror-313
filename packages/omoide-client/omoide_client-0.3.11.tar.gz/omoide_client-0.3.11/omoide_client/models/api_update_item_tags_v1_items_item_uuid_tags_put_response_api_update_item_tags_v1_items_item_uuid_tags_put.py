from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ApiUpdateItemTagsV1ItemsItemUuidTagsPutResponseApiUpdateItemTagsV1ItemsItemUuidTagsPut")


@_attrs_define
class ApiUpdateItemTagsV1ItemsItemUuidTagsPutResponseApiUpdateItemTagsV1ItemsItemUuidTagsPut:
    """ """

    additional_properties: Dict[str, Union[None, int, str]] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        api_update_item_tags_v1_items_item_uuid_tags_put_response_api_update_item_tags_v1_items_item_uuid_tags_put = (
            cls()
        )

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(data: object) -> Union[None, int, str]:
                if data is None:
                    return data
                return cast(Union[None, int, str], data)

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        api_update_item_tags_v1_items_item_uuid_tags_put_response_api_update_item_tags_v1_items_item_uuid_tags_put.additional_properties = additional_properties
        return (
            api_update_item_tags_v1_items_item_uuid_tags_put_response_api_update_item_tags_v1_items_item_uuid_tags_put
        )

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Union[None, int, str]:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Union[None, int, str]) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
