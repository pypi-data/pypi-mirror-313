from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.item_output_extras import ItemOutputExtras
    from ..models.permission import Permission


T = TypeVar("T", bound="ItemOutput")


@_attrs_define
class ItemOutput:
    """Model of a standard item.

    Attributes:
        uuid (UUID):
        parent_uuid (Union[None, UUID]):
        owner_uuid (UUID):
        status (str):
        number (int):
        name (str):
        is_collection (bool):
        content_ext (Union[None, str]):
        preview_ext (Union[None, str]):
        thumbnail_ext (Union[None, str]):
        tags (Union[Unset, List[str]]):
        permissions (Union[Unset, List['Permission']]):
        extras (Union[Unset, ItemOutputExtras]):
    """

    uuid: UUID
    parent_uuid: Union[None, UUID]
    owner_uuid: UUID
    status: str
    number: int
    name: str
    is_collection: bool
    content_ext: Union[None, str]
    preview_ext: Union[None, str]
    thumbnail_ext: Union[None, str]
    tags: Union[Unset, List[str]] = UNSET
    permissions: Union[Unset, List["Permission"]] = UNSET
    extras: Union[Unset, "ItemOutputExtras"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        uuid = str(self.uuid)

        parent_uuid: Union[None, str]
        if isinstance(self.parent_uuid, UUID):
            parent_uuid = str(self.parent_uuid)
        else:
            parent_uuid = self.parent_uuid

        owner_uuid = str(self.owner_uuid)

        status = self.status

        number = self.number

        name = self.name

        is_collection = self.is_collection

        content_ext: Union[None, str]
        content_ext = self.content_ext

        preview_ext: Union[None, str]
        preview_ext = self.preview_ext

        thumbnail_ext: Union[None, str]
        thumbnail_ext = self.thumbnail_ext

        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        permissions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = []
            for permissions_item_data in self.permissions:
                permissions_item = permissions_item_data.to_dict()
                permissions.append(permissions_item)

        extras: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.extras, Unset):
            extras = self.extras.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "parent_uuid": parent_uuid,
                "owner_uuid": owner_uuid,
                "status": status,
                "number": number,
                "name": name,
                "is_collection": is_collection,
                "content_ext": content_ext,
                "preview_ext": preview_ext,
                "thumbnail_ext": thumbnail_ext,
            }
        )
        if tags is not UNSET:
            field_dict["tags"] = tags
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if extras is not UNSET:
            field_dict["extras"] = extras

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.item_output_extras import ItemOutputExtras
        from ..models.permission import Permission

        d = src_dict.copy()
        uuid = UUID(d.pop("uuid"))

        def _parse_parent_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                parent_uuid_type_0 = UUID(data)

                return parent_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        parent_uuid = _parse_parent_uuid(d.pop("parent_uuid"))

        owner_uuid = UUID(d.pop("owner_uuid"))

        status = d.pop("status")

        number = d.pop("number")

        name = d.pop("name")

        is_collection = d.pop("is_collection")

        def _parse_content_ext(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        content_ext = _parse_content_ext(d.pop("content_ext"))

        def _parse_preview_ext(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        preview_ext = _parse_preview_ext(d.pop("preview_ext"))

        def _parse_thumbnail_ext(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        thumbnail_ext = _parse_thumbnail_ext(d.pop("thumbnail_ext"))

        tags = cast(List[str], d.pop("tags", UNSET))

        permissions = []
        _permissions = d.pop("permissions", UNSET)
        for permissions_item_data in _permissions or []:
            permissions_item = Permission.from_dict(permissions_item_data)

            permissions.append(permissions_item)

        _extras = d.pop("extras", UNSET)
        extras: Union[Unset, ItemOutputExtras]
        if isinstance(_extras, Unset):
            extras = UNSET
        else:
            extras = ItemOutputExtras.from_dict(_extras)

        item_output = cls(
            uuid=uuid,
            parent_uuid=parent_uuid,
            owner_uuid=owner_uuid,
            status=status,
            number=number,
            name=name,
            is_collection=is_collection,
            content_ext=content_ext,
            preview_ext=preview_ext,
            thumbnail_ext=thumbnail_ext,
            tags=tags,
            permissions=permissions,
            extras=extras,
        )

        item_output.additional_properties = d
        return item_output

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
