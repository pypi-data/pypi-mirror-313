from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ApiGetUserTagsV1UsersUserUuidKnownTagsGetResponseApiGetUserTagsV1UsersUserUuidKnownTagsGet")


@_attrs_define
class ApiGetUserTagsV1UsersUserUuidKnownTagsGetResponseApiGetUserTagsV1UsersUserUuidKnownTagsGet:
    """ """

    additional_properties: Dict[str, int] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        api_get_user_tags_v1_users_user_uuid_known_tags_get_response_api_get_user_tags_v1_users_user_uuid_known_tags_get = cls()

        api_get_user_tags_v1_users_user_uuid_known_tags_get_response_api_get_user_tags_v1_users_user_uuid_known_tags_get.additional_properties = d
        return api_get_user_tags_v1_users_user_uuid_known_tags_get_response_api_get_user_tags_v1_users_user_uuid_known_tags_get

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> int:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: int) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
