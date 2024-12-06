from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LogEmbeddingRequestEmbeddings")


@_attrs_define
class LogEmbeddingRequestEmbeddings:
    """ """

    additional_properties: Dict[str, Union[List[List[float]], List[List[int]], List[List[str]]]] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, list):
                field_dict[prop_name] = []
                for additional_property_type_0_item_data in prop:
                    additional_property_type_0_item = additional_property_type_0_item_data

                    field_dict[prop_name].append(additional_property_type_0_item)

            elif isinstance(prop, list):
                field_dict[prop_name] = []
                for additional_property_type_1_item_data in prop:
                    additional_property_type_1_item = additional_property_type_1_item_data

                    field_dict[prop_name].append(additional_property_type_1_item)

            else:
                field_dict[prop_name] = []
                for additional_property_type_2_item_data in prop:
                    additional_property_type_2_item = additional_property_type_2_item_data

                    field_dict[prop_name].append(additional_property_type_2_item)

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        log_embedding_request_embeddings = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(data: object) -> Union[List[List[float]], List[List[int]], List[List[str]]]:
                try:
                    if not isinstance(data, list):
                        raise TypeError()
                    additional_property_type_0 = []
                    _additional_property_type_0 = data
                    for additional_property_type_0_item_data in _additional_property_type_0:
                        additional_property_type_0_item = cast(List[float], additional_property_type_0_item_data)

                        additional_property_type_0.append(additional_property_type_0_item)

                    return additional_property_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, list):
                        raise TypeError()
                    additional_property_type_1 = []
                    _additional_property_type_1 = data
                    for additional_property_type_1_item_data in _additional_property_type_1:
                        additional_property_type_1_item = cast(List[int], additional_property_type_1_item_data)

                        additional_property_type_1.append(additional_property_type_1_item)

                    return additional_property_type_1
                except:  # noqa: E722
                    pass
                if not isinstance(data, list):
                    raise TypeError()
                additional_property_type_2 = []
                _additional_property_type_2 = data
                for additional_property_type_2_item_data in _additional_property_type_2:
                    additional_property_type_2_item = cast(List[str], additional_property_type_2_item_data)

                    additional_property_type_2.append(additional_property_type_2_item)

                return additional_property_type_2

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        log_embedding_request_embeddings.additional_properties = additional_properties
        return log_embedding_request_embeddings

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Union[List[List[float]], List[List[int]], List[List[str]]]:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Union[List[List[float]], List[List[int]], List[List[str]]]) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
