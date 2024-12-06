from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.action_type import ActionType
from ..types import UNSET, Unset

T = TypeVar("T", bound="Action")


@_attrs_define
class Action:
    """
    Attributes:
        action_type (Union[ActionType, Any, Unset]):  Default: ActionType.PASS.
        message (Union[None, Unset, str]):
    """

    action_type: Union[ActionType, Any, Unset] = ActionType.PASS
    message: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        action_type: Union[Any, Unset, str]
        if isinstance(self.action_type, Unset):
            action_type = UNSET
        elif isinstance(self.action_type, ActionType):
            action_type = self.action_type.value
        else:
            action_type = self.action_type

        message: Union[None, Unset, str]
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if action_type is not UNSET:
            field_dict["action_type"] = action_type
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_action_type(data: object) -> Union[ActionType, Any, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                action_type_type_0 = ActionType(data)

                return action_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[ActionType, Any, Unset], data)

        action_type = _parse_action_type(d.pop("action_type", UNSET))

        def _parse_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        message = _parse_message(d.pop("message", UNSET))

        action = cls(
            action_type=action_type,
            message=message,
        )

        action.additional_properties = d
        return action

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
