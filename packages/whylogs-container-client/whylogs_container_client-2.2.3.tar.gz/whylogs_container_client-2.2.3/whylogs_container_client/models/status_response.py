from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.status_response_config import StatusResponseConfig
    from ..models.status_response_whylogs_logger_status import StatusResponseWhylogsLoggerStatus


T = TypeVar("T", bound="StatusResponse")


@_attrs_define
class StatusResponse:
    """
    Attributes:
        version (str):
        whylogs_logger_status (StatusResponseWhylogsLoggerStatus):
        config (StatusResponseConfig):
    """

    version: str
    whylogs_logger_status: "StatusResponseWhylogsLoggerStatus"
    config: "StatusResponseConfig"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        version = self.version

        whylogs_logger_status = self.whylogs_logger_status.to_dict()

        config = self.config.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "version": version,
                "whylogs_logger_status": whylogs_logger_status,
                "config": config,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.status_response_config import StatusResponseConfig
        from ..models.status_response_whylogs_logger_status import StatusResponseWhylogsLoggerStatus

        d = src_dict.copy()
        version = d.pop("version")

        whylogs_logger_status = StatusResponseWhylogsLoggerStatus.from_dict(d.pop("whylogs_logger_status"))

        config = StatusResponseConfig.from_dict(d.pop("config"))

        status_response = cls(
            version=version,
            whylogs_logger_status=whylogs_logger_status,
            config=config,
        )

        status_response.additional_properties = d
        return status_response

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
