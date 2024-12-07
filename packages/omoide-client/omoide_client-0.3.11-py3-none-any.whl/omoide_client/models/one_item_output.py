from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.item_output import ItemOutput


T = TypeVar("T", bound="OneItemOutput")


@_attrs_define
class OneItemOutput:
    """Response with one item.

    Attributes:
        item (ItemOutput): Model of a standard item.
    """

    item: "ItemOutput"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        item = self.item.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "item": item,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.item_output import ItemOutput

        d = src_dict.copy()
        item = ItemOutput.from_dict(d.pop("item"))

        one_item_output = cls(
            item=item,
        )

        one_item_output.additional_properties = d
        return one_item_output

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
