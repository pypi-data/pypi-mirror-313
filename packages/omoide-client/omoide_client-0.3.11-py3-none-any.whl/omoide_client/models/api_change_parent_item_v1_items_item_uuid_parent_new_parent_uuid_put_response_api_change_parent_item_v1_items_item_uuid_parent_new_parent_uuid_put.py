from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar(
    "T",
    bound="ApiChangeParentItemV1ItemsItemUuidParentNewParentUuidPutResponseApiChangeParentItemV1ItemsItemUuidParentNewParentUuidPut",
)


@_attrs_define
class ApiChangeParentItemV1ItemsItemUuidParentNewParentUuidPutResponseApiChangeParentItemV1ItemsItemUuidParentNewParentUuidPut:
    """ """

    additional_properties: Dict[str, Union[List[int], int, str]] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, list):
                field_dict[prop_name] = prop

            else:
                field_dict[prop_name] = prop

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        api_change_parent_item_v1_items_item_uuid_parent_new_parent_uuid_put_response_api_change_parent_item_v1_items_item_uuid_parent_new_parent_uuid_put = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(data: object) -> Union[List[int], int, str]:
                try:
                    if not isinstance(data, list):
                        raise TypeError()
                    additional_property_type_2 = cast(List[int], data)

                    return additional_property_type_2
                except:  # noqa: E722
                    pass
                return cast(Union[List[int], int, str], data)

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        api_change_parent_item_v1_items_item_uuid_parent_new_parent_uuid_put_response_api_change_parent_item_v1_items_item_uuid_parent_new_parent_uuid_put.additional_properties = additional_properties
        return api_change_parent_item_v1_items_item_uuid_parent_new_parent_uuid_put_response_api_change_parent_item_v1_items_item_uuid_parent_new_parent_uuid_put

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Union[List[int], int, str]:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Union[List[int], int, str]) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
