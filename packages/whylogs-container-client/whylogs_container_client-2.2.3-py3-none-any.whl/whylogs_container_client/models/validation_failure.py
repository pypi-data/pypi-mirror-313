from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.validation_failure_failure_level import ValidationFailureFailureLevel
from ..types import UNSET, Unset

T = TypeVar("T", bound="ValidationFailure")


@_attrs_define
class ValidationFailure:
    """
    Attributes:
        id (str):
        metric (str):
        details (str):
        value (Union[None, float, int, str]):
        upper_threshold (Union[None, Unset, float]):
        lower_threshold (Union[None, Unset, float]):
        allowed_values (Union[List[Union[float, int, str]], None, Unset]):
        disallowed_values (Union[List[Union[float, int, str]], None, Unset]):
        must_be_none (Union[None, Unset, bool]):
        must_be_non_none (Union[None, Unset, bool]):
        failure_level (Union[Unset, ValidationFailureFailureLevel]):  Default: ValidationFailureFailureLevel.BLOCK.
    """

    id: str
    metric: str
    details: str
    value: Union[None, float, int, str]
    upper_threshold: Union[None, Unset, float] = UNSET
    lower_threshold: Union[None, Unset, float] = UNSET
    allowed_values: Union[List[Union[float, int, str]], None, Unset] = UNSET
    disallowed_values: Union[List[Union[float, int, str]], None, Unset] = UNSET
    must_be_none: Union[None, Unset, bool] = UNSET
    must_be_non_none: Union[None, Unset, bool] = UNSET
    failure_level: Union[Unset, ValidationFailureFailureLevel] = ValidationFailureFailureLevel.BLOCK
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        metric = self.metric

        details = self.details

        value: Union[None, float, int, str]
        value = self.value

        upper_threshold: Union[None, Unset, float]
        if isinstance(self.upper_threshold, Unset):
            upper_threshold = UNSET
        else:
            upper_threshold = self.upper_threshold

        lower_threshold: Union[None, Unset, float]
        if isinstance(self.lower_threshold, Unset):
            lower_threshold = UNSET
        else:
            lower_threshold = self.lower_threshold

        allowed_values: Union[List[Union[float, int, str]], None, Unset]
        if isinstance(self.allowed_values, Unset):
            allowed_values = UNSET
        elif isinstance(self.allowed_values, list):
            allowed_values = []
            for allowed_values_type_0_item_data in self.allowed_values:
                allowed_values_type_0_item: Union[float, int, str]
                allowed_values_type_0_item = allowed_values_type_0_item_data
                allowed_values.append(allowed_values_type_0_item)

        else:
            allowed_values = self.allowed_values

        disallowed_values: Union[List[Union[float, int, str]], None, Unset]
        if isinstance(self.disallowed_values, Unset):
            disallowed_values = UNSET
        elif isinstance(self.disallowed_values, list):
            disallowed_values = []
            for disallowed_values_type_0_item_data in self.disallowed_values:
                disallowed_values_type_0_item: Union[float, int, str]
                disallowed_values_type_0_item = disallowed_values_type_0_item_data
                disallowed_values.append(disallowed_values_type_0_item)

        else:
            disallowed_values = self.disallowed_values

        must_be_none: Union[None, Unset, bool]
        if isinstance(self.must_be_none, Unset):
            must_be_none = UNSET
        else:
            must_be_none = self.must_be_none

        must_be_non_none: Union[None, Unset, bool]
        if isinstance(self.must_be_non_none, Unset):
            must_be_non_none = UNSET
        else:
            must_be_non_none = self.must_be_non_none

        failure_level: Union[Unset, str] = UNSET
        if not isinstance(self.failure_level, Unset):
            failure_level = self.failure_level.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "metric": metric,
                "details": details,
                "value": value,
            }
        )
        if upper_threshold is not UNSET:
            field_dict["upper_threshold"] = upper_threshold
        if lower_threshold is not UNSET:
            field_dict["lower_threshold"] = lower_threshold
        if allowed_values is not UNSET:
            field_dict["allowed_values"] = allowed_values
        if disallowed_values is not UNSET:
            field_dict["disallowed_values"] = disallowed_values
        if must_be_none is not UNSET:
            field_dict["must_be_none"] = must_be_none
        if must_be_non_none is not UNSET:
            field_dict["must_be_non_none"] = must_be_non_none
        if failure_level is not UNSET:
            field_dict["failure_level"] = failure_level

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        metric = d.pop("metric")

        details = d.pop("details")

        def _parse_value(data: object) -> Union[None, float, int, str]:
            if data is None:
                return data
            return cast(Union[None, float, int, str], data)

        value = _parse_value(d.pop("value"))

        def _parse_upper_threshold(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        upper_threshold = _parse_upper_threshold(d.pop("upper_threshold", UNSET))

        def _parse_lower_threshold(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        lower_threshold = _parse_lower_threshold(d.pop("lower_threshold", UNSET))

        def _parse_allowed_values(data: object) -> Union[List[Union[float, int, str]], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                allowed_values_type_0 = []
                _allowed_values_type_0 = data
                for allowed_values_type_0_item_data in _allowed_values_type_0:

                    def _parse_allowed_values_type_0_item(data: object) -> Union[float, int, str]:
                        return cast(Union[float, int, str], data)

                    allowed_values_type_0_item = _parse_allowed_values_type_0_item(allowed_values_type_0_item_data)

                    allowed_values_type_0.append(allowed_values_type_0_item)

                return allowed_values_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[Union[float, int, str]], None, Unset], data)

        allowed_values = _parse_allowed_values(d.pop("allowed_values", UNSET))

        def _parse_disallowed_values(data: object) -> Union[List[Union[float, int, str]], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                disallowed_values_type_0 = []
                _disallowed_values_type_0 = data
                for disallowed_values_type_0_item_data in _disallowed_values_type_0:

                    def _parse_disallowed_values_type_0_item(data: object) -> Union[float, int, str]:
                        return cast(Union[float, int, str], data)

                    disallowed_values_type_0_item = _parse_disallowed_values_type_0_item(
                        disallowed_values_type_0_item_data
                    )

                    disallowed_values_type_0.append(disallowed_values_type_0_item)

                return disallowed_values_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[Union[float, int, str]], None, Unset], data)

        disallowed_values = _parse_disallowed_values(d.pop("disallowed_values", UNSET))

        def _parse_must_be_none(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        must_be_none = _parse_must_be_none(d.pop("must_be_none", UNSET))

        def _parse_must_be_non_none(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        must_be_non_none = _parse_must_be_non_none(d.pop("must_be_non_none", UNSET))

        _failure_level = d.pop("failure_level", UNSET)
        failure_level: Union[Unset, ValidationFailureFailureLevel]
        if isinstance(_failure_level, Unset):
            failure_level = UNSET
        else:
            failure_level = ValidationFailureFailureLevel(_failure_level)

        validation_failure = cls(
            id=id,
            metric=metric,
            details=details,
            value=value,
            upper_threshold=upper_threshold,
            lower_threshold=lower_threshold,
            allowed_values=allowed_values,
            disallowed_values=disallowed_values,
            must_be_none=must_be_none,
            must_be_non_none=must_be_non_none,
            failure_level=failure_level,
        )

        validation_failure.additional_properties = d
        return validation_failure

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
