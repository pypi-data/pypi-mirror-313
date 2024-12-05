from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .searched_artifact import SearchedArtifact

@dataclass
class ArtifactSearchResults(AdditionalDataHolder, Parsable):
    """
    Describes the response received when searching for artifacts.
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The artifacts returned in the result set.
    artifacts: Optional[List[SearchedArtifact]] = None
    # The total number of artifacts that matched the query that produced the result set (may be more than the number of artifacts in the result set).
    count: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ArtifactSearchResults:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ArtifactSearchResults
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return ArtifactSearchResults()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .searched_artifact import SearchedArtifact

        from .searched_artifact import SearchedArtifact

        fields: Dict[str, Callable[[Any], None]] = {
            "artifacts": lambda n : setattr(self, 'artifacts', n.get_collection_of_object_values(SearchedArtifact)),
            "count": lambda n : setattr(self, 'count', n.get_int_value()),
        }
        return fields
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        param writer: Serialization writer to use to serialize this model
        Returns: None
        """
        if writer is None:
            raise TypeError("writer cannot be null.")
        from .searched_artifact import SearchedArtifact

        writer.write_collection_of_object_values("artifacts", self.artifacts)
        writer.write_int_value("count", self.count)
        writer.write_additional_data_value(self.additional_data)
    

