from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.input_context import InputContext


T = TypeVar("T", bound="EmbeddingRequest")


@_attrs_define
class EmbeddingRequest:
    """
    Attributes:
        prompt (Union[None, Unset, str]):
        response (Union[None, Unset, str]):
        context (Union['InputContext', None, Unset]):
    """

    prompt: Union[None, Unset, str] = UNSET
    response: Union[None, Unset, str] = UNSET
    context: Union["InputContext", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.input_context import InputContext

        prompt: Union[None, Unset, str]
        if isinstance(self.prompt, Unset):
            prompt = UNSET
        else:
            prompt = self.prompt

        response: Union[None, Unset, str]
        if isinstance(self.response, Unset):
            response = UNSET
        else:
            response = self.response

        context: Union[Dict[str, Any], None, Unset]
        if isinstance(self.context, Unset):
            context = UNSET
        elif isinstance(self.context, InputContext):
            context = self.context.to_dict()
        else:
            context = self.context

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if prompt is not UNSET:
            field_dict["prompt"] = prompt
        if response is not UNSET:
            field_dict["response"] = response
        if context is not UNSET:
            field_dict["context"] = context

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.input_context import InputContext

        d = src_dict.copy()

        def _parse_prompt(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        prompt = _parse_prompt(d.pop("prompt", UNSET))

        def _parse_response(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        response = _parse_response(d.pop("response", UNSET))

        def _parse_context(data: object) -> Union["InputContext", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                context_type_0 = InputContext.from_dict(data)

                return context_type_0
            except:  # noqa: E722
                pass
            return cast(Union["InputContext", None, Unset], data)

        context = _parse_context(d.pop("context", UNSET))

        embedding_request = cls(
            prompt=prompt,
            response=response,
            context=context,
        )

        embedding_request.additional_properties = d
        return embedding_request

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
