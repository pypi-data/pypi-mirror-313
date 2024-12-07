from typing import Any, Dict, List, Type, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.apply_as import ApplyAs
from ..types import UNSET, Unset

T = TypeVar("T", bound="PermissionsInput")


@_attrs_define
class PermissionsInput:
    """Input info for new item permissions.

    Attributes:
        permissions (List[UUID]):
        apply_to_parents (Union[Unset, bool]):  Default: False.
        apply_to_children (Union[Unset, bool]):  Default: True.
        apply_to_children_as (Union[Unset, ApplyAs]): How to apply changes.
    """

    permissions: List[UUID]
    apply_to_parents: Union[Unset, bool] = False
    apply_to_children: Union[Unset, bool] = True
    apply_to_children_as: Union[Unset, ApplyAs] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        permissions = []
        for permissions_item_data in self.permissions:
            permissions_item = str(permissions_item_data)
            permissions.append(permissions_item)

        apply_to_parents = self.apply_to_parents

        apply_to_children = self.apply_to_children

        apply_to_children_as: Union[Unset, str] = UNSET
        if not isinstance(self.apply_to_children_as, Unset):
            apply_to_children_as = self.apply_to_children_as.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "permissions": permissions,
            }
        )
        if apply_to_parents is not UNSET:
            field_dict["apply_to_parents"] = apply_to_parents
        if apply_to_children is not UNSET:
            field_dict["apply_to_children"] = apply_to_children
        if apply_to_children_as is not UNSET:
            field_dict["apply_to_children_as"] = apply_to_children_as

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        permissions = []
        _permissions = d.pop("permissions")
        for permissions_item_data in _permissions:
            permissions_item = UUID(permissions_item_data)

            permissions.append(permissions_item)

        apply_to_parents = d.pop("apply_to_parents", UNSET)

        apply_to_children = d.pop("apply_to_children", UNSET)

        _apply_to_children_as = d.pop("apply_to_children_as", UNSET)
        apply_to_children_as: Union[Unset, ApplyAs]
        if isinstance(_apply_to_children_as, Unset):
            apply_to_children_as = UNSET
        else:
            apply_to_children_as = ApplyAs(_apply_to_children_as)

        permissions_input = cls(
            permissions=permissions,
            apply_to_parents=apply_to_parents,
            apply_to_children=apply_to_children,
            apply_to_children_as=apply_to_children_as,
        )

        permissions_input.additional_properties = d
        return permissions_input

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
