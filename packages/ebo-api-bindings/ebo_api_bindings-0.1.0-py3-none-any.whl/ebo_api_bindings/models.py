from enum import Enum
from .base import ApiBaseModel
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Union


@dataclass(kw_only=True)
class GenericApiResponse(ApiBaseModel):
    success: bool
    """Whether the operation succeeded"""
    error: Optional[str] = None
    """Optional error description (set if 'success' was false)"""


@dataclass(kw_only=True)
class WindowSettings(ApiBaseModel):
    windowSizeMs: float
    windowIncreaseMs: float
    windowIncreasePct: float
    zeroPadPercentage: float
    windowCount: int
    balanceScore: float
    valid: bool


@dataclass(kw_only=True)
class CreateSignedUploadLinkResponse(GenericApiResponse):
    url: Optional[str] = None
    """S3 Upload Link"""
    ETag: Optional[str] = None
    """S3 File Tag"""


@dataclass(kw_only=True)
class CreateSignedUploadLinkRequest(ApiBaseModel):
    fileName: str
    """file name"""
    fileSize: int
    """file size in bytes"""
    fileHash: str
    """hash to identify file changes"""


@dataclass(kw_only=True)
class PortalFileTypeEnum(Enum):
    folder = "folder"
    file = "file"


@dataclass(kw_only=True)
class PortalFile(ApiBaseModel):
    name: str
    path: str
    type: PortalFileTypeEnum
    addedDate: Optional[datetime] = None
    size: Optional[int] = None
    ETag: Optional[str] = None


@dataclass(kw_only=True)
class ListPortalFilesInFolderResponse(GenericApiResponse):
    files: List[PortalFile]
    continuationToken: Optional[str] = None


@dataclass(kw_only=True)
class ListPortalFilesInFolderRequest(ApiBaseModel):
    prefix: str
    """S3 prefix"""
    continuationToken: Optional[str] = None
    """Only one S3 page (1000 items typically) is returned. Pass in the continuationToken on the next request to receive the next page."""
    onlyFetchFolders: Optional[bool] = None
    """If set, then no files will be returned"""


@dataclass(kw_only=True)
class TruncationReason(Enum):
    too_many_results = "too-many-results"
    too_expensive_search = "too-expensive-search"


@dataclass(kw_only=True)
class PreviewDefaultFilesInFolderResponse(GenericApiResponse):
    files: List[PortalFile]
    isTruncated: Optional[bool] = None
    """True if results are truncated."""
    truncationReason: TruncationReason = None
    """Explains why results are truncated; only present in the response if isTruncated is true. Results can be truncated if there are too many results (more than 500 matches), or if searching for more results is too expensive (for example, the dataset contains many items but very few match the given wildcard). """


@dataclass(kw_only=True)
class PreviewDefaultFilesInFolderRequestItemsToListEnum(Enum):
    files = "files"
    folders = "folders"


@dataclass(kw_only=True)
class PreviewDefaultFilesInFolderRequest(ApiBaseModel):
    prefix: str
    """S3 prefix"""
    itemsToList: PreviewDefaultFilesInFolderRequestItemsToListEnum


@dataclass(kw_only=True)
class DeletePortalFileRequest(ApiBaseModel):
    path: str
    """S3 path (within the portal)"""


@dataclass(kw_only=True)
class RenamePortalFileRequest(ApiBaseModel):
    oldPath: str
    """S3 path (within the portal)"""
    newPath: str
    """S3 path (within the portal)"""


@dataclass(kw_only=True)
class DownloadPortalFileRequest(ApiBaseModel):
    path: str
    """S3 path (within the portal)"""


@dataclass(kw_only=True)
class DownloadPortalFileResponse(GenericApiResponse):
    url: str
    """Signed URL to download the file"""


@dataclass(kw_only=True)
class LoginResponse(GenericApiResponse):
    token: str
    """JWT token, to be used to log in in the future through JWTAuthentication"""


@dataclass(kw_only=True)
class GetJWTRequestSsoTypeEnum(Enum):
    browser = "browser"
    cli = "cli"


@dataclass(kw_only=True)
class GetJWTRequest(ApiBaseModel):
    username: str
    """Username or e-mail address"""
    password: str
    """Password"""
    uuid: Optional[str] = None
    """Evaluation user UUID"""
    ssoType: GetJWTRequestSsoTypeEnum = None
    sessionId: Optional[str] = None
    """Session ID"""
    totpToken: Optional[str] = None
    """TOTP Token. Required if a user has multi-factor authentication with a TOTP token enabled. If a user has MFA enabled, but no totpToken is submitted; then an error starting with "ERR_TOTP_TOKEN IS REQUIRED" is returned. Use this to then prompt for an MFA token and re-login."""


@dataclass(kw_only=True)
class GetJWTResponse(GenericApiResponse):
    token: Optional[str] = None
    """JWT token, to be used to log in in the future through JWTAuthentication"""
    redirectUrl: Optional[str] = None
    """Redirect URL to follow to complete login"""


@dataclass(kw_only=True)
class ProjectPublicDataReadme(ApiBaseModel):
    markdown: str
    html: str


@dataclass(kw_only=True)
class ProjectType(Enum):
    kws = "kws"
    audio = "audio"
    object_detection = "object-detection"
    image = "image"
    accelerometer = "accelerometer"
    other = "other"


@dataclass(kw_only=True)
class ProjectPublicData(ApiBaseModel):
    id: int
    name: str
    description: str
    created: datetime
    owner: str
    """User or organization that owns the project"""
    publicUrl: str
    """URL of the latest public version of the project, if any"""
    projectType: ProjectType
    pageViewCount: int
    cloneCount: int
    tags: List[str]
    """List of project tags"""
    ownerAvatar: Optional[str] = None
    """URL to the project owner avatar, if any"""
    totalSamplesCount: Optional[str] = None
    trainingAccuracy: Optional[float] = None
    """Accuracy on training set."""
    testAccuracy: Optional[float] = None
    """Accuracy on test set."""
    readme: ProjectPublicDataReadme = None


@dataclass(kw_only=True)
class StaffInfo(ApiBaseModel):
    isStaff: bool
    hasSudoRights: bool
    companyName: Optional[str] = None


@dataclass(kw_only=True)
class Permission(Enum):
    admin_infra_disallowedEmailDomains_write = (
        "admin:infra:disallowedEmailDomains:write"
    )
    admin_infra_featureFlags_read = "admin:infra:featureFlags:read"
    admin_infra_featureFlags_write = "admin:infra:featureFlags:write"
    admin_infra_config_read = "admin:infra:config:read"
    admin_infra_config_write = "admin:infra:config:write"
    admin_infra_migrations_read = "admin:infra:migrations:read"
    admin_infra_migrations_write = "admin:infra:migrations:write"
    admin_metrics_read = "admin:metrics:read"
    admin_metrics_write = "admin:metrics:write"
    admin_organizations_read = "admin:organizations:read"
    admin_organizations_write = "admin:organizations:write"
    admin_organizations_members_write = "admin:organizations:members:write"
    admin_projects_members_write = "admin:projects:members:write"
    admin_projects_read = "admin:projects:read"
    admin_projects_write = "admin:projects:write"
    admin_trials_read = "admin:trials:read"
    admin_trials_write = "admin:trials:write"
    admin_users_permissions_write = "admin:users:permissions:write"
    admin_users_read = "admin:users:read"
    admin_users_write = "admin:users:write"
    admin_jobs_read = "admin:jobs:read"
    admin_emails_verification_code_read = "admin:emails:verification:code:read"
    projects_limits_write = "projects:limits:write"
    projects_training_keras_write = "projects:training:keras:write"
    thirdpartyauth_read = "thirdpartyauth:read"
    thirdpartyauth_write = "thirdpartyauth:write"
    users_emails_read = "users:emails:read"
    whitelabels_read = "whitelabels:read"
    whitelabels_write = "whitelabels:write"


@dataclass(kw_only=True)
class UserTierEnum(Enum):
    free = "free"
    community_plus = "community-plus"
    professional = "professional"
    enterprise = "enterprise"


@dataclass(kw_only=True)
class User(ApiBaseModel):
    id: int
    username: str
    name: str
    email: str
    created: datetime
    staffInfo: StaffInfo
    pending: bool
    activated: bool
    """Whether the user has activated their account or not."""
    mfaConfigured: bool
    """Whether the user has configured multi-factor authentication"""
    photo: Optional[str] = None
    lastSeen: Optional[datetime] = None
    lastTosAcceptanceDate: Optional[datetime] = None
    jobTitle: Optional[str] = None
    permissions: Optional[List[Permission]] = None
    """List of permissions the user has"""
    companyName: Optional[str] = None
    stripeCustomerId: Optional[str] = None
    """Stripe customer ID, if any."""
    hasPendingPayments: Optional[bool] = None
    """Whether the user has pending payments."""
    tier: UserTierEnum = None


@dataclass(kw_only=True)
class ProjectCollaborator(User):
    isOwner: bool


@dataclass(kw_only=True)
class ProjectPrivateData(ApiBaseModel):
    metadata: Dict[str, Any]
    """Metadata about the project"""
    isEnterpriseProject: bool
    """Whether this is an enterprise project"""
    whitelabelId: int
    """Unique identifier of the white label this project belongs to, if any."""
    lastAccessed: Optional[datetime] = None
    dataExplorerScreenshot: Optional[str] = None
    collaborators: Optional[List[ProjectCollaborator]] = None


@dataclass(kw_only=True)
class ProjectLabelingMethodEnum(Enum):
    single_label = "single_label"
    object_detection = "object_detection"


@dataclass(kw_only=True)
class ProjectTierEnum(Enum):
    free = "free"
    community_plus = "community-plus"
    professional = "professional"
    enterprise = "enterprise"


@dataclass(kw_only=True)
class Project(ApiBaseModel):
    id: int
    name: str
    description: str
    created: datetime
    owner: str
    """User or organization that owns the project"""
    ownerIsDeveloperProfile: bool
    collaborators: List[ProjectCollaborator]
    labelingMethod: ProjectLabelingMethodEnum
    metadata: Dict[str, Any]
    """Metadata about the project"""
    isEnterpriseProject: bool
    """Whether this is an enterprise project"""
    whitelabelId: int
    """Unique identifier of the white label this project belongs to, if any."""
    tier: ProjectTierEnum
    hasPublicVersion: bool
    """Whether this project has been published or not."""
    isPublic: bool
    """Whether this is a public version of a project. A version is a snapshot of a project at a certain point in time, which can be used to periodically save the state of a project. Versions can be private (just for internal use and reference) or public, available to everyone. A public version can be cloned by anyone, restoring the state of the project at the time into a new, separate project. """
    allowsLivePublicAccess: bool
    """Whether this project allows live, public access. Unlike a public version, a live public project is not fixed in time, and always includes the latest project changes. Similar to public versions, a live public project can be cloned by anyone, creating a new, separate project. """
    indPauseProcessingSamples: bool
    publicProjectListed: bool
    """If the project allows public access, whether to list it the public projects overview response. If not listed, the project is still accessible via direct link. If the project does not allow public access, this field has no effect. """
    lastAccessed: Optional[datetime] = None
    lastModified: Optional[datetime] = None
    lastModificationDetails: Optional[str] = None
    """Details about the last modification"""
    logo: Optional[str] = None
    """Custom logo for this project (not available for all projects)"""
    ownerUserId: Optional[int] = None
    ownerOrganizationId: Optional[int] = None
    ownerAvatar: Optional[str] = None
    """URL of the project owner avatar, if any."""
    developerProfileUserId: Optional[int] = None
    """User ID of the developer profile, if any."""
    dataExplorerScreenshot: Optional[str] = None
    tags: Optional[List[Optional[str]]] = None
    """List of project tags"""
    category: Optional[str] = None
    """Project category"""
    license: Optional[str] = None
    """Public project license, if any."""


@dataclass(kw_only=True)
class UtmParameter(ApiBaseModel):
    pass


@dataclass(kw_only=True)
class UserExperiment(ApiBaseModel):
    type: str
    title: str
    enabled: bool
    showToUser: bool
    help: Optional[str] = None


@dataclass(kw_only=True)
class EntitlementLimits(ApiBaseModel):
    totalStorage: Optional[float] = None
    """Storage entitlement, in bytes"""
    computeTimePerYear: Optional[float] = None
    """Total compute time entitlement (CPU + GPU), in seconds"""
    gpuComputeTimePerYear: Optional[float] = None
    """GPU compute time entitlement, in seconds"""
    numberOfProjects: Optional[int] = None
    """Number of projects allowed for this organization"""
    numberOfUsers: Optional[int] = None
    """Number of users allowed for this organization"""


@dataclass(kw_only=True)
class UserOrganization(ApiBaseModel):
    id: int
    name: str
    isDeveloperProfile: bool
    whitelabelId: int
    """Unique identifier of the white label this project belongs to, if any."""
    isAdmin: bool
    """Whether the user is admin of this organization or not."""
    created: datetime
    """When the organization was created."""
    trialId: float
    """Unique identifier of the trial this organization belongs to, if any."""
    trialExpiredDate: datetime
    """Date when the trial expired, if any. A expired trial has a grace period of 30 days before it's associated organization is deleted."""
    trialUpgradedDate: datetime
    """Date when the trial was upgraded to a full enterprise account, if any."""
    entitlementLimits: EntitlementLimits
    userCount: int
    """The total number of users that are a member of this organization."""
    adminCount: int
    """The number of admin users for this organization."""
    privateProjectCount: int
    """The number of private projects for this organization."""
    logo: Optional[str] = None
    lastAccessed: Optional[datetime] = None
    """Last time this user accessed this organization."""


@dataclass(kw_only=True)
class TrialExpirationDate(ApiBaseModel):
    pass


@dataclass(kw_only=True)
class TrialNotes(ApiBaseModel):
    pass


@dataclass(kw_only=True)
class EnterpriseTrial(ApiBaseModel):
    id: int
    """Unique identifier of the trial."""
    userId: int
    """ID of the user who created the trial."""
    organizationId: int
    """ID of the organization created for the trial."""
    created: datetime
    """Date when the trial was created. Trials start immediately on creation."""
    expirationDate: TrialExpirationDate
    expiredDate: datetime
    """Date when the trial actually expired. This is set when the trial is expired by the system."""
    deletedDate: datetime
    """Date when the trial was deleted. This is set when the trial is fully  deleted by the system."""
    upgradedDate: datetime
    """Date when the trial was upgraded to a full enterprise account."""
    notes: TrialNotes = None


@dataclass(kw_only=True)
class DailyMetricsRecord(ApiBaseModel):
    date: datetime
    """Date of the metrics record."""
    totalUsers: int
    """Total number of users, if the metrics record applies to a non-developer profile organization. For developer profile organizations, we default to 0. """
    totalStaffUsers: int
    """Total number of staff users, if the metrics record applies to a non-developer profile organization. For developer profile organizations, we default to 0. """
    totalProjects: int
    """Total number of projects at the end of the metrics record date. """
    totalCurrentContractCpuComputeTimeSeconds: int
    """Total CPU compute time since contract start date, or organization / user creation date, at the end of the metrics record date. """
    totalCurrentContractGpuComputeTimeSeconds: int
    """Total GPU compute time since contract start date, or organization / user creation date, at the end of the metrics record date. """
    totalCurrentContractComputeTimeSeconds: int
    """Total compute time since contract start date, or organization / user creation date, at the end of the metrics record date. Compute time is calculated as CPU + 3*GPU compute time. """
    computeTimeCalculatedSince: datetime
    """Date from which the total compute time is calculated. This is the contract start date for billing organizations, or organization / user creation date. """
    totalStorageSizeBytes: int
    """Total storage size in bytes at the end of the metrics record date. """
    usersAdded: int
    """Number of users added during the metrics record date. """
    usersDeleted: int
    """Number of users deleted during the metrics record date. """
    projectsAdded: int
    """Number of projects added during the metrics record date. """
    projectsDeleted: int
    """Number of projects deleted during the metrics record date. """
    cpuComputeTimeSeconds: int
    """Total CPU compute time during the metrics record date. """
    gpuComputeTimeSeconds: int
    """Total GPU compute time during the metrics record date. """
    computeTimeSeconds: int
    """Total compute time during the metrics record date. Compute time is calculated as CPU + 3*GPU compute time. """
    storageBytesAdded: int
    """Total storage size in bytes added during the metrics record date. """
    storageBytesDeleted: int
    """Total storage size in bytes deleted during the metrics record date. """
    staffUsersAdded: Optional[int] = None
    """Number of staff users added during the metrics record date. """
    staffUsersDeleted: Optional[int] = None
    """Number of staff users deleted during the metrics record date. """


@dataclass(kw_only=True)
class AdminApiUser(User):
    email: str
    activated: bool
    organizations: List[UserOrganization]
    """Organizations that the user is a member of. Only filled when requesting information about yourself."""
    projects: List[Project]
    experiments: List[UserExperiment]
    """Experiments the user has access to. Enabling experiments can only be done through a JWT token."""
    tier: UserTierEnum
    suspended: bool
    """Whether the user is suspended."""
    trials: List[EnterpriseTrial]
    """Current or past enterprise trials."""
    evaluation: Optional[bool] = None
    """Whether this is an ephemeral evaluation account."""
    ambassador: Optional[bool] = None
    """Whether this user is an ambassador."""
    lastSeen: Optional[datetime] = None
    dailyMetrics: Optional[List[DailyMetricsRecord]] = None
    """Metrics for the last 365 days"""


@dataclass(kw_only=True)
class OrganizationMemberRole(Enum):
    admin = "admin"
    member = "member"
    guest = "guest"


@dataclass(kw_only=True)
class OrganizationUser(User):
    added: datetime
    role: OrganizationMemberRole
    projectCount: int
    datasets: List[str]
    lastAccessToOrganization: Optional[datetime] = None
    """Date when the user last accessed the organization data."""
    lastOrganizationProjectAccessed: Optional[int] = None
    """ID of the last project accessed by the user in the organization."""


@dataclass(kw_only=True)
class Organization(ApiBaseModel):
    id: int
    name: str
    """EdgeImpulse Inc."""
    showHeaderImgMask: bool
    users: List[OrganizationUser]
    isDeveloperProfile: bool
    whitelabelId: int
    """Unique identifier of the white label this organization belongs to, if any."""
    trialId: int
    """Unique identifier of the trial this organization belongs to, if any."""
    trialExpiredDate: datetime
    """Date when the trial expired, if any. A expired trial has a grace period of 30 days before it's associated organization is deleted."""
    trialUpgradedDate: datetime
    """Date when the trial was upgraded to a full enterprise account, if any."""
    created: datetime
    """Date when the organization was created."""
    logo: Optional[str] = None
    headerImg: Optional[str] = None
    projects: Optional[List[Project]] = None
    contractStartDate: Optional[datetime] = None
    """Date when the current contract started, if any."""
    deletedDate: Optional[datetime] = None
    """The date in which the organization was deleted. If the organization is not deleted, this field is not set."""


@dataclass(kw_only=True)
class AdminApiOrganization(Organization):
    projects: List[Project]
    """Array with organizational projects"""


@dataclass(kw_only=True)
class ListProjects(ApiBaseModel):
    projects: List[Project]
    """Array with projects"""


@dataclass(kw_only=True)
class ListProjectsResponse(GenericApiResponse, ListProjects):
    pass


@dataclass(kw_only=True)
class ListPublicProjects(ApiBaseModel):
    projects: List[ProjectPublicData]
    """Array with public projects"""
    totalProjectCount: int


@dataclass(kw_only=True)
class ListPublicProjectsResponse(GenericApiResponse, ListPublicProjects):
    pass


@dataclass(kw_only=True)
class ProjectTypes(ApiBaseModel):
    value: ProjectType
    label: str


@dataclass(kw_only=True)
class ListPublicProjectTypes(ApiBaseModel):
    projectTypes: List[ProjectTypes]
    """Array with project types"""


@dataclass(kw_only=True)
class ListPublicProjectTypesResponse(GenericApiResponse, ListPublicProjectTypes):
    pass


@dataclass(kw_only=True)
class DevelopmentKeys(ApiBaseModel):
    apiKey: Optional[str] = None
    """API Key"""
    hmacKey: Optional[str] = None
    """HMAC Key"""


@dataclass(kw_only=True)
class DevelopmentKeysResponse(GenericApiResponse, DevelopmentKeys):
    pass


@dataclass(kw_only=True)
class CreateDeviceRequest(ApiBaseModel):
    deviceId: str
    """Globally unique device identifier (e.g. MAC address)"""
    deviceType: str
    """Device type, for example the exact model of the device. Should be the same for all similar devices"""
    ifNotExists: bool
    """Whether to throw an error when this device already exists."""


@dataclass(kw_only=True)
class RenameDeviceRequest(ApiBaseModel):
    name: str
    """New name for this device"""


@dataclass(kw_only=True)
class DeviceNameResponse(GenericApiResponse):
    name: Optional[str] = None
    """Device name"""


@dataclass(kw_only=True)
class DatasetRatioDataRatio(ApiBaseModel):
    training: Optional[int] = None
    """number of training samples after rebalance"""
    testing: Optional[int] = None
    """number of testing samples after rebalance"""


@dataclass(kw_only=True)
class DatasetRatioData(ApiBaseModel):
    ratio: DatasetRatioDataRatio = None


@dataclass(kw_only=True)
class Sensor(Enum):
    accelerometer = "accelerometer"
    microphone = "microphone"
    camera = "camera"
    positional = "positional"
    environmental = "environmental"
    fusion = "fusion"
    unknown = "unknown"


@dataclass(kw_only=True)
class BoundingBox(ApiBaseModel):
    label: str
    x: int
    y: int
    width: int
    height: int


@dataclass(kw_only=True)
class SampleBoundingBoxesTypeEnum(Enum):
    object_detection = "object_detection"
    constrained_object_detection = "constrained_object_detection"


@dataclass(kw_only=True)
class SampleChartTypeEnum(Enum):
    chart = "chart"
    image = "image"
    video = "video"
    table = "table"


@dataclass(kw_only=True)
class SampleProjectLabelingMethodEnum(Enum):
    single_label = "single_label"
    object_detection = "object_detection"


@dataclass(kw_only=True)
class StructuredLabel(ApiBaseModel):
    startIndex: int
    """Start index of the label (e.g. 0)"""
    endIndex: int
    """End index of the label (e.g. 3). This value is inclusive, so { startIndex: 0, endIndex: 3 } covers 0, 1, 2, 3."""
    label: str
    """The label for this section."""


@dataclass(kw_only=True)
class SampleImageDimensions(ApiBaseModel):
    width: int
    height: int


@dataclass(kw_only=True)
class Sample(ApiBaseModel):
    id: float
    name: str
    startMs: float
    endMs: float


@dataclass(kw_only=True)
class RawSamplePayload(ApiBaseModel):
    device_type: str
    """Device type, for example the exact model of the device. Should be the same for all similar devices."""
    sensors: List[Sensor]
    """Array with sensor axes"""
    values: List[List[float]]
    """Array of sensor values. One array item per interval, and as many items in this array as there are sensor axes. This type is returned if there are multiple axes. """
    device_name: Optional[str] = None
    """Unique identifier for this device. **Only** set this when the device has a globally unique identifier (e.g. MAC address)."""
    cropStart: Optional[int] = None
    """New start index of the cropped sample"""
    cropEnd: Optional[int] = None
    """New end index of the cropped sample"""


@dataclass(kw_only=True)
class RawSampleData(ApiBaseModel):
    sample: Sample
    payload: RawSamplePayload
    totalPayloadLength: int
    """Total number of payload values"""


@dataclass(kw_only=True)
class SampleMetadata(ApiBaseModel):
    id: int
    """Sample ID"""
    metadata: Dict[str, str]
    """Sample free form associated metadata"""


@dataclass(kw_only=True)
class ProjectSampleMetadata(ApiBaseModel):
    metadata: List[SampleMetadata]
    """Array with all available sample metadata."""


@dataclass(kw_only=True)
class RenameSampleRequest(ApiBaseModel):
    name: str
    """New name for this sample"""


@dataclass(kw_only=True)
class EditSampleLabelRequest(ApiBaseModel):
    label: Optional[str] = None
    """New label for this sample"""


@dataclass(kw_only=True)
class CropSampleRequest(ApiBaseModel):
    cropStart: int
    """New start index of the sample"""
    cropEnd: int
    """New end index of the sample"""


@dataclass(kw_only=True)
class SplitSampleInFramesRequest(ApiBaseModel):
    fps: Optional[int] = None
    """Frames per second to extract from this video."""


@dataclass(kw_only=True)
class StoreSegmentLengthRequest(ApiBaseModel):
    segmentLength: float
    """Last segment length in milliseconds."""


@dataclass(kw_only=True)
class LearnBlockType(Enum):
    anomaly = "anomaly"
    anomaly_gmm = "anomaly-gmm"
    keras = "keras"
    keras_transfer_image = "keras-transfer-image"
    keras_transfer_kws = "keras-transfer-kws"
    keras_object_detection = "keras-object-detection"
    keras_regression = "keras-regression"
    keras_akida = "keras-akida"
    keras_akida_transfer_image = "keras-akida-transfer-image"
    keras_akida_object_detection = "keras-akida-object-detection"
    keras_visual_anomaly = "keras-visual-anomaly"


@dataclass(kw_only=True)
class ImpulseLearnBlock(ApiBaseModel):
    id: int
    """Identifier for this block. Make sure to up this number when creating a new block, and don't re-use identifiers. If the block hasn't changed, keep the ID as-is. ID must be unique across the project and greather than zero (>0)."""
    type: LearnBlockType
    name: str
    """Block name, will be used in menus. If a block has a baseBlockId, this field is ignored and the base block's name is used instead."""
    dsp: List[int]
    """DSP dependencies, identified by DSP block ID"""
    title: str
    """Block title, used in the impulse UI"""
    description: Optional[str] = None
    """A short description of the block version, displayed in the block versioning UI"""
    createdBy: Optional[str] = None
    """The system component that created the block version (createImpulse | clone | tuner). Cannot be set via API."""
    createdAt: Optional[datetime] = None
    """The datetime that the block version was created. Cannot be set via API."""


@dataclass(kw_only=True)
class BoundingBoxWithScore(ApiBaseModel):
    label: str
    x: float
    y: float
    width: float
    height: float
    score: float


@dataclass(kw_only=True)
class AnomalyResult(ApiBaseModel):
    boxes: Optional[List[BoundingBoxWithScore]] = None
    """For visual anomaly detection. An array of bounding box objects, (x, y, width, height, score, label), one per detection in the image. Filtered by the minimum confidence rating of the learn block."""
    scores: Optional[List[Optional[List[Optional[float]]]]] = None
    """2D array of shape (n, n) with raw anomaly scores for visual anomaly detection, where n can be calculated as ((1/8 of image input size)/2 - 1). The scores corresponds to each grid cell in the image's spatial matrix."""
    meanScore: Optional[float] = None
    """Mean value of the scores."""
    maxScore: Optional[float] = None
    """Maximum value of the scores."""


@dataclass(kw_only=True)
class StructuredClassifyResult(ApiBaseModel):
    boxes: List[List[float]]
    """For object detection. An array of bounding box arrays, (x, y, width, height), one per detection in the image."""
    scores: List[float]
    """For object detection. An array of probability scores, one per detection in the image."""
    mAP: float
    """For object detection. A score that indicates accuracy compared to the ground truth, if available."""
    f1: float
    """For FOMO. A score that combines the precision and recall of a classifier into a single metric, if available."""
    precision: float
    """A measure of how many of the positive predictions made are correct (true positives)."""
    recall: float
    """A measure of how many of the positive cases the classifier correctly predicted, over all the positive cases."""
    labels: Optional[List[Optional[str]]] = None
    """For object detection. An array of labels, one per detection in the image."""
    debugInfoJson: Optional[str] = None
    """Debug info in JSON format"""


@dataclass(kw_only=True)
class ClassifySampleResponseClassificationDetails(ApiBaseModel):
    boxes: Optional[List[Optional[List[Optional[float]]]]] = None
    """Bounding boxes predicted by localization model"""
    labels: Optional[List[Optional[float]]] = None
    """Labels predicted by localization model"""
    scores: Optional[List[Optional[float]]] = None
    """Scores predicted by localization model"""
    mAP: Optional[float] = None
    """For object detection, the COCO mAP computed for the predictions on this image"""
    f1: Optional[float] = None
    """For FOMO, the F1 score computed for the predictions on this image"""


@dataclass(kw_only=True)
class ObjectDetectionLastLayer(Enum):
    mobilenet_ssd = "mobilenet-ssd"
    fomo = "fomo"
    yolov2_akida = "yolov2-akida"
    yolov5 = "yolov5"
    yolov5v5_drpai = "yolov5v5-drpai"
    yolox = "yolox"
    yolov7 = "yolov7"
    tao_retinanet = "tao-retinanet"
    tao_ssd = "tao-ssd"
    tao_yolov3 = "tao-yolov3"
    tao_yolov4 = "tao-yolov4"


@dataclass(kw_only=True)
class ClassifySampleResponseClassification(ApiBaseModel):
    learnBlock: ImpulseLearnBlock
    result: List[Dict[str, float]]
    """Classification result, one item per window."""
    minimumConfidenceRating: float
    """The minimum confidence rating for this block. For regression, this is the absolute error (which can be larger than 1)."""
    expectedLabels: List[StructuredLabel]
    """An array with an expected label per window."""
    anomalyResult: Optional[List[AnomalyResult]] = None
    """Anomaly scores and computed metrics for visual anomaly detection, one item per window."""
    structuredResult: Optional[List[StructuredClassifyResult]] = None
    """Results of inferencing that returns structured data, such as object detection"""
    details: Optional[List[ClassifySampleResponseClassificationDetails]] = None
    """Structured outputs and computed metrics for some model types (e.g. object detection), one item per window."""
    objectDetectionLastLayer: ObjectDetectionLastLayer = None


@dataclass(kw_only=True)
class ClassifySampleResponse(GenericApiResponse):
    classifications: List[ClassifySampleResponseClassification]
    sample: RawSampleData
    windowSizeMs: int
    """Size of the sliding window (as set by the impulse) in milliseconds."""
    windowIncreaseMs: int
    """Number of milliseconds that the sliding window increased with (as set by the impulse)"""
    alreadyInDatabase: bool
    """Whether this sample is already in the training database"""
    warning: Optional[str] = None


@dataclass(kw_only=True)
class KerasModelVariantEnum(Enum):
    int8 = "int8"
    float32 = "float32"
    akida = "akida"


@dataclass(kw_only=True)
class ClassifySampleResponseVariantResults(ApiBaseModel):
    variant: KerasModelVariantEnum
    """The model variant"""
    classifications: List[ClassifySampleResponseClassification]


@dataclass(kw_only=True)
class ClassifySampleResponseMultipleVariants(GenericApiResponse):
    sample: RawSampleData
    windowSizeMs: int
    """Size of the sliding window (as set by the impulse) in milliseconds."""
    windowIncreaseMs: int
    """Number of milliseconds that the sliding window increased with (as set by the impulse)"""
    alreadyInDatabase: bool
    """Whether this sample is already in the training database"""
    results: Optional[List[ClassifySampleResponseVariantResults]] = None


@dataclass(kw_only=True)
class ModelResult(ApiBaseModel):
    sampleId: int
    sample: Sample
    classifications: List[ClassifySampleResponseClassification]


@dataclass(kw_only=True)
class ModelPrediction(ApiBaseModel):
    sampleId: int
    startMs: float
    endMs: float
    prediction: str
    label: Optional[str] = None
    predictionCorrect: Optional[bool] = None
    f1Score: Optional[float] = None
    """Only set for object detection projects"""
    anomalyScores: Optional[List[Optional[List[Optional[float]]]]] = None
    """Only set for visual anomaly projects. 2D array of shape (n, n) with raw anomaly scores, where n varies based on the image input size and the specific visual anomaly algorithm used. The scores corresponds to each grid cell in the image's spatial matrix."""


@dataclass(kw_only=True)
class TotalSummary(ApiBaseModel):
    good: int
    bad: int


@dataclass(kw_only=True)
class SummaryPerClass(ApiBaseModel):
    good: int
    bad: int


@dataclass(kw_only=True)
class Accuracy(ApiBaseModel):
    totalSummary: TotalSummary
    summaryPerClass: Dict[str, SummaryPerClass]
    confusionMatrixValues: Dict[str, Dict[str, float]]
    allLabels: List[str]
    accuracyScore: Optional[float] = None
    mseScore: Optional[float] = None


@dataclass(kw_only=True)
class AdditionalMetric(ApiBaseModel):
    name: str
    value: str
    fullPrecisionValue: float
    tooltipText: Optional[str] = None
    link: Optional[str] = None


@dataclass(kw_only=True)
class AdditionalMetricsByLearnBlock(ApiBaseModel):
    learnBlockId: int
    learnBlockName: str
    additionalMetrics: List[AdditionalMetric]


@dataclass(kw_only=True)
class ClassifyJobResponse(GenericApiResponse):
    result: List[ModelResult]
    predictions: List[ModelPrediction]
    accuracy: Accuracy
    additionalMetricsByLearnBlock: List[AdditionalMetricsByLearnBlock]
    availableVariants: List[KerasModelVariantEnum]
    """List of all model variants for which classification results exist"""


@dataclass(kw_only=True)
class ClassifyJobResponsePage(GenericApiResponse):
    result: List[ModelResult]
    predictions: List[ModelPrediction]


@dataclass(kw_only=True)
class MetricsForModelVariant(ApiBaseModel):
    variant: KerasModelVariantEnum
    """The model variant"""
    accuracy: Optional[float] = None
    """The overall accuracy for the given model variant"""


@dataclass(kw_only=True)
class MetricsAllVariantsResponse(GenericApiResponse):
    metrics: Optional[List[MetricsForModelVariant]] = None


@dataclass(kw_only=True)
class EvaluateResultValue(ApiBaseModel):
    raw: Optional[float] = None
    """The value based on the model alone"""
    withAnomaly: Optional[float] = None
    """The value including the result of anomaly detection"""


@dataclass(kw_only=True)
class KerasModelTypeEnum(Enum):
    int8 = "int8"
    float32 = "float32"
    akida = "akida"
    requiresRetrain = "requiresRetrain"


@dataclass(kw_only=True)
class ModelVariantStats(ApiBaseModel):
    modelType: KerasModelTypeEnum
    """The type of model"""
    learnBlockId: int
    """The learning block this model variant is from"""
    learnBlockType: LearnBlockType
    confusionMatrix: Dict[str, Dict[str, EvaluateResultValue]]
    """A map from actual labels to predicted labels, where actual labels are listed in `trainingLabels` and possible predicted labels are listed in `classificationLabels`."""
    trainingLabels: List[str]
    """The labels present in the model's training data. These are all present in the first dimension of the confusion matrix."""
    classificationLabels: List[str]
    """The possible labels resulting from classification. These may be present in the second dimension of the confusion matrix."""
    accuracy: EvaluateResultValue
    """The model's accuracy as a percentage"""
    totalWindowCount: Optional[int] = None
    """The total number of windows that were evaluated"""
    totalCorrectWindowCount: EvaluateResultValue = None
    """The total number of windows that the model classified correctly"""


