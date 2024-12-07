from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.user_output import UserOutput


T = TypeVar("T", bound="UserCollectionOutput")


@_attrs_define
class UserCollectionOutput:
    """Collection of users.

    Attributes:
        users (List['UserOutput']):
    """

    users: List["UserOutput"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        users = []
        for users_item_data in self.users:
            users_item = users_item_data.to_dict()
            users.append(users_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "users": users,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.user_output import UserOutput

        d = src_dict.copy()
        users = []
        _users = d.pop("users")
        for users_item_data in _users:
            users_item = UserOutput.from_dict(users_item_data)

            users.append(users_item)

        user_collection_output = cls(
            users=users,
        )

        user_collection_output.additional_properties = d
        return user_collection_output

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
