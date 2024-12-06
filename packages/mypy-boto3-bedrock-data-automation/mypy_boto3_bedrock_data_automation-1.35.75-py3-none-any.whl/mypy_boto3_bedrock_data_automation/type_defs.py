"""
Type annotations for bedrock-data-automation service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_data_automation/type_defs/)

Usage::

    ```python
    from mypy_boto3_bedrock_data_automation.type_defs import AudioExtractionCategoryOutputTypeDef

    data: AudioExtractionCategoryOutputTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AudioExtractionCategoryTypeType,
    AudioStandardGenerativeFieldTypeType,
    BlueprintStageFilterType,
    BlueprintStageType,
    DataAutomationProjectStageFilterType,
    DataAutomationProjectStageType,
    DataAutomationProjectStatusType,
    DocumentExtractionGranularityTypeType,
    DocumentOutputTextFormatTypeType,
    ImageExtractionCategoryTypeType,
    ImageStandardGenerativeFieldTypeType,
    ResourceOwnerType,
    StateType,
    TypeType,
    VideoExtractionCategoryTypeType,
    VideoStandardGenerativeFieldTypeType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AudioExtractionCategoryOutputTypeDef",
    "AudioExtractionCategoryTypeDef",
    "AudioExtractionCategoryUnionTypeDef",
    "AudioStandardExtractionOutputTypeDef",
    "AudioStandardExtractionTypeDef",
    "AudioStandardExtractionUnionTypeDef",
    "AudioStandardGenerativeFieldOutputTypeDef",
    "AudioStandardGenerativeFieldTypeDef",
    "AudioStandardGenerativeFieldUnionTypeDef",
    "AudioStandardOutputConfigurationOutputTypeDef",
    "AudioStandardOutputConfigurationTypeDef",
    "AudioStandardOutputConfigurationUnionTypeDef",
    "BlueprintFilterTypeDef",
    "BlueprintItemTypeDef",
    "BlueprintSummaryTypeDef",
    "BlueprintTypeDef",
    "CreateBlueprintRequestRequestTypeDef",
    "CreateBlueprintResponseTypeDef",
    "CreateBlueprintVersionRequestRequestTypeDef",
    "CreateBlueprintVersionResponseTypeDef",
    "CreateDataAutomationProjectRequestRequestTypeDef",
    "CreateDataAutomationProjectResponseTypeDef",
    "CustomOutputConfigurationOutputTypeDef",
    "CustomOutputConfigurationTypeDef",
    "DataAutomationProjectFilterTypeDef",
    "DataAutomationProjectSummaryTypeDef",
    "DataAutomationProjectTypeDef",
    "DeleteBlueprintRequestRequestTypeDef",
    "DeleteDataAutomationProjectRequestRequestTypeDef",
    "DeleteDataAutomationProjectResponseTypeDef",
    "DocumentBoundingBoxTypeDef",
    "DocumentExtractionGranularityOutputTypeDef",
    "DocumentExtractionGranularityTypeDef",
    "DocumentExtractionGranularityUnionTypeDef",
    "DocumentOutputAdditionalFileFormatTypeDef",
    "DocumentOutputFormatOutputTypeDef",
    "DocumentOutputFormatTypeDef",
    "DocumentOutputFormatUnionTypeDef",
    "DocumentOutputTextFormatOutputTypeDef",
    "DocumentOutputTextFormatTypeDef",
    "DocumentOutputTextFormatUnionTypeDef",
    "DocumentOverrideConfigurationTypeDef",
    "DocumentStandardExtractionOutputTypeDef",
    "DocumentStandardExtractionTypeDef",
    "DocumentStandardExtractionUnionTypeDef",
    "DocumentStandardGenerativeFieldTypeDef",
    "DocumentStandardOutputConfigurationOutputTypeDef",
    "DocumentStandardOutputConfigurationTypeDef",
    "DocumentStandardOutputConfigurationUnionTypeDef",
    "EncryptionConfigurationTypeDef",
    "GetBlueprintRequestRequestTypeDef",
    "GetBlueprintResponseTypeDef",
    "GetDataAutomationProjectRequestRequestTypeDef",
    "GetDataAutomationProjectResponseTypeDef",
    "ImageBoundingBoxTypeDef",
    "ImageExtractionCategoryOutputTypeDef",
    "ImageExtractionCategoryTypeDef",
    "ImageExtractionCategoryUnionTypeDef",
    "ImageStandardExtractionOutputTypeDef",
    "ImageStandardExtractionTypeDef",
    "ImageStandardExtractionUnionTypeDef",
    "ImageStandardGenerativeFieldOutputTypeDef",
    "ImageStandardGenerativeFieldTypeDef",
    "ImageStandardGenerativeFieldUnionTypeDef",
    "ImageStandardOutputConfigurationOutputTypeDef",
    "ImageStandardOutputConfigurationTypeDef",
    "ImageStandardOutputConfigurationUnionTypeDef",
    "ListBlueprintsRequestListBlueprintsPaginateTypeDef",
    "ListBlueprintsRequestRequestTypeDef",
    "ListBlueprintsResponseTypeDef",
    "ListDataAutomationProjectsRequestListDataAutomationProjectsPaginateTypeDef",
    "ListDataAutomationProjectsRequestRequestTypeDef",
    "ListDataAutomationProjectsResponseTypeDef",
    "OverrideConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "SplitterConfigurationTypeDef",
    "StandardOutputConfigurationOutputTypeDef",
    "StandardOutputConfigurationTypeDef",
    "UpdateBlueprintRequestRequestTypeDef",
    "UpdateBlueprintResponseTypeDef",
    "UpdateDataAutomationProjectRequestRequestTypeDef",
    "UpdateDataAutomationProjectResponseTypeDef",
    "VideoBoundingBoxTypeDef",
    "VideoExtractionCategoryOutputTypeDef",
    "VideoExtractionCategoryTypeDef",
    "VideoExtractionCategoryUnionTypeDef",
    "VideoStandardExtractionOutputTypeDef",
    "VideoStandardExtractionTypeDef",
    "VideoStandardExtractionUnionTypeDef",
    "VideoStandardGenerativeFieldOutputTypeDef",
    "VideoStandardGenerativeFieldTypeDef",
    "VideoStandardGenerativeFieldUnionTypeDef",
    "VideoStandardOutputConfigurationOutputTypeDef",
    "VideoStandardOutputConfigurationTypeDef",
    "VideoStandardOutputConfigurationUnionTypeDef",
)

AudioExtractionCategoryOutputTypeDef = TypedDict(
    "AudioExtractionCategoryOutputTypeDef",
    {
        "state": StateType,
        "types": NotRequired[List[AudioExtractionCategoryTypeType]],
    },
)
AudioExtractionCategoryTypeDef = TypedDict(
    "AudioExtractionCategoryTypeDef",
    {
        "state": StateType,
        "types": NotRequired[Sequence[AudioExtractionCategoryTypeType]],
    },
)
AudioStandardGenerativeFieldOutputTypeDef = TypedDict(
    "AudioStandardGenerativeFieldOutputTypeDef",
    {
        "state": StateType,
        "types": NotRequired[List[AudioStandardGenerativeFieldTypeType]],
    },
)
AudioStandardGenerativeFieldTypeDef = TypedDict(
    "AudioStandardGenerativeFieldTypeDef",
    {
        "state": StateType,
        "types": NotRequired[Sequence[AudioStandardGenerativeFieldTypeType]],
    },
)


class BlueprintFilterTypeDef(TypedDict):
    blueprintArn: str
    blueprintVersion: NotRequired[str]
    blueprintStage: NotRequired[BlueprintStageType]


class BlueprintItemTypeDef(TypedDict):
    blueprintArn: str
    blueprintVersion: NotRequired[str]
    blueprintStage: NotRequired[BlueprintStageType]


class BlueprintSummaryTypeDef(TypedDict):
    blueprintArn: str
    creationTime: datetime
    blueprintVersion: NotRequired[str]
    blueprintStage: NotRequired[BlueprintStageType]
    blueprintName: NotRequired[str]
    lastModifiedTime: NotRequired[datetime]


BlueprintTypeDef = TypedDict(
    "BlueprintTypeDef",
    {
        "blueprintArn": str,
        "schema": str,
        "type": TypeType,
        "creationTime": datetime,
        "lastModifiedTime": datetime,
        "blueprintName": str,
        "blueprintVersion": NotRequired[str],
        "blueprintStage": NotRequired[BlueprintStageType],
        "kmsKeyId": NotRequired[str],
        "kmsEncryptionContext": NotRequired[Dict[str, str]],
    },
)


class EncryptionConfigurationTypeDef(TypedDict):
    kmsKeyId: str
    kmsEncryptionContext: NotRequired[Mapping[str, str]]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CreateBlueprintVersionRequestRequestTypeDef(TypedDict):
    blueprintArn: str
    clientToken: NotRequired[str]


class DataAutomationProjectFilterTypeDef(TypedDict):
    projectArn: str
    projectStage: NotRequired[DataAutomationProjectStageType]


class DataAutomationProjectSummaryTypeDef(TypedDict):
    projectArn: str
    creationTime: datetime
    projectStage: NotRequired[DataAutomationProjectStageType]
    projectName: NotRequired[str]


class DeleteBlueprintRequestRequestTypeDef(TypedDict):
    blueprintArn: str
    blueprintVersion: NotRequired[str]


class DeleteDataAutomationProjectRequestRequestTypeDef(TypedDict):
    projectArn: str


class DocumentBoundingBoxTypeDef(TypedDict):
    state: StateType


DocumentExtractionGranularityOutputTypeDef = TypedDict(
    "DocumentExtractionGranularityOutputTypeDef",
    {
        "types": NotRequired[List[DocumentExtractionGranularityTypeType]],
    },
)
DocumentExtractionGranularityTypeDef = TypedDict(
    "DocumentExtractionGranularityTypeDef",
    {
        "types": NotRequired[Sequence[DocumentExtractionGranularityTypeType]],
    },
)


class DocumentOutputAdditionalFileFormatTypeDef(TypedDict):
    state: StateType


DocumentOutputTextFormatOutputTypeDef = TypedDict(
    "DocumentOutputTextFormatOutputTypeDef",
    {
        "types": NotRequired[List[DocumentOutputTextFormatTypeType]],
    },
)
DocumentOutputTextFormatTypeDef = TypedDict(
    "DocumentOutputTextFormatTypeDef",
    {
        "types": NotRequired[Sequence[DocumentOutputTextFormatTypeType]],
    },
)


class SplitterConfigurationTypeDef(TypedDict):
    state: NotRequired[StateType]


class DocumentStandardGenerativeFieldTypeDef(TypedDict):
    state: StateType


class GetBlueprintRequestRequestTypeDef(TypedDict):
    blueprintArn: str
    blueprintVersion: NotRequired[str]
    blueprintStage: NotRequired[BlueprintStageType]


class GetDataAutomationProjectRequestRequestTypeDef(TypedDict):
    projectArn: str
    projectStage: NotRequired[DataAutomationProjectStageType]


class ImageBoundingBoxTypeDef(TypedDict):
    state: StateType


ImageExtractionCategoryOutputTypeDef = TypedDict(
    "ImageExtractionCategoryOutputTypeDef",
    {
        "state": StateType,
        "types": NotRequired[List[ImageExtractionCategoryTypeType]],
    },
)
ImageExtractionCategoryTypeDef = TypedDict(
    "ImageExtractionCategoryTypeDef",
    {
        "state": StateType,
        "types": NotRequired[Sequence[ImageExtractionCategoryTypeType]],
    },
)
ImageStandardGenerativeFieldOutputTypeDef = TypedDict(
    "ImageStandardGenerativeFieldOutputTypeDef",
    {
        "state": StateType,
        "types": NotRequired[List[ImageStandardGenerativeFieldTypeType]],
    },
)
ImageStandardGenerativeFieldTypeDef = TypedDict(
    "ImageStandardGenerativeFieldTypeDef",
    {
        "state": StateType,
        "types": NotRequired[Sequence[ImageStandardGenerativeFieldTypeType]],
    },
)


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class UpdateBlueprintRequestRequestTypeDef(TypedDict):
    blueprintArn: str
    schema: str
    blueprintStage: NotRequired[BlueprintStageType]


class VideoBoundingBoxTypeDef(TypedDict):
    state: StateType


VideoExtractionCategoryOutputTypeDef = TypedDict(
    "VideoExtractionCategoryOutputTypeDef",
    {
        "state": StateType,
        "types": NotRequired[List[VideoExtractionCategoryTypeType]],
    },
)
VideoExtractionCategoryTypeDef = TypedDict(
    "VideoExtractionCategoryTypeDef",
    {
        "state": StateType,
        "types": NotRequired[Sequence[VideoExtractionCategoryTypeType]],
    },
)
VideoStandardGenerativeFieldOutputTypeDef = TypedDict(
    "VideoStandardGenerativeFieldOutputTypeDef",
    {
        "state": StateType,
        "types": NotRequired[List[VideoStandardGenerativeFieldTypeType]],
    },
)
VideoStandardGenerativeFieldTypeDef = TypedDict(
    "VideoStandardGenerativeFieldTypeDef",
    {
        "state": StateType,
        "types": NotRequired[Sequence[VideoStandardGenerativeFieldTypeType]],
    },
)


class AudioStandardExtractionOutputTypeDef(TypedDict):
    category: AudioExtractionCategoryOutputTypeDef


AudioExtractionCategoryUnionTypeDef = Union[
    AudioExtractionCategoryTypeDef, AudioExtractionCategoryOutputTypeDef
]
AudioStandardGenerativeFieldUnionTypeDef = Union[
    AudioStandardGenerativeFieldTypeDef, AudioStandardGenerativeFieldOutputTypeDef
]


class ListDataAutomationProjectsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    projectStageFilter: NotRequired[DataAutomationProjectStageFilterType]
    blueprintFilter: NotRequired[BlueprintFilterTypeDef]
    resourceOwner: NotRequired[ResourceOwnerType]


class CustomOutputConfigurationOutputTypeDef(TypedDict):
    blueprints: NotRequired[List[BlueprintItemTypeDef]]


class CustomOutputConfigurationTypeDef(TypedDict):
    blueprints: NotRequired[Sequence[BlueprintItemTypeDef]]


CreateBlueprintRequestRequestTypeDef = TypedDict(
    "CreateBlueprintRequestRequestTypeDef",
    {
        "blueprintName": str,
        "type": TypeType,
        "schema": str,
        "blueprintStage": NotRequired[BlueprintStageType],
        "clientToken": NotRequired[str],
        "encryptionConfiguration": NotRequired[EncryptionConfigurationTypeDef],
    },
)


class CreateBlueprintResponseTypeDef(TypedDict):
    blueprint: BlueprintTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateBlueprintVersionResponseTypeDef(TypedDict):
    blueprint: BlueprintTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDataAutomationProjectResponseTypeDef(TypedDict):
    projectArn: str
    projectStage: DataAutomationProjectStageType
    status: DataAutomationProjectStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDataAutomationProjectResponseTypeDef(TypedDict):
    projectArn: str
    status: DataAutomationProjectStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class GetBlueprintResponseTypeDef(TypedDict):
    blueprint: BlueprintTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListBlueprintsResponseTypeDef(TypedDict):
    blueprints: List[BlueprintSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateBlueprintResponseTypeDef(TypedDict):
    blueprint: BlueprintTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDataAutomationProjectResponseTypeDef(TypedDict):
    projectArn: str
    projectStage: DataAutomationProjectStageType
    status: DataAutomationProjectStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class ListBlueprintsRequestRequestTypeDef(TypedDict):
    blueprintArn: NotRequired[str]
    resourceOwner: NotRequired[ResourceOwnerType]
    blueprintStageFilter: NotRequired[BlueprintStageFilterType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    projectFilter: NotRequired[DataAutomationProjectFilterTypeDef]


class ListDataAutomationProjectsResponseTypeDef(TypedDict):
    projects: List[DataAutomationProjectSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DocumentStandardExtractionOutputTypeDef(TypedDict):
    granularity: DocumentExtractionGranularityOutputTypeDef
    boundingBox: DocumentBoundingBoxTypeDef


DocumentExtractionGranularityUnionTypeDef = Union[
    DocumentExtractionGranularityTypeDef, DocumentExtractionGranularityOutputTypeDef
]


class DocumentOutputFormatOutputTypeDef(TypedDict):
    textFormat: DocumentOutputTextFormatOutputTypeDef
    additionalFileFormat: DocumentOutputAdditionalFileFormatTypeDef


DocumentOutputTextFormatUnionTypeDef = Union[
    DocumentOutputTextFormatTypeDef, DocumentOutputTextFormatOutputTypeDef
]


class DocumentOverrideConfigurationTypeDef(TypedDict):
    splitter: NotRequired[SplitterConfigurationTypeDef]


class ImageStandardExtractionOutputTypeDef(TypedDict):
    category: ImageExtractionCategoryOutputTypeDef
    boundingBox: ImageBoundingBoxTypeDef


ImageExtractionCategoryUnionTypeDef = Union[
    ImageExtractionCategoryTypeDef, ImageExtractionCategoryOutputTypeDef
]
ImageStandardGenerativeFieldUnionTypeDef = Union[
    ImageStandardGenerativeFieldTypeDef, ImageStandardGenerativeFieldOutputTypeDef
]


class ListBlueprintsRequestListBlueprintsPaginateTypeDef(TypedDict):
    blueprintArn: NotRequired[str]
    resourceOwner: NotRequired[ResourceOwnerType]
    blueprintStageFilter: NotRequired[BlueprintStageFilterType]
    projectFilter: NotRequired[DataAutomationProjectFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDataAutomationProjectsRequestListDataAutomationProjectsPaginateTypeDef(TypedDict):
    projectStageFilter: NotRequired[DataAutomationProjectStageFilterType]
    blueprintFilter: NotRequired[BlueprintFilterTypeDef]
    resourceOwner: NotRequired[ResourceOwnerType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class VideoStandardExtractionOutputTypeDef(TypedDict):
    category: VideoExtractionCategoryOutputTypeDef
    boundingBox: VideoBoundingBoxTypeDef


VideoExtractionCategoryUnionTypeDef = Union[
    VideoExtractionCategoryTypeDef, VideoExtractionCategoryOutputTypeDef
]
VideoStandardGenerativeFieldUnionTypeDef = Union[
    VideoStandardGenerativeFieldTypeDef, VideoStandardGenerativeFieldOutputTypeDef
]


class AudioStandardOutputConfigurationOutputTypeDef(TypedDict):
    extraction: NotRequired[AudioStandardExtractionOutputTypeDef]
    generativeField: NotRequired[AudioStandardGenerativeFieldOutputTypeDef]


class AudioStandardExtractionTypeDef(TypedDict):
    category: AudioExtractionCategoryUnionTypeDef


class DocumentStandardExtractionTypeDef(TypedDict):
    granularity: DocumentExtractionGranularityUnionTypeDef
    boundingBox: DocumentBoundingBoxTypeDef


class DocumentStandardOutputConfigurationOutputTypeDef(TypedDict):
    extraction: NotRequired[DocumentStandardExtractionOutputTypeDef]
    generativeField: NotRequired[DocumentStandardGenerativeFieldTypeDef]
    outputFormat: NotRequired[DocumentOutputFormatOutputTypeDef]


class DocumentOutputFormatTypeDef(TypedDict):
    textFormat: DocumentOutputTextFormatUnionTypeDef
    additionalFileFormat: DocumentOutputAdditionalFileFormatTypeDef


class OverrideConfigurationTypeDef(TypedDict):
    document: NotRequired[DocumentOverrideConfigurationTypeDef]


class ImageStandardOutputConfigurationOutputTypeDef(TypedDict):
    extraction: NotRequired[ImageStandardExtractionOutputTypeDef]
    generativeField: NotRequired[ImageStandardGenerativeFieldOutputTypeDef]


class ImageStandardExtractionTypeDef(TypedDict):
    category: ImageExtractionCategoryUnionTypeDef
    boundingBox: ImageBoundingBoxTypeDef


class VideoStandardOutputConfigurationOutputTypeDef(TypedDict):
    extraction: NotRequired[VideoStandardExtractionOutputTypeDef]
    generativeField: NotRequired[VideoStandardGenerativeFieldOutputTypeDef]


class VideoStandardExtractionTypeDef(TypedDict):
    category: VideoExtractionCategoryUnionTypeDef
    boundingBox: VideoBoundingBoxTypeDef


AudioStandardExtractionUnionTypeDef = Union[
    AudioStandardExtractionTypeDef, AudioStandardExtractionOutputTypeDef
]
DocumentStandardExtractionUnionTypeDef = Union[
    DocumentStandardExtractionTypeDef, DocumentStandardExtractionOutputTypeDef
]
DocumentOutputFormatUnionTypeDef = Union[
    DocumentOutputFormatTypeDef, DocumentOutputFormatOutputTypeDef
]
ImageStandardExtractionUnionTypeDef = Union[
    ImageStandardExtractionTypeDef, ImageStandardExtractionOutputTypeDef
]


class StandardOutputConfigurationOutputTypeDef(TypedDict):
    document: NotRequired[DocumentStandardOutputConfigurationOutputTypeDef]
    image: NotRequired[ImageStandardOutputConfigurationOutputTypeDef]
    video: NotRequired[VideoStandardOutputConfigurationOutputTypeDef]
    audio: NotRequired[AudioStandardOutputConfigurationOutputTypeDef]


VideoStandardExtractionUnionTypeDef = Union[
    VideoStandardExtractionTypeDef, VideoStandardExtractionOutputTypeDef
]


class AudioStandardOutputConfigurationTypeDef(TypedDict):
    extraction: NotRequired[AudioStandardExtractionUnionTypeDef]
    generativeField: NotRequired[AudioStandardGenerativeFieldUnionTypeDef]


class DocumentStandardOutputConfigurationTypeDef(TypedDict):
    extraction: NotRequired[DocumentStandardExtractionUnionTypeDef]
    generativeField: NotRequired[DocumentStandardGenerativeFieldTypeDef]
    outputFormat: NotRequired[DocumentOutputFormatUnionTypeDef]


class ImageStandardOutputConfigurationTypeDef(TypedDict):
    extraction: NotRequired[ImageStandardExtractionUnionTypeDef]
    generativeField: NotRequired[ImageStandardGenerativeFieldUnionTypeDef]


class DataAutomationProjectTypeDef(TypedDict):
    projectArn: str
    creationTime: datetime
    lastModifiedTime: datetime
    projectName: str
    status: DataAutomationProjectStatusType
    projectStage: NotRequired[DataAutomationProjectStageType]
    projectDescription: NotRequired[str]
    standardOutputConfiguration: NotRequired[StandardOutputConfigurationOutputTypeDef]
    customOutputConfiguration: NotRequired[CustomOutputConfigurationOutputTypeDef]
    overrideConfiguration: NotRequired[OverrideConfigurationTypeDef]
    kmsKeyId: NotRequired[str]
    kmsEncryptionContext: NotRequired[Dict[str, str]]


class VideoStandardOutputConfigurationTypeDef(TypedDict):
    extraction: NotRequired[VideoStandardExtractionUnionTypeDef]
    generativeField: NotRequired[VideoStandardGenerativeFieldUnionTypeDef]


AudioStandardOutputConfigurationUnionTypeDef = Union[
    AudioStandardOutputConfigurationTypeDef, AudioStandardOutputConfigurationOutputTypeDef
]
DocumentStandardOutputConfigurationUnionTypeDef = Union[
    DocumentStandardOutputConfigurationTypeDef, DocumentStandardOutputConfigurationOutputTypeDef
]
ImageStandardOutputConfigurationUnionTypeDef = Union[
    ImageStandardOutputConfigurationTypeDef, ImageStandardOutputConfigurationOutputTypeDef
]


class GetDataAutomationProjectResponseTypeDef(TypedDict):
    project: DataAutomationProjectTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


VideoStandardOutputConfigurationUnionTypeDef = Union[
    VideoStandardOutputConfigurationTypeDef, VideoStandardOutputConfigurationOutputTypeDef
]


class StandardOutputConfigurationTypeDef(TypedDict):
    document: NotRequired[DocumentStandardOutputConfigurationUnionTypeDef]
    image: NotRequired[ImageStandardOutputConfigurationUnionTypeDef]
    video: NotRequired[VideoStandardOutputConfigurationUnionTypeDef]
    audio: NotRequired[AudioStandardOutputConfigurationUnionTypeDef]


class CreateDataAutomationProjectRequestRequestTypeDef(TypedDict):
    projectName: str
    standardOutputConfiguration: StandardOutputConfigurationTypeDef
    projectDescription: NotRequired[str]
    projectStage: NotRequired[DataAutomationProjectStageType]
    customOutputConfiguration: NotRequired[CustomOutputConfigurationTypeDef]
    overrideConfiguration: NotRequired[OverrideConfigurationTypeDef]
    clientToken: NotRequired[str]
    encryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]


class UpdateDataAutomationProjectRequestRequestTypeDef(TypedDict):
    projectArn: str
    standardOutputConfiguration: StandardOutputConfigurationTypeDef
    projectStage: NotRequired[DataAutomationProjectStageType]
    projectDescription: NotRequired[str]
    customOutputConfiguration: NotRequired[CustomOutputConfigurationTypeDef]
    overrideConfiguration: NotRequired[OverrideConfigurationTypeDef]