@dataclass(kw_only=True)
class EvaluateJobResponse(GenericApiResponse):
    result: List[ModelVariantStats]


@dataclass(kw_only=True)
class TargetConstraintsSelectedTargetBasedOnEnum(Enum):
    user_configured = "user-configured"
    default = "default"
    default_accepted = "default-accepted"
    recent_project = "recent-project"
    connected_device = "connected-device"


@dataclass(kw_only=True)
class ResourceRange(ApiBaseModel):
    minimum: Optional[float] = None
    maximum: Optional[float] = None


@dataclass(kw_only=True)
class MemorySpec(ApiBaseModel):
    fastBytes: ResourceRange = None
    slowBytes: ResourceRange = None


@dataclass(kw_only=True)
class TargetMemory(ApiBaseModel):
    ram: MemorySpec = None
    rom: MemorySpec = None


@dataclass(kw_only=True)
class TargetProcessor(ApiBaseModel):
    part: Optional[str] = None
    """The exact part number, if available"""
    format: Optional[str] = None
    """Processor type, serving as a broad descriptor for the intended use-case"""
    architecture: Optional[str] = None
    """Processor family, informing about the processor's instruction set and core design"""
    specificArchitecture: Optional[str] = None
    """Processor architecture, informing about the specific processor, if known"""
    accelerator: Optional[str] = None
    """Target accelerator, if any"""
    fpu: Optional[bool] = None
    """Does the target processor have a floating point unit"""
    clockRateMhz: ResourceRange = None
    """Clock rate of the processor"""
    memory: TargetMemory = None


@dataclass(kw_only=True)
class TargetConstraintsDevice(ApiBaseModel):
    processors: Optional[List[TargetProcessor]] = None
    """Target processors"""
    board: Optional[str] = None
    """The exact dev board part number, if available"""
    name: Optional[str] = None
    """Display name in Studio"""
    latencyDevice: Optional[str] = None
    """MCU identifier, if available"""


@dataclass(kw_only=True)
class ApplicationBudget(ApiBaseModel):
    latencyPerInferenceMs: ResourceRange = None
    energyPerInferenceJoules: ResourceRange = None
    memoryOverhead: TargetMemory = None


@dataclass(kw_only=True)
class TargetConstraints(ApiBaseModel):
    targetDevices: List[TargetConstraintsDevice]
    """The potential targets for the project, where each entry captures hardware attributes that allow target guidance throughout the Studio workflow. The first target in the list is considered as the selected target for the project."""
    applicationBudgets: List[ApplicationBudget]
    """A list of application budgets to be configured based on target device. An application budget enables guidance on performance and resource usage. The first application budget in the list is considered as the selected budget for the project."""
    selectedTargetBasedOn: TargetConstraintsSelectedTargetBasedOnEnum = None


@dataclass(kw_only=True)
class AllProjectModelVariants(ApiBaseModel):
    pass


@dataclass(kw_only=True)
class ProjectModelVariant(ApiBaseModel):
    variant: KerasModelVariantEnum
    isReferenceVariant: bool
    """True if this model variant is the default or "reference variant" for this project"""
    isEnabled: bool
    """True if profiling for this model variant is enabled for the current project"""
    isSelected: bool
    """True if this is the selected model variant for this project, used to keep the same view after refreshing. Update this via defaultProfilingVariant in UpdateProjectRequest."""


@dataclass(kw_only=True)
class ImpulseInputBlockTypeEnum(Enum):
    time_series = "time-series"
    image = "image"
    features = "features"


@dataclass(kw_only=True)
class ImpulseInputBlockResizeModeEnum(Enum):
    squash = "squash"
    fit_short = "fit-short"
    fit_long = "fit-long"
    crop = "crop"


@dataclass(kw_only=True)
class ImpulseInputBlockResizeMethodEnum(Enum):
    lanczos3 = "lanczos3"
    nearest = "nearest"


@dataclass(kw_only=True)
class ImpulseInputBlockCropAnchorEnum(Enum):
    top_left = "top-left"
    top_center = "top-center"
    top_right = "top-right"
    middle_left = "middle-left"
    middle_center = "middle-center"
    middle_right = "middle-right"
    bottom_left = "bottom-left"
    bottom_center = "bottom-center"
    bottom_right = "bottom-right"


@dataclass(kw_only=True)
class ImpulseInputBlockDatasetSubset(ApiBaseModel):
    subsetModulo: Optional[float] = None
    subsetSeed: Optional[float] = None


@dataclass(kw_only=True)
class ImpulseInputBlock(ApiBaseModel):
    id: int
    """Identifier for this block. Make sure to up this number when creating a new block, and don't re-use identifiers. If the block hasn't changed, keep the ID as-is. ID must be unique across the project and greather than zero (>0)."""
    type: ImpulseInputBlockTypeEnum
    name: str
    """Block name, will be used in menus"""
    title: str
    """Block title, used in the impulse UI"""
    windowSizeMs: Optional[int] = None
    """Size of the sliding window in milliseconds"""
    windowIncreaseMs: Optional[int] = None
    """We use a sliding window to go over the raw data. How many milliseconds to increase the sliding window with for each step."""
    frequencyHz: Optional[float] = None
    """(Input only) Frequency of the input data in Hz"""
    classificationWindowIncreaseMs: Optional[int] = None
    """We use a sliding window to go over the raw data. How many milliseconds to increase the sliding window with for each step in classification mode."""
    padZeros: Optional[bool] = None
    """Whether to zero pad data when a data item is too short"""
    imageWidth: Optional[int] = None
    """Width all images are resized to before training"""
    imageHeight: Optional[int] = None
    """Width all images are resized to before training"""
    resizeMode: ImpulseInputBlockResizeModeEnum = None
    resizeMethod: ImpulseInputBlockResizeMethodEnum = None
    cropAnchor: ImpulseInputBlockCropAnchorEnum = None
    description: Optional[str] = None
    """A short description of the block version, displayed in the block versioning UI"""
    createdBy: Optional[str] = None
    """The system component that created the block version (createImpulse | clone | tuner). Cannot be set via API."""
    createdAt: Optional[datetime] = None
    """The datetime that the block version was created. Cannot be set via API."""
    datasetSubset: ImpulseInputBlockDatasetSubset = None


@dataclass(kw_only=True)
class ImpulseDspBlockOrganization(ApiBaseModel):
    id: int
    dspId: int


@dataclass(kw_only=True)
class NamedAxes(ApiBaseModel):
    name: str
    """Name of the axis"""
    description: Optional[str] = None
    """Description of the axis"""
    required: Optional[bool] = None
    """Whether the axis is required"""
    selectedAxis: Optional[str] = None
    """The selected axis for the block"""


@dataclass(kw_only=True)
class ImpulseDspBlock(ApiBaseModel):
    id: int
    """Identifier for this block. Make sure to up this number when creating a new block, and don't re-use identifiers. If the block hasn't changed, keep the ID as-is. ID must be unique across the project and greather than zero (>0)."""
    type: str
    """Block type"""
    name: str
    """Block name, will be used in menus"""
    axes: List[str]
    """Input axes, identified by the name in the name of the axis"""
    title: str
    """Block title, used in the impulse UI"""
    implementationVersion: int
    """Implementation version of the block"""
    valuesPerAxis: Optional[int] = None
    """Number of features this DSP block outputs per axis. This is only set when the DSP block is configured."""
    input: Optional[int] = None
    """The ID of the Input block a DSP block is connected to"""
    description: Optional[str] = None
    """A short description of the block version, displayed in the block versioning UI"""
    createdBy: Optional[str] = None
    """The system component that created the block version (createImpulse | clone | tuner). Cannot be set via API."""
    createdAt: Optional[datetime] = None
    """The datetime that the block version was created. Cannot be set via API."""
    organization: ImpulseDspBlockOrganization = None
    customUrl: Optional[str] = None
    """Required for type 'custom'"""
    namedAxes: Optional[List[Optional[NamedAxes]]] = None
    """Named axes for the block"""


@dataclass(kw_only=True)
class CreateImpulseRequest(ApiBaseModel):
    inputBlocks: List[ImpulseInputBlock]
    """Input Blocks that are part of this impulse"""
    dspBlocks: List[ImpulseDspBlock]
    """DSP Blocks that are part of this impulse"""
    learnBlocks: List[ImpulseLearnBlock]
    """Learning Blocks that are part of this impulse"""
    name: Optional[str] = None
    """Name for this impulse (optional). If no name is provided one is created based on your blocks."""


@dataclass(kw_only=True)
class CreateImpulseResponse(GenericApiResponse):
    id: int
    """ID of the new impulse"""


@dataclass(kw_only=True)
class CreateNewEmptyImpulseResponse(GenericApiResponse):
    id: int
    """ID of the new impulse"""
    redirectUrl: str
    """Link to redirect the user to afterwards"""


@dataclass(kw_only=True)
class Impulse(ApiBaseModel):
    created: bool
    """Whether an impulse was created"""
    configured: bool
    """Whether an impulse was configured"""
    complete: bool
    """Whether an impulse was fully trained and configured"""


@dataclass(kw_only=True)
class DspRunRequestWithFeatures(ApiBaseModel):
    features: List[int]
    """Array of features. If you have multiple axes the data should be interleaved (e.g. [ax0_val0, ax1_val0, ax2_val0, ax0_val1, ax1_val1, ax2_val1])."""
    params: Dict[str, str]
    """DSP parameters with values"""
    drawGraphs: bool
    """Whether to generate graphs (will take longer)"""
    requestPerformance: bool
    """Whether to request performance info (will take longer unless cached)"""


@dataclass(kw_only=True)
class DspRunRequestWithoutFeatures(ApiBaseModel):
    params: Dict[str, str]
    """DSP parameters with values"""
    store: bool
    """Whether to store the DSP parameters as the new default parameters."""


@dataclass(kw_only=True)
class DspRunRequestWithoutFeaturesReadOnly(ApiBaseModel):
    params: Dict[str, str]
    """DSP parameters with values"""


@dataclass(kw_only=True)
class DspRunGraphAxisLabels(ApiBaseModel):
    X: str
    y: str


@dataclass(kw_only=True)
class DspRunGraph(ApiBaseModel):
    name: str
    """Name of the graph"""
    type: str
    """Type of graph (either `logarithmic`, `linear` or `image`)"""
    image: Optional[str] = None
    """Base64 encoded image, only present if type is 'image'"""
    imageMimeType: Optional[str] = None
    """Mime type of the Base64 encoded image, only present if type is 'image'"""
    X: Optional[Dict[str, Optional[List[Optional[float]]]]] = None
    """Values on the x-axis per plot. Key is the name of the raw feature. Present if type is 'logarithmic' or 'linear'."""
    y: Optional[List[Optional[float]]] = None
    """Values of the y-axis. Present if type is 'logarithmic' or 'linear'."""
    suggestedXMin: Optional[float] = None
    """Suggested minimum value of x-axis"""
    suggestedXMax: Optional[float] = None
    """Suggested maxium value of x-axis"""
    suggestedYMin: Optional[float] = None
    """Suggested minimum value of y-axis"""
    suggestedYMax: Optional[float] = None
    """Suggested maximum value of y-axis"""
    lineWidth: Optional[float] = None
    """Width of the graph line (if type is `logarithmic` or `linear`). Default 3."""
    smoothing: Optional[bool] = None
    """Whether to apply smoothing to the graph."""
    axisLabels: DspRunGraphAxisLabels = None
    highlights: Optional[Dict[str, Optional[List[Optional[float]]]]] = None
    """Indices of points to highlight, per axis."""


@dataclass(kw_only=True)
class Performance(ApiBaseModel):
    latency: int
    ram: int


@dataclass(kw_only=True)
class DspRunResponse(GenericApiResponse):
    features: List[float]
    """Array of processed features. Laid out according to the names in 'labels'"""
    graphs: List[DspRunGraph]
    """Graphs to plot to give an insight in how the DSP process ran"""
    labels: Optional[List[Optional[str]]] = None
    """Labels of the feature axes"""
    state_string: Optional[str] = None
    """String representation of the DSP state returned"""
    performance: Optional[Performance] = None


@dataclass(kw_only=True)
class DspRunResponseWithSample(GenericApiResponse):
    features: List[float]
    """Array of processed features. Laid out according to the names in 'labels'"""
    graphs: List[DspRunGraph]
    """Graphs to plot to give an insight in how the DSP process ran"""
    sample: RawSampleData
    canProfilePerformance: bool
    labels: Optional[List[Optional[str]]] = None
    """Labels of the feature axes"""
    state_string: Optional[str] = None
    """String representation of the DSP state returned"""
    labelAtEndOfWindow: Optional[str] = None
    """Label for the window (only present for time-series data)"""
    performance: Optional[Performance] = None


@dataclass(kw_only=True)
class DspFeatureLabelsResponse(GenericApiResponse):
    labels: List[str]


@dataclass(kw_only=True)
class Data(ApiBaseModel):
    X: Dict[str, float]
    """Data by feature index for this window"""
    y: int
    """Training label index"""
    yLabel: str
    """Training label string"""
    sample: Optional[Sample] = None


@dataclass(kw_only=True)
class DspTrainedFeaturesResponse(GenericApiResponse):
    totalSampleCount: int
    """Total number of windows in the data set"""
    data: List[Data]
    skipFirstFeatures: int
    """When showing the processed features, skip the first X features. This is used in dimensionality reduction where artificial features are introduced in the response (on the first few positions)."""


@dataclass(kw_only=True)
class XXYSampleClash1150288656(ApiBaseModel):
    id: int
    name: str
    startMs: float
    endMs: float


@dataclass(kw_only=True)
class XXYDataClash405219629(ApiBaseModel):
    X: List[float]
    """Feature data for this window"""
    y: int
    """Training label index"""
    yLabel: str
    """Training label string"""
    sample: Optional[XXYSampleClash1150288656] = None


@dataclass(kw_only=True)
class DspSampleFeaturesResponse(GenericApiResponse):
    totalSampleCount: int
    """Total number of windows in the data set"""
    data: List[XXYDataClash405219629]
    skipFirstFeatures: int
    """When showing the processed features, skip the first X features. This is used in dimensionality reduction where artificial features are introduced in the response (on the first few positions)."""


@dataclass(kw_only=True)
class Category(Enum):
    training = "training"
    testing = "testing"


@dataclass(kw_only=True)
class XXYSampleClash650381201(ApiBaseModel):
    id: float
    name: str
    startMs: float
    endMs: float
    category: Category


@dataclass(kw_only=True)
class XXYDataClash778903379(ApiBaseModel):
    X: Dict[str, float]
    """Data by feature index for this window"""
    y: int
    """Training label index"""
    yLabel: str
    """Training label string"""
    sample: Optional[XXYSampleClash650381201] = None


@dataclass(kw_only=True)
class GetDataExplorerFeaturesResponse(GenericApiResponse):
    hasFeatures: bool
    data: List[XXYDataClash778903379]
    inputBlock: ImpulseInputBlock = None


@dataclass(kw_only=True)
class HasDataExplorerFeaturesResponse(GenericApiResponse):
    hasFeatures: bool
    inputBlock: ImpulseInputBlock = None


@dataclass(kw_only=True)
class ClusterInfos(ApiBaseModel):
    idx: int
    """Unique index of the cluster"""
    indexes: List[int]
    """Indexes of all windows contained in the cluster (for debugging)"""
    windows: List[List[int]]
    """The sample ID and window start and end of every window in the cluster"""
    vendiScore: float
    """Raw vendi score"""
    vendiRatio: float
    """Vendi score expressed as ratio from 0 to 1"""
    count: int
    """The number if windows in the cluster"""
    distance: float
    """The distance of the cluster from the origin"""
    leftIdx: int
    """The cluster id on the left branch of the dendrogram"""
    rightIdx: int
    """The cluster id on the right branch of the dendrogram"""
    samples: Optional[List[Sample]] = None
    """Details of every sample in the cluster"""


@dataclass(kw_only=True)
class XXYDataClash1554249175(ApiBaseModel):
    maxDistance: float
    clusterInfos: List[ClusterInfos]
    labelId: Optional[float] = None


@dataclass(kw_only=True)
class GetDiversityDataResponse(GenericApiResponse):
    data: Optional[List[Optional[XXYDataClash1554249175]]] = None


@dataclass(kw_only=True)
class Windows(ApiBaseModel):
    windowStart: int
    """The start time of this window in milliseconds"""
    windowEnd: int
    """The end time of this window in milliseconds"""
    score: float
    """The cosine similarity score between this window and a window from the sample in the parent object."""


@dataclass(kw_only=True)
class Issues(ApiBaseModel):
    id: int
    """The ID of this sample"""
    label: int
    """The label of this sample, in index form"""
    windows: List[Windows]
    """The windows in this sample that are symptomatic of this issue."""
    sample: Sample = None
    """Detailed information about the sample"""


@dataclass(kw_only=True)
class CosineSimilarityIssue(ApiBaseModel):
    id: int
    """The ID of this sample"""
    label: int
    """The label of this sample, in index form"""
    issues: List[Issues]
    """A list of samples that have windows that are symptomatic of this issue."""
    sample: Sample = None
    """Detailed information about the sample"""


@dataclass(kw_only=True)
class CosineSimilarityData(ApiBaseModel):
    similarButDifferentLabel: List[CosineSimilarityIssue]
    """A list of samples that have windows that are similar to windows of other samples that have a different label."""
    differentButSameLabel: List[CosineSimilarityIssue]
    """A list of samples that have windows that are dissimilar to windows of other samples that have the same label."""


@dataclass(kw_only=True)
class NeighborWindows(ApiBaseModel):
    id: int
    """The ID of the sample this window belongs to"""
    windowStart: int
    """The start time of this window in milliseconds"""
    windowEnd: int
    """The end time of this window in milliseconds"""
    sample: Sample = None
    """Detailed information about the sample this window belongs to"""


@dataclass(kw_only=True)
class NeighborsScore(ApiBaseModel):
    id: int
    """The ID of the sample this window belongs to"""
    windowStart: int
    """The start time of this window in milliseconds"""
    windowEnd: int
    """The end time of this window in milliseconds"""
    score: float
    """The label noise score for this window, from 0 to the total number of windows."""
    neighborWindows: List[NeighborWindows]
    """Details of the nearest neighbors to this window"""
    sample: Sample = None
    """Detailed information about the sample this window belongs to"""


@dataclass(kw_only=True)
class NeighborsData(ApiBaseModel):
    scoresAndNeighbors: List[NeighborsScore]
    """The label noise score and nearest neighbors for each window of data in the project that shows a potential label noise issue."""
    numNeighbors: int
    """The number of neighbors used in the nearest neighbors algorithm."""


@dataclass(kw_only=True)
class Scores(ApiBaseModel):
    id: int
    """The ID of the sample this window belongs to"""
    windowStart: int
    """The start time of this window in milliseconds"""
    windowEnd: int
    """The end time of this window in milliseconds"""
    label: int
    """The label of this window, in index form"""
    probability: float
    """The probability of this window being the label it was assigned, as estimated by a classifier trained on the whole dataset."""
    score: float
    """The z-score of the probability with respect to other class members, so that outliers (i.e. windows whose probability is low) can be easily spotted. This assumes that most correctly labelled class members will have a high probability."""
    sample: Sample = None
    """Detailed information about the sample this window belongs to"""


@dataclass(kw_only=True)
class CrossValidationData(ApiBaseModel):
    scores: List[Scores]


@dataclass(kw_only=True)
class XXYDataClash512802137(ApiBaseModel):
    cosineSimilarity: CosineSimilarityData = None
    neighbors: NeighborsData = None
    crossValidation: CrossValidationData = None


@dataclass(kw_only=True)
class GetLabelNoiseDataResponse(GenericApiResponse):
    data: XXYDataClash512802137


@dataclass(kw_only=True)
class KerasModelLayerInput(ApiBaseModel):
    shape: int
    """Input size"""
    name: str
    """TensorFlow name"""
    type: str
    """TensorFlow type"""


@dataclass(kw_only=True)
class KerasModelLayerOutput(ApiBaseModel):
    shape: int
    """Output size"""
    name: str
    """TensorFlow name"""
    type: str
    """TensorFlow type"""


@dataclass(kw_only=True)
class KerasModelLayer(ApiBaseModel):
    input: KerasModelLayerInput
    output: KerasModelLayerOutput


@dataclass(kw_only=True)
class KerasModelMetadataMetricsVisualizationEnum(Enum):
    featureExplorer = "featureExplorer"
    dataExplorer = "dataExplorer"
    none = "none"


@dataclass(kw_only=True)
class Tflite(ApiBaseModel):
    ramRequired: int
    romRequired: int
    arenaSize: int
    modelSize: int


@dataclass(kw_only=True)
class Eon(ApiBaseModel):
    ramRequired: int
    romRequired: int
    arenaSize: int
    modelSize: int


@dataclass(kw_only=True)
class Eon_ram_optimized(ApiBaseModel):
    ramRequired: int
    romRequired: int
    arenaSize: int
    modelSize: int


@dataclass(kw_only=True)
class KerasCustomMetric(ApiBaseModel):
    name: str
    """The name of the metric"""
    value: str
    """The value of this metric for this model type"""


@dataclass(kw_only=True)
class OnDevicePerformance(ApiBaseModel):
    mcu: str
    name: str
    isDefault: bool
    latency: float
    tflite: Tflite
    eon: Eon
    eon_ram_optimized: Optional[Eon_ram_optimized] = None
    customMetrics: Optional[List[KerasCustomMetric]] = None
    """Custom, device-specific performance metrics"""


@dataclass(kw_only=True)
class KerasModelMetadataMetrics(ApiBaseModel):
    type: KerasModelTypeEnum
    """The type of model"""
    loss: float
    """The model's loss on the validation set after training"""
    confusionMatrix: List[List[float]]
    report: Dict[str, Any]
    """Precision, recall, F1 and support scores"""
    onDevicePerformance: List[OnDevicePerformance]
    visualization: KerasModelMetadataMetricsVisualizationEnum
    isSupportedOnMcu: bool
    additionalMetrics: List[AdditionalMetric]
    accuracy: Optional[float] = None
    """The model's accuracy on the validation set after training"""
    predictions: Optional[List[ModelPrediction]] = None
    mcuSupportError: Optional[str] = None
    profilingJobId: Optional[int] = None
    """If this is set, then we're still profiling this model. Subscribe to job updates to see when it's done (afterward the metadata will be updated)."""
    profilingJobFailed: Optional[bool] = None
    """If this is set, then the profiling job failed (get the status by getting the job logs for 'profilingJobId')."""


@dataclass(kw_only=True)
class KerasModelMode(Enum):
    classification = "classification"
    regression = "regression"
    object_detection = "object-detection"
    visual_anomaly = "visual-anomaly"
    anomaly_gmm = "anomaly-gmm"


@dataclass(kw_only=True)
class KerasModelMetadataModeEnum(Enum):
    classification = "classification"
    regression = "regression"
    object_detection = "object-detection"
    visual_anomaly = "visual-anomaly"
    anomaly_gmm = "anomaly-gmm"


@dataclass(kw_only=True)
class ImageInputScaling(Enum):
    _0__1 = "0..1"
    _1__1 = "-1..1"
    _128__127 = "-128..127"
    _0__255 = "0..255"
    torch = "torch"
    bgr_subtract_imagenet_mean = "bgr-subtract-imagenet-mean"


@dataclass(kw_only=True)
class KerasModelMetadata(ApiBaseModel):
    created: datetime
    """Date when the model was trained"""
    layers: List[KerasModelLayer]
    """Layers of the neural network"""
    classNames: List[str]
    """Labels for the output layer"""
    labels: List[str]
    """Original labels in the dataset when features were generated, e.g. used to render the feature explorer."""
    availableModelTypes: List[KerasModelTypeEnum]
    """The types of model that are available"""
    recommendedModelType: KerasModelTypeEnum
    """The model type that is recommended for use"""
    modelValidationMetrics: List[KerasModelMetadataMetrics]
    """Metrics for each of the available model types"""
    hasTrainedModel: bool
    mode: KerasModelMetadataModeEnum
    imageInputScaling: ImageInputScaling
    objectDetectionLastLayer: ObjectDetectionLastLayer = None


@dataclass(kw_only=True)
class KerasModelMetadataResponse(GenericApiResponse, KerasModelMetadata):
    pass


@dataclass(kw_only=True)
class UploadKerasFilesRequest(ApiBaseModel):
    zip: bytes


@dataclass(kw_only=True)
class AddKerasFilesRequest(ApiBaseModel):
    zip: bytes


@dataclass(kw_only=True)
class SetLegacyImpulseStateInternalRequest(ApiBaseModel):
    zip: bytes
    impulse: bytes
    config: bytes


@dataclass(kw_only=True)
class Clusters(ApiBaseModel):
    center: List[float]
    """Center of each cluster (one value per axis)"""
    maxError: float
    """Size of the cluster"""


@dataclass(kw_only=True)
class AnomalyModelMetadata(ApiBaseModel):
    created: datetime
    """Date when the model was trained"""
    scale: List[float]
    """Scale input for StandardScaler. Values are scaled like this (where `ix` is axis index): `input[ix] = (input[ix] - mean[ix]) / scale[ix];`"""
    mean: List[float]
    """Mean input for StandardScaler. Values are scaled like this (where `ix` is axis index): `input[ix] = (input[ix] - mean[ix]) / scale[ix];`"""
    clusters: List[Clusters]
    """Trained K-means clusters"""
    axes: List[int]
    """Which axes were included during training (by index)"""
    defaultMinimumConfidenceRating: Optional[float] = None
    """Default minimum confidence rating required before tagging as anomaly, based on scores of training data (GMM only)."""
    availableModelTypes: Optional[List[KerasModelTypeEnum]] = None
    """The types of model that are available"""
    recommendedModelType: KerasModelTypeEnum = None
    """The model type that is recommended for use"""
    modelValidationMetrics: Optional[List[KerasModelMetadataMetrics]] = None
    """Metrics for each of the available model types"""
    hasTrainedModel: Optional[bool] = None


@dataclass(kw_only=True)
class AnomalyModelMetadataResponse(GenericApiResponse, AnomalyModelMetadata):
    pass


@dataclass(kw_only=True)
class AnomalyGmmMetadata(ApiBaseModel):
    means: List[List[float]]
    """2D array of shape (n, m)"""
    covariances: List[List[List[float]]]
    """3D array of shape (n, m, m)"""
    weights: List[float]
    """1D array of shape (n,)"""


@dataclass(kw_only=True)
class AnomalyGmmMetadataResponse(GenericApiResponse, AnomalyGmmMetadata):
    pass


@dataclass(kw_only=True)
class XXYDataClash78845026(ApiBaseModel):
    X: Dict[str, float]
    """Data by feature index for this window. Note that this data was scaled by the StandardScaler, use the anomaly metadata to unscale if needed."""
    label: Optional[float] = None
    """Label used for datapoint colorscale in anomaly explorer (for gmm only). Is currently the result of the scoring function."""


@dataclass(kw_only=True)
class AnomalyTrainedFeaturesResponse(GenericApiResponse):
    totalSampleCount: int
    """Total number of windows in the data set"""
    data: List[XXYDataClash78845026]


@dataclass(kw_only=True)
class GenerateFeaturesRequest(ApiBaseModel):
    dspId: int
    """DSP block ID to generate features for"""
    calculateFeatureImportance: Optional[bool] = None
    """Whether to generate feature importance (only when available)"""
    skipFeatureExplorer: Optional[bool] = None
    """If set, skips feature explorer (used in tests)"""


@dataclass(kw_only=True)
class AutotuneDspRequest(ApiBaseModel):
    dspId: int
    """DSP block ID to autotune parameters of"""


@dataclass(kw_only=True)
class ListModelsResponse(GenericApiResponse):
    id: Optional[int] = None
    """projectId"""


@dataclass(kw_only=True)
class StartTrainingRequestAnomaly(ApiBaseModel):
    axes: List[int]
    """Which axes (indexes from DSP script) to include in the training set"""
    minimumConfidenceRating: float
    """Minimum confidence rating required before tagging as anomaly"""
    clusterCount: Optional[int] = None
    """Number of clusters for K-means, or number of components for GMM"""
    skipEmbeddingsAndMemory: Optional[bool] = None
    """If set, skips creating embeddings and measuring memory (used in tests)"""


@dataclass(kw_only=True)
class StartJobResponse(GenericApiResponse):
    id: int
    """Job identifier. Status updates will include this identifier."""


@dataclass(kw_only=True)
class Download(ApiBaseModel):
    name: str
    type: str
    link: str
    id: Optional[str] = None
    size: Optional[str] = None
    impulseId: Optional[float] = None


@dataclass(kw_only=True)
class DeviceRemoteMgmtModeEnum(Enum):
    disconnected = "disconnected"
    ingestion = "ingestion"
    inference = "inference"


@dataclass(kw_only=True)
class DeviceInferenceInfoModelTypeEnum(Enum):
    classification = "classification"
    objectDetection = "objectDetection"
    constrainedObjectDetection = "constrainedObjectDetection"


@dataclass(kw_only=True)
class DeviceInferenceInfo(ApiBaseModel):
    projectId: int
    projectOwner: str
    projectName: str
    deployedVersion: int
    modelType: DeviceInferenceInfoModelTypeEnum = None


@dataclass(kw_only=True)
class Sensors(ApiBaseModel):
    name: str
    maxSampleLengthS: int
    """Maximum supported sample length in seconds"""
    frequencies: List[float]
    """Supported frequencies for this sensor in Hz."""


@dataclass(kw_only=True)
class Device(ApiBaseModel):
    id: int
    deviceId: str
    """Unique identifier (such as MAC address) for a device"""
    created: datetime
    lastSeen: datetime
    """Last message that was received from the device (ignoring keep-alive)"""
    name: str
    deviceType: str
    sensors: List[Sensors]
    remote_mgmt_connected: bool
    """Whether the device is connected to the remote management interface. This property is deprecated, use `remoteMgmtMode` instead."""
    supportsSnapshotStreaming: bool
    remoteMgmtMode: DeviceRemoteMgmtModeEnum
    remote_mgmt_host: Optional[str] = None
    """The remote management host that the device is connected to"""
    inferenceInfo: DeviceInferenceInfo = None


@dataclass(kw_only=True)
class ProjectDataSummary(ApiBaseModel):
    totalLengthMs: float
    """Total length (in ms.) of all data in the training set"""
    labels: List[str]
    """Labels in the training set"""
    dataCount: int


@dataclass(kw_only=True)
class LatencyDevice(ApiBaseModel):
    mcu: str
    name: str
    selected: bool
    int8Latency: float
    int8ConvLatency: float
    float32Latency: float
    float32ConvLatency: float
    helpText: str


@dataclass(kw_only=True)
class DataSummaryPerCategory(ApiBaseModel):
    training: ProjectDataSummary
    testing: ProjectDataSummary
    anomaly: ProjectDataSummary


@dataclass(kw_only=True)
class ComputeTime(ApiBaseModel):
    periodStartDate: datetime
    """Start of the current time period."""
    periodEndDate: datetime
    """End of the current time period. This is the date when the compute time resets again."""
    timeUsedMs: int
    """The amount of compute used for the current time period."""
    timeLeftMs: int
    """The amount of compute left for the current time period."""


@dataclass(kw_only=True)
class ViewType(Enum):
    list = "list"
    grid = "grid"


@dataclass(kw_only=True)
class AcquisitionSettings(ApiBaseModel):
    intervalMs: float
    """Interval during the last acquisition, or the recommended interval based on the data set."""
    lengthMs: int
    """Length of the last acquisition, or a recommended interval based on the data set."""
    segmentShift: bool
    """Whether to auto-shift segments"""
    defaultPageSize: int
    """Default page size on data acquisition"""
    viewType: ViewType
    """Default view type on data acquisition"""
    gridColumnCount: int
    """Number of grid columns in non-detailed view"""
    gridColumnCountDetailed: int
    """Number of grid columns in detailed view"""
    showExactSampleLength: bool
    """If enabled, does not round sample length to hours/minutes/seconds, but always displays sample length in milliseconds. E.g. instead of 1m 32s, this'll say 92,142ms."""
    inlineEditBoundingBoxes: bool
    """If enabled, allows editing bounding box labels directly from the acquisition UI."""
    sensor: Optional[str] = None
    """Sensor that was used during the last acquisition."""
    label: Optional[str] = None
    """Label that was used during the last acquisition."""
    segmentLength: Optional[float] = None
    """Length of the last sample segment after segmenting a larger sample."""


@dataclass(kw_only=True)
class ModelEngineShortEnum(Enum):
    tflite_eon = "tflite-eon"
    tflite_eon_ram_optimized = "tflite-eon-ram-optimized"
    tflite = "tflite"


@dataclass(kw_only=True)
class DeploySettings(ApiBaseModel):
    eonCompiler: bool
    sensor: Sensor
    arduinoLibraryName: str
    tinkergenLibraryName: str
    particleLibraryName: str
    lastDeployModelEngine: ModelEngineShortEnum = None
    """Model engine for last deploy"""


@dataclass(kw_only=True)
class Experiments(ApiBaseModel):
    type: str
    title: str
    enabled: bool
    showToUser: bool
    help: Optional[str] = None


@dataclass(kw_only=True)
class Urls(ApiBaseModel):
    mobileClient: Optional[str] = None
    """Base URL for the mobile client. If this is undefined then no development API key is set."""
    mobileClientComputer: Optional[str] = None
    """Base URL for collecting data with the mobile client from a computer. If this is undefined then no development API key is set."""
    mobileClientInference: Optional[str] = None
    """Base URL for running inference with the mobile client. If this is undefined then no development API key is set."""


@dataclass(kw_only=True)
class ShowGettingStartedWizard(ApiBaseModel):
    showWizard: bool
    step: int
    """Current step of the getting started wizard"""


@dataclass(kw_only=True)
class XXYPerformanceClash200866325(ApiBaseModel):
    gpu: bool
    jobLimitM: int
    """Compute time limit per job in minutes (applies only to DSP and learning jobs)."""
    dspFileSizeMb: int
    """Maximum size for DSP file output"""
    enterprisePerformance: bool
    trainJobRamMb: int
    """Amount of RAM allocated to training jobs"""


@dataclass(kw_only=True)
class Readme(ApiBaseModel):
    markdown: str
    html: str


