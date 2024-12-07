from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.exif_model_exif import EXIFModelExif


T = TypeVar("T", bound="EXIFModel")


@_attrs_define
class EXIFModel:
    """Input info for EXIF creation.

    Attributes:
        exif (EXIFModelExif):
    """

    exif: "EXIFModelExif"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        exif = self.exif.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "exif": exif,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.exif_model_exif import EXIFModelExif

        d = src_dict.copy()
        exif = EXIFModelExif.from_dict(d.pop("exif"))

        exif_model = cls(
            exif=exif,
        )

        exif_model.additional_properties = d
        return exif_model

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
