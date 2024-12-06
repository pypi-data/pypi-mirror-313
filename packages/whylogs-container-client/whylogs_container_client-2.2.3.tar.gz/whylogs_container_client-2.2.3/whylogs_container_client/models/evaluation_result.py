from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.action import Action
    from ..models.evaluation_result_metadata import EvaluationResultMetadata
    from ..models.evaluation_result_metrics_item import EvaluationResultMetricsItem
    from ..models.evaluation_result_scores_item import EvaluationResultScoresItem
    from ..models.run_perf import RunPerf
    from ..models.validation_result import ValidationResult


T = TypeVar("T", bound="EvaluationResult")


@_attrs_define
class EvaluationResult:
    """
    Attributes:
        metrics (List['EvaluationResultMetricsItem']):
        validation_results (ValidationResult):
        perf_info (Union['RunPerf', None]):
        action (Action):
        score_perf_info (Union['RunPerf', None, Unset]):
        scores (Union[Unset, List['EvaluationResultScoresItem']]):
        metadata (Union[Unset, EvaluationResultMetadata]):
    """

    metrics: List["EvaluationResultMetricsItem"]
    validation_results: "ValidationResult"
    perf_info: Union["RunPerf", None]
    action: "Action"
    score_perf_info: Union["RunPerf", None, Unset] = UNSET
    scores: Union[Unset, List["EvaluationResultScoresItem"]] = UNSET
    metadata: Union[Unset, "EvaluationResultMetadata"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.run_perf import RunPerf

        metrics = []
        for metrics_item_data in self.metrics:
            metrics_item = metrics_item_data.to_dict()
            metrics.append(metrics_item)

        validation_results = self.validation_results.to_dict()

        perf_info: Union[Dict[str, Any], None]
        if isinstance(self.perf_info, RunPerf):
            perf_info = self.perf_info.to_dict()
        else:
            perf_info = self.perf_info

        action = self.action.to_dict()

        score_perf_info: Union[Dict[str, Any], None, Unset]
        if isinstance(self.score_perf_info, Unset):
            score_perf_info = UNSET
        elif isinstance(self.score_perf_info, RunPerf):
            score_perf_info = self.score_perf_info.to_dict()
        else:
            score_perf_info = self.score_perf_info

        scores: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.scores, Unset):
            scores = []
            for scores_item_data in self.scores:
                scores_item = scores_item_data.to_dict()
                scores.append(scores_item)

        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metrics": metrics,
                "validation_results": validation_results,
                "perf_info": perf_info,
                "action": action,
            }
        )
        if score_perf_info is not UNSET:
            field_dict["score_perf_info"] = score_perf_info
        if scores is not UNSET:
            field_dict["scores"] = scores
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.action import Action
        from ..models.evaluation_result_metadata import EvaluationResultMetadata
        from ..models.evaluation_result_metrics_item import EvaluationResultMetricsItem
        from ..models.evaluation_result_scores_item import EvaluationResultScoresItem
        from ..models.run_perf import RunPerf
        from ..models.validation_result import ValidationResult

        d = src_dict.copy()
        metrics = []
        _metrics = d.pop("metrics")
        for metrics_item_data in _metrics:
            metrics_item = EvaluationResultMetricsItem.from_dict(metrics_item_data)

            metrics.append(metrics_item)

        validation_results = ValidationResult.from_dict(d.pop("validation_results"))

        def _parse_perf_info(data: object) -> Union["RunPerf", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                perf_info_type_0 = RunPerf.from_dict(data)

                return perf_info_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RunPerf", None], data)

        perf_info = _parse_perf_info(d.pop("perf_info"))

        action = Action.from_dict(d.pop("action"))

        def _parse_score_perf_info(data: object) -> Union["RunPerf", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                score_perf_info_type_0 = RunPerf.from_dict(data)

                return score_perf_info_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RunPerf", None, Unset], data)

        score_perf_info = _parse_score_perf_info(d.pop("score_perf_info", UNSET))

        scores = []
        _scores = d.pop("scores", UNSET)
        for scores_item_data in _scores or []:
            scores_item = EvaluationResultScoresItem.from_dict(scores_item_data)

            scores.append(scores_item)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, EvaluationResultMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = EvaluationResultMetadata.from_dict(_metadata)

        evaluation_result = cls(
            metrics=metrics,
            validation_results=validation_results,
            perf_info=perf_info,
            action=action,
            score_perf_info=score_perf_info,
            scores=scores,
            metadata=metadata,
        )

        evaluation_result.additional_properties = d
        return evaluation_result

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