@dataclass(kw_only=True)
class ProjectInfoResponse(GenericApiResponse):
    project: Project
    developmentKeys: DevelopmentKeys
    impulse: Impulse
    devices: List[Device]
    dataSummary: ProjectDataSummary
    dataSummaryPerCategory: DataSummaryPerCategory
    computeTime: ComputeTime
    acquisitionSettings: AcquisitionSettings
    collaborators: List[User]
    deploySettings: DeploySettings
    experiments: List[Experiments]
    """Experiments that the project has access to. Enabling experiments can only be done through a JWT token."""
    latencyDevices: List[LatencyDevice]
    urls: Urls
    showCreateFirstImpulse: bool
    showGettingStartedWizard: ShowGettingStartedWizard
    performance: XXYPerformanceClash200866325
    trainJobNotificationUids: List[int]
    """The IDs of users who should be notified when a Keras or retrain job is finished."""
    dspJobNotificationUids: List[int]
    """The IDs of users who should be notified when a DSP job is finished."""
    modelTestingJobNotificationUids: List[int]
    """The IDs of users who should be notified when a model testing job is finished."""
    exportJobNotificationUids: List[int]
    """The IDs of users who should be notified when an export job is finished."""
    hasNewTrainingData: bool
    studioUrl: str
    inPretrainedModelFlow: bool
    showSensorDataInAcquisitionGraph: bool
    """Whether to show the actual sensor data in acquisition charts (only applies when you have structured labels)"""
    notifications: List[str]
    """List of notifications to show within the project"""
    readme: Optional[Readme] = None
    """Present if a readme is set for this project"""
    csvImportConfig: Optional[Dict[str, Any]] = None
    """Config file specifying how to process CSV files."""
    dspPageSize: Optional[int] = None
    targetConstraints: TargetConstraints = None
    defaultImpulseId: Optional[int] = None
    """Default selected impulse (by ID)."""


@dataclass(kw_only=True)
class ListDevicesResponse(GenericApiResponse):
    devices: List[Device]


@dataclass(kw_only=True)
class GetDeviceResponse(GenericApiResponse):
    device: Device = None


@dataclass(kw_only=True)
class GetSampleResponse(GenericApiResponse, RawSampleData):
    pass


@dataclass(kw_only=True)
class GetSampleMetadataResponse(GenericApiResponse, ProjectSampleMetadata):
    pass


@dataclass(kw_only=True)
class ListSamplesResponse(GenericApiResponse):
    samples: List[Sample]
    totalCount: int


@dataclass(kw_only=True)
class CountSamplesResponse(GenericApiResponse):
    count: int


@dataclass(kw_only=True)
class RebalanceDatasetResponse(GenericApiResponse, DatasetRatioData):
    pass


@dataclass(kw_only=True)
class DSPGroupItemShowIfOperatorEnum(Enum):
    eq = "eq"
    neq = "neq"


@dataclass(kw_only=True)
class DSPGroupItemShowIf(ApiBaseModel):
    parameter: str
    operator: DSPGroupItemShowIfOperatorEnum
    value: str


@dataclass(kw_only=True)
class DSPGroupItemSectionEnum(Enum):
    advanced = "advanced"
    augmentation = "augmentation"
    modelProfiling = "modelProfiling"


@dataclass(kw_only=True)
class SelectOptions(ApiBaseModel):
    value: Optional[str] = None
    selected: Optional[bool] = None
    optionLabel: Optional[str] = None


@dataclass(kw_only=True)
class DSPGroupItem(ApiBaseModel):
    name: str
    defaultValue: str
    type: str
    param: str
    readonly: bool
    shouldShow: bool
    required: bool
    value: Optional[str] = None
    help: Optional[str] = None
    selectOptions: Optional[List[Optional[SelectOptions]]] = None
    showIf: DSPGroupItemShowIf = None
    invalidText: Optional[str] = None
    section: DSPGroupItemSectionEnum = None
    multiline: Optional[bool] = None
    """Only valid for type "string". Will render a multiline text area."""
    hint: Optional[str] = None
    """If set, shows a hint below the input."""
    placeholder: Optional[str] = None
    """Sets the placeholder text on the input element (for types "string", "int", "float" and "secret")"""


@dataclass(kw_only=True)
class DSPGroup(ApiBaseModel):
    group: str
    items: List[DSPGroupItem]


@dataclass(kw_only=True)
class DSPInfoFeatures(ApiBaseModel):
    generated: bool
    """Whether this block has generated features"""
    count: Optional[int] = None
    """Number of generated features"""
    labels: Optional[List[Optional[str]]] = None
    """Names of the features"""
    classes: Optional[List[Optional[str]]] = None
    """Classes that the features were generated on"""


@dataclass(kw_only=True)
class DSPInfoPerformance(ApiBaseModel):
    latency: int
    ram: int


@dataclass(kw_only=True)
class DSPInfo(ApiBaseModel):
    id: int
    name: str
    windowLength: int
    type: str
    classes: List[str]
    features: DSPInfoFeatures
    expectedWindowCount: int
    """Expected number of windows that would be generated"""
    inputAxes: List[str]
    """Axes that this block depends on."""
    canCalculateFeatureImportance: bool
    calculateFeatureImportance: bool
    performance: DSPInfoPerformance = None
    hasAutoTune: Optional[bool] = None
    """Whether this type of DSP block supports autotuning."""
    minimumVersionForAutotune: Optional[float] = None
    """For DSP blocks that support autotuning, this value specifies the minimum block implementation version for which autotuning is supported."""
    hasAutotunerResults: Optional[bool] = None
    """Whether autotune results exist for this DSP block."""
    usesState: Optional[bool] = None
    """Whether this DSP block uses state."""


@dataclass(kw_only=True)
class DSPConfig(ApiBaseModel):
    dsp: DSPInfo
    config: Optional[List[DSPGroup]] = None
    configError: Optional[str] = None


@dataclass(kw_only=True)
class DSPConfigResponse(GenericApiResponse, DSPConfig):
    pass


@dataclass(kw_only=True)
class DSPConfigRequest(ApiBaseModel):
    config: Dict[str, str]


@dataclass(kw_only=True)
class GetAllImpulsesResponse(GenericApiResponse):
    impulses: List[Impulse]


@dataclass(kw_only=True)
class DetailedImpulseMetricCategory(Enum):
    impulseMetrics = "impulseMetrics"
    inputBlockConfig = "inputBlockConfig"
    dspBlockConfig = "dspBlockConfig"
    learnBlockConfig = "learnBlockConfig"
    learnBlockMetrics = "learnBlockMetrics"


@dataclass(kw_only=True)
class DetailedImpulseMetricTypeEnum(Enum):
    core = "core"
    additional = "additional"


@dataclass(kw_only=True)
class DetailedImpulseMetricFilteringTypeTypeEnum(Enum):
    numeric = "numeric"
    string = "string"
    select = "select"
    boolean = "boolean"
    list = "list"


@dataclass(kw_only=True)
class DetailedImpulseMetricFilteringType(ApiBaseModel):
    type: DetailedImpulseMetricFilteringTypeTypeEnum
    options: List[str]


@dataclass(kw_only=True)
class DetailedImpulseMetric(ApiBaseModel):
    name: str
    type: DetailedImpulseMetricTypeEnum
    category: DetailedImpulseMetricCategory
    description: str
    value: Union[str, bool]
    filteringType: DetailedImpulseMetricFilteringType = None
    title: Optional[str] = None
    valueForSorting: Optional[int] = None
    valueHint: Optional[str] = None
    """Additional help explaining the value for this metric"""


@dataclass(kw_only=True)
class DetailedImpulsePretrainedModelInfo(ApiBaseModel):
    fileName: str


@dataclass(kw_only=True)
class IncludedSamples(ApiBaseModel):
    id: int
    windowCount: int


@dataclass(kw_only=True)
class DSPMetadataOutputConfigTypeEnum(Enum):
    image = "image"
    spectrogram = "spectrogram"
    flat = "flat"


@dataclass(kw_only=True)
class DSPMetadataOutputConfigShape(ApiBaseModel):
    width: int
    """Available on all types. Denotes the width of an 'image' or 'spectrogram', or the number of features in a 'flat' block."""
    height: Optional[int] = None
    """Only available for type 'image' and 'spectrogram'"""
    channels: Optional[int] = None
    """Only available for type 'image'"""
    frames: Optional[int] = None
    """Number of frames, only available for type 'image'"""


@dataclass(kw_only=True)
class DSPMetadataOutputConfig(ApiBaseModel):
    type: DSPMetadataOutputConfigTypeEnum
    shape: DSPMetadataOutputConfigShape


@dataclass(kw_only=True)
class DSPMetadata(ApiBaseModel):
    created: datetime
    """Date when the features were created"""
    dspConfig: Dict[str, str]
    labels: List[str]
    """Labels in the dataset when generator ran"""
    windowCount: int
    featureCount: int
    """Number of features for this DSP block"""
    includedSamples: List[IncludedSamples]
    """The included samples in this DSP block. Note that these are sorted in the same way as the `npy` files are laid out. So with the `windowCount` parameter you can exactly search back to see which file contributed to which windows there."""
    windowSizeMs: int
    """Length of the sliding window when generating features."""
    windowIncreaseMs: int
    """Increase of the sliding window when generating features."""
    padZeros: bool
    """Whether data was zero-padded when generating features."""
    frequency: float
    """Frequency of the original data in Hz."""
    outputConfig: DSPMetadataOutputConfig
    featureLabels: Optional[List[Optional[str]]] = None
    """Names of the generated features. Only set if axes have explicit labels."""
    fftUsed: Optional[List[Optional[int]]] = None
    resamplingAlgorithmVersion: Optional[float] = None
    """The version number of the resampling algorithm used (for resampled time series data only)"""


@dataclass(kw_only=True)
class DspBlockConfigs(ApiBaseModel):
    blockId: int
    config: DSPConfig
    """This returns a DSPConfig object, but "dsp.classes" and "dsp.features.classes" will be set to an empty array (use getDspConfig to retrieve these)."""
    metadata: DSPMetadata = None
    """This returns a DSPMetadata object, but "labels" will be set to an empty array (use getDspMetadata to retrieve these)."""


@dataclass(kw_only=True)
class DependencyData(ApiBaseModel):
    classes: List[str]
    blockNames: List[str]
    featureCount: int
    sampleCount: int


@dataclass(kw_only=True)
class KerasConfigModeEnum(Enum):
    visual = "visual"
    expert = "expert"


@dataclass(kw_only=True)
class KerasVisualLayerType(Enum):
    dense = "dense"
    conv1d = "conv1d"
    conv2d = "conv2d"
    reshape = "reshape"
    flatten = "flatten"
    dropout = "dropout"
    batchNormalization = "batchNormalization"
    transfer_mobilenetv2_a35 = "transfer_mobilenetv2_a35"
    transfer_mobilenetv2_a1 = "transfer_mobilenetv2_a1"
    transfer_mobilenetv2_a05 = "transfer_mobilenetv2_a05"
    transfer_mobilenetv2_160_a1 = "transfer_mobilenetv2_160_a1"
    transfer_mobilenetv2_160_a75 = "transfer_mobilenetv2_160_a75"
    transfer_mobilenetv2_160_a5 = "transfer_mobilenetv2_160_a5"
    transfer_mobilenetv2_160_a35 = "transfer_mobilenetv2_160_a35"
    transfer_mobilenetv1_a25_d100 = "transfer_mobilenetv1_a25_d100"
    transfer_mobilenetv1_a2_d100 = "transfer_mobilenetv1_a2_d100"
    transfer_mobilenetv1_a1_d100 = "transfer_mobilenetv1_a1_d100"
    transfer_kws_mobilenetv1_a1_d100 = "transfer_kws_mobilenetv1_a1_d100"
    transfer_kws_mobilenetv2_a35_d100 = "transfer_kws_mobilenetv2_a35_d100"
    transfer_kws_syntiant_ndp10x = "transfer_kws_syntiant_ndp10x"
    transfer_kws_conv2d_tiny = "transfer_kws_conv2d_tiny"
    object_ssd_mobilenet_v2_fpnlite_320x320 = "object_ssd_mobilenet_v2_fpnlite_320x320"
    fomo_mobilenet_v2_a01 = "fomo_mobilenet_v2_a01"
    fomo_mobilenet_v2_a35 = "fomo_mobilenet_v2_a35"
    transfer_organization = "transfer_organization"
    transfer_akidanet_imagenet_160_a100 = "transfer_akidanet_imagenet_160_a100"
    transfer_akidanet_imagenet_160_a50 = "transfer_akidanet_imagenet_160_a50"
    transfer_akidanet_imagenet_160_a25 = "transfer_akidanet_imagenet_160_a25"
    transfer_akidanet_imagenet_224_a100 = "transfer_akidanet_imagenet_224_a100"
    transfer_akidanet_imagenet_224_a50 = "transfer_akidanet_imagenet_224_a50"
    transfer_akidanet_imagenet_224_a25 = "transfer_akidanet_imagenet_224_a25"
    fomo_akidanet_a50 = "fomo_akidanet_a50"
    fomo_ad_gmm = "fomo_ad_gmm"
    fomo_ad_patchcore = "fomo_ad_patchcore"


@dataclass(kw_only=True)
class KerasVisualLayer(ApiBaseModel):
    type: KerasVisualLayerType
    neurons: Optional[int] = None
    """Number of neurons or filters in this layer (only for dense, conv1d, conv2d) or in the final conv2d layer (only for transfer layers)"""
    kernelSize: Optional[int] = None
    """Kernel size for the convolutional layers (only for conv1d, conv2d)"""
    dropoutRate: Optional[float] = None
    """Fraction of input units to drop (only for dropout) or in the final layer dropout (only for transfer layers)"""
    columns: Optional[int] = None
    """Number of columns for the reshape operation (only for reshape)"""
    stack: Optional[int] = None
    """Number of convolutional layers before the pooling layer (only for conv1d, conv2d)"""
    enabled: Optional[bool] = None
    organizationModelId: Optional[int] = None
    """Custom transfer learning model ID (when type is set to transfer_organization)"""


@dataclass(kw_only=True)
class AugmentationPolicyImageEnum(Enum):
    none = "none"
    all = "all"


@dataclass(kw_only=True)
class BlockType(Enum):
    official = "official"
    personal = "personal"
    enterprise = "enterprise"
    pro_or_enterprise = "pro-or-enterprise"
    community = "community"


@dataclass(kw_only=True)
class BlockDisplayCategory(Enum):
    classical = "classical"
    tao = "tao"


@dataclass(kw_only=True)
class TransferLearningModel(ApiBaseModel):
    name: str
    shortName: str
    description: str
    hasNeurons: bool
    hasDropout: bool
    type: KerasVisualLayerType
    author: str
    blockType: BlockType
    abbreviatedName: Optional[str] = None
    defaultNeurons: Optional[int] = None
    defaultDropout: Optional[float] = None
    defaultLearningRate: Optional[float] = None
    defaultTrainingCycles: Optional[float] = None
    hasImageAugmentation: Optional[bool] = None
    learnBlockType: LearnBlockType = None
    organizationModelId: Optional[int] = None
    implementationVersion: Optional[int] = None
    repositoryUrl: Optional[str] = None
    """URL to the source code of this custom learn block."""
    customParameters: Optional[List[DSPGroupItem]] = None
    displayCategory: BlockDisplayCategory = None


@dataclass(kw_only=True)
class AugmentationPolicySpectrogramFreqMaskingEnum(Enum):
    none = "none"
    low = "low"
    high = "high"


@dataclass(kw_only=True)
class AugmentationPolicySpectrogramTimeMaskingEnum(Enum):
    none = "none"
    low = "low"
    high = "high"


@dataclass(kw_only=True)
class AugmentationPolicySpectrogramGaussianNoiseEnum(Enum):
    none = "none"
    low = "low"
    high = "high"


@dataclass(kw_only=True)
class AugmentationPolicySpectrogram(ApiBaseModel):
    enabled: bool
    """True if spectrogram augmentation is enabled. Other properties will be ignored if this is false."""
    warping: Optional[bool] = None
    """True if warping along the time axis is enabled."""
    freqMasking: AugmentationPolicySpectrogramFreqMaskingEnum = None
    timeMasking: AugmentationPolicySpectrogramTimeMaskingEnum = None
    gaussianNoise: AugmentationPolicySpectrogramGaussianNoiseEnum = None


@dataclass(kw_only=True)
class AkidaEdgeLearningConfig(ApiBaseModel):
    enabled: bool
    """True if Akida Edge Learning model creation is enabled. Other properties will be ignored if this is false."""
    additionalClasses: Optional[float] = None
    """Number of additional classes that will be added to the Edge Learning model."""
    neuronsPerClass: Optional[float] = None
    """Number of neurons in each class on the last layer in the Edge Learning model."""


@dataclass(kw_only=True)
class AnomalyCapacity(Enum):
    low = "low"
    medium = "medium"
    high = "high"


@dataclass(kw_only=True)
class BlockParameters(ApiBaseModel):
    pass


@dataclass(kw_only=True)
class KerasConfig(ApiBaseModel):
    dependencies: DependencyData
    trained: bool
    """Whether the block is trained"""
    name: str
    script: str
    """The Keras script. This script might be empty if the mode is visual."""
    minimumConfidenceRating: float
    """Minimum confidence rating required for the neural network. Scores below this confidence are tagged as uncertain."""
    selectedModelType: KerasModelTypeEnum
    """The model type that is currently selected."""
    mode: KerasConfigModeEnum
    visualLayers: List[KerasVisualLayer]
    """The visual layers (if in visual mode) for the neural network. This will be an empty array when in expert mode."""
    trainingCycles: int
    """Number of training cycles. If in expert mode this will be 0."""
    learningRate: float
    """Learning rate (between 0 and 1). If in expert mode this will be 0."""
    defaultBatchSize: int
    """The default batch size if a value is not configured."""
    shape: str
    """Python-formatted tuple of input axes"""
    augmentationPolicyImage: AugmentationPolicyImageEnum
    transferLearningModels: List[TransferLearningModel]
    profileInt8: bool
    """Whether to profile the i8 model (might take a very long time)"""
    skipEmbeddingsAndMemory: bool
    """If set, skips creating embeddings and measuring memory (used in tests)"""
    showAdvancedTrainingSettings: bool
    """Whether the 'Advanced training settings' UI element should be expanded."""
    showAugmentationTrainingSettings: bool
    """Whether the 'Augmentation training settings' UI element should be expanded."""
    type: LearnBlockType = None
    batchSize: Optional[int] = None
    """The batch size used during training."""
    trainTestSplit: Optional[float] = None
    """Train/test split (between 0 and 1)"""
    autoClassWeights: Optional[bool] = None
    """Whether to automatically balance class weights, use this for skewed datasets."""
    useLearnedOptimizer: Optional[bool] = None
    """Use learned optimizer and ignore learning rate."""
    augmentationPolicySpectrogram: AugmentationPolicySpectrogram = None
    akidaEdgeLearningConfig: AkidaEdgeLearningConfig = None
    customValidationMetadataKey: Optional[str] = None
    """This metadata key is used to prevent group data leakage between train and validation datasets."""
    customParameters: Optional[Dict[str, Optional[str]]] = None
    """Training parameters, this list depends on the list of parameters that the model exposes."""
    anomalyCapacity: AnomalyCapacity = None
    """Capacity level for visual anomaly detection (GMM). Determines which set of default configurations to use. The higher capacity, the higher number of (Gaussian) components, and the more adapted the model becomes to the original distribution"""
    lastShownModelVariant: KerasModelVariantEnum = None
    """Last shown variant on the Keras screen. Used to keep the same view after refreshing."""
    lastShownModelEngine: ModelEngineShortEnum = None
    """Last shown model engine on the Keras screen. Used to keep the same view after refreshing."""
    blockParameters: BlockParameters = None
    """Training parameters specific to the type of the learn block. Parameters may be adjusted depending on the model defined in the visual layers. Used for our built-in blocks."""


@dataclass(kw_only=True)
class LearnBlockKerasConfigs(ApiBaseModel):
    blockId: int
    config: KerasConfig
    """This returns a KerasConfig object, but "transferLearningModels" and "dependencies.classes" will be set to an empty array (use getKeras to retrieve these)."""
    metadata: KerasModelMetadata = None
    """This returns a KerasModelMetadata object, but 1) non-default "onDevicePerformance", 2) "predictions", 3) "labels"; are omitted (use getKerasMetadata to retrieve these)."""


@dataclass(kw_only=True)
class Axes(ApiBaseModel):
    label: str
    selected: bool
    favourite: bool


@dataclass(kw_only=True)
class AnomalyConfig(ApiBaseModel):
    dependencies: DependencyData
    name: str
    axes: List[Axes]
    """Selectable axes for the anomaly detection block"""
    trained: bool
    """Whether the block is trained"""
    selectedAxes: List[int]
    """Selected clusters (in config)"""
    minimumConfidenceRating: float
    """Minimum confidence rating for this block, scores above this number will be flagged as anomaly."""
    clusterCount: Optional[int] = None
    """Number of clusters for K-means, or number of components for GMM (in config)"""


@dataclass(kw_only=True)
class LearnBlockAnomalyConfigs(ApiBaseModel):
    blockId: int
    config: AnomalyConfig
    metadata: AnomalyModelMetadata = None
    """This returns a AnomalyModelMetadata object, but 1) non-default "onDevicePerformance", 2) "predictions" are omitted (use getAnomalyMetadata to retrieve these)."""
    gmmMetadata: AnomalyGmmMetadata = None


@dataclass(kw_only=True)
class DetailedImpulse(ApiBaseModel):
    impulse: Impulse
    metrics: List[DetailedImpulseMetric]
    dspBlockConfigs: List[DspBlockConfigs]
    learnBlockKerasConfigs: List[LearnBlockKerasConfigs]
    learnBlockAnomalyConfigs: List[LearnBlockAnomalyConfigs]
    isStale: bool
    """Whether this impulse contains blocks with "stale" features (i.e. the dataset has changed since features were generated)"""
    tags: List[str]
    """Tags associated with this impulse"""
    pretrainedModelInfo: DetailedImpulsePretrainedModelInfo = None
    createdFromTunerTrialId: Optional[float] = None
    """The source EON Tuner trial ID for impulses created from the EON Tuner"""


@dataclass(kw_only=True)
class Type(Enum):
    input = "input"
    dsp = "dsp"
    learn = "learn"


@dataclass(kw_only=True)
class MetricKeys(ApiBaseModel):
    name: str
    description: str
    type: Type
    showInTable: bool
    filteringType: DetailedImpulseMetricFilteringType = None


@dataclass(kw_only=True)
class MetricKeysByCategory(ApiBaseModel):
    category: DetailedImpulseMetricCategory
    metricKeys: List[MetricKeys]


@dataclass(kw_only=True)
class GetAllDetailedImpulsesResponse(GenericApiResponse):
    impulses: List[DetailedImpulse]
    metricKeysByCategory: List[MetricKeysByCategory]
    extraTableColumns: List[str]
    """Which extra impulse information should be shown in the impulses table."""


@dataclass(kw_only=True)
class GetImpulseResponse(GenericApiResponse):
    impulse: Impulse = None


@dataclass(kw_only=True)
class GetTargetConstraintsResponse(GenericApiResponse):
    targetConstraints: TargetConstraints = None


@dataclass(kw_only=True)
class GetModelVariantsResponse(GenericApiResponse):
    modelVariants: AllProjectModelVariants


@dataclass(kw_only=True)
class InputBlockTypeEnum(Enum):
    time_series = "time-series"
    image = "image"
    features = "features"


@dataclass(kw_only=True)
class InputBlock(ApiBaseModel):
    type: InputBlockTypeEnum
    title: str
    author: str
    description: str
    name: str
    blockType: BlockType
    recommended: Optional[bool] = None


@dataclass(kw_only=True)
class DSPNamedAxis(ApiBaseModel):
    name: str
    description: str
    required: bool


@dataclass(kw_only=True)
class DSPBlock(ApiBaseModel):
    type: str
    title: str
    author: str
    description: str
    name: str
    experimental: bool
    latestImplementationVersion: int
    blockType: BlockType
    recommended: Optional[bool] = None
    organizationId: Optional[int] = None
    organizationDspId: Optional[int] = None
    namedAxes: Optional[List[DSPNamedAxis]] = None


@dataclass(kw_only=True)
class PublicProjectTierAvailability(Enum):
    enterprise_only = "enterprise-only"
    pro_or_enterprise = "pro-or-enterprise"
    all_projects = "all-projects"


@dataclass(kw_only=True)
class LearnBlock(ApiBaseModel):
    type: str
    title: str
    author: str
    description: str
    name: str
    blockType: BlockType
    recommended: Optional[bool] = None
    organizationModelId: Optional[int] = None
    publicProjectTierAvailability: PublicProjectTierAvailability = None
    isPublicEnterpriseOnly: Optional[bool] = None
    """Whether this block is publicly available to only enterprise users"""
    displayCategory: BlockDisplayCategory = None


@dataclass(kw_only=True)
class GetImpulseBlocksResponse(GenericApiResponse):
    inputBlocks: List[InputBlock]
    dspBlocks: List[DSPBlock]
    learnBlocks: List[LearnBlock]


@dataclass(kw_only=True)
class AnomalyConfigResponse(GenericApiResponse, AnomalyConfig):
    pass


@dataclass(kw_only=True)
class OrganizationDatasetTypeEnum(Enum):
    clinical = "clinical"
    files = "files"


@dataclass(kw_only=True)
class JobParentTypeEnum(Enum):
    project = "project"
    organization = "organization"
    standalone = "standalone"


@dataclass(kw_only=True)
class KerasResponse(GenericApiResponse, KerasConfig):
    pass


@dataclass(kw_only=True)
class DSPMetadataResponse(GenericApiResponse, DSPMetadata):
    pass


@dataclass(kw_only=True)
class JobFailureDetails(ApiBaseModel):
    reason: Optional[str] = None
    """short code describing the reason of the failure"""
    message: Optional[str] = None
    """full description of the failure"""
    exitCode: Optional[int] = None
    """exit code of the failed job process"""


@dataclass(kw_only=True)
class JobStep(ApiBaseModel):
    ordinal: float
    """ordinal number representing the step"""
    name: str
    """short name describing the step"""
    progress: Optional[float] = None
    """progress percentage inside the same step example for "scheduled" step, we have the following values: 0%: pod scheduled to some node (but node creation may not be finished yet) 50%: image pulling started 90%: image pulled """
    attempt: Optional[int] = None
    """execution attempt (starts at 0)"""
    failureDetails: JobFailureDetails = None
    """failure details"""


@dataclass(kw_only=True)
class JobStateExecutionDetails(ApiBaseModel):
    podName: Optional[str] = None
    """Kubernetes pod name"""


@dataclass(kw_only=True)
class JobState(ApiBaseModel):
    version: int
    """version number (indicates the order of the state)"""
    timestamp: datetime
    """timestamp when the job transistioned to this new step"""
    step: JobStep
    executionDetails: JobStateExecutionDetails = None


@dataclass(kw_only=True)
class JobCreatedByUser(ApiBaseModel):
    id: int
    name: str
    username: str
    photo: Optional[str] = None


@dataclass(kw_only=True)
class Job(ApiBaseModel):
    id: int
    """Job id, use this to refer back to the job. The web socket API also uses this ID."""
    category: str
    key: str
    """External job identifier, this can be used to categorize jobs, and recover job status. E.g. set this to 'keras-192' for a Keras learning block with ID 192. When a user refreshes the page you can check whether a job is active for this ID and re-attach. """
    created: datetime
    """When the job was created."""
    jobNotificationUids: List[int]
    """The IDs of users who should be notified when a job is finished."""
    started: Optional[datetime] = None
    """When the job was started."""
    finished: Optional[datetime] = None
    """When the job was finished."""
    finishedSuccessful: Optional[bool] = None
    """Whether the job finished successfully."""
    additionalInfo: Optional[str] = None
    """Additional metadata associated with this job."""
    computeTime: Optional[float] = None
    """Job duration time in seconds from start to finished, measured by k8s job watcher."""
    createdByUser: JobCreatedByUser = None
    categoryCount: Optional[int] = None
    """Some job categories keep a counter on the job number, e.g. in synthetic data, so we know what the 1st, 2nd etc. job was in the UI."""


@dataclass(kw_only=True)
class JobDetails(Job):
    states: List[JobState]
    """List of states the job went through"""
    childrenIds: Optional[List[Optional[int]]] = None
    """List of jobs children isd triggered by this job"""
    spec: Optional[Dict[str, Any]] = None
    """Job specification (Kubernetes specification or other underlying engine)"""


@dataclass(kw_only=True)
class JobDetailsResponse(GenericApiResponse):
    jobs: Optional[List[JobDetails]] = None


@dataclass(kw_only=True)
class ListJobsResponse(GenericApiResponse):
    jobs: List[Job]
    """Active jobs"""
    totalJobCount: int


@dataclass(kw_only=True)
class CreateUserRequest(ApiBaseModel):
    name: str
    """Your name"""
    username: str
    """Username, minimum 4 and maximum 30 characters. May contain alphanumeric characters, hyphens, underscores and dots. Validated according to `^(?=.{4,30}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._-]+(?<![_.])$`."""
    email: str
    """E-mail address. Will need to be validated before the account will become active."""
    privacyPolicy: bool
    """Whether the user accepted the privacy policy"""
    password: Optional[str] = None
    """Password, minimum length 8 characters."""
    projectName: Optional[str] = None
    """A project will automatically be created. Sets the name of the first project. If not set, this will be derived from the username."""
    activationToken: Optional[str] = None
    """Activation token for users created via SSO"""
    identityProvider: Optional[str] = None
    """Unique identifier of the identity provider asserting the identity of this user"""
    jobTitle: Optional[str] = None
    """Job title of the user. Optional field"""
    sessionId: Optional[str] = None
    """Session ID. Optional field"""
    companyName: Optional[str] = None
    """ACME Inc."""
    utmParams: Optional[List[UtmParameter]] = None
    """List of UTM parameters."""
    ignoreEmailValidation: Optional[bool] = None
    """If true, allows signup to proceed despite a potentially invalid email. Note that this will enforce email verification post-signup"""


@dataclass(kw_only=True)
class CreateProTierUserRequest(CreateUserRequest):
    redirectUrlOrigin: Optional[str] = None
    """Origin of the redirect URL returned as result of creating the professional user."""
    redirectUrlQueryParams: Optional[str] = None
    """Query parameters to be appended to the redirect URL returned as result of creating the professional user."""


@dataclass(kw_only=True)
class CreateUserResponse(GenericApiResponse):
    redirectUrl: Optional[str] = None
    """URL to redirect user to."""
    id: Optional[int] = None
    """User unique identifier"""


@dataclass(kw_only=True)
class CreateEvaluationUserResponse(GenericApiResponse):
    token: str
    """JWT token, to be used to log in in the future through JWTAuthentication"""
    redirectUrl: str
    """URL to redirect user to."""


@dataclass(kw_only=True)
class ConvertUserRequest(ApiBaseModel):
    name: str
    """Your name"""
    username: str
    """Username, minimum 4 and maximum 30 characters. May contain alphanumeric characters, hyphens, underscores and dots. Validated according to `^(?=.{4,30}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._-]+(?<![_.])$`."""
    email: str
    """E-mail address. Will need to be validated before the account will become active."""
    password: str
    """Password, minimum length 8 characters."""
    privacyPolicy: bool
    """Whether the user accepted the privacy policy"""
    projectName: Optional[str] = None
    """A project will automatically be created. Sets the name of the first project. If not set, this will be derived from the username."""


@dataclass(kw_only=True)
class ProjectVisibility(Enum):
    public = "public"
    private = "private"


@dataclass(kw_only=True)
class CreateProjectRequest(ApiBaseModel):
    projectName: str
    """The name of the first project."""
    projectVisibility: ProjectVisibility = None
    originalProjectVersionId: Optional[int] = None
    """The ID of the version that was used to restore this project."""


@dataclass(kw_only=True)
class CreateProjectResponse(GenericApiResponse):
    id: int
    """Project ID for the new project"""
    apiKey: str
    """API key for the new project"""


@dataclass(kw_only=True)
class OptimizeConfigTargetDevice(ApiBaseModel):
    name: str
    ram: Optional[int] = None
    rom: Optional[int] = None


@dataclass(kw_only=True)
class OptimizeConfigTuningAlgorithmEnum(Enum):
    random = "random"
    hyperband = "hyperband"
    bayesian = "bayesian"
    custom = "custom"


@dataclass(kw_only=True)
class OptimizeConfigOptimizationPrecisionEnum(Enum):
    float32 = "float32"
    int8 = "int8"


@dataclass(kw_only=True)
class OptimizeConfigSearchSpaceTemplateIdentifierEnum(Enum):
    speech_keyword = "speech_keyword"
    speech_continuous = "speech_continuous"
    audio_event = "audio_event"
    audio_continuous = "audio_continuous"
    visual = "visual"
    motion_event = "motion_event"
    motion_continuous = "motion_continuous"
    audio_syntiant = "audio_syntiant"
    object_detection_bounding_boxes = "object_detection_bounding_boxes"
    object_detection_centroids = "object_detection_centroids"
    visual_ad = "visual_ad"


@dataclass(kw_only=True)
class OptimizeConfigSearchSpaceTemplate(ApiBaseModel):
    identifier: OptimizeConfigSearchSpaceTemplateIdentifierEnum
    classification: Optional[bool] = None
    """Whether a classification block should be added to the search space"""
    anomaly: Optional[bool] = None
    """Whether an anomaly block should be added to the search space"""
    regression: Optional[bool] = None
    """Whether a regression block should be added to the search space"""


@dataclass(kw_only=True)
class TunerSpaceInputBlock(ApiBaseModel):
    pass


@dataclass(kw_only=True)
class TunerSpaceDSPBlock(ApiBaseModel):
    pass


@dataclass(kw_only=True)
class TunerSpaceLearnBlock(ApiBaseModel):
    pass


@dataclass(kw_only=True)
class TunerSpaceImpulse(ApiBaseModel):
    inputBlocks: List[TunerSpaceInputBlock]
    """Input Blocks that are part of this impulse"""
    dspBlocks: List[TunerSpaceDSPBlock]
    """DSP Blocks that are part of this impulse"""
    learnBlocks: List[List[TunerSpaceLearnBlock]]
    """Learning Blocks that are part of this impulse"""
    parameters: Optional[Dict[str, Any]] = None
    """Hyperparameters with potential values that can be used in any block in this impulse"""


