from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar(
    "T",
    bound="ApiActionRebuildKnownTagsUserV1ActionsRebuildKnownTagsUserUserUuidPostResponseApiActionRebuildKnownTagsUserV1ActionsRebuildKnownTagsUserUserUuidPost",
)


@_attrs_define
class ApiActionRebuildKnownTagsUserV1ActionsRebuildKnownTagsUserUserUuidPostResponseApiActionRebuildKnownTagsUserV1ActionsRebuildKnownTagsUserUserUuidPost:
    """ """

    additional_properties: Dict[str, Union[int, str]] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        api_action_rebuild_known_tags_user_v1_actions_rebuild_known_tags_user_user_uuid_post_response_api_action_rebuild_known_tags_user_v1_actions_rebuild_known_tags_user_user_uuid_post = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(data: object) -> Union[int, str]:
                return cast(Union[int, str], data)

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        api_action_rebuild_known_tags_user_v1_actions_rebuild_known_tags_user_user_uuid_post_response_api_action_rebuild_known_tags_user_v1_actions_rebuild_known_tags_user_user_uuid_post.additional_properties = additional_properties
        return api_action_rebuild_known_tags_user_v1_actions_rebuild_known_tags_user_user_uuid_post_response_api_action_rebuild_known_tags_user_v1_actions_rebuild_known_tags_user_user_uuid_post

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Union[int, str]:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Union[int, str]) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
