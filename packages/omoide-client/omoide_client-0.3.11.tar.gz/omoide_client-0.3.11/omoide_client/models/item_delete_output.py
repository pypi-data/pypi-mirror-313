from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.item_output import ItemOutput


T = TypeVar("T", bound="ItemDeleteOutput")


@_attrs_define
class ItemDeleteOutput:
    """Output info after item deletion.

    Attributes:
        result (str):
        item_uuid (str):
        switch_to (Union['ItemOutput', None]):
    """

    result: str
    item_uuid: str
    switch_to: Union["ItemOutput", None]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.item_output import ItemOutput

        result = self.result

        item_uuid = self.item_uuid

        switch_to: Union[Dict[str, Any], None]
        if isinstance(self.switch_to, ItemOutput):
            switch_to = self.switch_to.to_dict()
        else:
            switch_to = self.switch_to

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "result": result,
                "item_uuid": item_uuid,
                "switch_to": switch_to,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.item_output import ItemOutput

        d = src_dict.copy()
        result = d.pop("result")

        item_uuid = d.pop("item_uuid")

        def _parse_switch_to(data: object) -> Union["ItemOutput", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                switch_to_type_0 = ItemOutput.from_dict(data)

                return switch_to_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ItemOutput", None], data)

        switch_to = _parse_switch_to(d.pop("switch_to"))

        item_delete_output = cls(
            result=result,
            item_uuid=item_uuid,
            switch_to=switch_to,
        )

        item_delete_output.additional_properties = d
        return item_delete_output

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