@dataclass(kw_only=True)
class OptimizeConfig(ApiBaseModel):
    targetLatency: int
    """Target latency in MS"""
    targetDevice: OptimizeConfigTargetDevice
    name: Optional[str] = None
    compiler: Optional[List[Optional[str]]] = None
    precision: Optional[List[Optional[str]]] = None
    trainingCycles: Optional[int] = None
    """Maximum number of training cycles"""
    tuningMaxTrials: Optional[int] = None
    """Maximum number of trials"""
    tuningWorkers: Optional[int] = None
    """Maximum number of parallel workers/jobs"""
    initialTrials: Optional[int] = None
    """Number of initial trials"""
    optimizationRounds: Optional[int] = None
    """Number of optimization rounds"""
    trialsPerOptimizationRound: Optional[int] = None
    """Number of trials per optimization round"""
    minMACCS: Optional[float] = None
    maxMACCS: Optional[float] = None
    tuningAlgorithm: OptimizeConfigTuningAlgorithmEnum = None
    notificationOnCompletion: Optional[bool] = None
    importProjectMetrics: Optional[bool] = None
    """Whether to import metrics for previous EON tuner runs in the same project to accelerate the hyperparameter search process"""
    importResourceMetrics: Optional[bool] = None
    """Whether to import resource usage (RAM/ROM/latency) metrics to accelerate the hyperparameter search process"""
    numImportProjectMetrics: Optional[float] = None
    """Number of project trials to import"""
    numImportResourceMetrics: Optional[float] = None
    """Number of resource usage trials to import"""
    enableSEM: Optional[bool] = None
    """Enable standard error of the mean (SEM)"""
    accuracySEM: Optional[float] = None
    """Standard error of the trial accuracy mean"""
    latencySEM: Optional[float] = None
    """Standard error of the trial latency mean"""
    optimizationObjectives: Optional[List[Optional[str]]] = None
    """Hyperparameter optimization objectives ordered by priority"""
    rawObjectives: Optional[str] = None
    """Hyperparameter optimization objectives + weights in string format"""
    optimizationPrecision: OptimizeConfigOptimizationPrecisionEnum = None
    earlyStopping: Optional[bool] = None
    """Enable trial level early stopping based on loss metrics during training"""
    earlyStoppingWindowSize: Optional[float] = None
    """Stops the EON tuner if the feasible (mean) objective has not improved over the past “window_size” iterations"""
    earlyStoppingImprovementBar: Optional[float] = None
    """Threshold (in [0,1]) for considering relative improvement over the best point."""
    MOMF: Optional[bool] = None
    """Enable Multi-fidelity Multi-Objective optimization"""
    verboseLogging: Optional[bool] = None
    """Enable verbose logging"""
    disableConstraints: Optional[bool] = None
    """Disable search constraints"""
    disableDeduplicate: Optional[bool] = None
    """Disable trial deduplication"""
    tunerSpaceOptions: Optional[Dict[str, Optional[List[Optional[str]]]]] = None
    space: Optional[List[TunerSpaceImpulse]] = None
    """List of impulses specifying the EON Tuner search space"""
    searchSpaceTemplate: OptimizeConfigSearchSpaceTemplate = None


@dataclass(kw_only=True)
class OptimizeSpaceResponse(GenericApiResponse):
    impulse: List[TunerSpaceImpulse]
    """List of impulses specifying the EON Tuner search space"""


