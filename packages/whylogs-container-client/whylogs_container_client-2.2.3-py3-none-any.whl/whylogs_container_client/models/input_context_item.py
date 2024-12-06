from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.input_context_item_metadata import InputContextItemMetadata


T = TypeVar("T", bound="InputContextItem")


@_attrs_define
class InputContextItem:
    """
    Attributes:
        content (str):
        metadata (Union[Unset, InputContextItemMetadata]):
    """

    content: str
    metadata: Union[Unset, "InputContextItemMetadata"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        content = self.content

        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content": content,
            }
        )
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.input_context_item_metadata import InputContextItemMetadata

        d = src_dict.copy()
        content = d.pop("content")

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, InputContextItemMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = InputContextItemMetadata.from_dict(_metadata)

        input_context_item = cls(
            content=content,
            metadata=metadata,
        )

        input_context_item.additional_properties = d
        return input_context_item

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
