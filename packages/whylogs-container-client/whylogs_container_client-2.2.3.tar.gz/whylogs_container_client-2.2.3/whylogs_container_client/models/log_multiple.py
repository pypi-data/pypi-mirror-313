from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LogMultiple")


@_attrs_define
class LogMultiple:
    """
    Attributes:
        columns (List[str]):
        data (List[List[Union[List[List[float]], List[List[int]], List[List[str]], List[float], List[int], List[str],
            None, bool, float, int, str]]]):
    """

    columns: List[str]
    data: List[
        List[
            Union[
                List[List[float]],
                List[List[int]],
                List[List[str]],
                List[float],
                List[int],
                List[str],
                None,
                bool,
                float,
                int,
                str,
            ]
        ]
    ]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        columns = self.columns

        data = []
        for data_item_data in self.data:
            data_item = []
            for data_item_item_data in data_item_data:
                data_item_item: Union[
                    List[List[float]],
                    List[List[int]],
                    List[List[str]],
                    List[float],
                    List[int],
                    List[str],
                    None,
                    bool,
                    float,
                    int,
                    str,
                ]
                if isinstance(data_item_item_data, list):
                    data_item_item = data_item_item_data

                elif isinstance(data_item_item_data, list):
                    data_item_item = data_item_item_data

                elif isinstance(data_item_item_data, list):
                    data_item_item = data_item_item_data

                elif isinstance(data_item_item_data, list):
                    data_item_item = []
                    for data_item_item_type_7_item_data in data_item_item_data:
                        data_item_item_type_7_item = data_item_item_type_7_item_data

                        data_item_item.append(data_item_item_type_7_item)

                elif isinstance(data_item_item_data, list):
                    data_item_item = []
                    for data_item_item_type_8_item_data in data_item_item_data:
                        data_item_item_type_8_item = data_item_item_type_8_item_data

                        data_item_item.append(data_item_item_type_8_item)

                elif isinstance(data_item_item_data, list):
                    data_item_item = []
                    for data_item_item_type_9_item_data in data_item_item_data:
                        data_item_item_type_9_item = data_item_item_type_9_item_data

                        data_item_item.append(data_item_item_type_9_item)

                else:
                    data_item_item = data_item_item_data
                data_item.append(data_item_item)

            data.append(data_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "columns": columns,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        columns = cast(List[str], d.pop("columns"))

        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = []
            _data_item = data_item_data
            for data_item_item_data in _data_item:

                def _parse_data_item_item(
                    data: object,
                ) -> Union[
                    List[List[float]],
                    List[List[int]],
                    List[List[str]],
                    List[float],
                    List[int],
                    List[str],
                    None,
                    bool,
                    float,
                    int,
                    str,
                ]:
                    if data is None:
                        return data
                    try:
                        if not isinstance(data, list):
                            raise TypeError()
                        data_item_item_type_4 = cast(List[float], data)

                        return data_item_item_type_4
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, list):
                            raise TypeError()
                        data_item_item_type_5 = cast(List[int], data)

                        return data_item_item_type_5
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, list):
                            raise TypeError()
                        data_item_item_type_6 = cast(List[str], data)

                        return data_item_item_type_6
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, list):
                            raise TypeError()
                        data_item_item_type_7 = []
                        _data_item_item_type_7 = data
                        for data_item_item_type_7_item_data in _data_item_item_type_7:
                            data_item_item_type_7_item = cast(List[float], data_item_item_type_7_item_data)

                            data_item_item_type_7.append(data_item_item_type_7_item)

                        return data_item_item_type_7
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, list):
                            raise TypeError()
                        data_item_item_type_8 = []
                        _data_item_item_type_8 = data
                        for data_item_item_type_8_item_data in _data_item_item_type_8:
                            data_item_item_type_8_item = cast(List[int], data_item_item_type_8_item_data)

                            data_item_item_type_8.append(data_item_item_type_8_item)

                        return data_item_item_type_8
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, list):
                            raise TypeError()
                        data_item_item_type_9 = []
                        _data_item_item_type_9 = data
                        for data_item_item_type_9_item_data in _data_item_item_type_9:
                            data_item_item_type_9_item = cast(List[str], data_item_item_type_9_item_data)

                            data_item_item_type_9.append(data_item_item_type_9_item)

                        return data_item_item_type_9
                    except:  # noqa: E722
                        pass
                    return cast(
                        Union[
                            List[List[float]],
                            List[List[int]],
                            List[List[str]],
                            List[float],
                            List[int],
                            List[str],
                            None,
                            bool,
                            float,
                            int,
                            str,
                        ],
                        data,
                    )

                data_item_item = _parse_data_item_item(data_item_item_data)

                data_item.append(data_item_item)

            data.append(data_item)

        log_multiple = cls(
            columns=columns,
            data=data,
        )

        log_multiple.additional_properties = d
        return log_multiple

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