@dataclass(kw_only=True)
class TunerTrialStatusEnum(Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


@dataclass(kw_only=True)
class TunerTrialDspJobId(ApiBaseModel):
    training: Optional[float] = None
    testing: Optional[float] = None


@dataclass(kw_only=True)
class TunerTrialProgress(ApiBaseModel):
    epoch: float
    loss: float
    val_loss: float
    accuracy: float
    val_accuracy: float


@dataclass(kw_only=True)
class TunerTrialMetricsTest(ApiBaseModel):
    float32: KerasModelMetadataMetrics = None
    int8: KerasModelMetadataMetrics = None


@dataclass(kw_only=True)
class TunerTrialMetricsTrain(ApiBaseModel):
    float32: KerasModelMetadataMetrics = None
    int8: KerasModelMetadataMetrics = None


@dataclass(kw_only=True)
class TunerTrialMetricsValidation(ApiBaseModel):
    float32: KerasModelMetadataMetrics = None
    int8: KerasModelMetadataMetrics = None


@dataclass(kw_only=True)
class TunerTrialMetrics(ApiBaseModel):
    test: TunerTrialMetricsTest = None
    train: TunerTrialMetricsTrain = None
    validation: TunerTrialMetricsValidation = None


@dataclass(kw_only=True)
class TunerTrialImpulseAddedToProject(ApiBaseModel):
    impulseId: int
    link: str


@dataclass(kw_only=True)
class Status(Enum):
    pending = "pending"
    ready = "ready"
    busy = "busy"


@dataclass(kw_only=True)
class Blocks(ApiBaseModel):
    id: int
    retries: int
    status: Status
    type: Type
    lastActive: Optional[datetime] = None
    modelBlockIndex: Optional[int] = None
    """Index of corresponding DSP/learn block in the impulse model passed to createTrial()"""


@dataclass(kw_only=True)
class TunerCreateTrialInputBlock(ApiBaseModel):
    pass


@dataclass(kw_only=True)
class TunerCreateTrialDSPBlock(ApiBaseModel):
    pass


@dataclass(kw_only=True)
class TunerCreateTrialLearnBlock(ApiBaseModel):
    pass


@dataclass(kw_only=True)
class TunerTrialImpulse(ApiBaseModel):
    inputBlocks: Optional[List[TunerCreateTrialInputBlock]] = None
    dspBlocks: Optional[List[TunerCreateTrialDSPBlock]] = None
    learnBlocks: Optional[List[TunerCreateTrialLearnBlock]] = None


@dataclass(kw_only=True)
class TunerTrial(ApiBaseModel):
    id: str
    name: str
    status: TunerTrialStatusEnum
    blocks: List[Blocks]
    impulse: TunerTrialImpulse
    lastCompletedEpoch: Optional[datetime] = None
    lastCompletedTraining: Optional[datetime] = None
    retries: Optional[int] = None
    currentEpoch: Optional[int] = None
    workerId: Optional[str] = None
    experiment: Optional[str] = None
    original_trial_id: Optional[str] = None
    model: Optional[Dict[str, str]] = None
    dspJobId: TunerTrialDspJobId = None
    learnJobId: Optional[float] = None
    devicePerformance: Optional[Dict[str, str]] = None
    optimizationRound: Optional[float] = None
    progress: TunerTrialProgress = None
    metrics: TunerTrialMetrics = None
    impulseAddedToProject: TunerTrialImpulseAddedToProject = None


@dataclass(kw_only=True)
class OptimizeConfigResponse(GenericApiResponse, OptimizeConfig):
    device: Optional[Dict[str, Any]] = None


@dataclass(kw_only=True)
class OptimizeDSPParametersResponse(GenericApiResponse):
    parameters: Dict[str, Any]


@dataclass(kw_only=True)
class Models(ApiBaseModel):
    image: List[TransferLearningModel]
    objectDetection: List[TransferLearningModel]
    kws: List[TransferLearningModel]
    regression: List[TransferLearningModel]
    classification: List[TransferLearningModel]


@dataclass(kw_only=True)
class OptimizeTransferLearningModelsResponse(GenericApiResponse):
    models: Models


@dataclass(kw_only=True)
class ProjectDataType(Enum):
    audio = "audio"
    image = "image"
    motion = "motion"
    other = "other"


@dataclass(kw_only=True)
class Workers(ApiBaseModel):
    workerId: str
    status: Status


@dataclass(kw_only=True)
class OptimizeStateResponse(GenericApiResponse):
    config: OptimizeConfig
    status: Status
    tunerJobIsRunning: bool
    """Whether the job is active (if false => finished)"""
    trials: List[TunerTrial]
    projectDataType: ProjectDataType
    workers: List[Workers]
    nextRunIndex: int
    isWhitelabel: bool
    tunerJobId: Optional[int] = None
    """Actual tuner process, job message events will be tagged with this ID"""
    tunerCoordinatorJobId: Optional[int] = None
    """The coordinator pod, attach the job runner to this process for finished events"""
    continuationJobId: Optional[int] = None
    """Job ID for the initial job this job continuous the hyperparameter search process for."""
    jobError: Optional[str] = None


@dataclass(kw_only=True)
class JobStatus(Enum):
    cancelled = "cancelled"
    creating = "creating"
    failed = "failed"
    pending = "pending"
    running = "running"
    success = "success"


@dataclass(kw_only=True)
class TunerRun(ApiBaseModel):
    tunerJobId: int
    tunerCoordinatorJobId: int
    index: int
    created: datetime
    jobStatus: JobStatus
    name: Optional[str] = None
    space: Optional[List[TunerSpaceImpulse]] = None
    """List of impulses specifying the EON Tuner search space"""


@dataclass(kw_only=True)
class ListTunerRunsResponse(GenericApiResponse):
    runs: List[TunerRun]


@dataclass(kw_only=True)
class LearnBlocks(ApiBaseModel):
    type: LearnBlockType
    title: str
    author: str
    description: str
    name: str
    organizationModelId: Optional[float] = None
    experiment: Optional[str] = None
    displayCategory: BlockDisplayCategory = None
    publicProjectTierAvailability: PublicProjectTierAvailability = None


@dataclass(kw_only=True)
class AllLearnBlocksResponse(GenericApiResponse):
    learnBlocks: List[LearnBlocks]


@dataclass(kw_only=True)
class WindowSettingsResponse(GenericApiResponse):
    windowSettingsEvent: List[WindowSettings]
    windowSettingsContinuous: List[WindowSettings]


@dataclass(kw_only=True)
class Latency(ApiBaseModel):
    dspMips: float
    dspMs: float
    learnMaccs: float
    learnMs: float


@dataclass(kw_only=True)
class Ram(ApiBaseModel):
    dsp: float
    learn: float


@dataclass(kw_only=True)
class Rom(ApiBaseModel):
    dsp: float
    learn: float


@dataclass(kw_only=True)
class ScoreTrialResponse(GenericApiResponse):
    score: float
    latency: Latency
    ram: Ram
    rom: Rom


@dataclass(kw_only=True)
class Space(ApiBaseModel):
    impulse: List[TunerSpaceImpulse]
    """List of impulses specifying the EON Tuner search space"""


@dataclass(kw_only=True)
class SetOptimizeSpaceRequest:
    space: Optional[Space] = None


@dataclass(kw_only=True)
class TunerCompleteSearch(ApiBaseModel):
    success: bool


@dataclass(kw_only=True)
class TunerCreateTrialImpulse(ApiBaseModel):
    id: Optional[str] = None
    experiment: Optional[str] = None
    original_trial_id: Optional[str] = None
    optimizationRound: Optional[float] = None
    inputBlocks: Optional[List[TunerCreateTrialInputBlock]] = None
    dspBlocks: Optional[List[TunerCreateTrialDSPBlock]] = None
    learnBlocks: Optional[List[TunerCreateTrialLearnBlock]] = None


@dataclass(kw_only=True)
class UpdateProjectRequestLabelingMethodEnum(Enum):
    single_label = "single_label"
    object_detection = "object_detection"


@dataclass(kw_only=True)
class UpdateProjectRequestSelectedProjectTypeInWizardEnum(Enum):
    accelerometer = "accelerometer"
    audio = "audio"
    image_classification = "image_classification"
    object_detection = "object_detection"
    something_else = "something_else"


@dataclass(kw_only=True)
class UpdateProjectRequestDataAcquisitionViewTypeEnum(Enum):
    list = "list"
    grid = "grid"


@dataclass(kw_only=True)
class UpdateProjectRequest(ApiBaseModel):
    logo: Optional[str] = None
    """New logo URL, or set to `null` to remove the logo."""
    name: Optional[str] = None
    """New project name."""
    description: Optional[str] = None
    projectVisibility: ProjectVisibility = None
    publicProjectListed: Optional[bool] = None
    """If the project allows public access, whether to list it the public projects overview response. If not listed, the project is still accessible via direct link. If the project does not allow public access, this field has no effect. """
    lastDeployEonCompiler: Optional[bool] = None
    """Call this when clicking the Eon compiler setting"""
    lastDeployModelEngine: ModelEngineShortEnum = None
    """Model engine for last deploy"""
    latencyDevice: Optional[str] = None
    """MCU used for calculating latency"""
    experiments: Optional[List[Optional[str]]] = None
    showCreateFirstImpulse: Optional[bool] = None
    """Whether to show the 'Create your first impulse' section on the dashboard"""
    labelingMethod: UpdateProjectRequestLabelingMethodEnum = None
    selectedProjectTypeInWizard: UpdateProjectRequestSelectedProjectTypeInWizardEnum = (
        None
    )
    gettingStartedStep: Optional[int] = None
    """The next step in the getting started wizard, or set to -1 to clear the getting started wizard"""
    useGpu: Optional[bool] = None
    """Whether to use GPU for training"""
    computeTimeLimitM: Optional[int] = None
    """Job limit in minutes"""
    dspFileSizeMb: Optional[int] = None
    """DSP file size in MB"""
    enterprisePerformance: Optional[bool] = None
    trainJobRamMb: Optional[int] = None
    """Amount of RAM allocated to training jobs"""
    metadata: Optional[Dict[str, Any]] = None
    """New metadata about the project"""
    readme: Optional[str] = None
    """Readme for the project (in Markdown)"""
    lastAcquisitionLabel: Optional[str] = None
    trainJobNotificationUids: Optional[List[Optional[int]]] = None
    """The IDs of users who should be notified when a Keras or retrain job is finished."""
    dspJobNotificationUids: Optional[List[Optional[int]]] = None
    """The IDs of users who should be notified when a DSP job is finished."""
    modelTestingJobNotificationUids: Optional[List[Optional[int]]] = None
    """The IDs of users who should be notified when a model testing job is finished."""
    exportJobNotificationUids: Optional[List[Optional[int]]] = None
    """The IDs of users who should be notified when an export job is finished."""
    csvImportConfig: Optional[Dict[str, Any]] = None
    """Config file specifying how to process CSV files. (set to null to clear the config)"""
    inPretrainedModelFlow: Optional[bool] = None
    dspPageSize: Optional[int] = None
    """Set to '0' to disable DSP paging"""
    indPauseProcessingSamples: Optional[bool] = None
    """Used in tests, to ensure samples that need to be processed async are not picked up until the flag is set to FALSE again."""
    showSensorDataInAcquisitionGraph: Optional[bool] = None
    """Whether to show the actual sensor data in acquisition charts (only applies when you have structured labels)"""
    lastDeploymentTarget: Optional[str] = None
    """Which deployment target was last selected (used to populate this deployment target again the next time you visit the deployment page). Should match the _format_ property of the response from listDeploymentTargetsForProject."""
    dataAcquisitionPageSize: Optional[int] = None
    """Default page size on data acquisition"""
    dataAcquisitionViewType: UpdateProjectRequestDataAcquisitionViewTypeEnum = None
    dataAcquisitionGridColumnCount: Optional[int] = None
    """Number of grid columns in non-detailed view on data acquisition"""
    dataAcquisitionGridColumnCountDetailed: Optional[int] = None
    """Number of grid columns in detailed view on data acquisition"""
    showExactSampleLength: Optional[bool] = None
    """If enabled, does not round sample length to hours/minutes/seconds, but always displays sample length in milliseconds. E.g. instead of 1m 32s, this'll say 92,142ms."""
    inlineEditBoundingBoxes: Optional[bool] = None
    """If enabled, allows editing bounding box labels directly from the acquisition UI."""
    defaultProfilingVariant: KerasModelVariantEnum = None
    """Last shown variant on the model testing and live classification pages. Used to keep the same view after refreshing."""
    enabledModelProfilingVariants: Optional[List[KerasModelVariantEnum]] = None
    """Set of model variants enabled by default on the model testing and live classification pages."""
    impulseListCoreMetricsHiddenColumns: Optional[List[Optional[str]]] = None
    """Which core metrics should be hidden in the impulse list. See 'GetAllDetailedImpulsesResponse' for a list of all metrics."""
    impulseListAdditionalMetricsShownColumns: Optional[List[Optional[str]]] = None
    """Which additional metrics should be shown in the impulse list. See 'GetAllDetailedImpulsesResponse' for a list of all metrics."""
    impulseListExtraColumns: Optional[List[Optional[str]]] = None
    """Which extra columns should be shown in the impulse list."""
    aiActionsGridColumnCount: Optional[int] = None
    """Number of grid columns in AI Actions"""


@dataclass(kw_only=True)
class DeploymentTargetEngine(Enum):
    tflite = "tflite"
    tflite_eon = "tflite-eon"
    tflite_eon_ram_optimized = "tflite-eon-ram-optimized"
    tensorrt = "tensorrt"
    tensaiflow = "tensaiflow"
    drp_ai = "drp-ai"
    tidl = "tidl"
    akida = "akida"
    syntiant = "syntiant"
    memryx = "memryx"
    neox = "neox"
    ethos_linux = "ethos-linux"


@dataclass(kw_only=True)
class BuildOnDeviceModelRequest(ApiBaseModel):
    engine: DeploymentTargetEngine
    modelType: KerasModelTypeEnum = None


@dataclass(kw_only=True)
class BuildOrganizationOnDeviceModelRequest(ApiBaseModel):
    engine: DeploymentTargetEngine
    deployBlockId: int
    modelType: KerasModelTypeEnum = None


@dataclass(kw_only=True)
class AddCollaboratorRequest(ApiBaseModel):
    usernameOrEmail: str
    """Username or e-mail address"""


@dataclass(kw_only=True)
class RemoveCollaboratorRequest(ApiBaseModel):
    usernameOrEmail: str
    """Username or e-mail address"""


@dataclass(kw_only=True)
class HmacKeys(ApiBaseModel):
    id: int
    hmacKey: str
    isDevelopmentKey: bool
    name: str
    created: datetime


@dataclass(kw_only=True)
class ListHmacKeysResponse(GenericApiResponse):
    hmacKeys: List[HmacKeys]
    """List of HMAC keys"""


@dataclass(kw_only=True)
class Role(Enum):
    admin = "admin"
    member = "member"


@dataclass(kw_only=True)
class ApiKeys(ApiBaseModel):
    id: int
    apiKey: str
    isDevelopmentKey: bool
    name: str
    created: datetime
    role: Role


@dataclass(kw_only=True)
class ListApiKeysResponse(GenericApiResponse):
    apiKeys: List[ApiKeys]
    """List of API keys."""


@dataclass(kw_only=True)
class AddHmacKeyRequest(ApiBaseModel):
    name: str
    """Description of the key"""
    hmacKey: str
    """HMAC key."""
    isDevelopmentKey: bool
    """Whether this key should be used as a development key."""


@dataclass(kw_only=True)
class AddApiKeyRequest(ApiBaseModel):
    name: str
    """Description of the key"""
    apiKey: Optional[str] = None
    """Optional: API key. This needs to start with `ei_` and will need to be at least 32 characters long. If this field is not passed in, a new API key is generated for you."""


@dataclass(kw_only=True)
class AddProjectApiKeyRequest(AddApiKeyRequest):
    isDevelopmentKey: bool
    """Whether this key should be used as a development key."""
    role: Role


@dataclass(kw_only=True)
class AdminAddProjectApiKeyRequest(AddApiKeyRequest):
    ttl: Optional[int] = None
    """Time to live in seconds. If not set, the key will expire in 1 minute."""


@dataclass(kw_only=True)
class UserProjectsSortOrder(Enum):
    created_asc = "created-asc"
    created_desc = "created-desc"
    added_asc = "added-asc"
    added_desc = "added-desc"
    name_asc = "name-asc"
    name_desc = "name-desc"
    last_accessed_desc = "last-accessed-desc"


@dataclass(kw_only=True)
class Projects(ApiBaseModel):
    id: int
    name: str
    created: datetime
    lastAccessed: Optional[datetime] = None


@dataclass(kw_only=True)
class LastAccessedProjects(ApiBaseModel):
    projects: List[Projects]
    hasMoreProjects: bool


@dataclass(kw_only=True)
class Whitelabels(ApiBaseModel):
    id: float
    domain: str
    name: str
    ownerOrganizationId: float
    isAdmin: bool
    """Whether the user is an admin of the white label."""


@dataclass(kw_only=True)
class GetUserResponse(GenericApiResponse, User):
    email: str
    activated: bool
    organizations: List[UserOrganization]
    """Organizations that the user is a member of. Only filled when requesting information about yourself."""
    projects: List[Project]
    """List of all projects. This returns all projects for the user (regardless of whitelabel)"""
    experiments: List[UserExperiment]
    """Experiments the user has access to. Enabling experiments can only be done through a JWT token."""
    suspended: bool
    """Whether the user is suspended."""
    notifications: List[str]
    """List of notifications to show to the user."""
    passwordConfigured: bool
    """Whether the user has configured a password"""
    projectsSortOrder: UserProjectsSortOrder
    """Default sort order on the projects list"""
    hasEnterpriseFeaturesAccess: bool
    """Whether the current user has access to enterprise features. This is true if the user is an enterprise user, or has an active enterprise trial."""
    lastAccessedProjects: LastAccessedProjects
    """Last 5 accessed projects. This _only_ returns projects for the current whitelabel ID."""
    privatePersonalProjectsUsed: int
    """Number of private projects created by the current user."""
    evaluation: Optional[bool] = None
    """Whether this is an ephemeral evaluation account."""
    ambassador: Optional[bool] = None
    """Whether this user is an ambassador."""
    whitelabels: Optional[List[Optional[Whitelabels]]] = None
    """List of white labels the user is a member of"""
    subscriptionDowngradeDate: Optional[datetime] = None
    """The date at which the user's subscription will be downgraded due to cancellation."""
    subscriptionTerminationDate: Optional[datetime] = None
    """The date at which the user's subscription will be automatically terminated due to failed payments."""
    activeEnterpriseTrial: EnterpriseTrial = None
    """The ongoing free Enterprise trials that the user has created, if any."""
    timezone: Optional[str] = None
    """Timezone for the user (or undefined if not specified)."""


@dataclass(kw_only=True)
class GetUserProjectsResponse(GenericApiResponse):
    projects: List[Project]


@dataclass(kw_only=True)
class UpdateUserRequest(ApiBaseModel):
    name: Optional[str] = None
    """New full name"""
    jobTitle: Optional[str] = None
    """New job title"""
    companyName: Optional[str] = None
    """New company name"""
    experiments: Optional[List[Optional[str]]] = None
    """List of user experiments"""
    projectsSortOrder: UserProjectsSortOrder = None
    """Default sort order on the projects list"""
    timezone: Optional[str] = None
    """User timezone."""


@dataclass(kw_only=True)
class DeleteUserRequest(ApiBaseModel):
    password: Optional[str] = None
    """User's current password. Required if the user has a password set."""
    totpToken: Optional[str] = None
    """TOTP Token. Required if a user has multi-factor authentication with a TOTP token enabled. If a user has MFA enabled, but no totpToken is submitted; then an error starting with "ERR_TOTP_TOKEN IS REQUIRED" is returned. Use this to then prompt for an MFA token and re-try this request."""


@dataclass(kw_only=True)
class ActivateUserOrVerifyEmailRequest(ApiBaseModel):
    code: str
    """Activation or verification code (sent via email)"""


@dataclass(kw_only=True)
class Emails(ApiBaseModel):
    from_var: str
    to: str
    created: datetime
    subject: str
    bodyText: str
    bodyHTML: str
    sent: bool
    providerResponse: str
    userId: Optional[int] = None
    projectId: Optional[int] = None


@dataclass(kw_only=True)
class ListEmailResponse(GenericApiResponse):
    emails: List[Emails]
    """List of emails"""


@dataclass(kw_only=True)
class RequestResetPasswordRequest(ApiBaseModel):
    email: str


@dataclass(kw_only=True)
class ResetPasswordRequest(ApiBaseModel):
    email: str
    code: str
    newPassword: str


@dataclass(kw_only=True)
class VerifyResetPasswordRequest(ApiBaseModel):
    email: str
    code: str


@dataclass(kw_only=True)
class EmailValidationRequest(ApiBaseModel):
    email: str
    """E-mail address to validate"""


@dataclass(kw_only=True)
class SetAnomalyParameterRequest(ApiBaseModel):
    minimumConfidenceRating: Optional[float] = None
    """Minimum confidence score, if the anomaly block scores a sample above this threshold it will be flagged as anomaly."""


@dataclass(kw_only=True)
class SetKerasParameterRequestModeEnum(Enum):
    expert = "expert"
    visual = "visual"


@dataclass(kw_only=True)
class SetKerasParameterRequest(ApiBaseModel):
    mode: SetKerasParameterRequestModeEnum = None
    minimumConfidenceRating: Optional[float] = None
    """Minimum confidence score, if the neural network scores a sample below this threshold it will be flagged as uncertain."""
    selectedModelType: KerasModelTypeEnum = None
    """The model type to select, as described in the model metadata call."""
    script: Optional[str] = None
    """Raw Keras script (only used in expert mode)"""
    visualLayers: Optional[List[KerasVisualLayer]] = None
    """The visual layers for the neural network (only in visual mode)."""
    trainingCycles: Optional[int] = None
    """Number of training cycles (only in visual mode)."""
    learningRate: Optional[float] = None
    """Learning rate (between 0 and 1) (only in visual mode)."""
    batchSize: Optional[float] = None
    """Batch size used during training (only in visual mode)."""
    trainTestSplit: Optional[float] = None
    """Train/test split (between 0 and 1)"""
    autoClassWeights: Optional[bool] = None
    """Whether to automatically balance class weights, use this for skewed datasets."""
    useLearnedOptimizer: Optional[bool] = None
    """Use learned optimizer and ignore learning rate."""
    augmentationPolicyImage: AugmentationPolicyImageEnum = None
    augmentationPolicySpectrogram: AugmentationPolicySpectrogram = None
    profileInt8: Optional[bool] = None
    """Whether to profile the i8 model (might take a very long time)"""
    skipEmbeddingsAndMemory: Optional[bool] = None
    """If set, skips creating embeddings and measuring memory (used in tests)"""
    akidaEdgeLearningConfig: AkidaEdgeLearningConfig = None
    customValidationMetadataKey: Optional[str] = None
    """If the 'custom validation split' experiment is enabled, this metadata key is used to prevent group data leakage between train and validation datasets."""
    showAdvancedTrainingSettings: Optional[bool] = None
    """Whether the 'Advanced training settings' UI element should be expanded."""
    showAugmentationTrainingSettings: Optional[bool] = None
    """Whether the 'Augmentation training settings' UI element should be expanded."""
    customParameters: Optional[Dict[str, Optional[str]]] = None
    """Training parameters, this list depends on the list of parameters that the model exposes."""
    anomalyCapacity: AnomalyCapacity = None
    """Capacity level for visual anomaly detection. Determines which set of default configurations to use. The higher capacity, the higher number of (Gaussian) components, and the more adapted the model becomes to the original distribution"""
    lastShownModelVariant: KerasModelVariantEnum = None
    """Last shown variant on the Keras screen. Used to keep the same view after refreshing."""
    lastShownModelEngine: ModelEngineShortEnum = None
    """Last shown model engine on the Keras screen. Used to keep the same view after refreshing."""
    blockParameters: BlockParameters = None
    """Training parameters specific to the type of the learn block. Parameters may be adjusted depending on the model defined in the visual layers. Used for our built-in blocks."""


@dataclass(kw_only=True)
class MoveRawDataRequestNewCategoryEnum(Enum):
    training = "training"
    testing = "testing"
    anomaly = "anomaly"


@dataclass(kw_only=True)
class MoveRawDataRequest(ApiBaseModel):
    newCategory: MoveRawDataRequestNewCategoryEnum


@dataclass(kw_only=True)
class UploadUserPhotoRequest(ApiBaseModel):
    photo: bytes


@dataclass(kw_only=True)
class UploadUserPhotoResponse(GenericApiResponse):
    url: str


@dataclass(kw_only=True)
class UploadCustomBlockRequestTypeEnum(Enum):
    transform = "transform"
    deploy = "deploy"
    dsp = "dsp"
    transferLearning = "transferLearning"


@dataclass(kw_only=True)
class UploadCustomBlockRequest(ApiBaseModel):
    tar: bytes
    type: UploadCustomBlockRequestTypeEnum
    blockId: int


@dataclass(kw_only=True)
class ChangePasswordRequest(ApiBaseModel):
    currentPassword: str
    newPassword: str


@dataclass(kw_only=True)
class OrganizationTransferLearningBlockModelFileTypeEnum(Enum):
    binary = "binary"
    json = "json"
    text = "text"


@dataclass(kw_only=True)
class OrganizationTransferLearningBlockModelFile(ApiBaseModel):
    id: str
    """Output artifact unique file ID, in kebab case"""
    name: str
    """Output artifact file name"""
    type: OrganizationTransferLearningBlockModelFileTypeEnum
    description: str
    """Output artifact file description"""


@dataclass(kw_only=True)
class OrganizationTransferLearningBlockCustomVariant(ApiBaseModel):
    key: str
    """Unique identifier or key for this custom variant"""
    name: str
    """Custom variant display name"""
    inferencingEntrypoint: str
    """The entrypoint command to run custom inferencing for this model variant, via the learn block container"""
    profilingEntrypoint: Optional[str] = None
    """The entrypoint command to run custom profiling for this model variant, via the learn block container"""
    modelFiles: Optional[List[OrganizationTransferLearningBlockModelFile]] = None


@dataclass(kw_only=True)
class Summary(ApiBaseModel):
    category: str
    lengthMs: int
    """Length per category in milliseconds"""


@dataclass(kw_only=True)
class JobSummaryResponse(GenericApiResponse):
    summary: List[Summary]


@dataclass(kw_only=True)
class StartPerformanceCalibrationRequest(ApiBaseModel):
    backgroundNoiseLabel: str
    """The label used to signify background noise in the impulse"""
    otherNoiseLabels: Optional[List[Optional[str]]] = None
    """Any other labels that should be considered equivalent to background noise"""
    uploadKey: Optional[str] = None
    """The key of an uploaded sample. If not present, a synthetic sample will be created."""
    sampleLengthMinutes: Optional[float] = None
    """The length of sample to create (required for synthetic samples)"""


@dataclass(kw_only=True)
class GetPerformanceCalibrationStatusResponse(GenericApiResponse):
    available: bool
    unsupportedProjectError: Optional[str] = None
    """If the current project is unsupported by performance calibration, this field explains the reason why. Otherwise, it is undefined."""
    options: StartPerformanceCalibrationRequest = None


@dataclass(kw_only=True)
class PerformanceCalibrationGroundTruthTypeEnum(Enum):
    sample = "sample"
    noise = "noise"
    combined_noise = "combined_noise"


@dataclass(kw_only=True)
class Samples(ApiBaseModel):
    id: int
    """The ID of the samples in Studio"""
    start: float
    """The start time of the sample in milliseconds"""
    length: float
    """The length of the sample in milliseconds"""
    idx: int
    """For debugging. The index of the sample in the original Y array."""


@dataclass(kw_only=True)
class PerformanceCalibrationGroundTruth(ApiBaseModel):
    type: PerformanceCalibrationGroundTruthTypeEnum
    labelIdx: int
    """Index of the label in the array of all labels"""
    labelString: str
    """String label of the sample"""
    start: int
    """The start time of the region in milliseconds"""
    length: int
    """The length of the region in milliseconds"""
    samples: Optional[List[Optional[Samples]]] = None
    """If the region contains samples, all the samples within this region"""


@dataclass(kw_only=True)
class GetPerformanceCalibrationGroundTruthResponse(GenericApiResponse):
    samples: List[PerformanceCalibrationGroundTruth]


@dataclass(kw_only=True)
class PerformanceCalibrationRawDetection(ApiBaseModel):
    start: int
    """The start time of the detected window in milliseconds"""
    end: int
    """The end time of the detected window in milliseconds"""
    result: List[float]


@dataclass(kw_only=True)
class GetPerformanceCalibrationRawResultResponse(GenericApiResponse):
    detections: List[PerformanceCalibrationRawDetection]


@dataclass(kw_only=True)
class PerformanceCalibrationDetection(ApiBaseModel):
    time: int
    """The time of the detection in milliseconds"""
    label: str
    """The label that was detected"""


@dataclass(kw_only=True)
class PerformanceCalibrationFalsePositiveTypeEnum(Enum):
    incorrect = "incorrect"
    duplicate = "duplicate"
    spurious = "spurious"


@dataclass(kw_only=True)
class PerformanceCalibrationFalsePositive(ApiBaseModel):
    type: PerformanceCalibrationFalsePositiveTypeEnum
    detectionTime: int
    """The time of the detection in milliseconds"""
    groundTruthLabel: Optional[str] = None
    """The label of any associated ground truth"""
    groundTruthStart: Optional[float] = None
    """The start time of any associated ground truth"""
    sampleIds: Optional[List[Optional[int]]] = None
    """All of the sample IDs in the affected region"""


@dataclass(kw_only=True)
class PerformanceCalibrationParameterSetAggregateStats(ApiBaseModel):
    falsePositiveRate: float
    falseNegativeRate: float


@dataclass(kw_only=True)
class Stats(ApiBaseModel):
    label: str
    truePositives: int
    falsePositives: int
    falseNegatives: int
    trueNegatives: int
    falsePositiveRate: float
    falseNegativeRate: float
    falseNegativeTimes: List[float]
    """The times in ms at which false negatives occurred. These correspond to specific items in the ground truth."""
    falsePositiveDetails: Optional[List[PerformanceCalibrationFalsePositive]] = None
    """The details of every false positive detection."""


@dataclass(kw_only=True)
class PerformanceCalibrationParametersTypeEnum(Enum):
    standard = "standard"


@dataclass(kw_only=True)
class PerformanceCalibrationParametersStandard(ApiBaseModel):
    averageWindowDurationMs: float
    """The length of the averaging window in milliseconds."""
    detectionThreshold: float
    """The minimum threshold for detection, from 0-1."""
    suppressionMs: float
    """The amount of time new matches will be ignored after a positive result."""


@dataclass(kw_only=True)
class PerformanceCalibrationParameters(ApiBaseModel):
    type: PerformanceCalibrationParametersTypeEnum
    version: int
    """The version number of the post-processing algorithm."""
    parametersStandard: PerformanceCalibrationParametersStandard = None


@dataclass(kw_only=True)
class PerformanceCalibrationParameterSet(ApiBaseModel):
    detections: List[PerformanceCalibrationDetection]
    """All of the detections using this parameter set"""
    isBest: bool
    """Whether this is considered the best parameter set"""
    labels: List[str]
    """All of the possible labels in the detections array"""
    aggregateStats: PerformanceCalibrationParameterSetAggregateStats
    stats: List[Stats]
    params: PerformanceCalibrationParameters
    windowSizeMs: float
    """The size of the input block window in milliseconds."""


@dataclass(kw_only=True)
class GetPerformanceCalibrationParameterSetsResponse(GenericApiResponse):
    parameterSets: List[PerformanceCalibrationParameterSet]


@dataclass(kw_only=True)
class GetPerformanceCalibrationParametersResponse(GenericApiResponse):
    params: PerformanceCalibrationParameters = None


@dataclass(kw_only=True)
class PerformanceCalibrationUploadLabeledAudioRequest(ApiBaseModel):
    zip: bytes


@dataclass(kw_only=True)
class PerformanceCalibrationUploadLabeledAudioResponse(GenericApiResponse):
    uploadKey: str


@dataclass(kw_only=True)
class PerformanceCalibrationSaveParameterSetRequest(ApiBaseModel):
    params: PerformanceCalibrationParameters


@dataclass(kw_only=True)
class GetPostProcessingResultsResponse(GenericApiResponse):
    variableNames: List[str]
    """The names of the variables being tuned, in column order."""
    objectiveNames: List[str]
    """The names of the objectives being minimized, in column order."""
    variables: List[List[float]]
    """The variable values representing the pareto front of optimal solutions."""
    objectives: List[List[float]]
    """The objective values that correspond with the variables."""


@dataclass(kw_only=True)
class ListOrganizationsResponse(GenericApiResponse):
    organizations: List[Organization]
    """Array with organizations"""


@dataclass(kw_only=True)
class OrganizationDatasetBucket(ApiBaseModel):
    id: int
    """Bucket ID"""
    bucket: str
    path: str
    """Path in the bucket"""
    fullBucketPathDescription: str
    """Full bucket path, incl. protocol (e.g. s3://bucket/path) - to be used in the UI"""
    dataItemNamingLevelsDeep: int
    """Number of levels deep for data items, e.g. if you have folder "test/abc", with value 1 "test" will be a data item, with value 2 "test/abc" will be a data item. Only used for "clinical" type."""


@dataclass(kw_only=True)
class OrganizationDataset(ApiBaseModel):
    dataset: str
    lastFileCreated: datetime
    totalFileSize: int
    totalFileCount: int
    totalItemCount: int
    totalItemCountChecklistOK: int
    totalItemCountChecklistFailed: int
    tags: List[str]
    type: OrganizationDatasetTypeEnum
    category: Optional[str] = None
    bucket: OrganizationDatasetBucket = None
    bucketPath: Optional[str] = None
    """Location of the dataset within the bucket"""


@dataclass(kw_only=True)
class Metrics(ApiBaseModel):
    totalJobsComputeTime: float
    """Total compute time of all organizational jobs since the creation of the organization (including organizational project jobs). Compute time is the amount of computation time spent in jobs, in minutes used by an organization over a 12 month period, calculated as CPU + GPU minutes."""
    jobsComputeTimeCurrentYear: float
    """Total compute time of all organizational jobs in the current contract (including organizational project jobs). Compute time is the amount of computation time spent in jobs, in minutes used by an organization over a 12 month period, calculated as CPU + GPU minutes."""
    jobsComputeTimeCurrentYearSince: datetime
    """The date from which the compute time for the running contract is calculated."""
    cpuComputeTimeCurrentContract: float
    """CPU compute time of all jobs in the organization in the current contract (including organizational project jobs)."""
    gpuComputeTimeCurrentContract: float
    """GPU compute time of all jobs in the organization in the current contract (including organizational project jobs)."""
    totalStorage: float
    """Total storage used by the organization."""
    projectCount: int
    """Total number of projects owned by the organization."""
    userCount: int
    """Total number of users in the organization."""


@dataclass(kw_only=True)
class OrganizationMetricsResponse(GenericApiResponse):
    metrics: Metrics


@dataclass(kw_only=True)
class DefaultComputeLimits(ApiBaseModel):
    requestsCpu: float
    requestsMemory: float
    limitsCpu: float
    limitsMemory: float


@dataclass(kw_only=True)
class ObjectDetectionLastLayerOptions(ApiBaseModel):
    label: str
    value: ObjectDetectionLastLayer


@dataclass(kw_only=True)
class ImageInputScalingOptions(ApiBaseModel):
    label: str
    value: ImageInputScaling


@dataclass(kw_only=True)
class CliLists(ApiBaseModel):
    objectDetectionLastLayerOptions: List[ObjectDetectionLastLayerOptions]
    imageInputScalingOptions: List[ImageInputScalingOptions]


@dataclass(kw_only=True)
class XXYPerformanceClash2058601667(ApiBaseModel):
    jobLimitM: int
    """Compute time limit per job in minutes (for non-transformation jobs)."""


@dataclass(kw_only=True)
class OrganizationInfoResponse(GenericApiResponse):
    organization: Organization
    datasets: List[OrganizationDataset]
    defaultComputeLimits: DefaultComputeLimits
    experiments: List[Experiments]
    """Experiments that the organization has access to. Enabling experiments can only be done through a JWT token."""
    cliLists: CliLists
    performance: XXYPerformanceClash2058601667
    entitlementLimits: EntitlementLimits = None
    readme: Optional[Readme] = None
    """Present if a readme is set for this project"""
    whitelabelId: Optional[int] = None


@dataclass(kw_only=True)
class UpdateOrganizationRequest(ApiBaseModel):
    logo: Optional[str] = None
    """New logo URL, or set to `null` to remove the logo."""
    headerImg: Optional[str] = None
    """New leader image URL, or set to `null` to remove the leader."""
    showHeaderImgMask: Optional[bool] = None
    name: Optional[str] = None
    """New organization name."""
    experiments: Optional[List[Optional[str]]] = None
    readme: Optional[str] = None
    """Readme for the organization (in Markdown)"""
    jobLimitM: Optional[int] = None
    """New job limit in seconds."""


@dataclass(kw_only=True)
class CreateOrganizationRequest(ApiBaseModel):
    organizationName: str
    """The name of the organization."""


@dataclass(kw_only=True)
class WhitelabelAdminCreateOrganizationRequest(ApiBaseModel):
    organizationName: str
    """The name of the organization."""
    adminId: Optional[int] = None
    """Unique identifier of the administrator of the new organization."""
    adminEmail: Optional[str] = None
    """Email of the administrator of the new organization."""


@dataclass(kw_only=True)
class CreateOrganizationResponse(GenericApiResponse):
    id: int
    """Organization ID for the new organization"""
    apiKey: str
    """API key for the new organization (this is shown only once)"""


@dataclass(kw_only=True)
class AdminCreateProjectRequest(ApiBaseModel):
    projectName: str
    """The name of the project."""
    projectVisibility: ProjectVisibility = None
    ownerId: Optional[int] = None
    """Unique identifier of the owner of the new project. Either this parameter or ownerEmail must be set."""
    ownerEmail: Optional[str] = None
    """Email of the owner of the new project. Either this parameter or ownerId must be set."""


@dataclass(kw_only=True)
class CreateOrganizationPortalRequest(ApiBaseModel):
    name: str
    """The name of the upload portal."""
    bucketId: int
    """The S3 bucket id to store the uploaded data. Set to '0' to select a bucket hosted by Edge Impulse."""
    bucketPath: str
    """The path in the bucket the upload portal will write to."""
    description: Optional[str] = None
    """The purpose and description of the upload portal."""


@dataclass(kw_only=True)
class CreateOrganizationPortalResponse(GenericApiResponse):
    id: int
    """Portal ID for the new upload portal"""
    url: str
    """URL to the portal"""
    signedUrl: Optional[str] = None
    """pre-signed upload URL. Only set if using a non-built-in bucket."""
    bucketBucket: Optional[str] = None
    """Only set if using a non-built-in bucket."""


@dataclass(kw_only=True)
class UpdateOrganizationPortalResponse(GenericApiResponse):
    url: str
    """URL to the portal"""
    signedUrl: Optional[str] = None
    """pre-signed upload URL, only set if not using the Edge Impulse hosted bucket."""
    bucketBucket: Optional[str] = None
    """Only set if not using the Edge Impulse hosted bucket."""


@dataclass(kw_only=True)
class GetOrganizationPortalResponse(GenericApiResponse):
    id: int
    """Portal ID for the new upload portal"""
    name: str
    """The name of the upload portal."""
    url: str
    """The url postfix of the upload portal."""
    token: str
    """The token used to validate access to the upload portal."""
    bucketName: str
    """The S3 bucket name to store the uploaded data."""
    bucketPath: str
    """The S3 bucket path where uploaded data is stored."""
    description: Optional[str] = None
    """The purpose and description of the upload portal."""
    bucketId: Optional[int] = None
    """S3 bucket ID. If missing, then this is using the Edge Impulse hosted bucket."""
    bucketUrl: Optional[str] = None
    """The full S3 bucket path where uploaded data is stored."""


@dataclass(kw_only=True)
class Portals(ApiBaseModel):
    id: int
    name: str
    url: str
    bucketId: int
    bucketName: str
    bucketPath: str
    bucketUrl: str
    created: datetime
    description: Optional[str] = None


@dataclass(kw_only=True)
class ListOrganizationPortalsResponse(GenericApiResponse):
    portals: List[Portals]


@dataclass(kw_only=True)
class AddOrganizationApiKeyRequest(AddApiKeyRequest):
    role: Role


@dataclass(kw_only=True)
class AdminAddOrganizationApiKeyRequest(AddOrganizationApiKeyRequest):
    ttl: Optional[int] = None
    """Time to live in seconds. If not set, the key will expire in 1 minute."""


@dataclass(kw_only=True)
class XXYApiKeysClash201724240(ApiBaseModel):
    id: int
    apiKey: str
    name: str
    created: datetime
    role: Role
    isTransformationJobKey: bool


@dataclass(kw_only=True)
class ListOrganizationApiKeysResponse(GenericApiResponse):
    apiKeys: List[XXYApiKeysClash201724240]
    """List of API keys."""


@dataclass(kw_only=True)
class AddMemberRequest(ApiBaseModel):
    usernameOrEmail: str
    """Username or e-mail address"""
    role: OrganizationMemberRole
    datasets: List[str]
    """Only used for 'guest' users. Limits the datasets the user has access to."""


@dataclass(kw_only=True)
class InviteOrganizationMemberRequest(ApiBaseModel):
    email: str
    """E-mail address"""
    role: OrganizationMemberRole
    datasets: List[str]
    """Only used for 'guest' users. Limits the datasets the user has access to."""


@dataclass(kw_only=True)
class RemoveMemberRequest(ApiBaseModel):
    id: int


@dataclass(kw_only=True)
class SetMemberRoleRequest(ApiBaseModel):
    role: OrganizationMemberRole


@dataclass(kw_only=True)
class SetMemberDatasetsRequest(ApiBaseModel):
    datasets: List[str]


@dataclass(kw_only=True)
class StorageProvider(Enum):
    s3 = "s3"
    google = "google"
    azure = "azure"
    other = "other"


@dataclass(kw_only=True)
class VerifyOrganizationBucketRequest(ApiBaseModel):
    accessKey: str
    """Access key for the storage service: - For S3 and GCS: Use the access key. - For Azure: Use the Storage Account Name. """
    bucket: str
    """Name of the storage bucket or container."""
    endpoint: str
    """Endpoint URL for the storage service. For S3-compatible services, Azure, or custom endpoints. """
    storageProvider: StorageProvider = None
    """The type of storage backend to use. Supported options are: - 's3': Amazon S3 - 'google': Google Cloud Storage - 'azure': Azure Blob Storage - 'other': Other S3-compatible storage If not specified, defaults to 's3' """
    secretKey: Optional[str] = None
    """Secret key for the storage service: - For S3 and GCS: Use the secret key. - For Azure: Use the Storage Account Access Key. Note: You should either pass a `secretKey` value or a `bucketId` value. """
    bucketId: Optional[int] = None
    """ID of an existing bucket. If provided, the credentials from this bucket will be used unless overridden by the `secretKey` property. """
    region: Optional[str] = None
    """Optional region of the storage service (if applicable)."""
    prefix: Optional[str] = None
    """Optional prefix within the bucket. Set this if you don't have access to the full bucket or want to limit the scope. """


@dataclass(kw_only=True)
class ConnectionStatus(Enum):
    connected = "connected"
    connecting = "connecting"
    error = "error"


@dataclass(kw_only=True)
class Files(ApiBaseModel):
    name: str
    """The name of the file."""
    size: int
    """The size of the file in bytes."""
    folderName: str
    """The name of the folder containing the file."""


@dataclass(kw_only=True)
class VerifyOrganizationBucketResponse(GenericApiResponse):
    connectionStatus: ConnectionStatus
    """Indicates the current state of the connectivity verification process. - "connected": Verification successful, other properties are available. - "connecting": Verification in progress, continue polling. - "error": Verification failed, check connectionError for details. """
    connectionError: Optional[str] = None
    """Provides additional details if connectionStatus is "error". Helps diagnose verification failures. """
    connectionStatusSince: Optional[datetime] = None
    """Timestamp of when the connectionStatus last changed. """
    files: Optional[List[Optional[Files]]] = None
    """Random files from the bucket. Only available when connectionStatus is "connected"."""
    hasInfoLabelsFile: Optional[bool] = None
    """Indicates whether there are any info.labels files in this bucket. If so, those are used for category/labels. Only available when connectionStatus is "connected". """
    signedUrl: Optional[str] = None
    """A signed URL that allows you to PUT an item, to check whether CORS headers are set up correctly for this bucket. Only available when connectionStatus is "connected". """
    endpoint: Optional[str] = None
    """An alternative endpoint URL. Only returned and required for Azure storage accounts, where the endpoint must be reformatted. This field will be undefined for other storage providers. """


@dataclass(kw_only=True)
class AddOrganizationBucketRequest(ApiBaseModel):
    accessKey: str
    """Access key for the storage service (e.g., S3 access key, GCS access key)"""
    secretKey: str
    """Secret key for the storage service (e.g., S3 secret key, GCS secret key)"""
    endpoint: str
    """Endpoint URL for the storage service (e.g., S3 endpoint, custom endpoint for other services) """
    bucket: str
    """Name of the storage bucket"""
    region: str
    """Region of the storage service (if applicable)"""
    checkConnectivityPrefix: Optional[str] = None
    """Set this if you don't have access to the root of this bucket. Only used to verify connectivity to this bucket. """
    storageProvider: StorageProvider = None
    """The type of storage provider. Defaults to 's3' if not specified."""


@dataclass(kw_only=True)
class UpdateOrganizationBucketRequest(ApiBaseModel):
    accessKey: Optional[str] = None
    """S3 access key"""
    secretKey: Optional[str] = None
    """S3 secret key"""
    endpoint: Optional[str] = None
    """S3 endpoint"""
    bucket: Optional[str] = None
    """S3 bucket"""
    region: Optional[str] = None
    """S3 region"""
    checkConnectivityPrefix: Optional[str] = None
    """Set this if you don't have access to the root of this bucket. Only used to verify connectivity to this bucket. """
    storageAccountName: Optional[str] = None
    """The name of the storage account for Azure Blob Storage"""


@dataclass(kw_only=True)
class OrganizationBucket(ApiBaseModel):
    id: int
    accessKey: str
    """Access key for the storage service"""
    endpoint: str
    """Endpoint URL for the storage service"""
    bucket: str
    """Name of the storage bucket"""
    region: str
    """Region of the storage service (if applicable)"""
    connected: bool
    """Whether we can reach the bucket"""
    storageProvider: StorageProvider
    """The type of storage provider for this bucket"""
    checkConnectivityPrefix: Optional[str] = None
    """Optional prefix used for connectivity verification when root bucket access is restricted. """
    storageAccountName: Optional[str] = None
    """The name of the storage account for Azure Blob Storage"""


@dataclass(kw_only=True)
class ListOrganizationBucketsResponse(GenericApiResponse):
    buckets: List[OrganizationBucket]


@dataclass(kw_only=True)
class GetOrganizationBucketResponse(GenericApiResponse):
    bucket: OrganizationBucket


@dataclass(kw_only=True)
class XXYDataClash952810573(ApiBaseModel):
    id: int
    name: str
    bucketId: int
    bucketName: str
    bucketPath: str
    fullBucketPath: str
    dataset: str
    totalFileCount: int
    totalFileSize: int
    created: datetime
    metadata: Dict[str, str]
    metadataStringForCLI: str
    """String that's passed in to a transformation block in `--metadata` (the metadata + a `dataItemInfo` object)"""


@dataclass(kw_only=True)
class ListOrganizationDataResponse(GenericApiResponse):
    filterParseError: Optional[str] = None
    data: Optional[List[Optional[XXYDataClash952810573]]] = None
    totalFileCount: Optional[int] = None
    totalDataItemCount: Optional[int] = None


@dataclass(kw_only=True)
class OrganizationAddDataItemRequest(ApiBaseModel):
    name: str
    dataset: str
    metadata: str
    """Key-value pair of metadata (in JSON format)"""
    files__: List[bytes]
    bucketId: Optional[int] = None
    bucketName: Optional[str] = None
    """Name of the bucket name (as an Edge Impulse name)"""
    bucketPath: Optional[str] = None
    """Optional path in the bucket to create this data item (files are created under this path)."""


@dataclass(kw_only=True)
class XXYFilesClash1114814094(ApiBaseModel):
    name: str
    bucketPath: str
    size: int
    lastModified: Optional[datetime] = None


@dataclass(kw_only=True)
class OrganizationDataItem(ApiBaseModel):
    id: int
    name: str
    bucketId: int
    bucketName: str
    bucketPath: str
    dataset: str
    totalFileCount: int
    totalFileSize: int
    created: datetime
    metadata: Dict[str, str]
    files: List[XXYFilesClash1114814094]


@dataclass(kw_only=True)
class GetOrganizationDataItemResponse(GenericApiResponse):
    data: OrganizationDataItem


@dataclass(kw_only=True)
class UpdateOrganizationDataItemRequest(ApiBaseModel):
    name: Optional[str] = None
    dataset: Optional[str] = None
    metadata: Optional[Dict[str, Optional[str]]] = None


@dataclass(kw_only=True)
class OrganizationAddDataFileRequest(ApiBaseModel):
    files__: List[bytes]


@dataclass(kw_only=True)
class OrganizationCreateProjectRequestUploadTypeEnum(Enum):
    project = "project"
    dataset = "dataset"


@dataclass(kw_only=True)
class OrganizationCreateProjectRequestCategoryEnum(Enum):
    training = "training"
    testing = "testing"
    split = "split"


@dataclass(kw_only=True)
class OrganizationCreateProjectPathFilter(ApiBaseModel):
    dataset: str
    """Dataset name of files to transform"""
    filter: str
    """Path filter with wildcards, relative to the root of the dataset. For example, /folder/*.json will transform all JSON files in /folder (when operating on files)"""


@dataclass(kw_only=True)
class OrganizationCreateProjectOutputDatasetPathRule(Enum):
    no_subfolders = "no-subfolders"
    subfolder_per_item = "subfolder-per-item"
    use_full_path = "use-full-path"


@dataclass(kw_only=True)
class OrganizationCreateProjectRequest(ApiBaseModel):
    name: str
    filter: Optional[str] = None
    """Filter in SQL format, used for creating transformation jobs on clinical datasets"""
    pathFilters: Optional[List[OrganizationCreateProjectPathFilter]] = None
    """Set of paths to apply the transformation to, used for creating transformation jobs on default datasets. This option is experimental and may change in the future."""
    uploadType: OrganizationCreateProjectRequestUploadTypeEnum = None
    projectId: Optional[int] = None
    projectVisibility: ProjectVisibility = None
    newProjectName: Optional[str] = None
    projectApiKey: Optional[str] = None
    projectHmacKey: Optional[str] = None
    transformationBlockId: Optional[int] = None
    builtinTransformationBlock: Optional[Dict[str, Any]] = None
    category: OrganizationCreateProjectRequestCategoryEnum = None
    outputDatasetName: Optional[str] = None
    outputDatasetBucketId: Optional[int] = None
    outputDatasetBucketPath: Optional[str] = None
    """Path of new dataset within the bucket; used only when creating a new dataset."""
    outputPathInDataset: Optional[str] = None
    """Path within the selected dataset to upload transformed files into. Used only when uploading into a default (non-clinical) dataset."""
    outputDatasetPathRule: OrganizationCreateProjectOutputDatasetPathRule = None
    label: Optional[str] = None
    emailRecipientUids: Optional[List[Optional[int]]] = None
    transformationParallel: Optional[int] = None
    """Number of parallel jobs to start"""
    extraCliArguments: Optional[str] = None
    """Optional extra arguments for this transformation block"""
    parameters: Optional[Dict[str, Optional[str]]] = None
    """List of custom parameters for this transformation job (see the list of parameters that the block exposes)."""


@dataclass(kw_only=True)
class OrganizationCreateProjectUploadTypeEnum(Enum):
    dataset = "dataset"
    project = "project"


@dataclass(kw_only=True)
class OrganizationCreateProjectCategoryEnum(Enum):
    training = "training"
    testing = "testing"
    split = "split"


@dataclass(kw_only=True)
class OrganizationCreateProjectTransformationSummary(ApiBaseModel):
    startedCount: int
    succeededCount: int
    finishedCount: int
    totalFileCount: int
    totalTimeSpentSeconds: int
    """Total amount of compute used for this job (in seconds)"""


@dataclass(kw_only=True)
class TransformationJobStatusEnum(Enum):
    waiting = "waiting"
    created = "created"
    started = "started"
    finished = "finished"
    failed = "failed"


@dataclass(kw_only=True)
class TransformationJobOperatesOnEnum(Enum):
    file = "file"
    directory = "directory"
    standalone = "standalone"


@dataclass(kw_only=True)
class CreatedUpdatedByUser(ApiBaseModel):
    id: int
    name: str
    username: str
    photo: Optional[str] = None


@dataclass(kw_only=True)
class OrganizationCreateProject(ApiBaseModel):
    id: int
    organizationId: int
    name: str
    uploadType: OrganizationCreateProjectUploadTypeEnum
    status: TransformationJobStatusEnum
    transformJobStatus: TransformationJobStatusEnum
    uploadJobStatus: TransformationJobStatusEnum
    category: OrganizationCreateProjectCategoryEnum
    created: datetime
    totalDownloadFileCount: int
    totalDownloadFileSize: int
    totalDownloadFileSizeString: str
    totalUploadFileCount: int
    transformationParallel: int
    """Number of transformation jobs that can be ran in parallel"""
    transformationSummary: OrganizationCreateProjectTransformationSummary
    inProgress: bool
    operatesOn: TransformationJobOperatesOnEnum
    totalTimeSpentSeconds: int
    """Total amount of compute used for this job (in seconds)"""
    totalTimeSpentString: str
    """Total amount of compute used (friendly string)"""
    uploadJobId: Optional[int] = None
    uploadJobFilesUploaded: Optional[int] = None
    projectOwner: Optional[str] = None
    projectId: Optional[int] = None
    projectName: Optional[str] = None
    transformationBlockId: Optional[int] = None
    builtinTransformationBlock: Optional[Dict[str, Any]] = None
    transformationBlockName: Optional[str] = None
    outputDatasetName: Optional[str] = None
    outputDatasetBucketId: Optional[int] = None
    outputDatasetBucketPath: Optional[str] = None
    label: Optional[str] = None
    filterQuery: Optional[str] = None
    emailRecipientUids: Optional[List[Optional[int]]] = None
    pipelineId: Optional[int] = None
    pipelineName: Optional[str] = None
    pipelineRunId: Optional[int] = None
    pipelineStep: Optional[int] = None
    createdByUser: CreatedUpdatedByUser = None


@dataclass(kw_only=True)
class XXYFilesClash2111272839(ApiBaseModel):
    id: int
    fileName: str
    bucketPath: str
    transformationJobStatus: TransformationJobStatusEnum
    linkToDataItem: str
    lengthString: str
    """Only set after job was finished"""
    sourceDatasetType: OrganizationDatasetTypeEnum
    transformationJobId: Optional[int] = None


@dataclass(kw_only=True)
class OrganizationCreateProjectWithFiles(OrganizationCreateProject):
    files: List[XXYFilesClash2111272839]
    fileCountForFilter: int


@dataclass(kw_only=True)
class OrganizationCreateProjectResponse(GenericApiResponse):
    createProjectId: int
    """Project ID for the new project"""
    apiKey: str
    """API key for the new project"""


@dataclass(kw_only=True)
class ExportOriginalDataRequest(ApiBaseModel):
    uploaderFriendlyFilenames: bool
    """Whether to rename the exported file names to an uploader friendly format (e.g. label.filename.cbor)"""
    retainCrops: bool
    """Whether to retain crops and splits. If this is disabled, then the original files are returned (as they were uploaded)."""


@dataclass(kw_only=True)
class ExportWavDataRequest(ApiBaseModel):
    retainCrops: bool
    """Whether to retain crops and splits. If this is disabled, then the original files are returned (as they were uploaded)."""


@dataclass(kw_only=True)
class StartClassifyJobRequest(ApiBaseModel):
    modelVariants: Optional[List[KerasModelVariantEnum]] = None
    """Set of model variants to run the classify job against."""


@dataclass(kw_only=True)
class StartPostProcessingRequestDatasetEnum(Enum):
    training = "training"
    validation = "validation"
    testing = "testing"


@dataclass(kw_only=True)
class StartPostProcessingRequest(ApiBaseModel):
    variant: KerasModelVariantEnum
    """Which model variant to use (int8, float32, etc.)"""
    dataset: StartPostProcessingRequestDatasetEnum
    algorithm: str
    """Which algorithm container to use"""
    evaluation: str
    """Which evaluation container to use"""
    population: Optional[int] = None
    """The population size for the genetic algorithm"""
    maxGenerations: Optional[int] = None
    """The maximum number of generations for the genetic algorithm"""
    designSpaceTolerance: Optional[float] = None
    """The tolerance for the design space"""
    objectiveSpaceTolerance: Optional[float] = None
    """The tolerance for the objective space"""
    terminationPeriod: Optional[int] = None
    """The number of generations the termination criteria are averaged across"""


@dataclass(kw_only=True)
class VerifyDspBlockUrlRequest(ApiBaseModel):
    url: str


@dataclass(kw_only=True)
class Block(ApiBaseModel):
    title: str
    author: str
    description: str
    name: str
    latestImplementationVersion: int
    namedAxes: Optional[List[DSPNamedAxis]] = None


@dataclass(kw_only=True)
class VerifyDspBlockUrlResponse(GenericApiResponse):
    block: Optional[Block] = None


@dataclass(kw_only=True)
class Token(ApiBaseModel):
    socketToken: str
    expires: datetime


@dataclass(kw_only=True)
class SocketTokenResponse(GenericApiResponse):
    token: Token


@dataclass(kw_only=True)
class StartSamplingRequestCategoryEnum(Enum):
    training = "training"
    testing = "testing"
    anomaly = "anomaly"


@dataclass(kw_only=True)
class StartSamplingRequest(ApiBaseModel):
    label: str
    """Label to be used during sampling."""
    lengthMs: int
    """Requested length of the sample (in ms)."""
    category: StartSamplingRequestCategoryEnum
    intervalMs: float
    """Interval between samples (can be calculated like `1/hz * 1000`)"""
    sensor: Optional[str] = None
    """The sensor to sample from."""


@dataclass(kw_only=True)
class StartSamplingResponse(GenericApiResponse):
    id: Optional[int] = None


@dataclass(kw_only=True)
class ProjectDataAxesSummaryResponse(GenericApiResponse):
    dataAxisSummary: Dict[str, int]
    """Summary of the amount of data (in ms.) per sensor axis"""


@dataclass(kw_only=True)
class DataSummary(ApiBaseModel):
    labels: List[str]
    """Labels in the training set"""
    dataCount: int


@dataclass(kw_only=True)
class ProjectTrainingDataSummaryResponse(GenericApiResponse):
    dataSummary: DataSummary


@dataclass(kw_only=True)
class ProjectDataIntervalResponse(GenericApiResponse):
    intervalMs: int


@dataclass(kw_only=True)
class SetProjectComputeTimeRequest(ApiBaseModel):
    jobLimitM: int
    """New job limit in seconds."""


@dataclass(kw_only=True)
class SetProjectDspFileSizeRequest(ApiBaseModel):
    dspFileSizeMb: int
    """DSP File size in MB (default is 4096 MB)"""


@dataclass(kw_only=True)
class EnvironmentVariable(ApiBaseModel):
    key: str
    """Environmental variable key. Needs to adhere to regex "^[a-zA-Z_]+[a-zA-Z0-9_]*$"."""
    value: Optional[str] = None
    """If value is left undefined, only the key is passed in as an environmental variable."""


@dataclass(kw_only=True)
class AIActionsOperatesOn(Enum):
    images_object_detection = "images_object_detection"
    images_single_label = "images_single_label"
    audio = "audio"
    other = "other"


@dataclass(kw_only=True)
class TransformationBlockAdditionalMountPointTypeEnum(Enum):
    bucket = "bucket"
    portal = "portal"


@dataclass(kw_only=True)
class TransformationBlockAdditionalMountPoint(ApiBaseModel):
    type: TransformationBlockAdditionalMountPointTypeEnum
    mountPoint: str
    bucketId: Optional[int] = None
    portalId: Optional[int] = None


@dataclass(kw_only=True)
class OrganizationTransformationBlock(ApiBaseModel):
    id: int
    name: str
    dockerContainer: str
    dockerContainerManagedByEdgeImpulse: bool
    created: datetime
    description: str
    cliArguments: str
    """These arguments are passed into the container"""
    indMetadata: bool
    additionalMountPoints: List[TransformationBlockAdditionalMountPoint]
    operatesOn: TransformationJobOperatesOnEnum
    allowExtraCliArguments: bool
    sourceCodeAvailable: bool
    isPublic: bool
    """Whether this block is publicly available to Edge Impulse users (if false, then only for members of the owning organization)"""
    showInDataSources: bool
    """Whether to show this block in 'Data sources'. Only applies for standalone blocks."""
    showInCreateTransformationJob: bool
    """Whether to show this block in 'Create transformation job'. Only applies for standalone blocks."""
    showInSyntheticData: bool
    """Whether to show this block in 'Synthetic data'. Only applies for standalone blocks."""
    showInAIActions: bool
    """Whether to show this block in 'AI Labeling'. Only applies for standalone blocks."""
    environmentVariables: List[EnvironmentVariable]
    """Extra environmental variables that are passed into the transformation block (key/value pairs)."""
    createdByUser: CreatedUpdatedByUser = None
    lastUpdated: Optional[datetime] = None
    lastUpdatedByUser: CreatedUpdatedByUser = None
    userId: Optional[int] = None
    userName: Optional[str] = None
    requestsCpu: Optional[float] = None
    requestsMemory: Optional[int] = None
    limitsCpu: Optional[float] = None
    limitsMemory: Optional[int] = None
    parameters: Optional[List[Optional[Dict[str, Any]]]] = None
    """List of parameters, spec'ed according to https://docs.edgeimpulse.com/docs/tips-and-tricks/adding-parameters-to-custom-blocks"""
    parametersUI: Optional[List[DSPGroupItem]] = None
    """List of parameters to be rendered in the UI"""
    maxRunningTimeStr: Optional[str] = None
    """15m for 15 minutes, 2h for 2 hours, 1d for 1 day. If not set, the default is 8 hours."""
    repositoryUrl: Optional[str] = None
    """URL to the source code of this custom learn block."""
    aiActionsOperatesOn: Optional[List[AIActionsOperatesOn]] = None
    """For AI labeling blocks, this lists the data types that the block supports. If this field is empty then there's no information about supported data types."""


@dataclass(kw_only=True)
class PublicOrganizationTransformationBlock(ApiBaseModel):
    id: int
    ownerOrganizationId: int
    ownerOrganizationName: str
    name: str
    created: datetime
    description: str
    operatesOn: TransformationJobOperatesOnEnum
    allowExtraCliArguments: bool
    showInDataSources: bool
    """Whether to show this block in 'Data sources'. Only applies for standalone blocks."""
    showInCreateTransformationJob: bool
    """Whether to show this block in 'Create transformation job'. Only applies for standalone blocks."""
    showInSyntheticData: bool
    """Whether to show this block in 'Synthetic data'. Only applies for standalone blocks."""
    showInAIActions: bool
    """Whether to show this block in 'AI Labeling'. Only applies for standalone blocks."""
    lastUpdated: Optional[datetime] = None
    parameters: Optional[List[Optional[Dict[str, Any]]]] = None
    """List of parameters, spec'ed according to https://docs.edgeimpulse.com/docs/tips-and-tricks/adding-parameters-to-custom-blocks"""
    parametersUI: Optional[List[DSPGroupItem]] = None
    """List of parameters to be rendered in the UI"""
    repositoryUrl: Optional[str] = None
    """URL to the source code of this custom learn block."""
    aiActionsOperatesOn: Optional[List[AIActionsOperatesOn]] = None
    """For AI labeling blocks, this lists the data types that the block supports. If this field is empty then there's no information about supported data types."""


@dataclass(kw_only=True)
class GetOrganizationTransformationBlockResponse(GenericApiResponse):
    transformationBlock: OrganizationTransformationBlock


@dataclass(kw_only=True)
class ListOrganizationTransformationBlocksResponse(GenericApiResponse):
    transformationBlocks: List[OrganizationTransformationBlock]


@dataclass(kw_only=True)
class ListPublicOrganizationTransformationBlocksResponse(GenericApiResponse):
    transformationBlocks: List[PublicOrganizationTransformationBlock]


@dataclass(kw_only=True)
class GetPublicOrganizationTransformationBlockResponse(GenericApiResponse):
    transformationBlock: PublicOrganizationTransformationBlock


@dataclass(kw_only=True)
class AddOrganizationTransformationBlockRequestOperatesOnEnum(Enum):
    file = "file"
    directory = "directory"
    dataitem = "dataitem"
    standalone = "standalone"


@dataclass(kw_only=True)
class AddOrganizationTransformationBlockRequest(ApiBaseModel):
    name: str
    dockerContainer: str
    indMetadata: bool
    """Whether to pass the `--metadata` parameter to the container."""
    description: str
    cliArguments: str
    additionalMountPoints: List[TransformationBlockAdditionalMountPoint]
    operatesOn: AddOrganizationTransformationBlockRequestOperatesOnEnum
    requestsCpu: Optional[float] = None
    requestsMemory: Optional[int] = None
    limitsCpu: Optional[float] = None
    limitsMemory: Optional[int] = None
    allowExtraCliArguments: Optional[bool] = None
    parameters: Optional[List[Optional[Dict[str, Any]]]] = None
    """List of parameters, spec'ed according to https://docs.edgeimpulse.com/docs/tips-and-tricks/adding-parameters-to-custom-blocks"""
    maxRunningTimeStr: Optional[str] = None
    """15m for 15 minutes, 2h for 2 hours, 1d for 1 day. If not set, the default is 8 hours."""
    isPublic: Optional[bool] = None
    repositoryUrl: Optional[str] = None
    """URL to the source code of this custom learn block."""
    showInDataSources: Optional[bool] = None
    """Whether to show this block in 'Data sources'. Only applies for standalone blocks. (defaults to 'true' when not provided)"""
    showInCreateTransformationJob: Optional[bool] = None
    """Whether to show this block in 'Create transformation job'. Only applies for standalone blocks."""
    showInSyntheticData: Optional[bool] = None
    """Whether to show this block in 'Synthetic data'. Only applies for standalone blocks."""
    showInAIActions: Optional[bool] = None
    """Whether to show this block in 'AI Labeling'. Only applies for standalone blocks."""
    environmentVariables: Optional[List[EnvironmentVariable]] = None
    aiActionsOperatesOn: Optional[List[AIActionsOperatesOn]] = None
    """For AI labeling blocks, this lists the data types that the block supports. If this field is empty then there's no information about supported data types."""


@dataclass(kw_only=True)
class UpdateOrganizationTransformationBlockRequest(ApiBaseModel):
    name: Optional[str] = None
    dockerContainer: Optional[str] = None
    indMetadata: Optional[bool] = None
    """Whether to pass the `--metadata` parameter to the container."""
    description: Optional[str] = None
    cliArguments: Optional[str] = None
    requestsCpu: Optional[float] = None
    requestsMemory: Optional[int] = None
    limitsCpu: Optional[float] = None
    limitsMemory: Optional[int] = None
    additionalMountPoints: Optional[List[TransformationBlockAdditionalMountPoint]] = (
        None
    )
    operatesOn: TransformationJobOperatesOnEnum = None
    allowExtraCliArguments: Optional[bool] = None
    parameters: Optional[List[Optional[Dict[str, Any]]]] = None
    """List of parameters, spec'ed according to https://docs.edgeimpulse.com/docs/tips-and-tricks/adding-parameters-to-custom-blocks"""
    maxRunningTimeStr: Optional[str] = None
    """15m for 15 minutes, 2h for 2 hours, 1d for 1 day. If not set, the default is 8 hours."""
    isPublic: Optional[bool] = None
    repositoryUrl: Optional[str] = None
    """URL to the source code of this custom learn block."""
    showInDataSources: Optional[bool] = None
    """Whether to show this block in 'Data sources'. Only applies for standalone blocks."""
    showInCreateTransformationJob: Optional[bool] = None
    """Whether to show this block in 'Create transformation job'. Only applies for standalone blocks."""
    showInSyntheticData: Optional[bool] = None
    """Whether to show this block in 'Synthetic data'. Only applies for standalone blocks."""
    showInAIActions: Optional[bool] = None
    """Whether to show this block in 'AI Labeling'. Only applies for standalone blocks."""
    environmentVariables: Optional[List[EnvironmentVariable]] = None
    aiActionsOperatesOn: Optional[List[AIActionsOperatesOn]] = None
    """For AI labeling blocks, this lists the data types that the block supports. If this field is empty then there's no information about supported data types."""


@dataclass(kw_only=True)
class OrganizationDeployBlockCategoryEnum(Enum):
    library = "library"
    firmware = "firmware"


@dataclass(kw_only=True)
class OrganizationDeployBlock(ApiBaseModel):
    id: int
    name: str
    dockerContainer: str
    dockerContainerManagedByEdgeImpulse: bool
    created: datetime
    description: str
    cliArguments: str
    """These arguments are passed into the container"""
    photo: str
    privileged: bool
    mountLearnBlock: bool
    supportsEonCompiler: bool
    showOptimizations: bool
    category: OrganizationDeployBlockCategoryEnum
    sourceCodeAvailable: bool
    createdByUser: CreatedUpdatedByUser = None
    lastUpdated: Optional[datetime] = None
    lastUpdatedByUser: CreatedUpdatedByUser = None
    userId: Optional[int] = None
    userName: Optional[str] = None
    requestsCpu: Optional[float] = None
    requestsMemory: Optional[int] = None
    limitsCpu: Optional[float] = None
    limitsMemory: Optional[int] = None
    integrateUrl: Optional[str] = None


@dataclass(kw_only=True)
class GetOrganizationDeployBlockResponse(GenericApiResponse):
    deployBlock: OrganizationDeployBlock


@dataclass(kw_only=True)
class ListOrganizationDeployBlocksResponse(GenericApiResponse):
    deployBlocks: List[OrganizationDeployBlock]


@dataclass(kw_only=True)
class AddOrganizationDeployBlockRequestCategoryEnum(Enum):
    library = "library"
    firmware = "firmware"


@dataclass(kw_only=True)
class AddOrganizationDeployBlockRequest(ApiBaseModel):
    name: str
    dockerContainer: str
    description: str
    cliArguments: str
    requestsCpu: Optional[float] = None
    requestsMemory: Optional[int] = None
    limitsCpu: Optional[float] = None
    limitsMemory: Optional[int] = None
    photo: Optional[bytes] = None
    integrateUrl: Optional[str] = None
    privileged: Optional[bool] = None
    mountLearnBlock: Optional[bool] = None
    supportsEonCompiler: Optional[bool] = None
    showOptimizations: Optional[bool] = None
    category: AddOrganizationDeployBlockRequestCategoryEnum = None


@dataclass(kw_only=True)
class UpdateOrganizationDeployBlockRequestCategoryEnum(Enum):
    library = "library"
    firmware = "firmware"


@dataclass(kw_only=True)
class UpdateOrganizationDeployBlockRequest(ApiBaseModel):
    name: Optional[str] = None
    dockerContainer: Optional[str] = None
    description: Optional[str] = None
    cliArguments: Optional[str] = None
    requestsCpu: Optional[float] = None
    requestsMemory: Optional[int] = None
    limitsCpu: Optional[float] = None
    limitsMemory: Optional[int] = None
    photo: Optional[bytes] = None
    integrateUrl: Optional[str] = None
    privileged: Optional[bool] = None
    mountLearnBlock: Optional[bool] = None
    supportsEonCompiler: Optional[bool] = None
    showOptimizations: Optional[bool] = None
    category: UpdateOrganizationDeployBlockRequestCategoryEnum = None


@dataclass(kw_only=True)
class OrganizationDspBlock(ApiBaseModel):
    id: int
    name: str
    dockerContainer: str
    dockerContainerManagedByEdgeImpulse: bool
    created: datetime
    description: str
    port: int
    isConnected: bool
    sourceCodeAvailable: bool
    createdByUser: CreatedUpdatedByUser = None
    lastUpdated: Optional[datetime] = None
    lastUpdatedByUser: CreatedUpdatedByUser = None
    userId: Optional[int] = None
    userName: Optional[str] = None
    requestsCpu: Optional[float] = None
    requestsMemory: Optional[int] = None
    limitsCpu: Optional[float] = None
    limitsMemory: Optional[int] = None
    error: Optional[str] = None


@dataclass(kw_only=True)
class GetOrganizationDspBlockResponse(GenericApiResponse):
    dspBlock: OrganizationDspBlock


@dataclass(kw_only=True)
class ListOrganizationDspBlocksResponse(GenericApiResponse):
    dspBlocks: List[OrganizationDspBlock]


@dataclass(kw_only=True)
class AddOrganizationDspBlockRequest(ApiBaseModel):
    name: str
    dockerContainer: str
    description: str
    port: int
    requestsCpu: Optional[float] = None
    requestsMemory: Optional[int] = None
    limitsCpu: Optional[float] = None
    limitsMemory: Optional[int] = None


@dataclass(kw_only=True)
class UpdateOrganizationDspBlockRequest(ApiBaseModel):
    name: Optional[str] = None
    dockerContainer: Optional[str] = None
    description: Optional[str] = None
    requestsCpu: Optional[float] = None
    requestsMemory: Optional[int] = None
    limitsCpu: Optional[float] = None
    limitsMemory: Optional[int] = None
    port: Optional[int] = None


@dataclass(kw_only=True)
class OrganizationTransferLearningOperatesOn(Enum):
    object_detection = "object_detection"
    audio = "audio"
    image = "image"
    regression = "regression"
    other = "other"


@dataclass(kw_only=True)
class OrganizationTransferLearningBlock(ApiBaseModel):
    id: int
    name: str
    dockerContainer: str
    dockerContainerManagedByEdgeImpulse: bool
    created: datetime
    description: str
    operatesOn: OrganizationTransferLearningOperatesOn
    implementationVersion: int
    isPublic: bool
    """Whether this block is publicly available to Edge Impulse users (if false, then only for members of the owning organization)"""
    isPublicForDevices: List[str]
    """If `isPublic` is true, the list of devices (from latencyDevices) for which this model can be shown."""
    isPublicEnterpriseOnly: bool
    """Whether this block is publicly available to only enterprise users"""
    parameters: List[Dict[str, Any]]
    """List of parameters, spec'ed according to https://docs.edgeimpulse.com/docs/tips-and-tricks/adding-parameters-to-custom-blocks"""
    indRequiresGpu: bool
    """If set, requires this block to be scheduled on GPU."""
    sourceCodeAvailable: bool
    createdByUser: CreatedUpdatedByUser = None
    lastUpdated: Optional[datetime] = None
    lastUpdatedByUser: CreatedUpdatedByUser = None
    userId: Optional[int] = None
    userName: Optional[str] = None
    objectDetectionLastLayer: ObjectDetectionLastLayer = None
    publicProjectTierAvailability: PublicProjectTierAvailability = None
    enterpriseOnly: Optional[bool] = None
    """Whether this block is available to only enterprise users"""
    repositoryUrl: Optional[str] = None
    """URL to the source code of this custom learn block."""
    imageInputScaling: ImageInputScaling = None
    displayCategory: BlockDisplayCategory = None
    customModelVariants: Optional[
        List[OrganizationTransferLearningBlockCustomVariant]
    ] = None
    """List of custom model variants produced when this block is trained. This is experimental and may change in the future."""


@dataclass(kw_only=True)
class GetOrganizationTransferLearningBlockResponse(GenericApiResponse):
    transferLearningBlock: OrganizationTransferLearningBlock


@dataclass(kw_only=True)
class ListOrganizationTransferLearningBlocksResponse(GenericApiResponse):
    transferLearningBlocks: List[OrganizationTransferLearningBlock]


@dataclass(kw_only=True)
class AddOrganizationTransferLearningBlockRequest(ApiBaseModel):
    name: str
    dockerContainer: str
    description: str
    operatesOn: OrganizationTransferLearningOperatesOn
    implementationVersion: int
    objectDetectionLastLayer: ObjectDetectionLastLayer = None
    isPublic: Optional[bool] = None
    """Whether this block is publicly available to Edge Impulse users (if false, then only for members of the owning organization)"""
    isPublicForDevices: Optional[List[Optional[str]]] = None
    """If `isPublic` is true, the list of devices (from latencyDevices) for which this model can be shown."""
    publicProjectTierAvailability: PublicProjectTierAvailability = None
    repositoryUrl: Optional[str] = None
    """URL to the source code of this custom learn block."""
    parameters: Optional[List[Optional[Dict[str, Any]]]] = None
    """List of parameters, spec'ed according to https://docs.edgeimpulse.com/docs/tips-and-tricks/adding-parameters-to-custom-blocks"""
    imageInputScaling: ImageInputScaling = None
    indRequiresGpu: Optional[bool] = None
    """If set, requires this block to be scheduled on GPU."""
    customModelVariants: Optional[
        List[OrganizationTransferLearningBlockCustomVariant]
    ] = None
    """List of custom model variants produced when this block is trained. This is experimental and may change in the future."""
    displayCategory: BlockDisplayCategory = None


@dataclass(kw_only=True)
class UpdateOrganizationTransferLearningBlockRequest(ApiBaseModel):
    name: Optional[str] = None
    dockerContainer: Optional[str] = None
    description: Optional[str] = None
    operatesOn: OrganizationTransferLearningOperatesOn = None
    objectDetectionLastLayer: ObjectDetectionLastLayer = None
    implementationVersion: Optional[int] = None
    isPublic: Optional[bool] = None
    """Whether this block is publicly available to Edge Impulse users (if false, then only for members of the owning organization)"""
    isPublicForDevices: Optional[List[Optional[str]]] = None
    """If `isPublic` is true, the list of devices (from latencyDevices) for which this model can be shown."""
    publicProjectTierAvailability: PublicProjectTierAvailability = None
    repositoryUrl: Optional[str] = None
    """URL to the source code of this custom learn block."""
    parameters: Optional[List[Optional[Dict[str, Any]]]] = None
    """List of parameters, spec'ed according to https://docs.edgeimpulse.com/docs/tips-and-tricks/adding-parameters-to-custom-blocks"""
    imageInputScaling: ImageInputScaling = None
    indRequiresGpu: Optional[bool] = None
    """If set, requires this block to be scheduled on GPU."""
    displayCategory: BlockDisplayCategory = None
    customModelVariants: Optional[
        List[OrganizationTransferLearningBlockCustomVariant]
    ] = None
    """List of custom model variants produced when this block is trained. This is experimental and may change in the future."""


@dataclass(kw_only=True)
class ListOrganizationFilesResponse(GenericApiResponse):
    totalFileSize: int
    totalFileCount: int
    totalDataItemCount: int
    data: List[OrganizationDataItem]
    filterParseError: Optional[str] = None


@dataclass(kw_only=True)
class OrganizationCreateProjectStatusResponse(GenericApiResponse):
    status: OrganizationCreateProjectWithFiles = None


@dataclass(kw_only=True)
class UploadType(Enum):
    dataset = "dataset"
    project = "project"


@dataclass(kw_only=True)
class Jobs(ApiBaseModel):
    id: int
    name: str
    uploadType: UploadType
    transformJobStatus: TransformationJobStatusEnum
    uploadJobStatus: TransformationJobStatusEnum
    created: datetime
    totalDownloadFileCount: int
    totalDownloadFileSize: int
    totalDownloadFileSizeString: str
    totalTimeSpentString: str
    """Total amount of compute used (friendly string)"""
    organizationId: Optional[int] = None
    uploadJobId: Optional[int] = None
    projectOwner: Optional[str] = None
    projectId: Optional[int] = None
    projectName: Optional[str] = None
    transformationBlockId: Optional[int] = None
    builtinTransformationBlock: Optional[Dict[str, Any]] = None
    transformationBlockName: Optional[str] = None
    transformationOperatesOn: TransformationJobOperatesOnEnum = None
    outputDatasetName: Optional[str] = None
    outputDatasetBucketId: Optional[int] = None
    outputDatasetBucketPath: Optional[str] = None
    totalUploadFileCount: Optional[int] = None
    totalTimeSpentSeconds: Optional[int] = None
    """Total amount of compute used for this job (in seconds)"""
    createdByUser: CreatedUpdatedByUser = None


@dataclass(kw_only=True)
class OrganizationGetCreateProjectsResponse(GenericApiResponse):
    totalJobCount: int
    jobs: List[Jobs]


@dataclass(kw_only=True)
class LogLevel(Enum):
    error = "error"
    warn = "warn"
    info = "info"
    debug = "debug"


@dataclass(kw_only=True)
class Stdout(ApiBaseModel):
    created: datetime
    data: str
    logLevel: LogLevel = None


@dataclass(kw_only=True)
class LogStdoutResponse(GenericApiResponse):
    stdout: List[Stdout]
    totalCount: int
    """Total number of logs (only the last 1000 lines are returned)"""


@dataclass(kw_only=True)
class XXYLogLevelClash144526475(Enum):
    error = "error"
    warn = "warn"
    info = "info"
    debug = "debug"


@dataclass(kw_only=True)
class Logs(ApiBaseModel):
    created: datetime
    data: str
    logLevel: XXYLogLevelClash144526475 = None


@dataclass(kw_only=True)
class JobLogsResponse(GenericApiResponse):
    logs: List[Logs]


@dataclass(kw_only=True)
class TimeSeriesDataPoint(ApiBaseModel):
    timestamp: datetime
    value: float


@dataclass(kw_only=True)
class JobMetricsResponse(GenericApiResponse):
    cpuUsage: Optional[List[TimeSeriesDataPoint]] = None
    memoryUsage: Optional[List[TimeSeriesDataPoint]] = None


@dataclass(kw_only=True)
class GetJobResponse(GenericApiResponse):
    job: Job


@dataclass(kw_only=True)
class UpdateOrganizationCreateProjectRequest(ApiBaseModel):
    transformationParallel: Optional[int] = None
    """Number of transformation jobs that can be ran in parallel"""
    emailRecipientUids: Optional[List[Optional[int]]] = None
    """List of user IDs to notify when a Job succeeds"""


@dataclass(kw_only=True)
class UpdateOrganizationCreateEmptyProjectRequest(ApiBaseModel):
    projectName: str
    """The name of the project."""
    projectVisibility: ProjectVisibility = None
    projectOwnerUsernameOrEmail: Optional[str] = None
    """The username or email of the owner of the project. This field is mandatory when authenticating via API key. If no email is provided when authenticating via JWT, the user ID attached to the JWT will be user as project owner."""


@dataclass(kw_only=True)
class UpdateOrganizationAddCollaboratorRequest(ApiBaseModel):
    projectId: int
    """The ID of the project to add the collaborator to."""
    userId: int
    """The user ID to add to the project. The user must be an admin of the organization."""


@dataclass(kw_only=True)
class Users(ApiBaseModel):
    id: int
    username: str
    email: str
    name: str
    created: datetime
    photo: Optional[str] = None
    lastSeen: Optional[datetime] = None
    activated: Optional[bool] = None
    from_evaluation: Optional[bool] = None
    tier: UserTierEnum = None


@dataclass(kw_only=True)
class AdminGetUsersResponse(GenericApiResponse):
    total: int
    users: List[Users]


@dataclass(kw_only=True)
class AdminGetUserResponse(GenericApiResponse):
    user: AdminApiUser


@dataclass(kw_only=True)
class ReportCreatedByUser(ApiBaseModel):
    id: int
    name: str
    username: str
    photo: Optional[str] = None


@dataclass(kw_only=True)
class Report(ApiBaseModel):
    id: int
    created: datetime
    jobId: int
    jobFinished: bool
    jobFinishedSuccessful: bool
    reportStartDate: datetime
    reportEndDate: datetime
    createdByUser: ReportCreatedByUser = None
    downloadLink: Optional[str] = None


@dataclass(kw_only=True)
class AdminGetReportsResponse(GenericApiResponse):
    reports: List[Report]
    """List of organization usage reports."""
    totalCount: int


@dataclass(kw_only=True)
class AdminGetReportResponse(GenericApiResponse):
    report: Report


@dataclass(kw_only=True)
class AdminApiProject(ApiBaseModel):
    id: int
    name: str
    owner: str
    """User or organization that owns the project"""
    description: Optional[str] = None
    created: Optional[datetime] = None
    ownerUserId: Optional[int] = None
    ownerOrganizationId: Optional[int] = None
    lastAccessed: Optional[datetime] = None
    whitelabelId: Optional[int] = None
    """Unique identifier of the white label this project belongs to, if any."""
    tier: ProjectTierEnum = None
    category: ProjectType = None


@dataclass(kw_only=True)
class AdminListProjects(ApiBaseModel):
    total: int
    projects: List[AdminApiProject]
    """Array with projects"""


@dataclass(kw_only=True)
class AdminListProjectsResponse(GenericApiResponse, AdminListProjects):
    pass


@dataclass(kw_only=True)
class Organizations(ApiBaseModel):
    id: int
    name: str
    created: datetime
    privateProjectCount: int
    logo: Optional[str] = None
    readme: Optional[str] = None
    experiments: Optional[List[Optional[str]]] = None
    domain: Optional[str] = None
    whitelabelId: Optional[int] = None
    billable: Optional[bool] = None
    entitlementLimits: EntitlementLimits = None


@dataclass(kw_only=True)
class AdminGetOrganizationsResponse(GenericApiResponse):
    total: int
    organizations: List[Organizations]
    """Array with organizations"""


@dataclass(kw_only=True)
class AdminCreateOrganizationRequest(ApiBaseModel):
    organizationName: str
    """The name of the organization."""
    adminId: Optional[int] = None
    """Unique identifier of the administrator of the new organization."""


@dataclass(kw_only=True)
class AdminAddUserRequest(ApiBaseModel):
    usernameOrEmail: Optional[str] = None
    """Username or email of the user to be added to the project or organization. If no user is provided, the user ID attached to the JWT will be used."""


@dataclass(kw_only=True)
class AdminAddProjectUserRequest(AdminAddUserRequest):
    pass


@dataclass(kw_only=True)
class AdminAddOrganizationUserRequest(AdminAddUserRequest):
    role: OrganizationMemberRole
    datasets: List[str]
    """Only used for 'guest' users. Limits the datasets the user has access to."""


@dataclass(kw_only=True)
class XXYUsersClash314920790(ApiBaseModel):
    id: int
    username: str
    name: str
    created: datetime
    email: str
    photo: Optional[str] = None


@dataclass(kw_only=True)
class FindUserResponse(GenericApiResponse):
    users: List[XXYUsersClash314920790]


@dataclass(kw_only=True)
class OrganizationAddDataFolderRequest(ApiBaseModel):
    dataset: str
    bucketId: int
    bucketPath: str
    metadataDataset: Optional[str] = None
    type: OrganizationDatasetTypeEnum = None


@dataclass(kw_only=True)
class OrganizationAddDatasetRequestBucket(ApiBaseModel):
    id: int
    """Bucket ID"""
    path: str
    """Path in the bucket"""
    dataItemNamingLevelsDeep: int
    """Number of levels deep for data items, e.g. if you have folder "test/abc", with value 1 "test" will be a data item, with value 2 "test/abc" will be a data item. Only used for "clinical" type."""


@dataclass(kw_only=True)
class OrganizationAddDatasetRequest(ApiBaseModel):
    dataset: str
    tags: List[str]
    category: str
    type: OrganizationDatasetTypeEnum
    bucket: OrganizationAddDatasetRequestBucket


@dataclass(kw_only=True)
class OrganizationAddDataFolderResponse(GenericApiResponse):
    dataItemCount: int
    dataFirstItems: List[str]


@dataclass(kw_only=True)
class Buckets(ApiBaseModel):
    id: int
    organizationId: int
    organizationName: str
    bucket: str
    """S3 bucket"""
    region: str
    """S3 region"""
    whitelabelId: int
    """The unique identifier of the white label this bucket belongs to, if any"""


@dataclass(kw_only=True)
class ListOrganizationBucketsUserResponse(GenericApiResponse):
    buckets: List[Buckets]


@dataclass(kw_only=True)
class ProjectVersionRequest(ApiBaseModel):
    description: str
    makePublic: bool
    """Whether to make this version available on a public URL."""
    bucketId: Optional[int] = None
    """Data bucket ID. Keep empty to store in Edge Impulse hosted storage."""
    runModelTestingWhileVersioning: Optional[bool] = None
    """Whether to run model testing when creating this version (if this value is omitted, it will use the current state of 'runModelTestingWhileVersioning' that is returned in ListVersionsResponse)."""


@dataclass(kw_only=True)
class Bucket(ApiBaseModel):
    path: str
    id: Optional[int] = None
    name: Optional[str] = None
    organizationName: Optional[str] = None
    bucket: Optional[str] = None


@dataclass(kw_only=True)
class Versions(ApiBaseModel):
    id: int
    version: int
    description: str
    bucket: Bucket
    created: datetime
    userId: Optional[int] = None
    userName: Optional[str] = None
    userPhoto: Optional[str] = None
    publicProjectId: Optional[int] = None
    publicProjectUrl: Optional[str] = None
    trainingAccuracy: Optional[float] = None
    """Accuracy on training set."""
    testAccuracy: Optional[float] = None
    """Accuracy on test set."""
    accuracyBasedOnImpulse: Optional[str] = None
    """If your project had multiple impulses, this field indicates which impulse was used to calculate the accuracy metrics."""
    totalSamplesCount: Optional[str] = None
    license: Optional[str] = None


@dataclass(kw_only=True)
class CustomLearnBlocks(ApiBaseModel):
    author: str
    name: str


@dataclass(kw_only=True)
class ListVersionsResponse(GenericApiResponse):
    nextVersion: int
    versions: List[Versions]
    customLearnBlocks: List[CustomLearnBlocks]
    """If you have any custom learn blocks (e.g. blocks you pushed through Bring Your Own Model), then these are listed here. We use these to show a warning in the UI that these blocks will also be available in a public version."""
    runModelTestingWhileVersioning: bool
    """Whether the 'Run model testing while versioning' checkbox should be enabled."""


@dataclass(kw_only=True)
class XXYVersionsClash187812558(ApiBaseModel):
    version: int
    publicProjectId: int
    publicProjectUrl: str


@dataclass(kw_only=True)
class ListPublicVersionsResponse(GenericApiResponse):
    versions: List[XXYVersionsClash187812558]


@dataclass(kw_only=True)
class UpdateVersionRequest(ApiBaseModel):
    description: Optional[str] = None


@dataclass(kw_only=True)
class RestoreProjectRequest(ApiBaseModel):
    projectId: int
    """Source project ID"""
    projectApiKey: str
    """Source project API key"""
    versionId: int
    """Source project version ID"""


@dataclass(kw_only=True)
class RestoreProjectFromPublicRequest(ApiBaseModel):
    projectId: int
    """Source project ID"""


@dataclass(kw_only=True)
class Segments(ApiBaseModel):
    startMs: int
    endMs: int


@dataclass(kw_only=True)
class SegmentSampleRequest(ApiBaseModel):
    segments: List[Segments]


@dataclass(kw_only=True)
class TransferOwnershipOrganizationRequest(ApiBaseModel):
    organizationId: int


@dataclass(kw_only=True)
class FindSegmentSampleRequest(ApiBaseModel):
    shiftSegments: bool
    """If set, the segments are automatically shifted randomly, to make the dataset distribution more uniform."""
    segmentLengthMs: int


@dataclass(kw_only=True)
class FindSegmentSampleResponse(GenericApiResponse):
    segments: List[Segments]


@dataclass(kw_only=True)
class OrganizationBulkMetadataRequest(ApiBaseModel):
    dataset: str
    csvFile: bytes


@dataclass(kw_only=True)
class PortalInfoResponse(ApiBaseModel):
    name: str
    description: str
    organizationId: int
    organizationName: str
    bucketName: str
    organizationLogo: Optional[str] = None


@dataclass(kw_only=True)
class XXYSamplesClash1642525809(ApiBaseModel):
    id: int


@dataclass(kw_only=True)
class ObjectDetectionLabelQueueResponse(GenericApiResponse):
    samples: List[XXYSamplesClash1642525809]


@dataclass(kw_only=True)
class ObjectDetectionLabelQueueCountResponse(GenericApiResponse):
    samplesCount: int


@dataclass(kw_only=True)
class SampleBoundingBoxesRequest(ApiBaseModel):
    boundingBoxes: List[BoundingBox]


@dataclass(kw_only=True)
class TrackObjectsRequest(ApiBaseModel):
    sourceSampleId: int
    nextSampleId: int


@dataclass(kw_only=True)
class TrackObjectsResponse(GenericApiResponse):
    boundingBoxes: List[BoundingBox]


@dataclass(kw_only=True)
class ExportGetUrlResponse(GenericApiResponse):
    hasExport: bool
    created: Optional[datetime] = None
    """Set if hasExport is true"""
    url: Optional[str] = None
    """Set if hasExport is true"""


@dataclass(kw_only=True)
class GetSyntiantPosteriorResponse(GenericApiResponse):
    hasPosteriorParameters: bool
    parameters: Optional[Dict[str, Any]] = None


@dataclass(kw_only=True)
class SetSyntiantPosteriorRequest(ApiBaseModel):
    parameters: Dict[str, Any]


@dataclass(kw_only=True)
class FindSyntiantPosteriorRequestReferenceSetEnum(Enum):
    _600_seconds = "600_seconds"
    full = "full"
    custom = "custom"
    no_calibration = "no_calibration"


@dataclass(kw_only=True)
class FindSyntiantPosteriorRequestDeploymentTargetEnum(Enum):
    syntiant_ndp101 = "syntiant-ndp101"
    syntiant_ndp101_lib = "syntiant-ndp101-lib"
    syntiant_ndp120_lib = "syntiant-ndp120-lib"
    syntiant_ndp120_lib_tdk_v14 = "syntiant-ndp120-lib-tdk-v14"
    syntiant_nicla_ndp120 = "syntiant-nicla-ndp120"
    syntiant_avnet_rasyn = "syntiant-avnet-rasyn"


@dataclass(kw_only=True)
class FindSyntiantPosteriorRequest(ApiBaseModel):
    targetWords: List[str]
    referenceSet: FindSyntiantPosteriorRequestReferenceSetEnum
    wavFile: Optional[bytes] = None
    metaCsvFile: Optional[bytes] = None
    deploymentTarget: FindSyntiantPosteriorRequestDeploymentTargetEnum = None


@dataclass(kw_only=True)
class GetDeploymentResponse(GenericApiResponse):
    hasDeployment: bool
    version: Optional[int] = None


@dataclass(kw_only=True)
class LastBuild(ApiBaseModel):
    version: int
    """The build version, incremented after each deployment build"""
    deploymentType: str
    """Deployment type of the build"""
    engine: DeploymentTargetEngine
    created: datetime
    """The time this build was created"""
    modelType: KerasModelTypeEnum = None


@dataclass(kw_only=True)
class DeploymentTargetUiSectionEnum(Enum):
    library = "library"
    firmware = "firmware"
    mobile = "mobile"
    hidden = "hidden"


@dataclass(kw_only=True)
class DeploymentTargetBadge(ApiBaseModel):
    name: str
    description: str


@dataclass(kw_only=True)
class DeploymentTarget(ApiBaseModel):
    name: str
    description: str
    image: str
    imageClasses: str
    format: str
    hasEonCompiler: bool
    """Preferably use supportedEngines / preferredEngine"""
    hasTensorRT: bool
    """Preferably use supportedEngines / preferredEngine"""
    hasTensaiFlow: bool
    """Preferably use supportedEngines / preferredEngine"""
    hasDRPAI: bool
    """Preferably use supportedEngines / preferredEngine"""
    hasTIDL: bool
    """Preferably use supportedEngines / preferredEngine"""
    hasAkida: bool
    """Preferably use supportedEngines / preferredEngine"""
    hasMemryx: bool
    """Preferably use supportedEngines / preferredEngine"""
    hideOptimizations: bool
    uiSection: DeploymentTargetUiSectionEnum
    supportedEngines: List[DeploymentTargetEngine]
    preferredEngine: DeploymentTargetEngine
    docsUrl: str
    latencyDevice: Optional[str] = None
    badge: DeploymentTargetBadge = None
    customDeployId: Optional[int] = None
    integrateUrl: Optional[str] = None
    ownerOrganizationName: Optional[str] = None
    url: Optional[str] = None
    firmwareRepoUrl: Optional[str] = None


@dataclass(kw_only=True)
class ProjectDeploymentTarget(DeploymentTarget):
    recommendedForProject: bool
    """Whether this deployment target is recommended for the project based on connected devices."""
    disabledForProject: bool
    """Whether this deployment target is disabled for the project based on various attributes of the project."""
    reasonTargetDisabled: Optional[str] = None
    """If the deployment target is disabled for the project, this gives the reason why."""


@dataclass(kw_only=True)
class GetLastDeploymentBuildResponse(GenericApiResponse):
    hasBuild: bool
    """Does the deployment build still exist? (Builds are deleted if they are no longer valid for the project)"""
    lastBuild: Optional[LastBuild] = None
    lastDeploymentTarget: ProjectDeploymentTarget = None


@dataclass(kw_only=True)
class ThirdPartyAuth(ApiBaseModel):
    id: int
    name: str
    description: str
    logo: str
    domains: List[str]
    created: datetime


@dataclass(kw_only=True)
class GetThirdPartyAuthResponse(GenericApiResponse):
    auth: ThirdPartyAuth


@dataclass(kw_only=True)
class AuthorizeThirdPartyRequest(ApiBaseModel):
    nextUrl: str
    """The URL to redirect to after authorization is completed."""


@dataclass(kw_only=True)
class GetAllThirdPartyAuthResponse(GenericApiResponse):
    auths: List[ThirdPartyAuth]


@dataclass(kw_only=True)
class CreateThirdPartyAuthRequest(ApiBaseModel):
    name: str
    description: str
    logo: str
    domains: List[str]
    secretKey: Optional[str] = None
    apiKey: Optional[str] = None


@dataclass(kw_only=True)
class CreateThirdPartyAuthResponse(GenericApiResponse):
    id: int
    secretKey: str
    apiKey: str


@dataclass(kw_only=True)
class UpdateThirdPartyAuthRequest(ApiBaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    logo: Optional[str] = None
    domains: Optional[List[Optional[str]]] = None


@dataclass(kw_only=True)
class CreateUserThirdPartyRequest(ApiBaseModel):
    name: str
    """Your name"""
    username: str
    """Username, minimum 4 and maximum 30 characters. May contain alphanumeric characters, hyphens, underscores and dots. Validated according to `^(?=.{4,30}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._-]+(?<![_.])$`."""
    email: str
    """E-mail address. Will need to be validated before the account will become active."""
    privacyPolicy: bool
    """Whether the user accepted the privacy policy"""
    projectName: Optional[str] = None
    """A project will automatically be created. Sets the name of the first project. If not set, this will be derived from the username."""


@dataclass(kw_only=True)
class CreateUserThirdPartyResponse(GenericApiResponse):
    status: Status
    jwtToken: Optional[str] = None


@dataclass(kw_only=True)
class UserByThirdPartyActivationRequest(ApiBaseModel):
    activationCode: str


@dataclass(kw_only=True)
class ActivateUserByThirdPartyActivationCodeRequest(ApiBaseModel):
    activationCode: str
    password: str
    """Password, minimum length 8 characters."""
    username: str
    """Username, minimum 4 and maximum 30 characters. May contain alphanumeric characters, hyphens, underscores and dots. Validated according to `^(?=.{4,30}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._-]+(?<![_.])$`."""
    name: Optional[str] = None
    """Your name"""
    privacyPolicy: Optional[bool] = None
    """Whether the user accepted the privacy policy"""


@dataclass(kw_only=True)
class CalculateDataQualityMetricsRequestRepresentationEnum(Enum):
    keywords = "keywords"
    images = "images"
    current_impulse = "current-impulse"
    current_impulse_embeddings = "current-impulse-embeddings"


@dataclass(kw_only=True)
class CalculateDataQualityMetricsRequest(ApiBaseModel):
    representation: CalculateDataQualityMetricsRequestRepresentationEnum = None


@dataclass(kw_only=True)
class ProjectDownloadsResponse(GenericApiResponse):
    downloads: List[Download]


@dataclass(kw_only=True)
class CropSampleResponse(GenericApiResponse):
    requiresProcessing: bool


@dataclass(kw_only=True)
class OrganizationPipelineStepUploadTypeEnum(Enum):
    project = "project"
    dataset = "dataset"


@dataclass(kw_only=True)
class OrganizationPipelineStepCategoryEnum(Enum):
    training = "training"
    testing = "testing"
    split = "split"


@dataclass(kw_only=True)
class OrganizationPipelineStep(ApiBaseModel):
    name: str
    filter: Optional[str] = None
    pathFilters: Optional[List[OrganizationCreateProjectPathFilter]] = None
    """Set of paths to apply the transformation to, used for creating transformation jobs on default datasets. This option is experimental and may change in the future."""
    uploadType: OrganizationPipelineStepUploadTypeEnum = None
    projectId: Optional[int] = None
    newProjectName: Optional[str] = None
    projectApiKey: Optional[str] = None
    projectHmacKey: Optional[str] = None
    transformationBlockId: Optional[int] = None
    builtinTransformationBlock: Optional[Dict[str, Any]] = None
    category: OrganizationPipelineStepCategoryEnum = None
    outputDatasetName: Optional[str] = None
    outputDatasetBucketId: Optional[int] = None
    outputDatasetBucketPath: Optional[str] = None
    outputPathInDataset: Optional[str] = None
    """Path within the selected dataset to upload transformed files into. Used only when uploading into a default (non-clinical) dataset."""
    outputDatasetPathRule: OrganizationCreateProjectOutputDatasetPathRule = None
    label: Optional[str] = None
    transformationParallel: Optional[int] = None
    extraCliArguments: Optional[str] = None
    parameters: Optional[Dict[str, Optional[str]]] = None


@dataclass(kw_only=True)
class OrganizationPipelineRunStepUploadTypeEnum(Enum):
    project = "project"
    dataset = "dataset"


@dataclass(kw_only=True)
class OrganizationPipelineRunStepCategoryEnum(Enum):
    training = "training"
    testing = "testing"
    split = "split"


@dataclass(kw_only=True)
class OrganizationPipelineRunStep(ApiBaseModel):
    name: str
    transformationJob: OrganizationCreateProject = None
    filter: Optional[str] = None
    uploadType: OrganizationPipelineRunStepUploadTypeEnum = None
    projectId: Optional[int] = None
    newProjectName: Optional[str] = None
    projectApiKey: Optional[str] = None
    projectHmacKey: Optional[str] = None
    transformationBlockId: Optional[int] = None
    builtinTransformationBlock: Optional[Dict[str, Any]] = None
    category: OrganizationPipelineRunStepCategoryEnum = None
    outputDatasetName: Optional[str] = None
    outputDatasetBucketId: Optional[int] = None
    outputDatasetBucketPath: Optional[str] = None
    label: Optional[str] = None
    extraCliArguments: Optional[str] = None
    parameters: Optional[Dict[str, Optional[str]]] = None


@dataclass(kw_only=True)
class OrganizationPipelineItemCount(ApiBaseModel):
    itemCount: int
    itemCountChecklistOK: int
    itemCountChecklistFailed: int


@dataclass(kw_only=True)
class OrganizationPipelineRun(ApiBaseModel):
    id: int
    steps: List[OrganizationPipelineRunStep]
    created: datetime
    finished: Optional[datetime] = None
    itemCountBefore: OrganizationPipelineItemCount = None
    """Item count before the pipeline ran, only set when the pipeline has a dataset attached."""
    itemCountAfter: OrganizationPipelineItemCount = None
    """Item count after the pipeline ran, only set when the pipeline has a dataset attached."""
    itemCountImportIntoProjectFailed: Optional[int] = None
    """Number of data items that failed to import into a project (through the s3-to-project, portal-to-project or dataset-to-project) transform blocks"""


@dataclass(kw_only=True)
class OrganizationPipelineFeedingIntoDataset(ApiBaseModel):
    dataset: str
    datasetLink: str
    itemCount: int
    itemCountChecklistOK: int
    itemCountChecklistError: int
    datasetType: OrganizationDatasetTypeEnum = None


@dataclass(kw_only=True)
class OrganizationPipelineFeedingIntoProject(ApiBaseModel):
    id: int
    name: str
    projectLink: str
    itemCount: int


@dataclass(kw_only=True)
class OrganizationPipelineWhenToEmailEnum(Enum):
    always = "always"
    on_new_data = "on_new_data"
    never = "never"


@dataclass(kw_only=True)
class OrganizationPipeline(ApiBaseModel):
    id: int
    name: str
    description: str
    steps: List[OrganizationPipelineStep]
    created: datetime
    emailRecipientUids: List[int]
    whenToEmail: OrganizationPipelineWhenToEmailEnum
    intervalStr: Optional[str] = None
    """15m for every 15 minutes, 2h for every 2 hours, 1d for every 1 day"""
    nextRun: Optional[datetime] = None
    currentRun: OrganizationPipelineRun = None
    lastRun: OrganizationPipelineRun = None
    feedingIntoDataset: OrganizationPipelineFeedingIntoDataset = None
    feedingIntoProject: OrganizationPipelineFeedingIntoProject = None
    lastRunStartError: Optional[str] = None
    notificationWebhook: Optional[str] = None


@dataclass(kw_only=True)
class OrganizationUpdatePipelineBodyWhenToEmailEnum(Enum):
    always = "always"
    on_new_data = "on_new_data"
    never = "never"


@dataclass(kw_only=True)
class OrganizationUpdatePipelineBody(ApiBaseModel):
    name: str
    description: str
    steps: List[OrganizationPipelineStep]
    emailRecipientUids: List[int]
    whenToEmail: OrganizationUpdatePipelineBodyWhenToEmailEnum
    intervalStr: Optional[str] = None
    """15m for every 15 minutes, 2h for every 2 hours, 1d for every 1 day"""
    dataset: Optional[str] = None
    projectId: Optional[int] = None
    notificationWebhook: Optional[str] = None
    archived: Optional[bool] = None


@dataclass(kw_only=True)
class ListOrganizationPipelinesResponse(GenericApiResponse):
    pipelines: List[OrganizationPipeline]


@dataclass(kw_only=True)
class GetOrganizationPipelinesResponse(GenericApiResponse):
    pipeline: OrganizationPipeline


@dataclass(kw_only=True)
class RunOrganizationPipelineResponse(GenericApiResponse):
    pipelineRun: OrganizationPipelineRun


@dataclass(kw_only=True)
class UploadReadmeImageResponse(GenericApiResponse):
    url: str


@dataclass(kw_only=True)
class UploadAssetRequest(ApiBaseModel):
    image: Optional[bytes] = None


@dataclass(kw_only=True)
class UploadAssetResponse(GenericApiResponse):
    url: Optional[str] = None


@dataclass(kw_only=True)
class SetOrganizationDataDatasetRequest(ApiBaseModel):
    dataset: str


@dataclass(kw_only=True)
class Features(ApiBaseModel):
    axis: str
    importance: float


@dataclass(kw_only=True)
class Labels(ApiBaseModel):
    features: List[Features]


@dataclass(kw_only=True)
class DspFeatureImportanceResponse(GenericApiResponse):
    hasFeatureImportance: bool
    labels: Dict[str, Labels]


@dataclass(kw_only=True)
class Results(ApiBaseModel):
    key: str
    value: str


@dataclass(kw_only=True)
class DspAutotunerResults(GenericApiResponse):
    results: List[Results]


@dataclass(kw_only=True)
class XXYPerformanceClash1186250921(ApiBaseModel):
    mcu: str
    latency: int
    """Latency estimate, in ms"""
    ram: int
    """RAM estimate, in bytes"""


@dataclass(kw_only=True)
class DspPerformanceAllVariantsResponse(GenericApiResponse):
    performance: Optional[List[Optional[XXYPerformanceClash1186250921]]] = None
    """List of performance estimates for each supported MCU."""


@dataclass(kw_only=True)
class DeploymentTargetsResponse(GenericApiResponse):
    targets: List[DeploymentTarget]


@dataclass(kw_only=True)
class ProjectDeploymentTargetsResponse(GenericApiResponse):
    targets: List[ProjectDeploymentTarget]


@dataclass(kw_only=True)
class DeploymentOptionsOrder(ApiBaseModel):
    pass


@dataclass(kw_only=True)
class ThemeFavicon(ApiBaseModel):
    favicon32: Optional[str] = None
    favicon57: Optional[str] = None
    favicon76: Optional[str] = None
    favicon96: Optional[str] = None
    favicon120: Optional[str] = None
    favicon128: Optional[str] = None
    favicon144: Optional[str] = None
    favicon152: Optional[str] = None
    favicon180: Optional[str] = None
    favicon228: Optional[str] = None


@dataclass(kw_only=True)
class ThemeLogos(ApiBaseModel):
    primary: Optional[str] = None
    primaryPng: Optional[str] = None
    primaryWhite: Optional[str] = None
    loginLogo: Optional[str] = None
    loginLogoWhite: Optional[str] = None
    mark: Optional[str] = None
    markWhite: Optional[str] = None
    deviceLogo: Optional[str] = None


@dataclass(kw_only=True)
class ThemeColors(ApiBaseModel):
    primaryColor: Optional[str] = None
    primaryColorRgb: Optional[List[Optional[float]]] = None
    primaryColorGradientEnd: Optional[str] = None


@dataclass(kw_only=True)
class Theme(ApiBaseModel):
    id: int
    name: str
    favicon: ThemeFavicon
    logos: ThemeLogos
    colors: ThemeColors
    ownerUserId: Optional[int] = None
    ownerOrganizationId: Optional[int] = None


@dataclass(kw_only=True)
class GetThemesResponse(GenericApiResponse):
    themes: List[Theme]


@dataclass(kw_only=True)
class GetThemeResponse(GenericApiResponse):
    theme: Theme = None


@dataclass(kw_only=True)
class UpdateJobRequest(ApiBaseModel):
    jobNotificationUids: Optional[List[Optional[int]]] = None
    """The IDs of users who should be notified when a job is finished."""


@dataclass(kw_only=True)
class UpdateThemeLogosRequest(ApiBaseModel):
    primary: Optional[str] = None
    """Primary logo URL"""
    primaryWhite: Optional[str] = None
    """Primary logo for dark background URL"""
    login: Optional[str] = None
    """Login logo URL"""
    loginWhite: Optional[str] = None
    """Login logo for dark background URL"""
    mark: Optional[str] = None
    """Mark URL"""
    markWhite: Optional[str] = None
    """Mark for dark background URL"""
    deviceLogo: Optional[str] = None
    """Device logo URL"""


@dataclass(kw_only=True)
class UpdateThemeColorsRequest(ApiBaseModel):
    primaryColor: Optional[str] = None
    """Primary color in hex format"""
    primaryColorGradientEnd: Optional[str] = None
    """Primary color gradient end in hex format"""


@dataclass(kw_only=True)
class UploadImageRequest(ApiBaseModel):
    image: bytes


@dataclass(kw_only=True)
class AllLearningBlocks(ApiBaseModel):
    title: str
    """The name of the learning block"""
    type: str
    """The learning block type"""


@dataclass(kw_only=True)
class DevelopmentBoardResponse(ApiBaseModel):
    id: int
    name: str
    image: str
    docsUrl: str


@dataclass(kw_only=True)
class CustomDeploymentBlocks(ApiBaseModel):
    name: str
    """The name of the custom deployment block"""
    id: float
    """The custom deployment block ID"""


@dataclass(kw_only=True)
class Whitelabel(ApiBaseModel):
    id: int
    name: str
    domain: str
    themeId: int
    identityProviders: List[str]
    allowPasswordAuth: bool
    deploymentTargets: List[str]
    """List of deployment targets enabled for this white label"""
    allDeploymentTargets: List[str]
    """List of all supported deployment targets"""
    allowSignup: bool
    allowFreeProjects: bool
    supportedProjectTypes: List[ProjectType]
    allowNewProjectUi: bool
    """Whether the new project UI should be enabled for this white label or not."""
    learningBlocks: List[str]
    """List of learning blocks enabled for this white label"""
    allLearningBlocks: List[AllLearningBlocks]
    """List of all supported learning blocks"""
    developmentBoards: List[DevelopmentBoardResponse]
    allDevelopmentBoards: List[DevelopmentBoardResponse]
    ownerOrganizationId: Optional[int] = None
    theme: Theme = None
    customDeploymentBlocks: Optional[List[Optional[CustomDeploymentBlocks]]] = None
    """List of custom deployment blocks available to this white label"""
    deploymentOptionsOrder: DeploymentOptionsOrder = None
    exposePublicProjects: Optional[bool] = None
    defaultDeploymentTarget: Optional[str] = None
    """The name of the default deployment target for this white label"""
    organizationsLimit: Optional[int] = None
    """The maximum number of organizations that can be created under this white label."""


@dataclass(kw_only=True)
class GetAllWhitelabelsResponse(GenericApiResponse):
    whitelabels: List[Whitelabel]


@dataclass(kw_only=True)
class CreateWhitelabelRequest(ApiBaseModel):
    name: str
    """The name of the white label."""
    domain: str
    """The domain where the white label lives."""
    ownerOrganizationId: int
    identityProviders: Optional[List[Optional[str]]] = None
    """The list of allowed identity providers."""
    allowPasswordAuth: Optional[bool] = None
    """Whether this white label accepts password based authentication."""
    deploymentTargets: Optional[List[Optional[str]]] = None
    """The list of deployment targets to show on the UI"""
    documentationUrl: Optional[str] = None
    """Custom documentation URL"""
    allowSignup: Optional[bool] = None
    """Whether this white label allow sign ups or not."""
    allowFreeProjects: Optional[bool] = None
    """Whether this white label allows the creation of free projects."""
    sandboxed: Optional[bool] = None
    """Whether this white label should work in sandboxed mode or not."""
    exposePublicProjects: Optional[bool] = None
    """Whether public projects created in this white label scope should be exposed through the Public Projects API or not."""
    learningBlocks: Optional[List[Optional[str]]] = None
    """The list of learning block types to show on the UI"""
    organizationsLimit: Optional[int] = None
    """The maximum number of organizations that can be created under this white label."""


@dataclass(kw_only=True)
class CreateWhitelabelResponse(GenericApiResponse):
    id: int
    """Unique whitelabel identifier"""
    themeId: int
    """Unique identifier for the theme associated with the white label"""


@dataclass(kw_only=True)
class GetWhitelabelResponse(GenericApiResponse):
    whitelabel: Whitelabel = None


@dataclass(kw_only=True)
class GetWhitelabelDomainResponse(GenericApiResponse):
    domain: str
    logo: Optional[str] = None


@dataclass(kw_only=True)
class UpdateWhitelabelInternalRequest(ApiBaseModel):
    organizationsLimit: Optional[int] = None
    """The maximum number of organizations that can be created under this white label."""


@dataclass(kw_only=True)
class UpdateWhitelabelDeploymentTargetsRequest(ApiBaseModel):
    targets: Optional[List[Optional[str]]] = None
    """The names of the deployment targets that are enabled for this whitelabel."""


@dataclass(kw_only=True)
class UpdateWhitelabelDeploymentOptionsOrderRequest(ApiBaseModel):
    order: DeploymentOptionsOrder = None


@dataclass(kw_only=True)
class UpdateWhitelabelLearningBlocksRequest(ApiBaseModel):
    learningBlocks: Optional[List[Optional[str]]] = None
    """The types of the learning blocks that are enabled for this whitelabel."""


@dataclass(kw_only=True)
class XXYResultsClash920046438(ApiBaseModel):
    label: str
    x: int
    y: int
    width: int
    height: int


@dataclass(kw_only=True)
class ObjectDetectionAutoLabelResponse(GenericApiResponse):
    results: List[XXYResultsClash920046438]
    allLabels: List[str]


@dataclass(kw_only=True)
class ObjectDetectionAutoLabelRequestNeuralNetworkEnum(Enum):
    yolov5 = "yolov5"
    currentProject = "currentProject"


@dataclass(kw_only=True)
class ObjectDetectionAutoLabelRequest(ApiBaseModel):
    neuralNetwork: ObjectDetectionAutoLabelRequestNeuralNetworkEnum


@dataclass(kw_only=True)
class Secrets(ApiBaseModel):
    id: int
    name: str
    description: str
    created: datetime
    createdByUser: CreatedUpdatedByUser = None


@dataclass(kw_only=True)
class ListOrganizationSecretsResponse(GenericApiResponse):
    secrets: List[Secrets]


@dataclass(kw_only=True)
class AddOrganizationSecretRequest(ApiBaseModel):
    name: str
    description: str
    secret: str


@dataclass(kw_only=True)
class DataExplorerSettingsPresetEnum(Enum):
    keywords = "keywords"
    images = "images"
    current_impulse = "current-impulse"
    current_impulse_embeddings = "current-impulse-embeddings"


@dataclass(kw_only=True)
class DataExplorerSettingsDimensionalityReductionTechniqueEnum(Enum):
    tsne = "tsne"
    pca = "pca"


@dataclass(kw_only=True)
class DataExplorerSettings(ApiBaseModel):
    preset: DataExplorerSettingsPresetEnum = None
    dimensionalityReductionTechnique: DataExplorerSettingsDimensionalityReductionTechniqueEnum = None
    impulseId: Optional[int] = None
    """Which impulse to use (if preset is either 'current-impulse' or 'current-impulse-embeddings'). If this is undefined then 'defaultImpulseId' is used."""


@dataclass(kw_only=True)
class DimensionalityReductionRecommendation(Enum):
    tsne = "tsne"
    pca = "pca"


@dataclass(kw_only=True)
class GetDataExplorerSettingsResponse(GenericApiResponse, DataExplorerSettings):
    dimensionalityReductionRecommendation: DimensionalityReductionRecommendation


@dataclass(kw_only=True)
class GetUserNeedToSetPasswordResponse(GenericApiResponse):
    email: Optional[str] = None
    """User email"""
    needPassword: Optional[bool] = None
    """Whether the user needs to set its password or not"""
    whitelabels: Optional[List[Optional[str]]] = None
    """White label domains the user belongs to, if any"""
    trials: Optional[List[EnterpriseTrial]] = None
    """Current or past enterprise trials."""
    emailVerified: Optional[bool] = None
    """Whether the user has verified its email address or not"""


@dataclass(kw_only=True)
class SetUserPasswordRequest(ApiBaseModel):
    accessToken: str
    identityProvider: str
    password: str


@dataclass(kw_only=True)
class GetOrganizationDatasetResponse(GenericApiResponse):
    dataset: OrganizationDataset


@dataclass(kw_only=True)
class UpdateOrganizationDatasetRequestBucket(ApiBaseModel):
    id: int
    """Bucket ID"""
    path: str
    """Path in the bucket"""
    dataItemNamingLevelsDeep: int
    """Number of levels deep for data items, e.g. if you have folder "test/abc", with value 1 "test" will be a data item, with value 2 "test/abc" will be a data item. Only used for "clinical" datasets."""


@dataclass(kw_only=True)
class UpdateOrganizationDatasetRequest(ApiBaseModel):
    dataset: Optional[str] = None
    tags: Optional[List[Optional[str]]] = None
    category: Optional[str] = None
    type: OrganizationDatasetTypeEnum = None
    bucket: UpdateOrganizationDatasetRequestBucket = None


@dataclass(kw_only=True)
class LastModificationDateResponse(GenericApiResponse):
    lastModificationDate: Optional[datetime] = None
    lastVersionDate: Optional[datetime] = None


@dataclass(kw_only=True)
class CreateDeveloperProfileResponse(GenericApiResponse):
    organizationId: int
    link: Optional[str] = None


@dataclass(kw_only=True)
class AdminUpdateUserRequest(ApiBaseModel):
    email: Optional[str] = None
    """New email. This will also update the forum's email address but the user may need to logout/login back"""
    name: Optional[str] = None
    """New user full name"""
    activated: Optional[bool] = None
    """Whether the user is active or not. Can only go from inactive to active."""
    suspended: Optional[bool] = None
    """Whether the user is suspended or not."""
    jobTitle: Optional[str] = None
    """New user job title"""
    experiments: Optional[List[Optional[str]]] = None
    """List of user experiments"""


@dataclass(kw_only=True)
class AdminUpdateConfigRequest(ApiBaseModel):
    value: str
    """New config value, given as a JSON string."""


@dataclass(kw_only=True)
class AdminUpdateOrganizationRequest(ApiBaseModel):
    logo: Optional[str] = None
    """New logo URL, or set to `null` to remove the logo."""
    headerImg: Optional[str] = None
    """New leader image URL, or set to `null` to remove the leader."""
    name: Optional[str] = None
    """New organization name."""
    experiments: Optional[List[Optional[str]]] = None
    readme: Optional[str] = None
    """Readme for the organization (in Markdown)"""
    billable: Optional[bool] = None
    entitlementLimits: EntitlementLimits = None
    contractStartDate: Optional[datetime] = None
    """The date in which the organization contract started. Compute time will be calculated from this date."""
    domain: Optional[str] = None
    """The domain of the organization. The organization domain is used to add new users to an organization. For example, new @edgeimpulse.com would be added to the Edge Impulse organization if this organization has edgeimpulse.com as the domain."""


@dataclass(kw_only=True)
class OrganizationComputeTimeUsage(ApiBaseModel):
    cpuComputeTime: Optional[float] = None
    """CPU compute time in seconds of all jobs in the organization (including organizational project jobs)."""
    gpuComputeTime: Optional[float] = None
    """GPU compute time in seconds of all jobs in the organization (including organizational project jobs)."""
    totalComputeTime: Optional[float] = None
    """Total compute time is the amount of computation time spent in jobs, in minutes used by an organization over the given period, calculated as CPU + GPU minutes."""


@dataclass(kw_only=True)
class AdminOrganizationInfoResponse(GenericApiResponse, OrganizationComputeTimeUsage):
    billable: Optional[bool] = None
    entitlementLimits: EntitlementLimits = None
    computeTimeCurrentContractSince: Optional[datetime] = None
    """The date from which the compute time for the running contract is calculated."""
    totalStorage: Optional[float] = None
    """Total storage used by the organization."""
    dailyMetrics: Optional[List[DailyMetricsRecord]] = None
    """Metrics for the last 365 days"""


@dataclass(kw_only=True)
class AdminGetOrganizationComputeTimeUsageResponse(
    GenericApiResponse, OrganizationComputeTimeUsage
):
    pass


@dataclass(kw_only=True)
class SetSampleMetadataRequest(ApiBaseModel):
    metadata: Optional[Dict[str, Optional[str]]] = None


@dataclass(kw_only=True)
class ClassificationType(Enum):
    classification = "classification"
    regression = "regression"


@dataclass(kw_only=True)
class DataExplorerPredictionsResponse(GenericApiResponse):
    predictions: List[ModelPrediction]
    labels: List[str]
    classificationType: ClassificationType


@dataclass(kw_only=True)
class AdminGetMetricsResponse(GenericApiResponse):
    metrics: Dict[str, Any]


@dataclass(kw_only=True)
class AdminGetUserMetricsResponse(GenericApiResponse):
    metrics: Dict[str, Any]


@dataclass(kw_only=True)
class AdminGetUserIdsResponse(GenericApiResponse):
    ids: List[int]


@dataclass(kw_only=True)
class GetPublicMetricsResponse(GenericApiResponse):
    projects: int
    data_samples: int
    jobs: int


@dataclass(kw_only=True)
class ProfileTfLiteRequest(ApiBaseModel):
    tfliteFileBase64: str
    """A base64 encoded TFLite file"""
    device: str
    """MCU used for calculating latency, query `latencyDevices` in `listProject` for a list of supported devices  (and use the "mcu" property here)."""


@dataclass(kw_only=True)
class ProfileModelInfoMemoryDetails(ApiBaseModel):
    ram: int
    """Estimated amount of RAM required by the model, measured in bytes"""
    rom: int
    """Estimated amount of ROM required by the model, measured in bytes"""
    arenaSize: int
    """Estimated arena size required for model inference, measured in bytes"""


@dataclass(kw_only=True)
class ProfileModelInfoMemory(ApiBaseModel):
    tflite: ProfileModelInfoMemoryDetails = None
    eon: ProfileModelInfoMemoryDetails = None
    eonRamOptimized: ProfileModelInfoMemoryDetails = None


@dataclass(kw_only=True)
class ProfileModelInfo(ApiBaseModel):
    device: str
    tfliteFileSizeBytes: int
    isSupportedOnMcu: bool
    memory: ProfileModelInfoMemory = None
    timePerInferenceMs: Optional[int] = None
    mcuSupportError: Optional[str] = None


@dataclass(kw_only=True)
class ProfileTfLiteResponse(GenericApiResponse, ProfileModelInfo):
    pass


@dataclass(kw_only=True)
class BlockParamsVisualAnomalyPatchcore(ApiBaseModel):
    backbone: Optional[str] = None
    """The backbone to use for feature extraction"""
    numLayers: Optional[int] = None
    """The number of layers in the feature extractor (1-3)"""
    poolSize: Optional[int] = None
    """The pool size for the feature extractor"""
    samplingRatio: Optional[float] = None
    """The sampling ratio for the coreset, used for anomaly scoring"""
    numNearestNeighbors: Optional[int] = None
    """The number of nearest neighbors to consider, used for anomaly scoring"""


@dataclass(kw_only=True)
class BlockParamsVisualAnomalyGmm(ApiBaseModel):
    backbone: Optional[str] = None
    """The backbone to use for feature extraction"""


@dataclass(kw_only=True)
class DeployPretrainedModelInputTimeSeriesInputTypeEnum(Enum):
    time_series = "time-series"


@dataclass(kw_only=True)
class DeployPretrainedModelInputTimeSeries(ApiBaseModel):
    inputType: DeployPretrainedModelInputTimeSeriesInputTypeEnum
    frequencyHz: float
    windowLengthMs: int


@dataclass(kw_only=True)
class DeployPretrainedModelInputAudioInputTypeEnum(Enum):
    audio = "audio"


@dataclass(kw_only=True)
class DeployPretrainedModelInputAudio(ApiBaseModel):
    inputType: DeployPretrainedModelInputAudioInputTypeEnum
    frequencyHz: float


@dataclass(kw_only=True)
class DeployPretrainedModelInputImageInputTypeEnum(Enum):
    image = "image"


@dataclass(kw_only=True)
class DeployPretrainedModelInputImage(ApiBaseModel):
    inputType: DeployPretrainedModelInputImageInputTypeEnum
    inputScaling: ImageInputScaling = None


@dataclass(kw_only=True)
class DeployPretrainedModelInputOtherInputTypeEnum(Enum):
    other = "other"


@dataclass(kw_only=True)
class DeployPretrainedModelInputOther(ApiBaseModel):
    inputType: DeployPretrainedModelInputOtherInputTypeEnum


@dataclass(kw_only=True)
class DeployPretrainedModelModelClassificationModelTypeEnum(Enum):
    classification = "classification"


@dataclass(kw_only=True)
class DeployPretrainedModelModelClassification(ApiBaseModel):
    modelType: DeployPretrainedModelModelClassificationModelTypeEnum
    labels: List[str]


@dataclass(kw_only=True)
class DeployPretrainedModelModelRegressionModelTypeEnum(Enum):
    regression = "regression"


@dataclass(kw_only=True)
class DeployPretrainedModelModelRegression(ApiBaseModel):
    modelType: DeployPretrainedModelModelRegressionModelTypeEnum


@dataclass(kw_only=True)
class DeployPretrainedModelModelObjectDetectionModelTypeEnum(Enum):
    object_detection = "object-detection"


@dataclass(kw_only=True)
class DeployPretrainedModelModelObjectDetection(ApiBaseModel):
    modelType: DeployPretrainedModelModelObjectDetectionModelTypeEnum
    labels: List[str]
    lastLayer: ObjectDetectionLastLayer
    minimumConfidence: float
    """Threshold for objects (f.e. 0.3)"""


@dataclass(kw_only=True)
class DeployPretrainedModelRequestModelFileTypeEnum(Enum):
    tflite = "tflite"
    onnx = "onnx"
    saved_model = "saved_model"
    lgbm = "lgbm"
    xgboost = "xgboost"
    pickle = "pickle"


@dataclass(kw_only=True)
class DeployPretrainedModelRequestModelInfo(ApiBaseModel):
    input: Union[
        DeployPretrainedModelInputTimeSeries,
        DeployPretrainedModelInputAudio,
        DeployPretrainedModelInputImage,
        DeployPretrainedModelInputOther,
    ]
    model: Union[
        DeployPretrainedModelModelClassification,
        DeployPretrainedModelModelRegression,
        DeployPretrainedModelModelObjectDetection,
    ]


@dataclass(kw_only=True)
class DeployPretrainedModelRequestDeployModelTypeEnum(Enum):
    int8 = "int8"
    float32 = "float32"


@dataclass(kw_only=True)
class DeployPretrainedModelRequestUseConverterEnum(Enum):
    onnx_tf = "onnx-tf"
    onnx2tf = "onnx2tf"


@dataclass(kw_only=True)
class DeployPretrainedModelRequest(ApiBaseModel):
    modelFileBase64: str
    """A base64 encoded pretrained model"""
    modelFileType: DeployPretrainedModelRequestModelFileTypeEnum
    deploymentType: str
    """The name of the built target. You can find this by listing all deployment targets through `listDeploymentTargetsForProject` (via `GET /v1/api/{projectId}/deployment/targets`) and see the `format` type."""
    modelInfo: DeployPretrainedModelRequestModelInfo
    engine: DeploymentTargetEngine = None
    representativeFeaturesBase64: Optional[str] = None
    """A base64 encoded .npy file containing the features from your validation set (optional for onnx and saved_model) - used to quantize your model."""
    deployModelType: DeployPretrainedModelRequestDeployModelTypeEnum = None
    useConverter: DeployPretrainedModelRequestUseConverterEnum = None


@dataclass(kw_only=True)
class UpdateProjectTagsRequest(ApiBaseModel):
    tags: List[str]


@dataclass(kw_only=True)
class UploadPretrainedModelRequestModelFileTypeEnum(Enum):
    tflite = "tflite"
    onnx = "onnx"
    saved_model = "saved_model"


@dataclass(kw_only=True)
class UploadPretrainedModelRequest(ApiBaseModel):
    modelFile: bytes
    modelFileName: str
    modelFileType: UploadPretrainedModelRequestModelFileTypeEnum
    representativeFeatures: Optional[bytes] = None
    device: Optional[str] = None
    """MCU used for calculating latency, query `latencyDevices` in `listProject` for a list of supported devices (and use the "mcu" property here). If this is kept empty then we'll show an overview of multiple devices."""


@dataclass(kw_only=True)
class PretrainedModelTensorDataTypeEnum(Enum):
    int8 = "int8"
    uint8 = "uint8"
    float32 = "float32"


@dataclass(kw_only=True)
class PretrainedModelTensor(ApiBaseModel):
    dataType: PretrainedModelTensorDataTypeEnum
    name: str
    shape: List[int]
    quantizationScale: Optional[float] = None
    quantizationZeroPoint: Optional[float] = None


@dataclass(kw_only=True)
class ProfileModelTableMcuMemoryTflite(ApiBaseModel):
    ram: int
    rom: int


@dataclass(kw_only=True)
class ProfileModelTableMcuMemoryEon(ApiBaseModel):
    ram: int
    rom: int


@dataclass(kw_only=True)
class ProfileModelTableMcuMemoryEonRamOptimized(ApiBaseModel):
    ram: int
    rom: int


@dataclass(kw_only=True)
class ProfileModelTableMcuMemory(ApiBaseModel):
    tflite: ProfileModelTableMcuMemoryTflite = None
    eon: ProfileModelTableMcuMemoryEon = None
    eonRamOptimized: ProfileModelTableMcuMemoryEonRamOptimized = None


@dataclass(kw_only=True)
class ProfileModelTableMcu(ApiBaseModel):
    description: str
    supported: bool
    timePerInferenceMs: Optional[int] = None
    memory: ProfileModelTableMcuMemory = None
    mcuSupportError: Optional[str] = None


@dataclass(kw_only=True)
class ProfileModelTableMpu(ApiBaseModel):
    description: str
    supported: bool
    timePerInferenceMs: Optional[int] = None
    rom: Optional[float] = None


@dataclass(kw_only=True)
class ProfileModelTableVariantEnum(Enum):
    int8 = "int8"
    float32 = "float32"


@dataclass(kw_only=True)
class ProfileModelTable(ApiBaseModel):
    variant: ProfileModelTableVariantEnum
    lowEndMcu: ProfileModelTableMcu
    highEndMcu: ProfileModelTableMcu
    highEndMcuPlusAccelerator: ProfileModelTableMcu
    mpu: ProfileModelTableMpu
    gpuOrMpuAccelerator: ProfileModelTableMpu


@dataclass(kw_only=True)
class ProfileInfo(ApiBaseModel):
    table: ProfileModelTable
    float32: ProfileModelInfo = None
    int8: ProfileModelInfo = None


@dataclass(kw_only=True)
class Model(ApiBaseModel):
    fileName: str
    inputs: List[PretrainedModelTensor]
    outputs: List[PretrainedModelTensor]
    profileInfo: Optional[ProfileInfo] = None
    profileJobId: Optional[int] = None
    supportsTFLite: Optional[bool] = None


@dataclass(kw_only=True)
class ModelInfo(ApiBaseModel):
    input: Union[
        DeployPretrainedModelInputTimeSeries,
        DeployPretrainedModelInputAudio,
        DeployPretrainedModelInputImage,
        DeployPretrainedModelInputOther,
    ]
    model: Union[
        DeployPretrainedModelModelClassification,
        DeployPretrainedModelModelRegression,
        DeployPretrainedModelModelObjectDetection,
    ]


@dataclass(kw_only=True)
class GetPretrainedModelResponse(GenericApiResponse):
    specificDeviceSelected: bool
    """Whether a specific device was selected for performance profiling"""
    availableModelTypes: List[KerasModelTypeEnum]
    """The types of model that are available"""
    model: Optional[Model] = None
    modelInfo: Optional[ModelInfo] = None


@dataclass(kw_only=True)
class TestPretrainedModelRequestModelInfo(ApiBaseModel):
    input: Union[
        DeployPretrainedModelInputTimeSeries,
        DeployPretrainedModelInputAudio,
        DeployPretrainedModelInputImage,
        DeployPretrainedModelInputOther,
    ]
    model: Union[
        DeployPretrainedModelModelClassification,
        DeployPretrainedModelModelRegression,
        DeployPretrainedModelModelObjectDetection,
    ]


@dataclass(kw_only=True)
class TestPretrainedModelRequest(ApiBaseModel):
    features: List[float]
    modelInfo: TestPretrainedModelRequestModelInfo


@dataclass(kw_only=True)
class TestPretrainedModelResponse(GenericApiResponse):
    result: Optional[Dict[str, Optional[float]]] = None
    """Classification value per label. For a neural network this will be the confidence, for anomalies the anomaly score."""
    boundingBoxes: Optional[List[BoundingBoxWithScore]] = None


@dataclass(kw_only=True)
class SavePretrainedModelRequest(ApiBaseModel):
    input: Union[
        DeployPretrainedModelInputTimeSeries,
        DeployPretrainedModelInputAudio,
        DeployPretrainedModelInputImage,
        DeployPretrainedModelInputOther,
    ]
    model: Union[
        DeployPretrainedModelModelClassification,
        DeployPretrainedModelModelRegression,
        DeployPretrainedModelModelObjectDetection,
    ]


@dataclass(kw_only=True)
class ProjectInfoSummaryResponse(GenericApiResponse):
    id: int
    owner: str
    name: str
    studioUrl: str


@dataclass(kw_only=True)
class DevelopmentBoardRequest(ApiBaseModel):
    name: str
    image: str
    docsUrl: str


@dataclass(kw_only=True)
class DevelopmentBoardRequestUpdate(ApiBaseModel):
    name: Optional[str] = None
    image: Optional[str] = None
    docsUrl: Optional[str] = None


@dataclass(kw_only=True)
class DevelopmentBoardsResponse(GenericApiResponse):
    developmentBoards: List[DevelopmentBoardResponse]


@dataclass(kw_only=True)
class SsoWhitelist(ApiBaseModel):
    domain: str
    idps: List[str]


@dataclass(kw_only=True)
class AdminGetSSOSettingsResponse(GenericApiResponse):
    ssoWhitelist: List[SsoWhitelist]


@dataclass(kw_only=True)
class AdminGetSSODomainIdPsResponse(GenericApiResponse):
    idps: List[str]


@dataclass(kw_only=True)
class AdminAddOrUpdateSSODomainIdPsRequest(ApiBaseModel):
    idps: List[str]


@dataclass(kw_only=True)
class SendUserFeedbackRequestTypeEnum(Enum):
    feedback = "feedback"


@dataclass(kw_only=True)
class SendUserFeedbackRequest(ApiBaseModel):
    type: SendUserFeedbackRequestTypeEnum
    subject: str
    """The reason the user is contacting Edge Impulse Support."""
    body: str
    """The body of the message."""
    workEmail: Optional[str] = None
    """The user's work email address. This is optional, if it's not provided, the registered email will be used."""
    company: Optional[str] = None
    """The user's company. This is optional."""
    jobTitle: Optional[str] = None
    """The user's job title. This is optional."""
    companySize: Optional[str] = None
    """The user's company size. This is optional."""
    organizationId: Optional[float] = None
    """The user's organization ID. This is optional."""


@dataclass(kw_only=True)
class EnterpriseUpgradeOrTrialExtensionRequest(ApiBaseModel):
    reason: Optional[str] = None
    """Answer to the question: 'Why is this the right time for your team to invest in edge AI?'. This is optional."""
    useCase: Optional[str] = None
    """Answer to the question: 'What best describes your use case?'. This is optional."""
    timeline: Optional[str] = None
    """Answer to the question: 'What is your timeline for solving your problem?'. This is optional."""
    objective: Optional[str] = None
    """Answer to the question: 'What are you hoping to achieve with an extension?'. This is optional."""
    trialId: Optional[float] = None
    """The user's trial ID. This is optional."""


@dataclass(kw_only=True)
class EnterpriseLimit(Enum):
    users = "users"
    projects = "projects"
    compute = "compute"
    storage = "storage"


@dataclass(kw_only=True)
class EnterpriseLimitsIncreaseRequest(ApiBaseModel):
    limits: List[EnterpriseLimit]
    reason: Optional[str] = None
    """Additional notes for the request. This is optional."""


@dataclass(kw_only=True)
class LogWebsitePageviewRequest(ApiBaseModel):
    sessionId: str
    pageUrl: str
    pageReferrer: Optional[str] = None


@dataclass(kw_only=True)
class LogAnalyticsEventRequest(ApiBaseModel):
    eventName: str
    eventProperties: Dict[str, Any]
    sessionId: Optional[str] = None
    """Optional session ID for users who have not signed in yet. Helps match anonymous activity with user activity once they sign in."""


@dataclass(kw_only=True)
class AdminUpdateUserPermissionsRequest(ApiBaseModel):
    permissions: List[Permission]


@dataclass(kw_only=True)
class TransformationJobs(ApiBaseModel):
    id: int
    transformationJobId: int
    createProjectId: int
    created: datetime
    jobId: int
    transformationBlockName: str
    jobStarted: Optional[datetime] = None
    jobFinished: Optional[datetime] = None
    jobFinishedSuccessful: Optional[bool] = None
    pipelineName: Optional[str] = None


@dataclass(kw_only=True)
class GetOrganizationDataItemTransformJobsResponse(GenericApiResponse):
    transformationJobs: List[TransformationJobs]
    totalTransformationJobCount: int


@dataclass(kw_only=True)
class DataCampaignDashboardWhenToEmailEnum(Enum):
    always = "always"
    on_changes = "on_changes"
    never = "never"


@dataclass(kw_only=True)
class DataCampaignDashboard(ApiBaseModel):
    id: int
    created: datetime
    name: str
    emailRecipientUids: List[int]
    """List of user IDs to notify for this dashboard (sent daily)"""
    whenToEmail: DataCampaignDashboardWhenToEmailEnum
    showNoOfDays: int
    latestScreenshot: Optional[str] = None


@dataclass(kw_only=True)
class DataCampaignQuery(ApiBaseModel):
    name: str
    dataset: str
    query: str


@dataclass(kw_only=True)
class DataCampaignLink(ApiBaseModel):
    icon: str
    name: str
    link: str


@dataclass(kw_only=True)
class DataCampaign(ApiBaseModel):
    id: int
    dataCampaignDashboardId: int
    created: datetime
    name: str
    description: str
    coordinatorUids: List[int]
    """List of user IDs that coordinate this campaign"""
    queries: List[DataCampaignQuery]
    links: List[DataCampaignLink]
    datasets: List[str]
    pipelineIds: List[int]
    projectIds: List[int]
    logo: Optional[str] = None


@dataclass(kw_only=True)
class GetOrganizationDataCampaignDashboardsResponse(GenericApiResponse):
    dashboards: List[DataCampaignDashboard]


@dataclass(kw_only=True)
class AddOrganizationDataCampaignDashboardRequestWhenToEmailEnum(Enum):
    always = "always"
    on_changes = "on_changes"
    never = "never"


@dataclass(kw_only=True)
class AddOrganizationDataCampaignDashboardRequest(ApiBaseModel):
    name: str
    emailRecipientUids: List[int]
    """List of user IDs to notify for this dashboard (sent daily)"""
    whenToEmail: AddOrganizationDataCampaignDashboardRequestWhenToEmailEnum
    showNoOfDays: int


@dataclass(kw_only=True)
class AddOrganizationDataCampaignDashboardResponse(GenericApiResponse):
    dataCampaignDashboardId: int


@dataclass(kw_only=True)
class GetOrganizationDataCampaignDashboardResponse(GenericApiResponse):
    dashboard: DataCampaignDashboard


@dataclass(kw_only=True)
class UpdateOrganizationDataCampaignDashboardRequestWhenToEmailEnum(Enum):
    always = "always"
    on_changes = "on_changes"
    never = "never"


@dataclass(kw_only=True)
class UpdateOrganizationDataCampaignDashboardRequest(ApiBaseModel):
    name: Optional[str] = None
    emailRecipientUids: Optional[List[Optional[int]]] = None
    """List of user IDs to notify for this dashboard (sent daily)"""
    whenToEmail: UpdateOrganizationDataCampaignDashboardRequestWhenToEmailEnum = None
    showNoOfDays: Optional[int] = None


@dataclass(kw_only=True)
class Values(ApiBaseModel):
    id: int
    value: Optional[float] = None


@dataclass(kw_only=True)
class DataType(Enum):
    dataItems = "dataItems"
    time = "time"
    percentage = "percentage"


@dataclass(kw_only=True)
class XData(ApiBaseModel):
    color: str
    legendText: str
    popupText: str
    values: List[Values]
    dataType: DataType
    dataset: Optional[str] = None
    query: Optional[str] = None


@dataclass(kw_only=True)
class DataCampaignGraph(ApiBaseModel):
    title: str
    link: str
    xData: List[XData]
    yTicks: List[datetime]
    nextUpdate: datetime


@dataclass(kw_only=True)
class Campaigns(ApiBaseModel):
    campaign: DataCampaign
    graphs: List[DataCampaignGraph]


@dataclass(kw_only=True)
class GetOrganizationDataCampaignsResponse(GenericApiResponse):
    campaigns: List[Campaigns]


@dataclass(kw_only=True)
class AddOrganizationDataCampaignRequest(ApiBaseModel):
    dataCampaignDashboardId: int
    name: str
    description: str
    coordinatorUids: List[int]
    """List of user IDs that coordinate this campaign"""
    queries: List[DataCampaignQuery]
    links: List[DataCampaignLink]
    datasets: List[str]
    pipelineIds: List[int]
    projectIds: List[int]
    id: Optional[int] = None
    created: Optional[datetime] = None
    logo: Optional[str] = None


@dataclass(kw_only=True)
class AddOrganizationDataCampaignResponse(GenericApiResponse):
    dataCampaignId: int


@dataclass(kw_only=True)
class UpdateOrganizationDataCampaignRequest(ApiBaseModel):
    dataCampaignDashboardId: Optional[int] = None
    name: Optional[str] = None
    coordinatorUids: Optional[List[Optional[int]]] = None
    """List of user IDs that coordinate this campaign"""
    logo: Optional[str] = None
    description: Optional[str] = None
    queries: Optional[List[DataCampaignQuery]] = None
    links: Optional[List[DataCampaignLink]] = None
    datasets: Optional[List[Optional[str]]] = None
    pipelineIds: Optional[List[Optional[int]]] = None
    projectIds: Optional[List[Optional[int]]] = None


@dataclass(kw_only=True)
class GetOrganizationDataCampaignResponse(GenericApiResponse):
    campaign: DataCampaign
    graphs: List[DataCampaignGraph]


@dataclass(kw_only=True)
class Queries(ApiBaseModel):
    dataset: str
    query: str
    graphValueId: int
    """Which point in the graph was clicked (from "graphs.values")"""


@dataclass(kw_only=True)
class OrganizationDataCampaignDiffRequest(ApiBaseModel):
    queries: List[Queries]


@dataclass(kw_only=True)
class XXYQueriesClash1410795742(ApiBaseModel):
    title: str
    dataset: str
    query: str
    newItems: List[str]
    deletedItems: List[str]


@dataclass(kw_only=True)
class OrganizationDataCampaignDiffResponse(GenericApiResponse):
    date: datetime
    queries: List[XXYQueriesClash1410795742]


@dataclass(kw_only=True)
class MigrationStateEnum(Enum):
    paused = "paused"
    queued = "queued"
    running = "running"
    done = "done"
    failed = "failed"


@dataclass(kw_only=True)
class Migration(ApiBaseModel):
    id: str
    """Unique identifier of the data migration"""
    state: MigrationStateEnum
    offset: Optional[int] = None
    """Number of items already processed"""


@dataclass(kw_only=True)
class AdminGetDataMigrationsResponse(GenericApiResponse):
    migrations: List[Migration]


@dataclass(kw_only=True)
class AdminGetDataMigrationResponse(GenericApiResponse):
    migration: Migration


@dataclass(kw_only=True)
class AdminToggleDataMigrationRequest(ApiBaseModel):
    id: str
    """Unique identifier of the data migration"""
    shouldRun: bool
    """Whether the migration should be queued for execution"""


@dataclass(kw_only=True)
class AdminAddDisallowedEmailDomainRequest(ApiBaseModel):
    domain: str


@dataclass(kw_only=True)
class AdminGetDisallowedEmailDomainsResponse(GenericApiResponse):
    domains: List[str]


@dataclass(kw_only=True)
class Items(ApiBaseModel):
    sampleId: int
    maskId: int
    imageUrl: str


@dataclass(kw_only=True)
class XXYClustersClash420222259(ApiBaseModel):
    items: List[Items]
    label: Optional[str] = None


@dataclass(kw_only=True)
class GetAutoLabelerResponse(GenericApiResponse):
    hasResults: bool
    clusters: List[XXYClustersClash420222259]
    simThreshold: float
    minObjectSizePx: int
    whichItemsToInclude: str
    maxObjectSizePx: Optional[int] = None


@dataclass(kw_only=True)
class UpdateWhitelabelDefaultDeploymentTargetRequest(ApiBaseModel):
    defaultDeploymentTarget: str
    """Name of the default deployment target"""


@dataclass(kw_only=True)
class XXYDataClash1547128465(ApiBaseModel):
    id: int
    category: str
    importedFrom: str


@dataclass(kw_only=True)
class GetAllImportedFromResponse(GenericApiResponse):
    data: List[XXYDataClash1547128465]


@dataclass(kw_only=True)
class ExportKerasBlockDataRequest(ApiBaseModel):
    overrideImageInputScaling: ImageInputScaling = None


@dataclass(kw_only=True)
class StartEnterpriseTrialRequestUserHasMLModelsInProductionEnum(Enum):
    yes = "yes"
    no = "no"
    no__but_we_will_soon = "no, but we will soon"


@dataclass(kw_only=True)
class StartEnterpriseTrialRequest(ApiBaseModel):
    email: Optional[str] = None
    """Email of the user requesting the trial. If this email is different to the one stored for the user requesting the trial, it will be used to replace the existing one."""
    organizationName: Optional[str] = None
    """Name of the trial organization. All enterprise features are tied to an organization. This organization will be deleted after the trial ends. If no organization name is provided, the user's name will be used."""
    expirationDate: TrialExpirationDate = None
    notes: TrialNotes = None
    useCase: Optional[str] = None
    """Use case of the trial."""
    userHasMLModelsInProduction: StartEnterpriseTrialRequestUserHasMLModelsInProductionEnum = None
    companyName: Optional[str] = None
    """Name of the company requesting the trial."""
    companySize: Optional[str] = None
    """Size of the company requesting the trial. This is a range of number of employees."""
    country: Optional[str] = None
    """Country of the company requesting the trial."""
    stateOrProvince: Optional[str] = None
    """State or province of the company requesting the trial."""
    redirectUrlOrigin: Optional[str] = None
    """Origin of the redirect URL returned as result of creating the trial user."""
    redirectUrlQueryParams: Optional[str] = None
    """Query parameters to be appended to the redirect URL returned as result of creating the trial user."""


@dataclass(kw_only=True)
class AdminStartEnterpriseTrialRequest(StartEnterpriseTrialRequest):
    userId: int
    """ID of the user requesting the trial."""


@dataclass(kw_only=True)
class CreateEnterpriseTrialUserRequest(StartEnterpriseTrialRequest):
    name: str
    """Name of the user."""
    username: str
    """Username, minimum 4 and maximum 30 characters. May contain alphanumeric characters, hyphens, underscores and dots. Validated according to `^(?=.{4,30}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._-]+(?<![_.])$`."""
    email: str
    """Email of the user. Only business email addresses are allowed. Emails with free domains like gmail.com or yahoo.com are not allowed."""
    privacyPolicy: bool
    """Whether the user has accepted the terms of service and privacy policy."""
    password: Optional[str] = None
    """Password of the user. Minimum length 8 characters."""
    jobTitle: Optional[str] = None
    """Job title of the user."""
    companyName: Optional[str] = None
    """Name of the company requesting the trial."""
    redirectUrlOrigin: Optional[str] = None
    """Origin of the redirect URL returned as result of creating the trial user."""
    redirectUrlQueryParams: Optional[str] = None
    """Query parameters to be appended to the redirect URL returned as result of creating the trial user."""
    utmParams: Optional[List[UtmParameter]] = None
    """List of UTM parameters."""


@dataclass(kw_only=True)
class EntityCreatedResponse(GenericApiResponse):
    id: int
    """Unique identifier of the created entity."""


@dataclass(kw_only=True)
class AdminGetTrialResponse(GenericApiResponse):
    trial: EnterpriseTrial


@dataclass(kw_only=True)
class AdminUpdateTrialRequest(ApiBaseModel):
    expirationDate: TrialExpirationDate = None
    notes: TrialNotes = None


@dataclass(kw_only=True)
class VerifyOrganizationExistingBucketRequest(ApiBaseModel):
    prefix: str


@dataclass(kw_only=True)
class UpdateWhitelabelRequest(ApiBaseModel):
    supportedProjectTypes: Optional[List[ProjectType]] = None


@dataclass(kw_only=True)
class ListEnterpriseTrialsResponse(GenericApiResponse):
    trials: List[EnterpriseTrial]
    """Current or past enterprise trials."""


@dataclass(kw_only=True)
class CreateEnterpriseTrialResponse(EntityCreatedResponse):
    userId: Optional[int] = None
    """ID of the user created for the trial, if the user did not already exist."""
    redirectUrl: Optional[str] = None
    """URL to redirect the user to in order to access the enterprise trial."""


@dataclass(kw_only=True)
class XXYMetricsClash1930404768(ApiBaseModel):
    computeMinutesCpu: float
    """Total compute of all user jobs, running on CPU, in the current billing period."""
    computeMinutesGpu: float
    """Total compute of all user jobs, running on GPU, in the current billing period."""
    computeMinutesTotal: float
    """Total compute of all user jobs in the current billing period, calculated as CPU + 3*GPU compute."""
    computeMinutesLimit: float
    """Overall compute limit for the current billing period."""
    computeResetDate: Optional[datetime] = None
    """The date at which the current compute billing period will reset."""


@dataclass(kw_only=True)
class UserSubscriptionMetricsResponse(GenericApiResponse):
    metrics: Optional[XXYMetricsClash1930404768] = None


@dataclass(kw_only=True)
class RequestEmailVerificationRequest(ApiBaseModel):
    redirectUrl: str
    """URL to redirect the user after email verification."""


@dataclass(kw_only=True)
class VerifyEmailResponse(GenericApiResponse):
    email: Optional[str] = None
    """Email address that was verified."""
    userId: Optional[float] = None
    """ID of the user associated with the verified email address, if any."""
    redirectUrl: Optional[str] = None
    """URL to redirect the user to after email verification."""


@dataclass(kw_only=True)
class Verdict(Enum):
    Valid = "Valid"
    Risky = "Risky"
    Invalid = "Invalid"


@dataclass(kw_only=True)
class ValidateEmailResponse(GenericApiResponse):
    email: str
    """Email address that was checked."""
    verdict: Verdict
    """Classification of the email's validity status"""
    score: float
    """This number from 0 to 1 represents the likelihood the email address is valid, expressed as a percentage."""
    suggestion: Optional[str] = None
    """A corrected domain, if a possible typo is detected."""
    local: Optional[str] = None
    """The first part of the email address (before the @ sign)"""
    host: Optional[str] = None
    """The second part of the email address (after the @ sign)"""


@dataclass(kw_only=True)
class GetEmailVerificationStatusResponse(GenericApiResponse):
    verified: bool
    """Whether the email address has been verified."""


@dataclass(kw_only=True)
class GetEmailVerificationCodeResponse(GenericApiResponse):
    code: Optional[str] = None
    """The verification code associated with the provided email."""


@dataclass(kw_only=True)
class Feature(Enum):
    signup_thank_you_page = "signup-thank-you-page"
    stripe_live_mode = "stripe-live-mode"


@dataclass(kw_only=True)
class Flags(ApiBaseModel):
    feature: Feature
    enabled: bool
    """Whether the feature is enabled."""


@dataclass(kw_only=True)
class GetFeatureFlagsResponse(GenericApiResponse):
    flags: List[Flags]
    """List of feature flags."""


@dataclass(kw_only=True)
class AdminEnableFeatureRequest(ApiBaseModel):
    feature: Feature
    """Feature to enable."""


@dataclass(kw_only=True)
class Config(ApiBaseModel):
    key: str
    """Config key"""
    value: str
    """Config value (as JSON string)"""


@dataclass(kw_only=True)
class GetStudioConfigResponse(GenericApiResponse):
    config: List[Config]
    """List of config items"""


@dataclass(kw_only=True)
class UserDismissNotificationRequest(ApiBaseModel):
    notification: str


@dataclass(kw_only=True)
class ProjectDismissNotificationRequest(ApiBaseModel):
    notification: str


@dataclass(kw_only=True)
class SetSampleStructuredLabelsRequest(ApiBaseModel):
    structuredLabels: List[StructuredLabel]


@dataclass(kw_only=True)
class ListOrganizationUsageReportsResponse(GenericApiResponse):
    reports: List[Report]
    """List of feature flags."""
    totalCount: int


@dataclass(kw_only=True)
class GetOrganizationUsageReportResponse(GenericApiResponse):
    report: Report


@dataclass(kw_only=True)
class CreateOrganizationUsageReportBody(ApiBaseModel):
    reportStartDate: datetime
    reportEndDate: datetime


@dataclass(kw_only=True)
class UpdateTunerRunRequest(ApiBaseModel):
    name: Optional[str] = None


@dataclass(kw_only=True)
class UploadCsvWizardUploadedFileRequest(ApiBaseModel):
    file: bytes


@dataclass(kw_only=True)
class GetCsvWizardUploadedFileInfo(GenericApiResponse):
    hasFile: bool
    link: Optional[str] = None


@dataclass(kw_only=True)
class ExportBlockResponse(GenericApiResponse):
    id: int
    """Job identifier. Status updates will include this identifier."""
    exportUrl: str


@dataclass(kw_only=True)
class UserGenerateNewMfaKeyResponse(GenericApiResponse):
    key: str
    """Secret key (use SHA-1)."""
    url: str
    """URL that will be converted into a QR code that can be scanned."""


@dataclass(kw_only=True)
class UserSetTotpMfaKeyRequest(ApiBaseModel):
    key: str
    """Secret key obtained through `userGenerateNewMfaKey`."""
    totpToken: str
    """TOTP token that is valid for the key (to ensure the device is configured correctly)"""


@dataclass(kw_only=True)
class UserSetTotpMfaKeyResponse(GenericApiResponse):
    recoveryCodes: List[str]
    """10 recovery codes, which can be used in case you've lost access to your MFA TOTP app. Recovery codes are single use. Once you've used a recovery code once, it can not be used again."""


@dataclass(kw_only=True)
class UserDeleteTotpMfaKeyRequest(ApiBaseModel):
    totpToken: str
    """Valid TOTP token"""


@dataclass(kw_only=True)
class OrganizationDataExportCreatedByUser(ApiBaseModel):
    id: int
    name: str
    username: str
    photo: Optional[str] = None


@dataclass(kw_only=True)
class OrganizationDataExport(ApiBaseModel):
    id: int
    created: datetime
    jobId: int
    jobFinished: bool
    jobFinishedSuccessful: bool
    expirationDate: datetime
    """Date when the export will expire. Default is 30 days. Maximum expiration date is 60 days from the creation date."""
    createdByUser: OrganizationDataExportCreatedByUser = None
    description: Optional[str] = None
    """Description of the data export"""
    downloadUrl: Optional[str] = None


@dataclass(kw_only=True)
class GetOrganizationDataExportsResponse(GenericApiResponse):
    exports: List[OrganizationDataExport]
    """List of organization data exports."""
    totalCount: int


@dataclass(kw_only=True)
class GetOrganizationDataExportResponse(GenericApiResponse):
    export: OrganizationDataExport


@dataclass(kw_only=True)
class AdminCreateOrganizationDataExportRequest(ApiBaseModel):
    description: str
    """Description of the data export"""
    expirationDate: Optional[datetime] = None
    """Date when the export will expire. Default is 30 days. Maximum expiration date is 60 days from the creation date."""


@dataclass(kw_only=True)
class AdminUpdateOrganizationDataExportRequest(ApiBaseModel):
    description: Optional[str] = None
    """Description of the data export"""
    expirationDate: Optional[datetime] = None
    """Date when the export will expire. Default is 30 days. Maximum expiration date is 60 days from the creation date."""


@dataclass(kw_only=True)
class DeviceDebugStreamType(Enum):
    snapshot = "snapshot"
    inference = "inference"


@dataclass(kw_only=True)
class StartDeviceSnapshotDebugStreamRequestResolutionEnum(Enum):
    high = "high"
    low = "low"


@dataclass(kw_only=True)
class StartDeviceSnapshotDebugStreamRequest(ApiBaseModel):
    resolution: StartDeviceSnapshotDebugStreamRequestResolutionEnum


@dataclass(kw_only=True)
class StartDeviceDebugStreamResponse(GenericApiResponse):
    streamId: int


@dataclass(kw_only=True)
class CanaryResponse(GenericApiResponse):
    routeToCanary: bool
    """Whether the request should be routed to the canary or not."""


@dataclass(kw_only=True)
class KeepDeviceDebugStreamAliveRequest(ApiBaseModel):
    streamId: int


@dataclass(kw_only=True)
class StopDeviceDebugStreamRequest(ApiBaseModel):
    streamId: int


@dataclass(kw_only=True)
class GetImpulseRecordsRequestRange(ApiBaseModel):
    first: Optional[int] = None
    last: Optional[int] = None


@dataclass(kw_only=True)
class GetImpulseRecordsRequest(ApiBaseModel):
    index: Optional[int] = None
    range: GetImpulseRecordsRequestRange = None
    list: Optional[List[Optional[int]]] = None


@dataclass(kw_only=True)
class BillingCycle(Enum):
    monthly = "monthly"
    yearly = "yearly"


@dataclass(kw_only=True)
class UpgradeSubscriptionRequest(ApiBaseModel):
    billingCycle: BillingCycle
    """Selects the billing frequency for the subscription. Either 'monthly' for regular monthly charges or 'yearly' for annual billing with a potential discount. """
    successUrl: str
    """URL to redirect the user to after a successful checkout process."""
    cancelUrl: str
    """URL to redirect the user to after the checkout process is canceled."""


@dataclass(kw_only=True)
class DowngradeSubscriptionRequest(ApiBaseModel):
    downgradeReason: Optional[str] = None
    """Reason for downgrading the subscription."""


@dataclass(kw_only=True)
class GetNewBlockIdResponse(GenericApiResponse):
    blockId: int


@dataclass(kw_only=True)
class UpdateImpulseRequest(ApiBaseModel):
    name: Optional[str] = None
    tags: Optional[List[Optional[str]]] = None


@dataclass(kw_only=True)
class SetTunerPrimaryJobRequest(ApiBaseModel):
    name: Optional[str] = None
    """Optional name. If no name is provided, the trial name is used."""


@dataclass(kw_only=True)
class CloneImpulseRequest(ApiBaseModel):
    name: str


@dataclass(kw_only=True)
class CreateSyntheticDataRequest(ApiBaseModel):
    transformationBlockId: int
    """The ID of a Synthetic Data transform block ID (public or private)"""
    parameters: Dict[str, str]
    """Properties for this synthetic data block"""


@dataclass(kw_only=True)
class RecentJobs(ApiBaseModel):
    job: Job
    samples: List[Sample]


@dataclass(kw_only=True)
class GetSyntheticDataConfigResponse(GenericApiResponse):
    recentJobs: List[RecentJobs]
    lastUsedTransformationBlockId: Optional[int] = None
    lastUsedParameters: Optional[Dict[str, Optional[str]]] = None


@dataclass(kw_only=True)
class AIActionsConfigStep(ApiBaseModel):
    transformationBlockId: int
    """The selected transformation block ID."""
    parameters: Dict[str, str]
    """Parameters for the transformation block. These map back to the parameters in OrganizationTransformationBlock 'parameters' property."""


@dataclass(kw_only=True)
class AIActionsDataCategory(Enum):
    allData = "allData"
    unlabeledData = "unlabeledData"
    dataWithoutMetadataKey = "dataWithoutMetadataKey"
    dataWithMetadata = "dataWithMetadata"


@dataclass(kw_only=True)
class AIActionsConfig(ApiBaseModel):
    dataCategory: AIActionsDataCategory
    """Type of data to run this AI action on."""
    steps: List[AIActionsConfigStep]
    dataMetadataKey: Optional[str] = None
    """Metadata key to filter on. Required if dataCategory is equal to "dataWithoutMetadataKey" or "dataWithMetadata"."""
    dataMetadataValue: Optional[str] = None
    """Metadata value to filter on. Required if dataCategory is equal to "dataWithMetadata"."""


@dataclass(kw_only=True)
class SampleProposedChanges(ApiBaseModel):
    label: Optional[str] = None
    """New label (single-label)"""
    isDisabled: Optional[bool] = None
    """True if the current sample should be disabled; or false if it should not be disabled."""
    boundingBoxes: Optional[List[BoundingBox]] = None
    """List of bounding boxes. The existing bounding boxes on the sample will be replaced (so if you want to add new bounding boxes, use the existing list as a basis)."""
    metadata: Optional[Dict[str, Optional[str]]] = None
    """Free form associated metadata. The existing metadata on the sample will be replaced (so if you want to add new metadata, use the existing list as a basis)."""
    structuredLabels: Optional[List[StructuredLabel]] = None
    """New label (multi-label)"""


@dataclass(kw_only=True)
class ProposedChanges(ApiBaseModel):
    sampleId: int
    step: int
    proposedChanges: SampleProposedChanges


@dataclass(kw_only=True)
class AIActionLastPreviewState(ApiBaseModel):
    samples: List[Sample]
    proposedChanges: List[ProposedChanges]


@dataclass(kw_only=True)
class SetMetadataAfterRunning(ApiBaseModel):
    key: str
    value: str


@dataclass(kw_only=True)
class AIAction(ApiBaseModel):
    id: int
    displayName: str
    """Name to show to the user when interacting with this action (e.g. in a table, or when running the action). Will return either "name" (if present), or a name derived from the transformation block."""
    config: AIActionsConfig
    previewConfig: AIActionsConfig
    maxDataPreviewCount: int
    """When rendering preview items, the max amount of items to show (pass this into the previewAIActionsSamples)"""
    gridColumnCount: int
    """Number of grid columns to use during preview."""
    setMetadataAfterRunning: List[SetMetadataAfterRunning]
    """After the action runs, add this key/value pair as metadata on the affected samples."""
    cacheUnchangedSteps: bool
    """If enabled, will load cached results from the previous preview job for unchanged jobs. Disable this if you're developing your own custom AI Labeling job, and want to always re-run all steps."""
    name: Optional[str] = None
    """Manually set name (optional)"""
    lastPreviewState: AIActionLastPreviewState = None


@dataclass(kw_only=True)
class ListAIActionsResponse(GenericApiResponse):
    actions: List[AIAction]


@dataclass(kw_only=True)
class GetAIActionResponse(GenericApiResponse):
    action: AIAction


@dataclass(kw_only=True)
class PreviewAIActionsSamplesRequest(ApiBaseModel):
    saveConfig: bool
    """If this is passed in, the `previewConfig` of the AI action is overwritten (requires actionId to be a valid action)."""
    dataCategory: AIActionsDataCategory
    """Type of data to preview. A random subset of this data will be returned."""
    maxDataPreviewCount: int
    """Max. amount of data items to return."""
    dataMetadataKey: Optional[str] = None
    """Metadata key to filter on. Required if dataCategory is equal to "dataWithoutMetadataKey" or "dataWithMetadata"."""
    dataMetadataValue: Optional[str] = None
    """Metadata value to filter on. Required if dataCategory is equal to "dataWithMetadata"."""


@dataclass(kw_only=True)
class SetSampleProposedChangesRequest(ApiBaseModel):
    jobId: int
    """Job ID of an AI Actions job. This is passed into your job via the --propose-actions argument."""
    proposedChanges: SampleProposedChanges


@dataclass(kw_only=True)
class CreatePreviewAIActionsJobRequest(ApiBaseModel):
    steps: List[AIActionsConfigStep]
    sampleIds: List[int]
    cacheUnchangedSteps: bool
    """If enabled, will load cached results from the previous preview job for unchanged jobs. Disable this if you're developing your own custom AI Labeling job, and want to always re-run all steps."""


@dataclass(kw_only=True)
class UpdateAIActionRequest(ApiBaseModel):
    steps: List[AIActionsConfigStep]
    dataCategory: AIActionsDataCategory
    """Type of data to run this AI action on."""
    setMetadataAfterRunning: List[SetMetadataAfterRunning]
    """After the action runs, add this key/value pair as metadata on the affected samples."""
    name: Optional[str] = None
    """User-provided name. If no name is set then displayName on the action will be automatically configured based on the transformation block."""
    dataMetadataKey: Optional[str] = None
    """Metadata key to filter on. Required if dataCategory is equal to "dataWithoutMetadataKey" or "dataWithMetadata"."""
    dataMetadataValue: Optional[str] = None
    """Metadata value to filter on. Required if dataCategory is equal to "dataWithMetadata"."""
    sortOrder: Optional[int] = None
    """Numeric value (1..n) where this action should be shown in the action list (and in which order the actions should run when started from a data source)."""


@dataclass(kw_only=True)
class GetAIActionsProposedChangesResponse(GenericApiResponse):
    proposedChanges: List[ProposedChanges]


@dataclass(kw_only=True)
class BatchAddMetadataRequest(ApiBaseModel):
    metadataKey: str
    metadataValue: str


@dataclass(kw_only=True)
class BatchClearMetadataByKeyRequest(ApiBaseModel):
    metadataKey: str


@dataclass(kw_only=True)
class SetAIActionsOrderRequest(ApiBaseModel):
    orderByActionId: List[int]


@dataclass(kw_only=True)
class AddApiKeyResponse(GenericApiResponse):
    id: int
    """ID of the new API key"""
    apiKey: str
    """New API Key (starts with "ei_...") - this'll be shared only once."""


@dataclass(kw_only=True)
class SplitSampleInFramesResponse(ApiBaseModel):
    pass


@dataclass(kw_only=True)
class BatchEditLabelsResponse(ApiBaseModel):
    pass


@dataclass(kw_only=True)
class BatchDeleteResponse(ApiBaseModel):
    pass


@dataclass(kw_only=True)
class BatchMoveResponse(ApiBaseModel):
    pass


@dataclass(kw_only=True)
class BatchEnableResponse(ApiBaseModel):
    pass


@dataclass(kw_only=True)
class BatchDisableResponse(ApiBaseModel):
    pass


@dataclass(kw_only=True)
class BatchAddMetadataResponse(ApiBaseModel):
    pass


@dataclass(kw_only=True)
class BatchClearMetadataByKeyResponse(ApiBaseModel):
    pass


@dataclass(kw_only=True)
class ClassifySampleV2Response(ApiBaseModel):
    pass


@dataclass(kw_only=True)
class ClassifySampleForVariantsResponse(ApiBaseModel):
    pass


@dataclass(kw_only=True)
class ClassifySampleByLearnBlockV2Response(ApiBaseModel):
    pass
