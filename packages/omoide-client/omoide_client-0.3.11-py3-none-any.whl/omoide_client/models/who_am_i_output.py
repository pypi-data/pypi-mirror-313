from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WhoAmIOutput")


@_attrs_define
class WhoAmIOutput:
    """WhoAmI response.

    Attributes:
        uuid (Union[None, str]):
        name (str):
    """

    uuid: Union[None, str]
    name: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        uuid: Union[None, str]
        uuid = self.uuid

        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        uuid = _parse_uuid(d.pop("uuid"))

        name = d.pop("name")

        who_am_i_output = cls(
            uuid=uuid,
            name=name,
        )

        who_am_i_output.additional_properties = d
        return who_am_i_output

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
