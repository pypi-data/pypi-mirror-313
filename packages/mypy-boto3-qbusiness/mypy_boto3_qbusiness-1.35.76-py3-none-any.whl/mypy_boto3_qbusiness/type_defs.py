"""
Type annotations for qbusiness service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qbusiness/type_defs/)

Usage::

    ```python
    from mypy_boto3_qbusiness.type_defs import S3TypeDef

    data: S3TypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.eventstream import EventStream
from botocore.response import StreamingBody

from .literals import (
    ActionPayloadFieldTypeType,
    ApplicationStatusType,
    AttachmentsControlModeType,
    AttachmentStatusType,
    AttributeTypeType,
    AutoSubscriptionStatusType,
    BrowserExtensionType,
    ChatModeType,
    ContentTypeType,
    CreatorModeControlType,
    DataSourceStatusType,
    DataSourceSyncJobStatusType,
    DocumentAttributeBoostingLevelType,
    DocumentEnrichmentConditionOperatorType,
    DocumentStatusType,
    ErrorCodeType,
    GroupStatusType,
    IdentityTypeType,
    ImageExtractionStatusType,
    IndexStatusType,
    IndexTypeType,
    MemberRelationType,
    MembershipTypeType,
    MessageTypeType,
    MessageUsefulnessReasonType,
    MessageUsefulnessType,
    NumberAttributeBoostingTypeType,
    PersonalizationControlModeType,
    PluginBuildStatusType,
    PluginStateType,
    PluginTypeCategoryType,
    PluginTypeType,
    QAppsControlModeType,
    ReadAccessTypeType,
    ResponseScopeType,
    RetrieverStatusType,
    RetrieverTypeType,
    RuleTypeType,
    ScoreConfidenceType,
    StatusType,
    StringAttributeValueBoostingLevelType,
    SubscriptionTypeType,
    WebExperienceSamplePromptsControlModeType,
    WebExperienceStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "APISchemaTypeDef",
    "AccessConfigurationTypeDef",
    "AccessControlTypeDef",
    "ActionConfigurationOutputTypeDef",
    "ActionConfigurationTypeDef",
    "ActionConfigurationUnionTypeDef",
    "ActionExecutionEventTypeDef",
    "ActionExecutionOutputTypeDef",
    "ActionExecutionPayloadFieldOutputTypeDef",
    "ActionExecutionPayloadFieldTypeDef",
    "ActionExecutionPayloadFieldUnionTypeDef",
    "ActionExecutionTypeDef",
    "ActionFilterConfigurationOutputTypeDef",
    "ActionFilterConfigurationTypeDef",
    "ActionFilterConfigurationUnionTypeDef",
    "ActionReviewEventTypeDef",
    "ActionReviewPayloadFieldAllowedValueTypeDef",
    "ActionReviewPayloadFieldTypeDef",
    "ActionReviewTypeDef",
    "ActionSummaryTypeDef",
    "ApplicationTypeDef",
    "AppliedAttachmentsConfigurationTypeDef",
    "AppliedCreatorModeConfigurationTypeDef",
    "AssociatePermissionRequestRequestTypeDef",
    "AssociatePermissionResponseTypeDef",
    "AttachmentInputEventTypeDef",
    "AttachmentInputTypeDef",
    "AttachmentOutputTypeDef",
    "AttachmentTypeDef",
    "AttachmentsConfigurationTypeDef",
    "AttributeFilterOutputTypeDef",
    "AttributeFilterPaginatorTypeDef",
    "AttributeFilterTypeDef",
    "AttributeFilterUnionTypeDef",
    "AuthChallengeRequestEventTypeDef",
    "AuthChallengeRequestTypeDef",
    "AuthChallengeResponseEventTypeDef",
    "AuthChallengeResponseTypeDef",
    "AutoSubscriptionConfigurationTypeDef",
    "BasicAuthConfigurationTypeDef",
    "BatchDeleteDocumentRequestRequestTypeDef",
    "BatchDeleteDocumentResponseTypeDef",
    "BatchPutDocumentRequestRequestTypeDef",
    "BatchPutDocumentResponseTypeDef",
    "BlobTypeDef",
    "BlockedPhrasesConfigurationTypeDef",
    "BlockedPhrasesConfigurationUpdateTypeDef",
    "BrowserExtensionConfigurationOutputTypeDef",
    "BrowserExtensionConfigurationTypeDef",
    "ChatInputRequestTypeDef",
    "ChatInputStreamTypeDef",
    "ChatModeConfigurationTypeDef",
    "ChatOutputStreamTypeDef",
    "ChatOutputTypeDef",
    "ChatSyncInputRequestTypeDef",
    "ChatSyncOutputTypeDef",
    "ConfigurationEventTypeDef",
    "ContentBlockerRuleTypeDef",
    "ContentRetrievalRuleOutputTypeDef",
    "ContentRetrievalRuleTypeDef",
    "ContentRetrievalRuleUnionTypeDef",
    "ContentSourceTypeDef",
    "ConversationSourceTypeDef",
    "ConversationTypeDef",
    "CopyFromSourceTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "CreateApplicationResponseTypeDef",
    "CreateDataAccessorRequestRequestTypeDef",
    "CreateDataAccessorResponseTypeDef",
    "CreateDataSourceRequestRequestTypeDef",
    "CreateDataSourceResponseTypeDef",
    "CreateIndexRequestRequestTypeDef",
    "CreateIndexResponseTypeDef",
    "CreatePluginRequestRequestTypeDef",
    "CreatePluginResponseTypeDef",
    "CreateRetrieverRequestRequestTypeDef",
    "CreateRetrieverResponseTypeDef",
    "CreateUserRequestRequestTypeDef",
    "CreateWebExperienceRequestRequestTypeDef",
    "CreateWebExperienceResponseTypeDef",
    "CreatorModeConfigurationTypeDef",
    "CustomPluginConfigurationTypeDef",
    "CustomizationConfigurationTypeDef",
    "DataAccessorTypeDef",
    "DataSourceSyncJobMetricsTypeDef",
    "DataSourceSyncJobTypeDef",
    "DataSourceTypeDef",
    "DataSourceVpcConfigurationOutputTypeDef",
    "DataSourceVpcConfigurationTypeDef",
    "DateAttributeBoostingConfigurationTypeDef",
    "DeleteApplicationRequestRequestTypeDef",
    "DeleteChatControlsConfigurationRequestRequestTypeDef",
    "DeleteConversationRequestRequestTypeDef",
    "DeleteDataAccessorRequestRequestTypeDef",
    "DeleteDataSourceRequestRequestTypeDef",
    "DeleteDocumentTypeDef",
    "DeleteGroupRequestRequestTypeDef",
    "DeleteIndexRequestRequestTypeDef",
    "DeletePluginRequestRequestTypeDef",
    "DeleteRetrieverRequestRequestTypeDef",
    "DeleteUserRequestRequestTypeDef",
    "DeleteWebExperienceRequestRequestTypeDef",
    "DisassociatePermissionRequestRequestTypeDef",
    "DocumentAttributeBoostingConfigurationOutputTypeDef",
    "DocumentAttributeBoostingConfigurationTypeDef",
    "DocumentAttributeBoostingConfigurationUnionTypeDef",
    "DocumentAttributeConditionOutputTypeDef",
    "DocumentAttributeConditionTypeDef",
    "DocumentAttributeConditionUnionTypeDef",
    "DocumentAttributeConfigurationTypeDef",
    "DocumentAttributeOutputTypeDef",
    "DocumentAttributeTargetOutputTypeDef",
    "DocumentAttributeTargetTypeDef",
    "DocumentAttributeTargetUnionTypeDef",
    "DocumentAttributeTypeDef",
    "DocumentAttributeUnionTypeDef",
    "DocumentAttributeValueOutputTypeDef",
    "DocumentAttributeValueTypeDef",
    "DocumentAttributeValueUnionTypeDef",
    "DocumentContentTypeDef",
    "DocumentDetailsTypeDef",
    "DocumentEnrichmentConfigurationOutputTypeDef",
    "DocumentEnrichmentConfigurationTypeDef",
    "DocumentEnrichmentConfigurationUnionTypeDef",
    "DocumentTypeDef",
    "EligibleDataSourceTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EncryptionConfigurationTypeDef",
    "ErrorDetailTypeDef",
    "FailedAttachmentEventTypeDef",
    "FailedDocumentTypeDef",
    "GetApplicationRequestRequestTypeDef",
    "GetApplicationResponseTypeDef",
    "GetChatControlsConfigurationRequestGetChatControlsConfigurationPaginateTypeDef",
    "GetChatControlsConfigurationRequestRequestTypeDef",
    "GetChatControlsConfigurationResponseTypeDef",
    "GetDataAccessorRequestRequestTypeDef",
    "GetDataAccessorResponseTypeDef",
    "GetDataSourceRequestRequestTypeDef",
    "GetDataSourceResponseTypeDef",
    "GetGroupRequestRequestTypeDef",
    "GetGroupResponseTypeDef",
    "GetIndexRequestRequestTypeDef",
    "GetIndexResponseTypeDef",
    "GetMediaRequestRequestTypeDef",
    "GetMediaResponseTypeDef",
    "GetPluginRequestRequestTypeDef",
    "GetPluginResponseTypeDef",
    "GetPolicyRequestRequestTypeDef",
    "GetPolicyResponseTypeDef",
    "GetRetrieverRequestRequestTypeDef",
    "GetRetrieverResponseTypeDef",
    "GetUserRequestRequestTypeDef",
    "GetUserResponseTypeDef",
    "GetWebExperienceRequestRequestTypeDef",
    "GetWebExperienceResponseTypeDef",
    "GroupMembersTypeDef",
    "GroupStatusDetailTypeDef",
    "GroupSummaryTypeDef",
    "HookConfigurationOutputTypeDef",
    "HookConfigurationTypeDef",
    "HookConfigurationUnionTypeDef",
    "IdcAuthConfigurationTypeDef",
    "IdentityProviderConfigurationTypeDef",
    "ImageExtractionConfigurationTypeDef",
    "IndexCapacityConfigurationTypeDef",
    "IndexStatisticsTypeDef",
    "IndexTypeDef",
    "InlineDocumentEnrichmentConfigurationOutputTypeDef",
    "InlineDocumentEnrichmentConfigurationTypeDef",
    "InlineDocumentEnrichmentConfigurationUnionTypeDef",
    "KendraIndexConfigurationTypeDef",
    "ListApplicationsRequestListApplicationsPaginateTypeDef",
    "ListApplicationsRequestRequestTypeDef",
    "ListApplicationsResponseTypeDef",
    "ListAttachmentsRequestListAttachmentsPaginateTypeDef",
    "ListAttachmentsRequestRequestTypeDef",
    "ListAttachmentsResponseTypeDef",
    "ListConversationsRequestListConversationsPaginateTypeDef",
    "ListConversationsRequestRequestTypeDef",
    "ListConversationsResponseTypeDef",
    "ListDataAccessorsRequestListDataAccessorsPaginateTypeDef",
    "ListDataAccessorsRequestRequestTypeDef",
    "ListDataAccessorsResponseTypeDef",
    "ListDataSourceSyncJobsRequestListDataSourceSyncJobsPaginateTypeDef",
    "ListDataSourceSyncJobsRequestRequestTypeDef",
    "ListDataSourceSyncJobsResponseTypeDef",
    "ListDataSourcesRequestListDataSourcesPaginateTypeDef",
    "ListDataSourcesRequestRequestTypeDef",
    "ListDataSourcesResponseTypeDef",
    "ListDocumentsRequestListDocumentsPaginateTypeDef",
    "ListDocumentsRequestRequestTypeDef",
    "ListDocumentsResponseTypeDef",
    "ListGroupsRequestListGroupsPaginateTypeDef",
    "ListGroupsRequestRequestTypeDef",
    "ListGroupsResponseTypeDef",
    "ListIndicesRequestListIndicesPaginateTypeDef",
    "ListIndicesRequestRequestTypeDef",
    "ListIndicesResponseTypeDef",
    "ListMessagesRequestListMessagesPaginateTypeDef",
    "ListMessagesRequestRequestTypeDef",
    "ListMessagesResponseTypeDef",
    "ListPluginActionsRequestListPluginActionsPaginateTypeDef",
    "ListPluginActionsRequestRequestTypeDef",
    "ListPluginActionsResponseTypeDef",
    "ListPluginTypeActionsRequestListPluginTypeActionsPaginateTypeDef",
    "ListPluginTypeActionsRequestRequestTypeDef",
    "ListPluginTypeActionsResponseTypeDef",
    "ListPluginTypeMetadataRequestListPluginTypeMetadataPaginateTypeDef",
    "ListPluginTypeMetadataRequestRequestTypeDef",
    "ListPluginTypeMetadataResponseTypeDef",
    "ListPluginsRequestListPluginsPaginateTypeDef",
    "ListPluginsRequestRequestTypeDef",
    "ListPluginsResponseTypeDef",
    "ListRetrieversRequestListRetrieversPaginateTypeDef",
    "ListRetrieversRequestRequestTypeDef",
    "ListRetrieversResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListWebExperiencesRequestListWebExperiencesPaginateTypeDef",
    "ListWebExperiencesRequestRequestTypeDef",
    "ListWebExperiencesResponseTypeDef",
    "MediaExtractionConfigurationTypeDef",
    "MemberGroupTypeDef",
    "MemberUserTypeDef",
    "MessageTypeDef",
    "MessageUsefulnessFeedbackTypeDef",
    "MetadataEventTypeDef",
    "NativeIndexConfigurationOutputTypeDef",
    "NativeIndexConfigurationTypeDef",
    "NativeIndexConfigurationUnionTypeDef",
    "NumberAttributeBoostingConfigurationTypeDef",
    "OAuth2ClientCredentialConfigurationTypeDef",
    "OpenIDConnectProviderConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "PersonalizationConfigurationTypeDef",
    "PluginAuthConfigurationOutputTypeDef",
    "PluginAuthConfigurationTypeDef",
    "PluginConfigurationTypeDef",
    "PluginTypeDef",
    "PluginTypeMetadataSummaryTypeDef",
    "PrincipalGroupTypeDef",
    "PrincipalTypeDef",
    "PrincipalUserTypeDef",
    "PutFeedbackRequestRequestTypeDef",
    "PutGroupRequestRequestTypeDef",
    "QAppsConfigurationTypeDef",
    "QuickSightConfigurationTypeDef",
    "RelevantContentTypeDef",
    "ResponseMetadataTypeDef",
    "RetrieverConfigurationOutputTypeDef",
    "RetrieverConfigurationTypeDef",
    "RetrieverContentSourceTypeDef",
    "RetrieverTypeDef",
    "RuleConfigurationOutputTypeDef",
    "RuleConfigurationTypeDef",
    "RuleConfigurationUnionTypeDef",
    "RuleOutputTypeDef",
    "RuleTypeDef",
    "RuleUnionTypeDef",
    "S3TypeDef",
    "SamlConfigurationTypeDef",
    "SamlProviderConfigurationTypeDef",
    "ScoreAttributesTypeDef",
    "SearchRelevantContentRequestRequestTypeDef",
    "SearchRelevantContentRequestSearchRelevantContentPaginateTypeDef",
    "SearchRelevantContentResponseTypeDef",
    "SnippetExcerptTypeDef",
    "SourceAttributionTypeDef",
    "StartDataSourceSyncJobRequestRequestTypeDef",
    "StartDataSourceSyncJobResponseTypeDef",
    "StopDataSourceSyncJobRequestRequestTypeDef",
    "StringAttributeBoostingConfigurationOutputTypeDef",
    "StringAttributeBoostingConfigurationTypeDef",
    "StringAttributeBoostingConfigurationUnionTypeDef",
    "StringListAttributeBoostingConfigurationTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TextDocumentStatisticsTypeDef",
    "TextInputEventTypeDef",
    "TextOutputEventTypeDef",
    "TextSegmentTypeDef",
    "TimestampTypeDef",
    "TopicConfigurationOutputTypeDef",
    "TopicConfigurationTypeDef",
    "TopicConfigurationUnionTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateApplicationRequestRequestTypeDef",
    "UpdateChatControlsConfigurationRequestRequestTypeDef",
    "UpdateDataAccessorRequestRequestTypeDef",
    "UpdateDataSourceRequestRequestTypeDef",
    "UpdateIndexRequestRequestTypeDef",
    "UpdatePluginRequestRequestTypeDef",
    "UpdateRetrieverRequestRequestTypeDef",
    "UpdateUserRequestRequestTypeDef",
    "UpdateUserResponseTypeDef",
    "UpdateWebExperienceRequestRequestTypeDef",
    "UserAliasTypeDef",
    "UsersAndGroupsOutputTypeDef",
    "UsersAndGroupsTypeDef",
    "UsersAndGroupsUnionTypeDef",
    "WebExperienceAuthConfigurationTypeDef",
    "WebExperienceTypeDef",
)


class S3TypeDef(TypedDict):
    bucket: str
    key: str


class ActionExecutionPayloadFieldOutputTypeDef(TypedDict):
    value: Dict[str, Any]


class ActionExecutionPayloadFieldTypeDef(TypedDict):
    value: Mapping[str, Any]


class ActionReviewPayloadFieldAllowedValueTypeDef(TypedDict):
    value: NotRequired[Dict[str, Any]]
    displayValue: NotRequired[Dict[str, Any]]


class ActionSummaryTypeDef(TypedDict):
    actionIdentifier: NotRequired[str]
    displayName: NotRequired[str]
    instructionExample: NotRequired[str]
    description: NotRequired[str]


class QuickSightConfigurationTypeDef(TypedDict):
    clientNamespace: str


class AppliedAttachmentsConfigurationTypeDef(TypedDict):
    attachmentsControlMode: NotRequired[AttachmentsControlModeType]


class AppliedCreatorModeConfigurationTypeDef(TypedDict):
    creatorModeControl: CreatorModeControlType


class AssociatePermissionRequestRequestTypeDef(TypedDict):
    applicationId: str
    statementId: str
    actions: Sequence[str]
    principal: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class ErrorDetailTypeDef(TypedDict):
    errorMessage: NotRequired[str]
    errorCode: NotRequired[ErrorCodeType]


class AttachmentsConfigurationTypeDef(TypedDict):
    attachmentsControlMode: AttachmentsControlModeType


class AuthChallengeRequestEventTypeDef(TypedDict):
    authorizationUrl: str


class AuthChallengeRequestTypeDef(TypedDict):
    authorizationUrl: str


class AuthChallengeResponseEventTypeDef(TypedDict):
    responseMap: Mapping[str, str]


class AuthChallengeResponseTypeDef(TypedDict):
    responseMap: Mapping[str, str]


class AutoSubscriptionConfigurationTypeDef(TypedDict):
    autoSubscribe: AutoSubscriptionStatusType
    defaultSubscriptionType: NotRequired[SubscriptionTypeType]


class BasicAuthConfigurationTypeDef(TypedDict):
    secretArn: str
    roleArn: str


class DeleteDocumentTypeDef(TypedDict):
    documentId: str


class BlockedPhrasesConfigurationTypeDef(TypedDict):
    blockedPhrases: NotRequired[List[str]]
    systemMessageOverride: NotRequired[str]


class BlockedPhrasesConfigurationUpdateTypeDef(TypedDict):
    blockedPhrasesToCreateOrUpdate: NotRequired[Sequence[str]]
    blockedPhrasesToDelete: NotRequired[Sequence[str]]
    systemMessageOverride: NotRequired[str]


class BrowserExtensionConfigurationOutputTypeDef(TypedDict):
    enabledBrowserExtensions: List[BrowserExtensionType]


class BrowserExtensionConfigurationTypeDef(TypedDict):
    enabledBrowserExtensions: Sequence[BrowserExtensionType]


class TextInputEventTypeDef(TypedDict):
    userMessage: str


class PluginConfigurationTypeDef(TypedDict):
    pluginId: str


class TextOutputEventTypeDef(TypedDict):
    conversationId: NotRequired[str]
    userMessageId: NotRequired[str]
    systemMessageId: NotRequired[str]
    systemMessage: NotRequired[str]


class ContentBlockerRuleTypeDef(TypedDict):
    systemMessageOverride: NotRequired[str]


class EligibleDataSourceTypeDef(TypedDict):
    indexId: NotRequired[str]
    dataSourceId: NotRequired[str]


class RetrieverContentSourceTypeDef(TypedDict):
    retrieverId: str


class ConversationSourceTypeDef(TypedDict):
    conversationId: str
    attachmentId: str


class ConversationTypeDef(TypedDict):
    conversationId: NotRequired[str]
    title: NotRequired[str]
    startTime: NotRequired[datetime]


class EncryptionConfigurationTypeDef(TypedDict):
    kmsKeyId: NotRequired[str]


class PersonalizationConfigurationTypeDef(TypedDict):
    personalizationControlMode: PersonalizationControlModeType


class QAppsConfigurationTypeDef(TypedDict):
    qAppsControlMode: QAppsControlModeType


class TagTypeDef(TypedDict):
    key: str
    value: str


class DataSourceVpcConfigurationTypeDef(TypedDict):
    subnetIds: Sequence[str]
    securityGroupIds: Sequence[str]


class IndexCapacityConfigurationTypeDef(TypedDict):
    units: NotRequired[int]


class UserAliasTypeDef(TypedDict):
    userId: str
    indexId: NotRequired[str]
    dataSourceId: NotRequired[str]


class CustomizationConfigurationTypeDef(TypedDict):
    customCSSUrl: NotRequired[str]
    logoUrl: NotRequired[str]
    fontUrl: NotRequired[str]
    faviconUrl: NotRequired[str]


class CreatorModeConfigurationTypeDef(TypedDict):
    creatorModeControl: CreatorModeControlType


class DataAccessorTypeDef(TypedDict):
    displayName: NotRequired[str]
    dataAccessorId: NotRequired[str]
    dataAccessorArn: NotRequired[str]
    idcApplicationArn: NotRequired[str]
    principal: NotRequired[str]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]


class DataSourceSyncJobMetricsTypeDef(TypedDict):
    documentsAdded: NotRequired[str]
    documentsModified: NotRequired[str]
    documentsDeleted: NotRequired[str]
    documentsFailed: NotRequired[str]
    documentsScanned: NotRequired[str]


DataSourceTypeDef = TypedDict(
    "DataSourceTypeDef",
    {
        "displayName": NotRequired[str],
        "dataSourceId": NotRequired[str],
        "type": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
        "status": NotRequired[DataSourceStatusType],
    },
)


class DataSourceVpcConfigurationOutputTypeDef(TypedDict):
    subnetIds: List[str]
    securityGroupIds: List[str]


class DateAttributeBoostingConfigurationTypeDef(TypedDict):
    boostingLevel: DocumentAttributeBoostingLevelType
    boostingDurationInSeconds: NotRequired[int]


class DeleteApplicationRequestRequestTypeDef(TypedDict):
    applicationId: str


class DeleteChatControlsConfigurationRequestRequestTypeDef(TypedDict):
    applicationId: str


class DeleteConversationRequestRequestTypeDef(TypedDict):
    conversationId: str
    applicationId: str
    userId: NotRequired[str]


class DeleteDataAccessorRequestRequestTypeDef(TypedDict):
    applicationId: str
    dataAccessorId: str


class DeleteDataSourceRequestRequestTypeDef(TypedDict):
    applicationId: str
    indexId: str
    dataSourceId: str


class DeleteGroupRequestRequestTypeDef(TypedDict):
    applicationId: str
    indexId: str
    groupName: str
    dataSourceId: NotRequired[str]


class DeleteIndexRequestRequestTypeDef(TypedDict):
    applicationId: str
    indexId: str


class DeletePluginRequestRequestTypeDef(TypedDict):
    applicationId: str
    pluginId: str


class DeleteRetrieverRequestRequestTypeDef(TypedDict):
    applicationId: str
    retrieverId: str


class DeleteUserRequestRequestTypeDef(TypedDict):
    applicationId: str
    userId: str


class DeleteWebExperienceRequestRequestTypeDef(TypedDict):
    applicationId: str
    webExperienceId: str


class DisassociatePermissionRequestRequestTypeDef(TypedDict):
    applicationId: str
    statementId: str


class NumberAttributeBoostingConfigurationTypeDef(TypedDict):
    boostingLevel: DocumentAttributeBoostingLevelType
    boostingType: NotRequired[NumberAttributeBoostingTypeType]


class StringAttributeBoostingConfigurationOutputTypeDef(TypedDict):
    boostingLevel: DocumentAttributeBoostingLevelType
    attributeValueBoosting: NotRequired[Dict[str, StringAttributeValueBoostingLevelType]]


class StringListAttributeBoostingConfigurationTypeDef(TypedDict):
    boostingLevel: DocumentAttributeBoostingLevelType


class DocumentAttributeValueOutputTypeDef(TypedDict):
    stringValue: NotRequired[str]
    stringListValue: NotRequired[List[str]]
    longValue: NotRequired[int]
    dateValue: NotRequired[datetime]


DocumentAttributeConfigurationTypeDef = TypedDict(
    "DocumentAttributeConfigurationTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[AttributeTypeType],
        "search": NotRequired[StatusType],
    },
)
TimestampTypeDef = Union[datetime, str]


class GetApplicationRequestRequestTypeDef(TypedDict):
    applicationId: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class GetChatControlsConfigurationRequestRequestTypeDef(TypedDict):
    applicationId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class GetDataAccessorRequestRequestTypeDef(TypedDict):
    applicationId: str
    dataAccessorId: str


class GetDataSourceRequestRequestTypeDef(TypedDict):
    applicationId: str
    indexId: str
    dataSourceId: str


class GetGroupRequestRequestTypeDef(TypedDict):
    applicationId: str
    indexId: str
    groupName: str
    dataSourceId: NotRequired[str]


class GetIndexRequestRequestTypeDef(TypedDict):
    applicationId: str
    indexId: str


class GetMediaRequestRequestTypeDef(TypedDict):
    applicationId: str
    conversationId: str
    messageId: str
    mediaId: str


class GetPluginRequestRequestTypeDef(TypedDict):
    applicationId: str
    pluginId: str


class GetPolicyRequestRequestTypeDef(TypedDict):
    applicationId: str


class GetRetrieverRequestRequestTypeDef(TypedDict):
    applicationId: str
    retrieverId: str


class GetUserRequestRequestTypeDef(TypedDict):
    applicationId: str
    userId: str


class GetWebExperienceRequestRequestTypeDef(TypedDict):
    applicationId: str
    webExperienceId: str


MemberGroupTypeDef = TypedDict(
    "MemberGroupTypeDef",
    {
        "groupName": str,
        "type": NotRequired[MembershipTypeType],
    },
)
MemberUserTypeDef = TypedDict(
    "MemberUserTypeDef",
    {
        "userId": str,
        "type": NotRequired[MembershipTypeType],
    },
)


class GroupSummaryTypeDef(TypedDict):
    groupName: NotRequired[str]


class IdcAuthConfigurationTypeDef(TypedDict):
    idcApplicationArn: str
    roleArn: str


class OpenIDConnectProviderConfigurationTypeDef(TypedDict):
    secretsArn: str
    secretsRole: str


class SamlProviderConfigurationTypeDef(TypedDict):
    authenticationUrl: str


class ImageExtractionConfigurationTypeDef(TypedDict):
    imageExtractionStatus: ImageExtractionStatusType


class TextDocumentStatisticsTypeDef(TypedDict):
    indexedTextBytes: NotRequired[int]
    indexedTextDocumentCount: NotRequired[int]


class IndexTypeDef(TypedDict):
    displayName: NotRequired[str]
    indexId: NotRequired[str]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]
    status: NotRequired[IndexStatusType]


class KendraIndexConfigurationTypeDef(TypedDict):
    indexId: str


class ListApplicationsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListAttachmentsRequestRequestTypeDef(TypedDict):
    applicationId: str
    conversationId: NotRequired[str]
    userId: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListConversationsRequestRequestTypeDef(TypedDict):
    applicationId: str
    userId: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListDataAccessorsRequestRequestTypeDef(TypedDict):
    applicationId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListDataSourcesRequestRequestTypeDef(TypedDict):
    applicationId: str
    indexId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListDocumentsRequestRequestTypeDef(TypedDict):
    applicationId: str
    indexId: str
    dataSourceIds: NotRequired[Sequence[str]]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListIndicesRequestRequestTypeDef(TypedDict):
    applicationId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListMessagesRequestRequestTypeDef(TypedDict):
    conversationId: str
    applicationId: str
    userId: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListPluginActionsRequestRequestTypeDef(TypedDict):
    applicationId: str
    pluginId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListPluginTypeActionsRequestRequestTypeDef(TypedDict):
    pluginType: PluginTypeType
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListPluginTypeMetadataRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


PluginTypeMetadataSummaryTypeDef = TypedDict(
    "PluginTypeMetadataSummaryTypeDef",
    {
        "type": NotRequired[PluginTypeType],
        "category": NotRequired[PluginTypeCategoryType],
        "description": NotRequired[str],
    },
)


class ListPluginsRequestRequestTypeDef(TypedDict):
    applicationId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


PluginTypeDef = TypedDict(
    "PluginTypeDef",
    {
        "pluginId": NotRequired[str],
        "displayName": NotRequired[str],
        "type": NotRequired[PluginTypeType],
        "serverUrl": NotRequired[str],
        "state": NotRequired[PluginStateType],
        "buildStatus": NotRequired[PluginBuildStatusType],
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
    },
)


class ListRetrieversRequestRequestTypeDef(TypedDict):
    applicationId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


RetrieverTypeDef = TypedDict(
    "RetrieverTypeDef",
    {
        "applicationId": NotRequired[str],
        "retrieverId": NotRequired[str],
        "type": NotRequired[RetrieverTypeType],
        "status": NotRequired[RetrieverStatusType],
        "displayName": NotRequired[str],
    },
)


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceARN: str


class ListWebExperiencesRequestRequestTypeDef(TypedDict):
    applicationId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class WebExperienceTypeDef(TypedDict):
    webExperienceId: NotRequired[str]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]
    defaultEndpoint: NotRequired[str]
    status: NotRequired[WebExperienceStatusType]


class OAuth2ClientCredentialConfigurationTypeDef(TypedDict):
    secretArn: str
    roleArn: str
    authorizationUrl: NotRequired[str]
    tokenUrl: NotRequired[str]


class PrincipalGroupTypeDef(TypedDict):
    access: ReadAccessTypeType
    name: NotRequired[str]
    membershipType: NotRequired[MembershipTypeType]


PrincipalUserTypeDef = TypedDict(
    "PrincipalUserTypeDef",
    {
        "access": ReadAccessTypeType,
        "id": NotRequired[str],
        "membershipType": NotRequired[MembershipTypeType],
    },
)


class ScoreAttributesTypeDef(TypedDict):
    scoreConfidence: NotRequired[ScoreConfidenceType]


class UsersAndGroupsOutputTypeDef(TypedDict):
    userIds: NotRequired[List[str]]
    userGroups: NotRequired[List[str]]


class SamlConfigurationTypeDef(TypedDict):
    metadataXML: str
    roleArn: str
    userIdAttribute: str
    userGroupAttribute: NotRequired[str]


class SnippetExcerptTypeDef(TypedDict):
    text: NotRequired[str]


class StartDataSourceSyncJobRequestRequestTypeDef(TypedDict):
    dataSourceId: str
    applicationId: str
    indexId: str


class StopDataSourceSyncJobRequestRequestTypeDef(TypedDict):
    dataSourceId: str
    applicationId: str
    indexId: str


class StringAttributeBoostingConfigurationTypeDef(TypedDict):
    boostingLevel: DocumentAttributeBoostingLevelType
    attributeValueBoosting: NotRequired[Mapping[str, StringAttributeValueBoostingLevelType]]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceARN: str
    tagKeys: Sequence[str]


class UsersAndGroupsTypeDef(TypedDict):
    userIds: NotRequired[Sequence[str]]
    userGroups: NotRequired[Sequence[str]]


class APISchemaTypeDef(TypedDict):
    payload: NotRequired[str]
    s3: NotRequired[S3TypeDef]


class ActionExecutionOutputTypeDef(TypedDict):
    pluginId: str
    payload: Dict[str, ActionExecutionPayloadFieldOutputTypeDef]
    payloadFieldNameSeparator: str


ActionExecutionPayloadFieldUnionTypeDef = Union[
    ActionExecutionPayloadFieldTypeDef, ActionExecutionPayloadFieldOutputTypeDef
]
ActionReviewPayloadFieldTypeDef = TypedDict(
    "ActionReviewPayloadFieldTypeDef",
    {
        "displayName": NotRequired[str],
        "displayOrder": NotRequired[int],
        "displayDescription": NotRequired[str],
        "type": NotRequired[ActionPayloadFieldTypeType],
        "value": NotRequired[Dict[str, Any]],
        "allowedValues": NotRequired[List[ActionReviewPayloadFieldAllowedValueTypeDef]],
        "allowedFormat": NotRequired[str],
        "arrayItemJsonSchema": NotRequired[Dict[str, Any]],
        "required": NotRequired[bool],
    },
)


class ApplicationTypeDef(TypedDict):
    displayName: NotRequired[str]
    applicationId: NotRequired[str]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]
    status: NotRequired[ApplicationStatusType]
    identityType: NotRequired[IdentityTypeType]
    quickSightConfiguration: NotRequired[QuickSightConfigurationTypeDef]


class AssociatePermissionResponseTypeDef(TypedDict):
    statement: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateApplicationResponseTypeDef(TypedDict):
    applicationId: str
    applicationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDataAccessorResponseTypeDef(TypedDict):
    dataAccessorId: str
    idcApplicationArn: str
    dataAccessorArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDataSourceResponseTypeDef(TypedDict):
    dataSourceId: str
    dataSourceArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateIndexResponseTypeDef(TypedDict):
    indexId: str
    indexArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePluginResponseTypeDef(TypedDict):
    pluginId: str
    pluginArn: str
    buildStatus: PluginBuildStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRetrieverResponseTypeDef(TypedDict):
    retrieverId: str
    retrieverArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateWebExperienceResponseTypeDef(TypedDict):
    webExperienceId: str
    webExperienceArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetMediaResponseTypeDef(TypedDict):
    mediaBytes: bytes
    mediaMimeType: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetPolicyResponseTypeDef(TypedDict):
    policy: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListPluginActionsResponseTypeDef(TypedDict):
    items: List[ActionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListPluginTypeActionsResponseTypeDef(TypedDict):
    items: List[ActionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class StartDataSourceSyncJobResponseTypeDef(TypedDict):
    executionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DocumentContentTypeDef(TypedDict):
    blob: NotRequired[BlobTypeDef]
    s3: NotRequired[S3TypeDef]


class AttachmentOutputTypeDef(TypedDict):
    name: NotRequired[str]
    status: NotRequired[AttachmentStatusType]
    error: NotRequired[ErrorDetailTypeDef]
    attachmentId: NotRequired[str]
    conversationId: NotRequired[str]


class DocumentDetailsTypeDef(TypedDict):
    documentId: NotRequired[str]
    status: NotRequired[DocumentStatusType]
    error: NotRequired[ErrorDetailTypeDef]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]


FailedDocumentTypeDef = TypedDict(
    "FailedDocumentTypeDef",
    {
        "id": NotRequired[str],
        "error": NotRequired[ErrorDetailTypeDef],
        "dataSourceId": NotRequired[str],
    },
)


class GroupStatusDetailTypeDef(TypedDict):
    status: NotRequired[GroupStatusType]
    lastUpdatedAt: NotRequired[datetime]
    errorDetail: NotRequired[ErrorDetailTypeDef]


class BatchDeleteDocumentRequestRequestTypeDef(TypedDict):
    applicationId: str
    indexId: str
    documents: Sequence[DeleteDocumentTypeDef]
    dataSourceSyncId: NotRequired[str]


class ChatModeConfigurationTypeDef(TypedDict):
    pluginConfiguration: NotRequired[PluginConfigurationTypeDef]


class ContentRetrievalRuleOutputTypeDef(TypedDict):
    eligibleDataSources: NotRequired[List[EligibleDataSourceTypeDef]]


class ContentRetrievalRuleTypeDef(TypedDict):
    eligibleDataSources: NotRequired[Sequence[EligibleDataSourceTypeDef]]


class ContentSourceTypeDef(TypedDict):
    retriever: NotRequired[RetrieverContentSourceTypeDef]


class CopyFromSourceTypeDef(TypedDict):
    conversation: NotRequired[ConversationSourceTypeDef]


class ListConversationsResponseTypeDef(TypedDict):
    conversations: List[ConversationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetApplicationResponseTypeDef(TypedDict):
    displayName: str
    applicationId: str
    applicationArn: str
    identityType: IdentityTypeType
    iamIdentityProviderArn: str
    identityCenterApplicationArn: str
    roleArn: str
    status: ApplicationStatusType
    description: str
    encryptionConfiguration: EncryptionConfigurationTypeDef
    createdAt: datetime
    updatedAt: datetime
    error: ErrorDetailTypeDef
    attachmentsConfiguration: AppliedAttachmentsConfigurationTypeDef
    qAppsConfiguration: QAppsConfigurationTypeDef
    personalizationConfiguration: PersonalizationConfigurationTypeDef
    autoSubscriptionConfiguration: AutoSubscriptionConfigurationTypeDef
    clientIdsForOIDC: List[str]
    quickSightConfiguration: QuickSightConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateApplicationRequestRequestTypeDef(TypedDict):
    applicationId: str
    identityCenterInstanceArn: NotRequired[str]
    displayName: NotRequired[str]
    description: NotRequired[str]
    roleArn: NotRequired[str]
    attachmentsConfiguration: NotRequired[AttachmentsConfigurationTypeDef]
    qAppsConfiguration: NotRequired[QAppsConfigurationTypeDef]
    personalizationConfiguration: NotRequired[PersonalizationConfigurationTypeDef]
    autoSubscriptionConfiguration: NotRequired[AutoSubscriptionConfigurationTypeDef]


class CreateApplicationRequestRequestTypeDef(TypedDict):
    displayName: str
    roleArn: NotRequired[str]
    identityType: NotRequired[IdentityTypeType]
    iamIdentityProviderArn: NotRequired[str]
    identityCenterInstanceArn: NotRequired[str]
    clientIdsForOIDC: NotRequired[Sequence[str]]
    description: NotRequired[str]
    encryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]
    clientToken: NotRequired[str]
    attachmentsConfiguration: NotRequired[AttachmentsConfigurationTypeDef]
    qAppsConfiguration: NotRequired[QAppsConfigurationTypeDef]
    personalizationConfiguration: NotRequired[PersonalizationConfigurationTypeDef]
    quickSightConfiguration: NotRequired[QuickSightConfigurationTypeDef]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceARN: str
    tags: Sequence[TagTypeDef]


CreateIndexRequestRequestTypeDef = TypedDict(
    "CreateIndexRequestRequestTypeDef",
    {
        "applicationId": str,
        "displayName": str,
        "description": NotRequired[str],
        "type": NotRequired[IndexTypeType],
        "tags": NotRequired[Sequence[TagTypeDef]],
        "capacityConfiguration": NotRequired[IndexCapacityConfigurationTypeDef],
        "clientToken": NotRequired[str],
    },
)


class CreateUserRequestRequestTypeDef(TypedDict):
    applicationId: str
    userId: str
    userAliases: NotRequired[Sequence[UserAliasTypeDef]]
    clientToken: NotRequired[str]


class GetUserResponseTypeDef(TypedDict):
    userAliases: List[UserAliasTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateUserRequestRequestTypeDef(TypedDict):
    applicationId: str
    userId: str
    userAliasesToUpdate: NotRequired[Sequence[UserAliasTypeDef]]
    userAliasesToDelete: NotRequired[Sequence[UserAliasTypeDef]]


class UpdateUserResponseTypeDef(TypedDict):
    userAliasesAdded: List[UserAliasTypeDef]
    userAliasesUpdated: List[UserAliasTypeDef]
    userAliasesDeleted: List[UserAliasTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListDataAccessorsResponseTypeDef(TypedDict):
    dataAccessors: List[DataAccessorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DataSourceSyncJobTypeDef(TypedDict):
    executionId: NotRequired[str]
    startTime: NotRequired[datetime]
    endTime: NotRequired[datetime]
    status: NotRequired[DataSourceSyncJobStatusType]
    error: NotRequired[ErrorDetailTypeDef]
    dataSourceErrorCode: NotRequired[str]
    metrics: NotRequired[DataSourceSyncJobMetricsTypeDef]


class ListDataSourcesResponseTypeDef(TypedDict):
    dataSources: List[DataSourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DocumentAttributeBoostingConfigurationOutputTypeDef(TypedDict):
    numberConfiguration: NotRequired[NumberAttributeBoostingConfigurationTypeDef]
    stringConfiguration: NotRequired[StringAttributeBoostingConfigurationOutputTypeDef]
    dateConfiguration: NotRequired[DateAttributeBoostingConfigurationTypeDef]
    stringListConfiguration: NotRequired[StringListAttributeBoostingConfigurationTypeDef]


DocumentAttributeConditionOutputTypeDef = TypedDict(
    "DocumentAttributeConditionOutputTypeDef",
    {
        "key": str,
        "operator": DocumentEnrichmentConditionOperatorType,
        "value": NotRequired[DocumentAttributeValueOutputTypeDef],
    },
)


class DocumentAttributeOutputTypeDef(TypedDict):
    name: str
    value: DocumentAttributeValueOutputTypeDef


class DocumentAttributeTargetOutputTypeDef(TypedDict):
    key: str
    value: NotRequired[DocumentAttributeValueOutputTypeDef]
    attributeValueOperator: NotRequired[Literal["DELETE"]]


class UpdateIndexRequestRequestTypeDef(TypedDict):
    applicationId: str
    indexId: str
    displayName: NotRequired[str]
    description: NotRequired[str]
    capacityConfiguration: NotRequired[IndexCapacityConfigurationTypeDef]
    documentAttributeConfigurations: NotRequired[Sequence[DocumentAttributeConfigurationTypeDef]]


class DocumentAttributeValueTypeDef(TypedDict):
    stringValue: NotRequired[str]
    stringListValue: NotRequired[Sequence[str]]
    longValue: NotRequired[int]
    dateValue: NotRequired[TimestampTypeDef]


class ListDataSourceSyncJobsRequestRequestTypeDef(TypedDict):
    dataSourceId: str
    applicationId: str
    indexId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    startTime: NotRequired[TimestampTypeDef]
    endTime: NotRequired[TimestampTypeDef]
    statusFilter: NotRequired[DataSourceSyncJobStatusType]


class ListGroupsRequestRequestTypeDef(TypedDict):
    applicationId: str
    indexId: str
    updatedEarlierThan: TimestampTypeDef
    dataSourceId: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class MessageUsefulnessFeedbackTypeDef(TypedDict):
    usefulness: MessageUsefulnessType
    submittedAt: TimestampTypeDef
    reason: NotRequired[MessageUsefulnessReasonType]
    comment: NotRequired[str]


class GetChatControlsConfigurationRequestGetChatControlsConfigurationPaginateTypeDef(TypedDict):
    applicationId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListApplicationsRequestListApplicationsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAttachmentsRequestListAttachmentsPaginateTypeDef(TypedDict):
    applicationId: str
    conversationId: NotRequired[str]
    userId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListConversationsRequestListConversationsPaginateTypeDef(TypedDict):
    applicationId: str
    userId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDataAccessorsRequestListDataAccessorsPaginateTypeDef(TypedDict):
    applicationId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDataSourceSyncJobsRequestListDataSourceSyncJobsPaginateTypeDef(TypedDict):
    dataSourceId: str
    applicationId: str
    indexId: str
    startTime: NotRequired[TimestampTypeDef]
    endTime: NotRequired[TimestampTypeDef]
    statusFilter: NotRequired[DataSourceSyncJobStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDataSourcesRequestListDataSourcesPaginateTypeDef(TypedDict):
    applicationId: str
    indexId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDocumentsRequestListDocumentsPaginateTypeDef(TypedDict):
    applicationId: str
    indexId: str
    dataSourceIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListGroupsRequestListGroupsPaginateTypeDef(TypedDict):
    applicationId: str
    indexId: str
    updatedEarlierThan: TimestampTypeDef
    dataSourceId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListIndicesRequestListIndicesPaginateTypeDef(TypedDict):
    applicationId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMessagesRequestListMessagesPaginateTypeDef(TypedDict):
    conversationId: str
    applicationId: str
    userId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPluginActionsRequestListPluginActionsPaginateTypeDef(TypedDict):
    applicationId: str
    pluginId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPluginTypeActionsRequestListPluginTypeActionsPaginateTypeDef(TypedDict):
    pluginType: PluginTypeType
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPluginTypeMetadataRequestListPluginTypeMetadataPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPluginsRequestListPluginsPaginateTypeDef(TypedDict):
    applicationId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRetrieversRequestListRetrieversPaginateTypeDef(TypedDict):
    applicationId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListWebExperiencesRequestListWebExperiencesPaginateTypeDef(TypedDict):
    applicationId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GroupMembersTypeDef(TypedDict):
    memberGroups: NotRequired[Sequence[MemberGroupTypeDef]]
    memberUsers: NotRequired[Sequence[MemberUserTypeDef]]
    s3PathForGroupMembers: NotRequired[S3TypeDef]


class ListGroupsResponseTypeDef(TypedDict):
    items: List[GroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class IdentityProviderConfigurationTypeDef(TypedDict):
    samlConfiguration: NotRequired[SamlProviderConfigurationTypeDef]
    openIDConnectConfiguration: NotRequired[OpenIDConnectProviderConfigurationTypeDef]


class MediaExtractionConfigurationTypeDef(TypedDict):
    imageExtractionConfiguration: NotRequired[ImageExtractionConfigurationTypeDef]


class IndexStatisticsTypeDef(TypedDict):
    textDocumentStatistics: NotRequired[TextDocumentStatisticsTypeDef]


class ListIndicesResponseTypeDef(TypedDict):
    indices: List[IndexTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListPluginTypeMetadataResponseTypeDef(TypedDict):
    items: List[PluginTypeMetadataSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListPluginsResponseTypeDef(TypedDict):
    plugins: List[PluginTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListRetrieversResponseTypeDef(TypedDict):
    retrievers: List[RetrieverTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListWebExperiencesResponseTypeDef(TypedDict):
    webExperiences: List[WebExperienceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class PluginAuthConfigurationOutputTypeDef(TypedDict):
    basicAuthConfiguration: NotRequired[BasicAuthConfigurationTypeDef]
    oAuth2ClientCredentialConfiguration: NotRequired[OAuth2ClientCredentialConfigurationTypeDef]
    noAuthConfiguration: NotRequired[Dict[str, Any]]
    idcAuthConfiguration: NotRequired[IdcAuthConfigurationTypeDef]


class PluginAuthConfigurationTypeDef(TypedDict):
    basicAuthConfiguration: NotRequired[BasicAuthConfigurationTypeDef]
    oAuth2ClientCredentialConfiguration: NotRequired[OAuth2ClientCredentialConfigurationTypeDef]
    noAuthConfiguration: NotRequired[Mapping[str, Any]]
    idcAuthConfiguration: NotRequired[IdcAuthConfigurationTypeDef]


class PrincipalTypeDef(TypedDict):
    user: NotRequired[PrincipalUserTypeDef]
    group: NotRequired[PrincipalGroupTypeDef]


class WebExperienceAuthConfigurationTypeDef(TypedDict):
    samlConfiguration: NotRequired[SamlConfigurationTypeDef]


class TextSegmentTypeDef(TypedDict):
    beginOffset: NotRequired[int]
    endOffset: NotRequired[int]
    snippetExcerpt: NotRequired[SnippetExcerptTypeDef]
    mediaId: NotRequired[str]
    mediaMimeType: NotRequired[str]


StringAttributeBoostingConfigurationUnionTypeDef = Union[
    StringAttributeBoostingConfigurationTypeDef, StringAttributeBoostingConfigurationOutputTypeDef
]
UsersAndGroupsUnionTypeDef = Union[UsersAndGroupsTypeDef, UsersAndGroupsOutputTypeDef]


class CustomPluginConfigurationTypeDef(TypedDict):
    description: str
    apiSchemaType: Literal["OPEN_API_V3"]
    apiSchema: APISchemaTypeDef


class ActionExecutionEventTypeDef(TypedDict):
    pluginId: str
    payload: Mapping[str, ActionExecutionPayloadFieldUnionTypeDef]
    payloadFieldNameSeparator: str


class ActionExecutionTypeDef(TypedDict):
    pluginId: str
    payload: Mapping[str, ActionExecutionPayloadFieldUnionTypeDef]
    payloadFieldNameSeparator: str


class ActionReviewEventTypeDef(TypedDict):
    conversationId: NotRequired[str]
    userMessageId: NotRequired[str]
    systemMessageId: NotRequired[str]
    pluginId: NotRequired[str]
    pluginType: NotRequired[PluginTypeType]
    payload: NotRequired[Dict[str, ActionReviewPayloadFieldTypeDef]]
    payloadFieldNameSeparator: NotRequired[str]


class ActionReviewTypeDef(TypedDict):
    pluginId: NotRequired[str]
    pluginType: NotRequired[PluginTypeType]
    payload: NotRequired[Dict[str, ActionReviewPayloadFieldTypeDef]]
    payloadFieldNameSeparator: NotRequired[str]


class ListApplicationsResponseTypeDef(TypedDict):
    applications: List[ApplicationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class FailedAttachmentEventTypeDef(TypedDict):
    conversationId: NotRequired[str]
    userMessageId: NotRequired[str]
    systemMessageId: NotRequired[str]
    attachment: NotRequired[AttachmentOutputTypeDef]


class ListDocumentsResponseTypeDef(TypedDict):
    documentDetailList: List[DocumentDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class BatchDeleteDocumentResponseTypeDef(TypedDict):
    failedDocuments: List[FailedDocumentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchPutDocumentResponseTypeDef(TypedDict):
    failedDocuments: List[FailedDocumentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetGroupResponseTypeDef(TypedDict):
    status: GroupStatusDetailTypeDef
    statusHistory: List[GroupStatusDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class RuleConfigurationOutputTypeDef(TypedDict):
    contentBlockerRule: NotRequired[ContentBlockerRuleTypeDef]
    contentRetrievalRule: NotRequired[ContentRetrievalRuleOutputTypeDef]


ContentRetrievalRuleUnionTypeDef = Union[
    ContentRetrievalRuleTypeDef, ContentRetrievalRuleOutputTypeDef
]


class AttachmentInputTypeDef(TypedDict):
    data: NotRequired[BlobTypeDef]
    name: NotRequired[str]
    copyFrom: NotRequired[CopyFromSourceTypeDef]


class AttachmentTypeDef(TypedDict):
    attachmentId: NotRequired[str]
    conversationId: NotRequired[str]
    name: NotRequired[str]
    copyFrom: NotRequired[CopyFromSourceTypeDef]
    fileType: NotRequired[str]
    fileSize: NotRequired[int]
    md5chksum: NotRequired[str]
    createdAt: NotRequired[datetime]
    status: NotRequired[AttachmentStatusType]
    error: NotRequired[ErrorDetailTypeDef]


class ListDataSourceSyncJobsResponseTypeDef(TypedDict):
    history: List[DataSourceSyncJobTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class NativeIndexConfigurationOutputTypeDef(TypedDict):
    indexId: str
    boostingOverride: NotRequired[Dict[str, DocumentAttributeBoostingConfigurationOutputTypeDef]]


class HookConfigurationOutputTypeDef(TypedDict):
    invocationCondition: NotRequired[DocumentAttributeConditionOutputTypeDef]
    lambdaArn: NotRequired[str]
    s3BucketName: NotRequired[str]
    roleArn: NotRequired[str]


class AttributeFilterOutputTypeDef(TypedDict):
    andAllFilters: NotRequired[List[Dict[str, Any]]]
    orAllFilters: NotRequired[List[Dict[str, Any]]]
    notFilter: NotRequired[Dict[str, Any]]
    equalsTo: NotRequired[DocumentAttributeOutputTypeDef]
    containsAll: NotRequired[DocumentAttributeOutputTypeDef]
    containsAny: NotRequired[DocumentAttributeOutputTypeDef]
    greaterThan: NotRequired[DocumentAttributeOutputTypeDef]
    greaterThanOrEquals: NotRequired[DocumentAttributeOutputTypeDef]
    lessThan: NotRequired[DocumentAttributeOutputTypeDef]
    lessThanOrEquals: NotRequired[DocumentAttributeOutputTypeDef]


class RelevantContentTypeDef(TypedDict):
    content: NotRequired[str]
    documentId: NotRequired[str]
    documentTitle: NotRequired[str]
    documentUri: NotRequired[str]
    documentAttributes: NotRequired[List[DocumentAttributeOutputTypeDef]]
    scoreAttributes: NotRequired[ScoreAttributesTypeDef]


class InlineDocumentEnrichmentConfigurationOutputTypeDef(TypedDict):
    condition: NotRequired[DocumentAttributeConditionOutputTypeDef]
    target: NotRequired[DocumentAttributeTargetOutputTypeDef]
    documentContentOperator: NotRequired[Literal["DELETE"]]


DocumentAttributeValueUnionTypeDef = Union[
    DocumentAttributeValueTypeDef, DocumentAttributeValueOutputTypeDef
]


class PutFeedbackRequestRequestTypeDef(TypedDict):
    applicationId: str
    conversationId: str
    messageId: str
    userId: NotRequired[str]
    messageCopiedAt: NotRequired[TimestampTypeDef]
    messageUsefulness: NotRequired[MessageUsefulnessFeedbackTypeDef]


PutGroupRequestRequestTypeDef = TypedDict(
    "PutGroupRequestRequestTypeDef",
    {
        "applicationId": str,
        "indexId": str,
        "groupName": str,
        "type": MembershipTypeType,
        "groupMembers": GroupMembersTypeDef,
        "dataSourceId": NotRequired[str],
        "roleArn": NotRequired[str],
    },
)


class CreateWebExperienceRequestRequestTypeDef(TypedDict):
    applicationId: str
    title: NotRequired[str]
    subtitle: NotRequired[str]
    welcomeMessage: NotRequired[str]
    samplePromptsControlMode: NotRequired[WebExperienceSamplePromptsControlModeType]
    origins: NotRequired[Sequence[str]]
    roleArn: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    clientToken: NotRequired[str]
    identityProviderConfiguration: NotRequired[IdentityProviderConfigurationTypeDef]
    browserExtensionConfiguration: NotRequired[BrowserExtensionConfigurationTypeDef]
    customizationConfiguration: NotRequired[CustomizationConfigurationTypeDef]


GetIndexResponseTypeDef = TypedDict(
    "GetIndexResponseTypeDef",
    {
        "applicationId": str,
        "indexId": str,
        "displayName": str,
        "indexArn": str,
        "status": IndexStatusType,
        "type": IndexTypeType,
        "description": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "capacityConfiguration": IndexCapacityConfigurationTypeDef,
        "documentAttributeConfigurations": List[DocumentAttributeConfigurationTypeDef],
        "error": ErrorDetailTypeDef,
        "indexStatistics": IndexStatisticsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class AccessControlTypeDef(TypedDict):
    principals: Sequence[PrincipalTypeDef]
    memberRelation: NotRequired[MemberRelationType]


class GetWebExperienceResponseTypeDef(TypedDict):
    applicationId: str
    webExperienceId: str
    webExperienceArn: str
    defaultEndpoint: str
    status: WebExperienceStatusType
    createdAt: datetime
    updatedAt: datetime
    title: str
    subtitle: str
    welcomeMessage: str
    samplePromptsControlMode: WebExperienceSamplePromptsControlModeType
    origins: List[str]
    roleArn: str
    identityProviderConfiguration: IdentityProviderConfigurationTypeDef
    authenticationConfiguration: WebExperienceAuthConfigurationTypeDef
    error: ErrorDetailTypeDef
    browserExtensionConfiguration: BrowserExtensionConfigurationOutputTypeDef
    customizationConfiguration: CustomizationConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateWebExperienceRequestRequestTypeDef(TypedDict):
    applicationId: str
    webExperienceId: str
    roleArn: NotRequired[str]
    authenticationConfiguration: NotRequired[WebExperienceAuthConfigurationTypeDef]
    title: NotRequired[str]
    subtitle: NotRequired[str]
    welcomeMessage: NotRequired[str]
    samplePromptsControlMode: NotRequired[WebExperienceSamplePromptsControlModeType]
    identityProviderConfiguration: NotRequired[IdentityProviderConfigurationTypeDef]
    origins: NotRequired[Sequence[str]]
    browserExtensionConfiguration: NotRequired[BrowserExtensionConfigurationTypeDef]
    customizationConfiguration: NotRequired[CustomizationConfigurationTypeDef]


class SourceAttributionTypeDef(TypedDict):
    title: NotRequired[str]
    snippet: NotRequired[str]
    url: NotRequired[str]
    citationNumber: NotRequired[int]
    updatedAt: NotRequired[datetime]
    textMessageSegments: NotRequired[List[TextSegmentTypeDef]]


class DocumentAttributeBoostingConfigurationTypeDef(TypedDict):
    numberConfiguration: NotRequired[NumberAttributeBoostingConfigurationTypeDef]
    stringConfiguration: NotRequired[StringAttributeBoostingConfigurationUnionTypeDef]
    dateConfiguration: NotRequired[DateAttributeBoostingConfigurationTypeDef]
    stringListConfiguration: NotRequired[StringListAttributeBoostingConfigurationTypeDef]


CreatePluginRequestRequestTypeDef = TypedDict(
    "CreatePluginRequestRequestTypeDef",
    {
        "applicationId": str,
        "displayName": str,
        "type": PluginTypeType,
        "authConfiguration": PluginAuthConfigurationTypeDef,
        "serverUrl": NotRequired[str],
        "customPluginConfiguration": NotRequired[CustomPluginConfigurationTypeDef],
        "tags": NotRequired[Sequence[TagTypeDef]],
        "clientToken": NotRequired[str],
    },
)
GetPluginResponseTypeDef = TypedDict(
    "GetPluginResponseTypeDef",
    {
        "applicationId": str,
        "pluginId": str,
        "displayName": str,
        "type": PluginTypeType,
        "serverUrl": str,
        "authConfiguration": PluginAuthConfigurationOutputTypeDef,
        "customPluginConfiguration": CustomPluginConfigurationTypeDef,
        "buildStatus": PluginBuildStatusType,
        "pluginArn": str,
        "state": PluginStateType,
        "createdAt": datetime,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class UpdatePluginRequestRequestTypeDef(TypedDict):
    applicationId: str
    pluginId: str
    displayName: NotRequired[str]
    state: NotRequired[PluginStateType]
    serverUrl: NotRequired[str]
    customPluginConfiguration: NotRequired[CustomPluginConfigurationTypeDef]
    authConfiguration: NotRequired[PluginAuthConfigurationTypeDef]


class RuleOutputTypeDef(TypedDict):
    ruleType: RuleTypeType
    includedUsersAndGroups: NotRequired[UsersAndGroupsOutputTypeDef]
    excludedUsersAndGroups: NotRequired[UsersAndGroupsOutputTypeDef]
    ruleConfiguration: NotRequired[RuleConfigurationOutputTypeDef]


class RuleConfigurationTypeDef(TypedDict):
    contentBlockerRule: NotRequired[ContentBlockerRuleTypeDef]
    contentRetrievalRule: NotRequired[ContentRetrievalRuleUnionTypeDef]


class AttachmentInputEventTypeDef(TypedDict):
    attachment: NotRequired[AttachmentInputTypeDef]


class ListAttachmentsResponseTypeDef(TypedDict):
    attachments: List[AttachmentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class RetrieverConfigurationOutputTypeDef(TypedDict):
    nativeIndexConfiguration: NotRequired[NativeIndexConfigurationOutputTypeDef]
    kendraIndexConfiguration: NotRequired[KendraIndexConfigurationTypeDef]


class ActionFilterConfigurationOutputTypeDef(TypedDict):
    documentAttributeFilter: AttributeFilterOutputTypeDef


class SearchRelevantContentResponseTypeDef(TypedDict):
    relevantContent: List[RelevantContentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DocumentEnrichmentConfigurationOutputTypeDef(TypedDict):
    inlineConfigurations: NotRequired[List[InlineDocumentEnrichmentConfigurationOutputTypeDef]]
    preExtractionHookConfiguration: NotRequired[HookConfigurationOutputTypeDef]
    postExtractionHookConfiguration: NotRequired[HookConfigurationOutputTypeDef]


DocumentAttributeConditionTypeDef = TypedDict(
    "DocumentAttributeConditionTypeDef",
    {
        "key": str,
        "operator": DocumentEnrichmentConditionOperatorType,
        "value": NotRequired[DocumentAttributeValueUnionTypeDef],
    },
)


class DocumentAttributeTargetTypeDef(TypedDict):
    key: str
    value: NotRequired[DocumentAttributeValueUnionTypeDef]
    attributeValueOperator: NotRequired[Literal["DELETE"]]


class DocumentAttributeTypeDef(TypedDict):
    name: str
    value: DocumentAttributeValueUnionTypeDef


class AccessConfigurationTypeDef(TypedDict):
    accessControls: Sequence[AccessControlTypeDef]
    memberRelation: NotRequired[MemberRelationType]


class ChatSyncOutputTypeDef(TypedDict):
    conversationId: str
    systemMessage: str
    systemMessageId: str
    userMessageId: str
    actionReview: ActionReviewTypeDef
    authChallengeRequest: AuthChallengeRequestTypeDef
    sourceAttributions: List[SourceAttributionTypeDef]
    failedAttachments: List[AttachmentOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


MessageTypeDef = TypedDict(
    "MessageTypeDef",
    {
        "messageId": NotRequired[str],
        "body": NotRequired[str],
        "time": NotRequired[datetime],
        "type": NotRequired[MessageTypeType],
        "attachments": NotRequired[List[AttachmentOutputTypeDef]],
        "sourceAttribution": NotRequired[List[SourceAttributionTypeDef]],
        "actionReview": NotRequired[ActionReviewTypeDef],
        "actionExecution": NotRequired[ActionExecutionOutputTypeDef],
    },
)


class MetadataEventTypeDef(TypedDict):
    conversationId: NotRequired[str]
    userMessageId: NotRequired[str]
    systemMessageId: NotRequired[str]
    sourceAttributions: NotRequired[List[SourceAttributionTypeDef]]
    finalTextMessage: NotRequired[str]


DocumentAttributeBoostingConfigurationUnionTypeDef = Union[
    DocumentAttributeBoostingConfigurationTypeDef,
    DocumentAttributeBoostingConfigurationOutputTypeDef,
]


class TopicConfigurationOutputTypeDef(TypedDict):
    name: str
    rules: List[RuleOutputTypeDef]
    description: NotRequired[str]
    exampleChatMessages: NotRequired[List[str]]


RuleConfigurationUnionTypeDef = Union[RuleConfigurationTypeDef, RuleConfigurationOutputTypeDef]
GetRetrieverResponseTypeDef = TypedDict(
    "GetRetrieverResponseTypeDef",
    {
        "applicationId": str,
        "retrieverId": str,
        "retrieverArn": str,
        "type": RetrieverTypeType,
        "status": RetrieverStatusType,
        "displayName": str,
        "configuration": RetrieverConfigurationOutputTypeDef,
        "roleArn": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class ActionConfigurationOutputTypeDef(TypedDict):
    action: str
    filterConfiguration: NotRequired[ActionFilterConfigurationOutputTypeDef]


GetDataSourceResponseTypeDef = TypedDict(
    "GetDataSourceResponseTypeDef",
    {
        "applicationId": str,
        "indexId": str,
        "dataSourceId": str,
        "dataSourceArn": str,
        "displayName": str,
        "type": str,
        "configuration": Dict[str, Any],
        "vpcConfiguration": DataSourceVpcConfigurationOutputTypeDef,
        "createdAt": datetime,
        "updatedAt": datetime,
        "description": str,
        "status": DataSourceStatusType,
        "syncSchedule": str,
        "roleArn": str,
        "error": ErrorDetailTypeDef,
        "documentEnrichmentConfiguration": DocumentEnrichmentConfigurationOutputTypeDef,
        "mediaExtractionConfiguration": MediaExtractionConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DocumentAttributeConditionUnionTypeDef = Union[
    DocumentAttributeConditionTypeDef, DocumentAttributeConditionOutputTypeDef
]
DocumentAttributeTargetUnionTypeDef = Union[
    DocumentAttributeTargetTypeDef, DocumentAttributeTargetOutputTypeDef
]
DocumentAttributeUnionTypeDef = Union[DocumentAttributeTypeDef, DocumentAttributeOutputTypeDef]


class ListMessagesResponseTypeDef(TypedDict):
    messages: List[MessageTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ChatOutputStreamTypeDef(TypedDict):
    textEvent: NotRequired[TextOutputEventTypeDef]
    metadataEvent: NotRequired[MetadataEventTypeDef]
    actionReviewEvent: NotRequired[ActionReviewEventTypeDef]
    failedAttachmentEvent: NotRequired[FailedAttachmentEventTypeDef]
    authChallengeRequestEvent: NotRequired[AuthChallengeRequestEventTypeDef]


class NativeIndexConfigurationTypeDef(TypedDict):
    indexId: str
    boostingOverride: NotRequired[Mapping[str, DocumentAttributeBoostingConfigurationUnionTypeDef]]


class GetChatControlsConfigurationResponseTypeDef(TypedDict):
    responseScope: ResponseScopeType
    blockedPhrases: BlockedPhrasesConfigurationTypeDef
    topicConfigurations: List[TopicConfigurationOutputTypeDef]
    creatorModeConfiguration: AppliedCreatorModeConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class RuleTypeDef(TypedDict):
    ruleType: RuleTypeType
    includedUsersAndGroups: NotRequired[UsersAndGroupsUnionTypeDef]
    excludedUsersAndGroups: NotRequired[UsersAndGroupsUnionTypeDef]
    ruleConfiguration: NotRequired[RuleConfigurationUnionTypeDef]


class GetDataAccessorResponseTypeDef(TypedDict):
    displayName: str
    dataAccessorId: str
    dataAccessorArn: str
    applicationId: str
    idcApplicationArn: str
    principal: str
    actionConfigurations: List[ActionConfigurationOutputTypeDef]
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class HookConfigurationTypeDef(TypedDict):
    invocationCondition: NotRequired[DocumentAttributeConditionUnionTypeDef]
    lambdaArn: NotRequired[str]
    s3BucketName: NotRequired[str]
    roleArn: NotRequired[str]


class InlineDocumentEnrichmentConfigurationTypeDef(TypedDict):
    condition: NotRequired[DocumentAttributeConditionUnionTypeDef]
    target: NotRequired[DocumentAttributeTargetUnionTypeDef]
    documentContentOperator: NotRequired[Literal["DELETE"]]


class AttributeFilterPaginatorTypeDef(TypedDict):
    andAllFilters: NotRequired[Sequence[Mapping[str, Any]]]
    orAllFilters: NotRequired[Sequence[Mapping[str, Any]]]
    notFilter: NotRequired[Mapping[str, Any]]
    equalsTo: NotRequired[DocumentAttributeUnionTypeDef]
    containsAll: NotRequired[DocumentAttributeUnionTypeDef]
    containsAny: NotRequired[DocumentAttributeUnionTypeDef]
    greaterThan: NotRequired[DocumentAttributeUnionTypeDef]
    greaterThanOrEquals: NotRequired[DocumentAttributeUnionTypeDef]
    lessThan: NotRequired[DocumentAttributeUnionTypeDef]
    lessThanOrEquals: NotRequired[DocumentAttributeUnionTypeDef]


class AttributeFilterTypeDef(TypedDict):
    andAllFilters: NotRequired[Sequence[Mapping[str, Any]]]
    orAllFilters: NotRequired[Sequence[Mapping[str, Any]]]
    notFilter: NotRequired[Mapping[str, Any]]
    equalsTo: NotRequired[DocumentAttributeUnionTypeDef]
    containsAll: NotRequired[DocumentAttributeUnionTypeDef]
    containsAny: NotRequired[DocumentAttributeUnionTypeDef]
    greaterThan: NotRequired[DocumentAttributeUnionTypeDef]
    greaterThanOrEquals: NotRequired[DocumentAttributeUnionTypeDef]
    lessThan: NotRequired[DocumentAttributeUnionTypeDef]
    lessThanOrEquals: NotRequired[DocumentAttributeUnionTypeDef]


class ChatOutputTypeDef(TypedDict):
    outputStream: "EventStream[ChatOutputStreamTypeDef]"
    ResponseMetadata: ResponseMetadataTypeDef


NativeIndexConfigurationUnionTypeDef = Union[
    NativeIndexConfigurationTypeDef, NativeIndexConfigurationOutputTypeDef
]
RuleUnionTypeDef = Union[RuleTypeDef, RuleOutputTypeDef]
HookConfigurationUnionTypeDef = Union[HookConfigurationTypeDef, HookConfigurationOutputTypeDef]
InlineDocumentEnrichmentConfigurationUnionTypeDef = Union[
    InlineDocumentEnrichmentConfigurationTypeDef, InlineDocumentEnrichmentConfigurationOutputTypeDef
]


class SearchRelevantContentRequestSearchRelevantContentPaginateTypeDef(TypedDict):
    applicationId: str
    queryText: str
    contentSource: ContentSourceTypeDef
    attributeFilter: NotRequired[AttributeFilterPaginatorTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


AttributeFilterUnionTypeDef = Union[AttributeFilterTypeDef, AttributeFilterOutputTypeDef]


class ChatSyncInputRequestTypeDef(TypedDict):
    applicationId: str
    userId: NotRequired[str]
    userGroups: NotRequired[Sequence[str]]
    userMessage: NotRequired[str]
    attachments: NotRequired[Sequence[AttachmentInputTypeDef]]
    actionExecution: NotRequired[ActionExecutionTypeDef]
    authChallengeResponse: NotRequired[AuthChallengeResponseTypeDef]
    conversationId: NotRequired[str]
    parentMessageId: NotRequired[str]
    attributeFilter: NotRequired[AttributeFilterTypeDef]
    chatMode: NotRequired[ChatModeType]
    chatModeConfiguration: NotRequired[ChatModeConfigurationTypeDef]
    clientToken: NotRequired[str]


class SearchRelevantContentRequestRequestTypeDef(TypedDict):
    applicationId: str
    queryText: str
    contentSource: ContentSourceTypeDef
    attributeFilter: NotRequired[AttributeFilterTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class RetrieverConfigurationTypeDef(TypedDict):
    nativeIndexConfiguration: NotRequired[NativeIndexConfigurationUnionTypeDef]
    kendraIndexConfiguration: NotRequired[KendraIndexConfigurationTypeDef]


class TopicConfigurationTypeDef(TypedDict):
    name: str
    rules: Sequence[RuleUnionTypeDef]
    description: NotRequired[str]
    exampleChatMessages: NotRequired[Sequence[str]]


class DocumentEnrichmentConfigurationTypeDef(TypedDict):
    inlineConfigurations: NotRequired[Sequence[InlineDocumentEnrichmentConfigurationUnionTypeDef]]
    preExtractionHookConfiguration: NotRequired[HookConfigurationUnionTypeDef]
    postExtractionHookConfiguration: NotRequired[HookConfigurationUnionTypeDef]


class ActionFilterConfigurationTypeDef(TypedDict):
    documentAttributeFilter: AttributeFilterUnionTypeDef


class ConfigurationEventTypeDef(TypedDict):
    chatMode: NotRequired[ChatModeType]
    chatModeConfiguration: NotRequired[ChatModeConfigurationTypeDef]
    attributeFilter: NotRequired[AttributeFilterUnionTypeDef]


CreateRetrieverRequestRequestTypeDef = TypedDict(
    "CreateRetrieverRequestRequestTypeDef",
    {
        "applicationId": str,
        "type": RetrieverTypeType,
        "displayName": str,
        "configuration": RetrieverConfigurationTypeDef,
        "roleArn": NotRequired[str],
        "clientToken": NotRequired[str],
        "tags": NotRequired[Sequence[TagTypeDef]],
    },
)


class UpdateRetrieverRequestRequestTypeDef(TypedDict):
    applicationId: str
    retrieverId: str
    configuration: NotRequired[RetrieverConfigurationTypeDef]
    displayName: NotRequired[str]
    roleArn: NotRequired[str]


TopicConfigurationUnionTypeDef = Union[TopicConfigurationTypeDef, TopicConfigurationOutputTypeDef]


class CreateDataSourceRequestRequestTypeDef(TypedDict):
    applicationId: str
    indexId: str
    displayName: str
    configuration: Mapping[str, Any]
    vpcConfiguration: NotRequired[DataSourceVpcConfigurationTypeDef]
    description: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    syncSchedule: NotRequired[str]
    roleArn: NotRequired[str]
    clientToken: NotRequired[str]
    documentEnrichmentConfiguration: NotRequired[DocumentEnrichmentConfigurationTypeDef]
    mediaExtractionConfiguration: NotRequired[MediaExtractionConfigurationTypeDef]


DocumentEnrichmentConfigurationUnionTypeDef = Union[
    DocumentEnrichmentConfigurationTypeDef, DocumentEnrichmentConfigurationOutputTypeDef
]


class UpdateDataSourceRequestRequestTypeDef(TypedDict):
    applicationId: str
    indexId: str
    dataSourceId: str
    displayName: NotRequired[str]
    configuration: NotRequired[Mapping[str, Any]]
    vpcConfiguration: NotRequired[DataSourceVpcConfigurationTypeDef]
    description: NotRequired[str]
    syncSchedule: NotRequired[str]
    roleArn: NotRequired[str]
    documentEnrichmentConfiguration: NotRequired[DocumentEnrichmentConfigurationTypeDef]
    mediaExtractionConfiguration: NotRequired[MediaExtractionConfigurationTypeDef]


ActionFilterConfigurationUnionTypeDef = Union[
    ActionFilterConfigurationTypeDef, ActionFilterConfigurationOutputTypeDef
]


class ChatInputStreamTypeDef(TypedDict):
    configurationEvent: NotRequired[ConfigurationEventTypeDef]
    textEvent: NotRequired[TextInputEventTypeDef]
    attachmentEvent: NotRequired[AttachmentInputEventTypeDef]
    actionExecutionEvent: NotRequired[ActionExecutionEventTypeDef]
    endOfInputEvent: NotRequired[Mapping[str, Any]]
    authChallengeResponseEvent: NotRequired[AuthChallengeResponseEventTypeDef]


class UpdateChatControlsConfigurationRequestRequestTypeDef(TypedDict):
    applicationId: str
    clientToken: NotRequired[str]
    responseScope: NotRequired[ResponseScopeType]
    blockedPhrasesConfigurationUpdate: NotRequired[BlockedPhrasesConfigurationUpdateTypeDef]
    topicConfigurationsToCreateOrUpdate: NotRequired[Sequence[TopicConfigurationUnionTypeDef]]
    topicConfigurationsToDelete: NotRequired[Sequence[TopicConfigurationTypeDef]]
    creatorModeConfiguration: NotRequired[CreatorModeConfigurationTypeDef]


DocumentTypeDef = TypedDict(
    "DocumentTypeDef",
    {
        "id": str,
        "attributes": NotRequired[Sequence[DocumentAttributeUnionTypeDef]],
        "content": NotRequired[DocumentContentTypeDef],
        "contentType": NotRequired[ContentTypeType],
        "title": NotRequired[str],
        "accessConfiguration": NotRequired[AccessConfigurationTypeDef],
        "documentEnrichmentConfiguration": NotRequired[DocumentEnrichmentConfigurationUnionTypeDef],
        "mediaExtractionConfiguration": NotRequired[MediaExtractionConfigurationTypeDef],
    },
)


class ActionConfigurationTypeDef(TypedDict):
    action: str
    filterConfiguration: NotRequired[ActionFilterConfigurationUnionTypeDef]


class ChatInputRequestTypeDef(TypedDict):
    applicationId: str
    userId: NotRequired[str]
    userGroups: NotRequired[Sequence[str]]
    conversationId: NotRequired[str]
    parentMessageId: NotRequired[str]
    clientToken: NotRequired[str]
    inputStream: NotRequired["EventStream[ChatInputStreamTypeDef]"]


class BatchPutDocumentRequestRequestTypeDef(TypedDict):
    applicationId: str
    indexId: str
    documents: Sequence[DocumentTypeDef]
    roleArn: NotRequired[str]
    dataSourceSyncId: NotRequired[str]


ActionConfigurationUnionTypeDef = Union[
    ActionConfigurationTypeDef, ActionConfigurationOutputTypeDef
]


class UpdateDataAccessorRequestRequestTypeDef(TypedDict):
    applicationId: str
    dataAccessorId: str
    actionConfigurations: Sequence[ActionConfigurationTypeDef]
    displayName: NotRequired[str]


class CreateDataAccessorRequestRequestTypeDef(TypedDict):
    applicationId: str
    principal: str
    actionConfigurations: Sequence[ActionConfigurationUnionTypeDef]
    displayName: str
    clientToken: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
