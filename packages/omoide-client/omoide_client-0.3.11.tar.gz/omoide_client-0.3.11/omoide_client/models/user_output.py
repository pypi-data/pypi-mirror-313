from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.user_output_extras import UserOutputExtras


T = TypeVar("T", bound="UserOutput")


@_attrs_define
class UserOutput:
    """Simple user format.

    Attributes:
        uuid (str):
        name (str):
        extras (UserOutputExtras):
    """

    uuid: str
    name: str
    extras: "UserOutputExtras"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        uuid = self.uuid

        name = self.name

        extras = self.extras.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "extras": extras,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.user_output_extras import UserOutputExtras

        d = src_dict.copy()
        uuid = d.pop("uuid")

        name = d.pop("name")

        extras = UserOutputExtras.from_dict(d.pop("extras"))

        user_output = cls(
            uuid=uuid,
            name=name,
            extras=extras,
        )

        user_output.additional_properties = d
        return user_output

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
