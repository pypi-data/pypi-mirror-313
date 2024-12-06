from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.input_context import InputContext
    from ..models.llm_validate_request_additional_data import LLMValidateRequestAdditionalData
    from ..models.llm_validate_request_metadata_type_0 import LLMValidateRequestMetadataType0
    from ..models.run_options import RunOptions


T = TypeVar("T", bound="LLMValidateRequest")


@_attrs_define
class LLMValidateRequest:
    """
    Attributes:
        dataset_id (str):
        prompt (Union[None, Unset, str]):
        response (Union[None, Unset, str]):
        context (Union['InputContext', None, Unset]):
        id (Union[None, Unset, str]):
        timestamp (Union[Unset, int]):
        additional_data (Union[Unset, LLMValidateRequestAdditionalData]):
        options (Union['RunOptions', None, Unset]):
        metadata (Union['LLMValidateRequestMetadataType0', None, Unset]):
    """

    dataset_id: str
    prompt: Union[None, Unset, str] = UNSET
    response: Union[None, Unset, str] = UNSET
    context: Union["InputContext", None, Unset] = UNSET
    id: Union[None, Unset, str] = UNSET
    timestamp: Union[Unset, int] = UNSET
    additional_data: Union[Unset, "LLMValidateRequestAdditionalData"] = UNSET
    options: Union["RunOptions", None, Unset] = UNSET
    metadata: Union["LLMValidateRequestMetadataType0", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.input_context import InputContext
        from ..models.llm_validate_request_metadata_type_0 import LLMValidateRequestMetadataType0
        from ..models.run_options import RunOptions

        dataset_id = self.dataset_id

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

        id: Union[None, Unset, str]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        timestamp = self.timestamp

        additional_data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.additional_data, Unset):
            additional_data = self.additional_data.to_dict()

        options: Union[Dict[str, Any], None, Unset]
        if isinstance(self.options, Unset):
            options = UNSET
        elif isinstance(self.options, RunOptions):
            options = self.options.to_dict()
        else:
            options = self.options

        metadata: Union[Dict[str, Any], None, Unset]
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, LLMValidateRequestMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "datasetId": dataset_id,
            }
        )
        if prompt is not UNSET:
            field_dict["prompt"] = prompt
        if response is not UNSET:
            field_dict["response"] = response
        if context is not UNSET:
            field_dict["context"] = context
        if id is not UNSET:
            field_dict["id"] = id
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if additional_data is not UNSET:
            field_dict["additional_data"] = additional_data
        if options is not UNSET:
            field_dict["options"] = options
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.input_context import InputContext
        from ..models.llm_validate_request_additional_data import LLMValidateRequestAdditionalData
        from ..models.llm_validate_request_metadata_type_0 import LLMValidateRequestMetadataType0
        from ..models.run_options import RunOptions

        d = src_dict.copy()
        dataset_id = d.pop("datasetId")

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

        def _parse_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        id = _parse_id(d.pop("id", UNSET))

        timestamp = d.pop("timestamp", UNSET)

        _additional_data = d.pop("additional_data", UNSET)
        additional_data: Union[Unset, LLMValidateRequestAdditionalData]
        if isinstance(_additional_data, Unset):
            additional_data = UNSET
        else:
            additional_data = LLMValidateRequestAdditionalData.from_dict(_additional_data)

        def _parse_options(data: object) -> Union["RunOptions", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                options_type_0 = RunOptions.from_dict(data)

                return options_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RunOptions", None, Unset], data)

        options = _parse_options(d.pop("options", UNSET))

        def _parse_metadata(data: object) -> Union["LLMValidateRequestMetadataType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = LLMValidateRequestMetadataType0.from_dict(data)

                return metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["LLMValidateRequestMetadataType0", None, Unset], data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        llm_validate_request = cls(
            dataset_id=dataset_id,
            prompt=prompt,
            response=response,
            context=context,
            id=id,
            timestamp=timestamp,
            additional_data=additional_data,
            options=options,
            metadata=metadata,
        )

        llm_validate_request.additional_properties = d
        return llm_validate_request

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
