from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.permission import Permission


T = TypeVar("T", bound="ItemInput")


@_attrs_define
class ItemInput:
    """Input info for item creation.

    Attributes:
        uuid (Union[None, UUID, Unset]):
        parent_uuid (Union[None, UUID, Unset]):
        name (Union[Unset, str]):  Default: ''.
        number (Union[None, Unset, int]):
        is_collection (Union[Unset, bool]):  Default: False.
        tags (Union[Unset, List[str]]):
        permissions (Union[Unset, List['Permission']]):
    """

    uuid: Union[None, UUID, Unset] = UNSET
    parent_uuid: Union[None, UUID, Unset] = UNSET
    name: Union[Unset, str] = ""
    number: Union[None, Unset, int] = UNSET
    is_collection: Union[Unset, bool] = False
    tags: Union[Unset, List[str]] = UNSET
    permissions: Union[Unset, List["Permission"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        uuid: Union[None, Unset, str]
        if isinstance(self.uuid, Unset):
            uuid = UNSET
        elif isinstance(self.uuid, UUID):
            uuid = str(self.uuid)
        else:
            uuid = self.uuid

        parent_uuid: Union[None, Unset, str]
        if isinstance(self.parent_uuid, Unset):
            parent_uuid = UNSET
        elif isinstance(self.parent_uuid, UUID):
            parent_uuid = str(self.parent_uuid)
        else:
            parent_uuid = self.parent_uuid

        name = self.name

        number: Union[None, Unset, int]
        if isinstance(self.number, Unset):
            number = UNSET
        else:
            number = self.number

        is_collection = self.is_collection

        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        permissions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = []
            for permissions_item_data in self.permissions:
                permissions_item = permissions_item_data.to_dict()
                permissions.append(permissions_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if parent_uuid is not UNSET:
            field_dict["parent_uuid"] = parent_uuid
        if name is not UNSET:
            field_dict["name"] = name
        if number is not UNSET:
            field_dict["number"] = number
        if is_collection is not UNSET:
            field_dict["is_collection"] = is_collection
        if tags is not UNSET:
            field_dict["tags"] = tags
        if permissions is not UNSET:
            field_dict["permissions"] = permissions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.permission import Permission

        d = src_dict.copy()

        def _parse_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                uuid_type_0 = UUID(data)

                return uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        uuid = _parse_uuid(d.pop("uuid", UNSET))

        def _parse_parent_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                parent_uuid_type_0 = UUID(data)

                return parent_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        parent_uuid = _parse_parent_uuid(d.pop("parent_uuid", UNSET))

        name = d.pop("name", UNSET)

        def _parse_number(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        number = _parse_number(d.pop("number", UNSET))

        is_collection = d.pop("is_collection", UNSET)

        tags = cast(List[str], d.pop("tags", UNSET))

        permissions = []
        _permissions = d.pop("permissions", UNSET)
        for permissions_item_data in _permissions or []:
            permissions_item = Permission.from_dict(permissions_item_data)

            permissions.append(permissions_item)

        item_input = cls(
            uuid=uuid,
            parent_uuid=parent_uuid,
            name=name,
            number=number,
            is_collection=is_collection,
            tags=tags,
            permissions=permissions,
        )

        item_input.additional_properties = d
        return item_input

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
