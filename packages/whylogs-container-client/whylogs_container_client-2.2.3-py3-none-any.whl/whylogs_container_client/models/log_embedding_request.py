from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.log_embedding_request_embeddings import LogEmbeddingRequestEmbeddings


T = TypeVar("T", bound="LogEmbeddingRequest")


@_attrs_define
class LogEmbeddingRequest:
    """
    Attributes:
        dataset_id (str):
        timestamp (int):
        embeddings (LogEmbeddingRequestEmbeddings):
    """

    dataset_id: str
    timestamp: int
    embeddings: "LogEmbeddingRequestEmbeddings"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        dataset_id = self.dataset_id

        timestamp = self.timestamp

        embeddings = self.embeddings.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dataset_id": dataset_id,
                "timestamp": timestamp,
                "embeddings": embeddings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.log_embedding_request_embeddings import LogEmbeddingRequestEmbeddings

        d = src_dict.copy()
        dataset_id = d.pop("dataset_id")

        timestamp = d.pop("timestamp")

        embeddings = LogEmbeddingRequestEmbeddings.from_dict(d.pop("embeddings"))

        log_embedding_request = cls(
            dataset_id=dataset_id,
            timestamp=timestamp,
            embeddings=embeddings,
        )

        log_embedding_request.additional_properties = d
        return log_embedding_request

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
