from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metric_filter_options import MetricFilterOptions


T = TypeVar("T", bound="RunOptions")


@_attrs_define
class RunOptions:
    """
    Attributes:
        metric_filter (Union['MetricFilterOptions', None, Unset]):
        remote_metric_timeout_sec (Union[Unset, float]):  Default: 20.0.
    """

    metric_filter: Union["MetricFilterOptions", None, Unset] = UNSET
    remote_metric_timeout_sec: Union[Unset, float] = 20.0
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.metric_filter_options import MetricFilterOptions

        metric_filter: Union[Dict[str, Any], None, Unset]
        if isinstance(self.metric_filter, Unset):
            metric_filter = UNSET
        elif isinstance(self.metric_filter, MetricFilterOptions):
            metric_filter = self.metric_filter.to_dict()
        else:
            metric_filter = self.metric_filter

        remote_metric_timeout_sec = self.remote_metric_timeout_sec

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if metric_filter is not UNSET:
            field_dict["metric_filter"] = metric_filter
        if remote_metric_timeout_sec is not UNSET:
            field_dict["remote_metric_timeout_sec"] = remote_metric_timeout_sec

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.metric_filter_options import MetricFilterOptions

        d = src_dict.copy()

        def _parse_metric_filter(data: object) -> Union["MetricFilterOptions", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metric_filter_type_0 = MetricFilterOptions.from_dict(data)

                return metric_filter_type_0
            except:  # noqa: E722
                pass
            return cast(Union["MetricFilterOptions", None, Unset], data)

        metric_filter = _parse_metric_filter(d.pop("metric_filter", UNSET))

        remote_metric_timeout_sec = d.pop("remote_metric_timeout_sec", UNSET)

        run_options = cls(
            metric_filter=metric_filter,
            remote_metric_timeout_sec=remote_metric_timeout_sec,
        )

        run_options.additional_properties = d
        return run_options

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
