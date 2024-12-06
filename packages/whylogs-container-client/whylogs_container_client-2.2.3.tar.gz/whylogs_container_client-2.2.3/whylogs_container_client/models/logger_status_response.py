from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LoggerStatusResponse")


@_attrs_define
class LoggerStatusResponse:
    """
    Attributes:
        dataset_timestamps (int):
        dataset_profiles (int):
        segment_caches (int):
        writers (int):
        pending_writables (int):
        pending_views (List[str]):
        views (List[str]):
    """

    dataset_timestamps: int
    dataset_profiles: int
    segment_caches: int
    writers: int
    pending_writables: int
    pending_views: List[str]
    views: List[str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        dataset_timestamps = self.dataset_timestamps

        dataset_profiles = self.dataset_profiles

        segment_caches = self.segment_caches

        writers = self.writers

        pending_writables = self.pending_writables

        pending_views = self.pending_views

        views = self.views

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dataset_timestamps": dataset_timestamps,
                "dataset_profiles": dataset_profiles,
                "segment_caches": segment_caches,
                "writers": writers,
                "pending_writables": pending_writables,
                "pending_views": pending_views,
                "views": views,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        dataset_timestamps = d.pop("dataset_timestamps")

        dataset_profiles = d.pop("dataset_profiles")

        segment_caches = d.pop("segment_caches")

        writers = d.pop("writers")

        pending_writables = d.pop("pending_writables")

        pending_views = cast(List[str], d.pop("pending_views"))

        views = cast(List[str], d.pop("views"))

        logger_status_response = cls(
            dataset_timestamps=dataset_timestamps,
            dataset_profiles=dataset_profiles,
            segment_caches=segment_caches,
            writers=writers,
            pending_writables=pending_writables,
            pending_views=pending_views,
            views=views,
        )

        logger_status_response.additional_properties = d
        return logger_status_response

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
