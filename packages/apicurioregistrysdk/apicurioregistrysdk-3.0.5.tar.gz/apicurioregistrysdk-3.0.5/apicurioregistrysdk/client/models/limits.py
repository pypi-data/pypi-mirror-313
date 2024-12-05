from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

@dataclass
class Limits(AdditionalDataHolder, Parsable):
    """
    List of limitations on used resources, that are applied on the current instance of Registry.Keys represent the resource type and are suffixed by the corresponding unit.Values are integers. Only non-negative values are allowed, with the exception of -1, which means that the limit is not applied.
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The maxArtifactDescriptionLengthChars property
    max_artifact_description_length_chars: Optional[int] = None
    # The maxArtifactLabelsCount property
    max_artifact_labels_count: Optional[int] = None
    # The maxArtifactNameLengthChars property
    max_artifact_name_length_chars: Optional[int] = None
    # The maxArtifactPropertiesCount property
    max_artifact_properties_count: Optional[int] = None
    # The maxArtifactsCount property
    max_artifacts_count: Optional[int] = None
    # The maxLabelSizeBytes property
    max_label_size_bytes: Optional[int] = None
    # The maxPropertyKeySizeBytes property
    max_property_key_size_bytes: Optional[int] = None
    # The maxPropertyValueSizeBytes property
    max_property_value_size_bytes: Optional[int] = None
    # The maxRequestsPerSecondCount property
    max_requests_per_second_count: Optional[int] = None
    # The maxSchemaSizeBytes property
    max_schema_size_bytes: Optional[int] = None
    # The maxTotalSchemasCount property
    max_total_schemas_count: Optional[int] = None
    # The maxVersionsPerArtifactCount property
    max_versions_per_artifact_count: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> Limits:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Limits
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return Limits()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        fields: Dict[str, Callable[[Any], None]] = {
            "maxArtifactDescriptionLengthChars": lambda n : setattr(self, 'max_artifact_description_length_chars', n.get_int_value()),
            "maxArtifactLabelsCount": lambda n : setattr(self, 'max_artifact_labels_count', n.get_int_value()),
            "maxArtifactNameLengthChars": lambda n : setattr(self, 'max_artifact_name_length_chars', n.get_int_value()),
            "maxArtifactPropertiesCount": lambda n : setattr(self, 'max_artifact_properties_count', n.get_int_value()),
            "maxArtifactsCount": lambda n : setattr(self, 'max_artifacts_count', n.get_int_value()),
            "maxLabelSizeBytes": lambda n : setattr(self, 'max_label_size_bytes', n.get_int_value()),
            "maxPropertyKeySizeBytes": lambda n : setattr(self, 'max_property_key_size_bytes', n.get_int_value()),
            "maxPropertyValueSizeBytes": lambda n : setattr(self, 'max_property_value_size_bytes', n.get_int_value()),
            "maxRequestsPerSecondCount": lambda n : setattr(self, 'max_requests_per_second_count', n.get_int_value()),
            "maxSchemaSizeBytes": lambda n : setattr(self, 'max_schema_size_bytes', n.get_int_value()),
            "maxTotalSchemasCount": lambda n : setattr(self, 'max_total_schemas_count', n.get_int_value()),
            "maxVersionsPerArtifactCount": lambda n : setattr(self, 'max_versions_per_artifact_count', n.get_int_value()),
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
        writer.write_int_value("maxArtifactDescriptionLengthChars", self.max_artifact_description_length_chars)
        writer.write_int_value("maxArtifactLabelsCount", self.max_artifact_labels_count)
        writer.write_int_value("maxArtifactNameLengthChars", self.max_artifact_name_length_chars)
        writer.write_int_value("maxArtifactPropertiesCount", self.max_artifact_properties_count)
        writer.write_int_value("maxArtifactsCount", self.max_artifacts_count)
        writer.write_int_value("maxLabelSizeBytes", self.max_label_size_bytes)
        writer.write_int_value("maxPropertyKeySizeBytes", self.max_property_key_size_bytes)
        writer.write_int_value("maxPropertyValueSizeBytes", self.max_property_value_size_bytes)
        writer.write_int_value("maxRequestsPerSecondCount", self.max_requests_per_second_count)
        writer.write_int_value("maxSchemaSizeBytes", self.max_schema_size_bytes)
        writer.write_int_value("maxTotalSchemasCount", self.max_total_schemas_count)
        writer.write_int_value("maxVersionsPerArtifactCount", self.max_versions_per_artifact_count)
        writer.write_additional_data_value(self.additional_data)
    

