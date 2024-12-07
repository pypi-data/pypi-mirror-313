"""Gateway API schema definitions."""

from enum import Enum
from typing import Literal, Optional, Union

import pydantic
from pydantic import BaseModel


class EntityInfo(BaseModel):
    owner: str
    contact_ids: list[str]
    links: list[str]


class CreateElement(BaseModel):
    name: str


class CreateEntity(CreateElement):
    label: str
    description: str


class CreateOutput(CreateEntity):
    output_type: str


class CreateEntityRequest(BaseModel):
    entity: CreateEntity
    entity_info: Optional[EntityInfo]


class UpdateEntityRequest(BaseModel):
    entity: CreateEntity


class FieldMetadata(BaseModel):
    tags: Optional[list[str]]
    description: Optional[str]


class UpdateEntityMetadataRequest(BaseModel):
    fields: dict[str, FieldMetadata]
    tags: list[str]


class DeleteEntityMetadataRequest(BaseModel):
    fields: dict[str, FieldMetadata]
    tags: list[str]


class FieldDataType(pydantic.BaseModel):
    meta: dict[str, str]
    column_type: str


class CreateFieldDefinition(pydantic.BaseModel):
    name: str
    description: Optional[str] = None
    primary: bool = False
    optional: bool = False
    data_type: FieldDataType


class IcebergTableProperties(pydantic.BaseModel):
    table_format: str
    partitioning: Optional[list[str]] = None
    location: Optional[str] = None
    format_version: Optional[int] = None


class StreamingDataProductSchema(pydantic.BaseModel):
    product_type: Literal["streaming"]
    iceberg_table_properties: Optional[IcebergTableProperties] = None

    fields: list[CreateFieldDefinition]


class StoredDataProductSchema(pydantic.BaseModel):
    product_type: Literal["stored"]
    iceberg_table_properties: Optional[IcebergTableProperties] = None

    fields: list[CreateFieldDefinition]


class UpdateDataProductSchema(pydantic.BaseModel):
    details: Union[
        StreamingDataProductSchema,
        StoredDataProductSchema,
    ] = pydantic.Field(discriminator="product_type")


class ExpectationItem(BaseModel):
    expectation_type: str
    kwargs: dict
    meta: dict


class ExpectationColumnThresholds(BaseModel):
    accuracy: Optional[float]
    completeness: Optional[float]
    consistency: Optional[float]
    uniqueness: Optional[float]
    validity: Optional[float]


class ExpectationThresholds(BaseModel):
    table: float
    columns: dict[str, ExpectationColumnThresholds]


class ExpectationWeights(BaseModel):
    accuracy: float
    completeness: float
    consistency: float
    uniqueness: float
    validity: float


class UpdateQualityExpectations(BaseModel):
    custom_details: list[ExpectationItem]
    weights: Optional[ExpectationWeights]
    thresholds: Optional[ExpectationThresholds]


class ClassificationRegexRecognizer(BaseModel):
    name: str
    description: str
    label: str
    patterns: list[str]


class ClassificationRule(BaseModel):
    model: str
    excluded_columns: list[str]
    regex_recognizers: list[ClassificationRegexRecognizer]


class UpdateClassificationResult(BaseModel):
    resolve: list[str]


class BuilderPipeline(BaseModel):
    config: dict
    inputs: dict[str, dict]
    transformations: list
    finalisers: dict
    preview: bool = False


class UpdateSparkState(BaseModel):
    state: dict


class UpdateDataSourceConnection(BaseModel):
    connection: dict  # TODO: add more details when input parameters will be stable


class UpdateDataSourceConnectionSecret(BaseModel):
    secrets: dict  # TODO: this type is differ from the type in gateway


class UpdateDataUnitConfiguration(BaseModel):
    configuration: dict  # TODO: add more details when input parameters will be stable


class UpdateSecret(BaseModel):
    name: str
    data: dict


class UpdateJournalNote(BaseModel):
    note: str
    owner: str


class SecretKeys(BaseModel):
    keys: list[str]


class TagScope(Enum):
    schema = "SCHEMA"
    field = "FIELD"


class UpdateTag(BaseModel):
    tag: str
    scope: str
