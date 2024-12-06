from enum import Enum
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Union
from .api import api
from .api import api
from .models import *
from .client import File


@api("/api-login", method="post")
def login(requestBody: GetJWTRequest) -> GetJWTResponse:
    """Get a JWT token to authenticate with the API."""
    pass


@api("/api-user-create", method="post")
def createUser(requestBody: CreateUserRequest) -> CreateUserResponse:
    """Create a new user and project"""
    pass


@api("/api-user-create-evaluate", method="post")
def createEvaluationUser() -> CreateEvaluationUserResponse:
    """Creates an evaluation user and a new project, and redirects the user to the new project."""
    pass


@api("/api-create-pro-user", method="post")
def createProTierUser(requestBody: CreateProTierUserRequest) -> CreateUserResponse:
    """Create a new user for the Professional Plan and a new project. Note that the Professional plan will not be enabled until the payment is successful."""
    pass


@api("/api-user-create-enterprise-trial", method="post")
def createEnterpriseTrialUser(
    requestBody: CreateEnterpriseTrialUserRequest,
) -> CreateEnterpriseTrialResponse:
    """Creates an enterprise trial user and a new trial organization, and redirects the user to the new organization."""
    pass


@api("/api/user", method="post")
def updateCurrentUser(requestBody: UpdateUserRequest) -> GenericApiResponse:
    """Update user properties such as name. This function is only available through a JWT token."""
    pass


@api("/api/user/convert", method="post")
def convertCurrentUser(requestBody: ConvertUserRequest) -> GenericApiResponse:
    """Convert current evaluation user account to regular account."""
    pass


@api("/api/user/activate", method="post")
def activateCurrentUser(
    requestBody: ActivateUserOrVerifyEmailRequest,
) -> GenericApiResponse:
    """Activate the current user account (requires an activation code). This function is only available through a JWT token."""
    pass


@api("/api/user/request-activation", method="post")
def requestActivationCodeCurrentUser() -> GenericApiResponse:
    """Request a new activation code for the current user. This function is only available through a JWT token."""
    pass


@api("/api/user/create-developer-profile", method="post")
def createDeveloperProfile() -> CreateDeveloperProfileResponse:
    """Create a developer profile for the current active user."""
    pass


@api("/api/user/trial", method="post")
def startEnterpriseTrial(
    requestBody: StartEnterpriseTrialRequest,
) -> CreateEnterpriseTrialResponse:
    """Create an enterprise trial for the current user. Users can only go through a trial once."""
    pass


@api("/api/user/photo", method="post")
def uploadPhotoCurrentUser(
    requestBody: UploadUserPhotoRequest,
) -> UploadUserPhotoResponse:
    """Upload a photo for the current user. This function is only available through a JWT token."""
    pass


@api("/api/user/change-password", method="post")
def changePasswordCurrentUser(requestBody: ChangePasswordRequest) -> GenericApiResponse:
    """Change the password for the current user account. This function is only available through a JWT token."""
    pass


@api("/api/user/by-third-party-activation-code", method="post")
def getUserByThirdPartyActivationCode(
    requestBody: UserByThirdPartyActivationRequest,
) -> GetUserResponse:
    """Get information about a user through an activation code. This function is only available through a JWT token."""
    pass


@api("/api/user/activate-by-third-party-activation-code", method="post")
def activateUserByThirdPartyActivationCode(
    requestBody: ActivateUserByThirdPartyActivationCodeRequest,
) -> GetJWTResponse:
    """Activate a user that was created by a third party. This function is only available through a JWT token."""
    pass


@api("/api/user/accept-tos", method="post")
def acceptTermsOfService() -> GenericApiResponse:
    """Accept Terms of Service."""
    pass


@api("/api/user/dismiss-notification", method="post")
def userDismissNotification(
    requestBody: UserDismissNotificationRequest,
) -> GenericApiResponse:
    """Dismiss a notification"""
    pass


@api("/api/user/mfa/totp/create-key", method="post")
def userGenerateNewTotpMfaKey() -> UserGenerateNewMfaKeyResponse:
    """Creates a new MFA key, only allowed if the user has no MFA configured. TOTP tokens use SHA-1 algorithm."""
    pass


@api("/api/user/mfa/totp/set-key", method="post")
def userSetTotpMfaKey(
    requestBody: UserSetTotpMfaKeyRequest,
) -> UserSetTotpMfaKeyResponse:
    """Enable MFA on this account using an TOTP token. First create a new key via `userGenerateNewTotpMfaKey`."""
    pass


@api("/api/user/mfa/totp/clear", method="post")
def userDeleteTotpMfaKey(
    requestBody: UserDeleteTotpMfaKeyRequest,
) -> GenericApiResponse:
    """Disable MFA on this account using an TOTP token."""
    pass


@api("/api/user/subscription/upgrade", method="post")
def userUpgradeSubscription(requestBody: UpgradeSubscriptionRequest) -> Any:
    """Upgrade the current subscription."""
    pass


@api("/api/user/subscription/cancel", method="post")
def userCancelSubscription(
    requestBody: DowngradeSubscriptionRequest,
) -> GenericApiResponse:
    """Cancel the current subscription."""
    pass


@api("/api/user/subscription/undo-cancel", method="post")
def userUndoCancelSubscription() -> GenericApiResponse:
    """Stop a pending cancellation. If you schedule a subscription to be canceled, and the subscription hasn't yet reached the end of the billing period, you can stop the cancellation. After a subscription has been canceled, you can't reactivate it."""
    pass


@api("/api/users/{userId}", method="post")
def updateUser(userId: str, requestBody: UpdateUserRequest) -> GenericApiResponse:
    """Update user properties such as name. This function is only available through a JWT token."""
    pass


@api("/api/users/{userId}/activate", method="post")
def activateUser(
    userId: str, requestBody: ActivateUserOrVerifyEmailRequest
) -> GenericApiResponse:
    """Activate a user account (requires an activation code). This function is only available through a JWT token."""
    pass


@api("/api/users/{userId}/request-activation", method="post")
def requestActivationCodeUser(userId: str) -> GenericApiResponse:
    """Request a new activation code. This function is only available through a JWT token."""
    pass


@api("/api/users/{userId}/photo", method="post")
def uploadPhotoUser(
    userId: str, requestBody: UploadUserPhotoRequest
) -> UploadUserPhotoResponse:
    """Upload a photo for a user. This function is only available through a JWT token, and is not available for all users."""
    pass


@api("/api/users/{userId}/change-password", method="post")
def changePasswordUser(
    userId: str, requestBody: ChangePasswordRequest
) -> GenericApiResponse:
    """Change the password for a user account. This function is only available through a JWT token."""
    pass


@api("/api/users/{userId}/set-password", method="post")
def setUserPassword(
    userId: str, requestBody: SetUserPasswordRequest
) -> GenericApiResponse:
    """Set the password for a new SSO user. This function is only available through an SSO access token."""
    pass


@api("/api/users/{userId}/feedback", method="post")
def sendUserFeedback(
    userId: str, requestBody: SendUserFeedbackRequest
) -> GenericApiResponse:
    """Send feedback to Edge Impulse or get in touch with sales."""
    pass


@api("/api/users/{userId}/upgrade", method="post")
def sendUserUpgradeRequest(
    userId: str, requestBody: EnterpriseUpgradeOrTrialExtensionRequest
) -> GenericApiResponse:
    """Send an upgrade to Enterprise request to Edge Impulse."""
    pass


@api("/api-user-request-reset-password", method="post")
def requestResetPassword(
    requestBody: RequestResetPasswordRequest,
) -> GenericApiResponse:
    """Request a password reset link for a user."""
    pass


@api("/api-user-reset-password", method="post")
def resetPassword(requestBody: ResetPasswordRequest) -> GenericApiResponse:
    """Reset the password for a user."""
    pass


@api("/api-user-verify-reset-password-code", method="post")
def verifyResetPassword(requestBody: VerifyResetPasswordRequest) -> GenericApiResponse:
    """Verify whether the reset password code for the user is valid."""
    pass


@api("/api-user-need-to-set-password/{usernameOrEmail}", method="get")
def getUserNeedToSetPassword(usernameOrEmail: str) -> GetUserNeedToSetPasswordResponse:
    """Tells whether a user is registered and whether it needs to set its password."""
    pass


@api("/api/user", method="get")
def getCurrentUser(excludeProjects: str = None) -> GetUserResponse:
    """Get information about the current user. This function is only available through a JWT token."""
    pass


@api("/api/user/projects", method="get")
def getCurrentUserProjects() -> GetUserProjectsResponse:
    """Get projects for the current user. This returns all projects regardless of whitelabel. This function is only available through a JWT token."""
    pass


@api("/api/user/emails", method="get")
def listEmailsCurrentUser() -> ListEmailResponse:
    """Get a list of all emails sent by Edge Impulse to the current user. This function is only available through a JWT token, and is not available for all users."""
    pass


@api("/api/user/organizations", method="get")
def listOrganizationsCurrentUser() -> ListOrganizationsResponse:
    """List all organizations that the current user is a member of. This function is only available through a JWT token."""
    pass


@api("/api/users/buckets", method="get")
def listOrganizationBucketsCurrentUser() -> ListOrganizationBucketsUserResponse:
    """List all organizational storage buckets that the current user has access to. This function is only available through a JWT token."""
    pass


@api("/api/user/subscription/metrics", method="get")
def userGetSubscriptionMetrics() -> UserSubscriptionMetricsResponse:
    """Get billable compute metrics for a user. This function is only available to users with an active subscription."""
    pass


@api("/api/users/{userId}", method="get")
def getUser(userId: str) -> GetUserResponse:
    """Get information about a user. This function is only available through a JWT token."""
    pass


@api("/api/users/{userId}/emails", method="get")
def listEmailsUser(userId: str) -> ListEmailResponse:
    """Get a list of all emails sent by Edge Impulse to a user. This function is only available through a JWT token, and is not available for all users."""
    pass


@api("/api/users/{userId}/organizations", method="get")
def listOrganizationsUser(userId: str) -> ListOrganizationsResponse:
    """List all organizations for a user. This function is only available through a JWT token."""
    pass


@api("/api/users/{userId}/buckets", method="get")
def listOrganizationBucketsUser(userId: str) -> ListOrganizationBucketsUserResponse:
    """List all organizational storage buckets that a user has access to. This function is only available through a JWT token."""
    pass


@api("/api/users/{userId}/trials", method="get")
def listEnterpriseTrialsUser(userId: str) -> ListEnterpriseTrialsResponse:
    """Get a list of all enterprise trials for a user. This function is only available through a JWT token."""
    pass


@api("/api/user", method="delete")
def deleteCurrentUser(requestBody: DeleteUserRequest) -> GenericApiResponse:
    """Delete a user. This function is only available through a JWT token, and can only remove the current user."""
    pass


@api("/api/user/photo", method="delete")
def deletePhotoCurrentUser() -> GenericApiResponse:
    """Delete user profile photo. This function is only available through a JWT token."""
    pass


@api("/api/users/{userId}", method="delete")
def deleteUser(userId: str, requestBody: DeleteUserRequest) -> GenericApiResponse:
    """Delete a user. This function is only available through a JWT token, and can only remove the current user."""
    pass


@api("/api/canary", method="get")
def shouldGoOnCanary(requestedUrl: str) -> CanaryResponse:
    """Get the decision to whether the requested URL goes on canary deployment or not"""
    pass


@api("/api/third-party-auth", method="get")
def getAllThirdPartyAuth() -> GetAllThirdPartyAuthResponse:
    """Get information about all third party authentication partners"""
    pass


@api("/api/third-party-auth/{authId}", method="get")
def getThirdPartyAuth(authId: str) -> GetThirdPartyAuthResponse:
    """Get information about a third party authentication partner"""
    pass


@api("/api/third-party-auth", method="post")
def createThirdPartyAuth(
    requestBody: CreateThirdPartyAuthRequest,
) -> CreateThirdPartyAuthResponse:
    """Create a new third party authentication partner"""
    pass


@api("/api/third-party-auth/{authId}", method="post")
def updateThirdPartyAuth(
    authId: str, requestBody: UpdateThirdPartyAuthRequest
) -> GenericApiResponse:
    """Update a third party authentication partner"""
    pass


@api("/api/{projectId}/third-party-auth/{authId}/authorize", method="post")
def authorizeThirdParty(
    projectId: str, authId: str, requestBody: AuthorizeThirdPartyRequest
) -> Any:
    """Authorize a third party to access a project"""
    pass


@api("/api/third-party-auth/{authId}/login", method="post")
def createUserThirdParty(
    authId: str, requestBody: CreateUserThirdPartyRequest
) -> CreateUserThirdPartyResponse:
    """Login as a user as a third-party authentication provider. If the user does not exists, it's automatically created. You can only log in as users that were previously created by you."""
    pass


@api("/api/third-party-auth/{authId}", method="delete")
def deleteThirdPartyAuth(authId: str) -> GenericApiResponse:
    """Delete a third party authentication partner"""
    pass


@api("/api/themes", method="get")
def getThemes() -> GetThemesResponse:
    """Get all available Studio themes."""
    pass


@api("/api/themes/{themeId}", method="get")
def getTheme(themeId: str) -> GetThemeResponse:
    """Get a theme given its unique identifier."""
    pass


@api("/api/themes/{themeId}", method="delete")
def deleteTheme(themeId: str) -> GenericApiResponse:
    """Delete a theme given its unique identifier."""
    pass


@api("/api/themes/{themeId}/logos", method="post")
def updateThemeLogos(
    themeId: str, requestBody: UpdateThemeLogosRequest
) -> GenericApiResponse:
    """Update some or all theme logos."""
    pass


@api("/api/themes/{themeId}/colors", method="post")
def updateThemeColors(
    themeId: str, requestBody: UpdateThemeColorsRequest
) -> GenericApiResponse:
    """Update some or all theme colors."""
    pass


@api("/api/themes/{themeId}/favicon", method="post")
def updateThemeFavicon(
    themeId: str, requestBody: UploadImageRequest
) -> GenericApiResponse:
    """Update the theme favicon"""
    pass


@api("/api/whitelabels", method="get")
def getAllWhitelabels() -> GetAllWhitelabelsResponse:
    """Retrieve the list of registered white labels."""
    pass


@api("/api/whitelabel/{whitelabelIdentifier}", method="get")
def getWhitelabel(whitelabelIdentifier: str) -> GetWhitelabelResponse:
    """Retrieve all the information about this white label."""
    pass


@api("/api/whitelabel/{whitelabelIdentifier}/domain", method="get")
def getWhitelabelDomain(whitelabelIdentifier: str) -> GetWhitelabelDomainResponse:
    """Get a white label domain given its unique identifier."""
    pass


@api("/api/whitelabel/{whitelabelIdentifier}/impulse/blocks", method="get")
def getAllImpulseBlocks(whitelabelIdentifier: str) -> GetImpulseBlocksResponse:
    """Lists all possible DSP and ML blocks available for this white label."""
    pass


@api("/api/whitelabels", method="post")
def createWhitelabel(requestBody: CreateWhitelabelRequest) -> CreateWhitelabelResponse:
    """Create a new white label"""
    pass


@api("/api/whitelabel/{whitelabelIdentifier}/deploymentTargets", method="post")
def updateDeploymentTargets(
    whitelabelIdentifier: str, requestBody: UpdateWhitelabelDeploymentTargetsRequest
) -> GenericApiResponse:
    """Update some or all of the deployment targets enabled for this white label."""
    pass


@api("/api/whitelabel/{whitelabelIdentifier}", method="put")
def updateWhitelabel(
    whitelabelIdentifier: str, requestBody: UpdateWhitelabelInternalRequest
) -> GenericApiResponse:
    """Update the white label with the given id."""
    pass


@api("/api/whitelabel/{whitelabelIdentifier}", method="delete")
def deleteWhitelabel(whitelabelIdentifier: str) -> GenericApiResponse:
    """Deletes the white label with the given id."""
    pass


@api("/api/deployment/targets", method="get")
def listAllDeploymentTargets() -> DeploymentTargetsResponse:
    """List all deployment targets"""
    pass


@api("/api/{projectId}/deployment/targets", method="get")
def listDeploymentTargetsForProject(
    projectId: str, impulseId: str = None
) -> ProjectDeploymentTargetsResponse:
    """List deployment targets for a project"""
    pass


@api("/api/{projectId}/deployment/targets/data-sources", method="get")
def listDeploymentTargetsForProjectDataSources(
    projectId: str, impulseId: str = None
) -> DeploymentTargetsResponse:
    """List deployment targets for a project from data sources page  (it shows some things like all Linux deploys, and hides 'fake' deploy targets like mobile phone / computer)"""
    pass


@api("/api/{projectId}/deployment/evaluate", method="get")
def getEvaluateJobResult(projectId: str, impulseId: str = None) -> EvaluateJobResponse:
    """Get evaluate job result, containing detailed performance statistics for every possible variant of the impulse."""
    pass


@api("/api/{projectId}/deployment/evaluate/cache", method="get")
def getEvaluateJobResultCache(
    projectId: str, impulseId: str = None
) -> EvaluateJobResponse:
    """Get evaluate job result, containing detailed performance statistics for every possible variant of the impulse. This only checks cache, and throws an error if there is no data in cache."""
    pass


@api("/api/{projectId}/deployment", method="get")
def getDeployment(
    projectId: str,
    type: str,
    modelType: str = None,
    engine: str = None,
    impulseId: str = None,
) -> GetDeploymentResponse:
    """Gives information on whether a deployment was already built for a type"""
    pass


@api("/api/{projectId}/deployment/download", method="get")
def downloadBuild(
    projectId: str,
    type: str,
    modelType: str = None,
    engine: str = None,
    impulseId: str = None,
) -> File:
    """Download the build artefacts for a project"""
    pass


@api("/api/{projectId}/deployment/last", method="get")
def getLastDeploymentBuild(
    projectId: str, impulseId: str = None
) -> GetLastDeploymentBuildResponse:
    """Get information on the result of the last successful deployment job, including info on the build e.g. whether it is still valid."""
    pass


@api("/api/{projectId}/deployment/syntiant/posterior", method="get")
def getSyntiantPosterior(
    projectId: str, impulseId: str = None
) -> GetSyntiantPosteriorResponse:
    """Get the current posterior parameters for the Syntiant deployment target"""
    pass


@api("/api/{projectId}/deployment/syntiant/posterior", method="post")
def setSyntiantPosterior(
    projectId: str, requestBody: SetSyntiantPosteriorRequest, impulseId: str = None
) -> GenericApiResponse:
    """Set the current posterior parameters for the Syntiant deployment target"""
    pass


@api("/api/{projectId}/jobs/find-syntiant-posterior", method="post")
def findSyntiantPosterior(
    projectId: str, requestBody: FindSyntiantPosteriorRequest, impulseId: str = None
) -> StartJobResponse:
    """Automatically find the current posterior parameters for the Syntiant deployment target"""
    pass


@api("/api/projects", method="get")
def listProjects() -> ListProjectsResponse:
    """Retrieve list of active projects. If authenticating using JWT token this lists all the projects the user has access to, if authenticating using an API key, this only lists that project."""
    pass


@api("/api/{projectId}/devkeys", method="get")
def listDevkeys(projectId: str) -> DevelopmentKeysResponse:
    """Retrieve the development API and HMAC keys for a project. These keys are specifically marked to be used during development. These keys can be `undefined` if no development keys are set."""
    pass


@api("/api/{projectId}/downloads", method="get")
def listDownloads(projectId: str, impulseId: str = None) -> ProjectDownloadsResponse:
    """Retrieve the downloads for a project."""
    pass


@api("/api/{projectId}/csv-wizard/download-config", method="get")
def downloadCsvWizardConfig(projectId: str) -> File:
    """Returns a JSON file with the current CSV wizard config. If there is no config this will throw a 5xx error."""
    pass


@api("/api/{projectId}/csv-wizard/uploaded-file", method="get")
def getCsvWizardUploadedFileInfo(projectId: str) -> GetCsvWizardUploadedFileInfo:
    """Returns whether the file that was uploaded when the CSV wizard was configured is available."""
    pass


@api("/api/{projectId}/csv-wizard/uploaded-file/download", method="get")
def downloadCsvWizardUploadedFile(projectId: str) -> File:
    """Returns the file that was uploaded when the CSV wizard was configured. If there is no config this will throw a 5xx error."""
    pass


@api("/api/{projectId}/hmackeys", method="get")
def listProjectHmacKeys(projectId: str) -> ListHmacKeysResponse:
    """Retrieve all HMAC keys."""
    pass


@api("/api/{projectId}/apikeys", method="get")
def listProjectApiKeys(projectId: str) -> ListApiKeysResponse:
    """Retrieve all API keys. This does **not** return the full API key, but only a portion (for security purposes). The development key will be returned in full, as it'll be set in devices and is thus not private."""
    pass


@api("/api/{projectId}/emails", method="get")
def listEmails(projectId: str) -> ListEmailResponse:
    """Get a list of all emails sent by Edge Impulse regarding this project."""
    pass


@api("/api/{projectId}/socket-token", method="get")
def getSocketToken(projectId: str) -> SocketTokenResponse:
    """Get a token to authenticate with the web socket interface."""
    pass


@api("/api/{projectId}/data-axes", method="get")
def getProjectDataAxesSummary(
    projectId: str, includeDisabled: str = None, includeNotProcessed: str = None
) -> ProjectDataAxesSummaryResponse:
    """Get a list of axes that are present in the training data."""
    pass


@api("/api/{projectId}/data-summary", method="get")
def getProjectTrainingDataSummary(
    projectId: str, includeDisabled: str = None, includeNotProcessed: str = None
) -> ProjectTrainingDataSummaryResponse:
    """Get summary of all data present in the training set. This returns the number of data items, the total length of all data, and the labels. This is similar to `dataSummary` in `ProjectInfoResponse` but allows you to exclude disabled items or items that are still processing."""
    pass


@api("/api/{projectId}/data-interval", method="get")
def getProjectRecommendedDataInterval(projectId: str) -> ProjectDataIntervalResponse:
    """Get the interval of the training data; if multiple intervals are present, the interval of the longest data item is returned."""
    pass


@api("/api/{projectId}/versions", method="get")
def listVersions(projectId: str) -> ListVersionsResponse:
    """Get all versions for this project."""
    pass


@api("/api/{projectId}/versions/public", method="get")
def listPublicVersions(projectId: str) -> ListPublicVersionsResponse:
    """Get all public versions for this project. You don't need any authentication for this function."""
    pass


@api("/api/{projectId}/last-modification", method="get")
def getProjectLastModificationDate(projectId: str) -> LastModificationDateResponse:
    """Get the last modification date for a project (will be upped when data is modified, or when an impulse is trained)"""
    pass


@api("/api/{projectId}/development-boards", method="get")
def listDevelopmentBoards(projectId: str) -> DevelopmentBoardsResponse:
    """List all development boards for a project"""
    pass


@api("/api/{projectId}/target-constraints", method="get")
def getTargetConstraints(projectId: str) -> GetTargetConstraintsResponse:
    """Retrieve target constraints for a project. The constraints object captures hardware attributes of your target device, along with an application budget to allow guidance on performance and resource usage"""
    pass


@api("/api/{projectId}/model-variants", method="get")
def getModelVariants(projectId: str, impulseId: str = None) -> GetModelVariantsResponse:
    """Get a list of model variants applicable to all trained learn blocks in this project."""
    pass


@api("/api/{projectId}/synthetic-data", method="get")
def getSyntheticDataConfig(projectId: str) -> GetSyntheticDataConfigResponse:
    """Get the last used synthetic data config"""
    pass


@api("/api/{projectId}/ai-actions", method="get")
def listAIActions(projectId: str) -> ListAIActionsResponse:
    """Get all AI actions."""
    pass


@api("/api/{projectId}/ai-actions/new", method="get")
def getNewAIAction(projectId: str) -> GetAIActionResponse:
    """Get the AI Actions config for a new action"""
    pass


@api("/api/{projectId}/ai-actions/{actionId}", method="get")
def getAIAction(projectId: str, actionId: str) -> GetAIActionResponse:
    """Get an AI Actions config"""
    pass


@api("/api/{projectId}/ai-actions/{actionId}/clear-proposed-changes", method="get")
def clearAIActionsProposedChanges(projectId: str, actionId: str) -> GenericApiResponse:
    """Remove all proposed changes for an AI Actions job."""
    pass


@api("/api/projects/public", method="get")
def listPublicProjects(
    limit: str = None,
    offset: str = None,
    project: str = None,
    projectTypes: str = None,
    sort: str = None,
) -> ListPublicProjectsResponse:
    """Retrieve the list of all public projects. You don't need any authentication for this method."""
    pass


@api("/api/projects/types", method="get")
def listPublicProjectTypes() -> ListPublicProjectTypesResponse:
    """Retrieve the list of available public project types. You don't need any authentication for this method."""
    pass


@api("/api/{projectId}", method="get")
def getProjectInfo(projectId: str, impulseId: str = None) -> ProjectInfoResponse:
    """List all information about this project."""
    pass


@api("/api/{projectId}/public-info", method="get")
def getProjectInfoSummary(projectId: str) -> ProjectInfoSummaryResponse:
    """List a summary about this project - available for public projects."""
    pass


@api("/api/projects/create", method="post")
def createProject(requestBody: CreateProjectRequest) -> CreateProjectResponse:
    """Create a new project. This API can only be called using a JWT token."""
    pass


@api("/api/{projectId}/csv-wizard/uploaded-file", method="post")
def uploadCsvWizardUploadedFile(
    projectId: str, requestBody: UploadCsvWizardUploadedFileRequest
) -> GenericApiResponse:
    """Asynchronously called in the CSV Wizard to store the file that the CSV wizard was based on."""
    pass


@api("/api/{projectId}/collaborators/add", method="post")
def addCollaborator(
    projectId: str, requestBody: AddCollaboratorRequest
) -> EntityCreatedResponse:
    """Add a collaborator to a project."""
    pass


@api("/api/{projectId}/collaborators/remove", method="post")
def removeCollaborator(
    projectId: str, requestBody: RemoveCollaboratorRequest
) -> GenericApiResponse:
    """Remove a collaborator to a project. Note that you cannot invoke this function if only a single collaborator is present."""
    pass


@api("/api/{projectId}/collaborators/transfer-ownership", method="post")
def transferOwnership(
    projectId: str, requestBody: AddCollaboratorRequest
) -> GenericApiResponse:
    """Transfer ownership of a project to another user."""
    pass


@api("/api/{projectId}/collaborators/transfer-ownership-org", method="post")
def transferOwnershipOrganization(
    projectId: str, requestBody: TransferOwnershipOrganizationRequest
) -> GenericApiResponse:
    """Transfer ownership of a project to another organization."""
    pass


@api("/api/{projectId}/hmackeys", method="post")
def addProjectHmacKey(
    projectId: str, requestBody: AddHmacKeyRequest
) -> EntityCreatedResponse:
    """Add an HMAC key. If you set `developmentKey` to `true` this flag will be removed from the current development HMAC key."""
    pass


@api("/api/{projectId}/apikeys", method="post")
def addProjectApiKey(
    projectId: str, requestBody: AddProjectApiKeyRequest
) -> AddApiKeyResponse:
    """Add an API key. If you set `developmentKey` to `true` this flag will be removed from the current development API key."""
    pass


@api("/api/{projectId}/compute-time-limit", method="post")
def setProjectComputeTimeLimit(
    projectId: str, requestBody: SetProjectComputeTimeRequest
) -> GenericApiResponse:
    """Change the job compute time limit for the project. This function is only available through a JWT token, and is not available to all users."""
    pass


@api("/api/{projectId}/dsp-file-size-limit", method="post")
def setProjectFileSizeLimit(
    projectId: str, requestBody: SetProjectDspFileSizeRequest
) -> GenericApiResponse:
    """Change the DSP file size limit for the project. This function is only available through a JWT token, and is not available to all users."""
    pass


@api("/api/{projectId}/versions/{versionId}", method="post")
def updateVersion(
    projectId: str, versionId: str, requestBody: UpdateVersionRequest
) -> GenericApiResponse:
    """Updates a version, this only updates fields that were set in the body."""
    pass


@api("/api/{projectId}/versions/{versionId}/make-private", method="post")
def makeVersionPrivate(projectId: str, versionId: str) -> GenericApiResponse:
    """Make a public version private."""
    pass


@api("/api/{projectId}/readme/upload-image", method="post")
def uploadReadmeImage(
    projectId: str, requestBody: UploadImageRequest
) -> UploadReadmeImageResponse:
    """Uploads an image to the user CDN and returns the path."""
    pass


@api("/api/{projectId}/launch-getting-started", method="post")
def launchGettingStartedWizard(projectId: str) -> GenericApiResponse:
    """This clears out *all data in your project*, and is irrevocable. This function is only available through a JWT token, and is not available to all users."""
    pass


@api("/api/{projectId}/target-constraints", method="post")
def setTargetConstraints(
    projectId: str, requestBody: TargetConstraints
) -> GenericApiResponse:
    """Set target constraints for a project. Use the constraints object to capture hardware attributes of your target device, along with an application budget to allow guidance on performance and resource usage"""
    pass


@api("/api/{projectId}/dismiss-notification", method="post")
def projectDismissNotification(
    projectId: str, requestBody: ProjectDismissNotificationRequest
) -> GenericApiResponse:
    """Dismiss a notification"""
    pass


@api("/api/{projectId}/ai-actions/order", method="post")
def setAIActionsOrder(
    projectId: str, requestBody: SetAIActionsOrderRequest
) -> GenericApiResponse:
    """Change the order of AI actions. Post the new order of all AI Actions by ID. You need to specify _all_ AI Actions here. If not, an error will be thrown."""
    pass


@api("/api/{projectId}/ai-actions/create", method="post")
def createAIAction(projectId: str) -> EntityCreatedResponse:
    """Create a new AI Action."""
    pass


@api("/api/{projectId}/ai-actions/{actionId}", method="post")
def updateAIAction(
    projectId: str, actionId: str, requestBody: UpdateAIActionRequest
) -> GenericApiResponse:
    """Store an AI Actions config. Use `createAIActionsJob` to run the job. Post the full AI Action here w/ all parameters."""
    pass


@api("/api/{projectId}/ai-actions/{actionId}/preview-samples", method="post")
def previewAIActionsSamples(
    projectId: str, actionId: str, requestBody: PreviewAIActionsSamplesRequest
) -> ListSamplesResponse:
    """Get a number of random samples to show in the AI Actions screen. If `saveConfig` is passed in, then a valid actionId is required in the URL. If you don't need to save the config (e.g. when creating a new action), you can use -1."""
    pass


@api("/api/{projectId}/tags", method="post")
def updateProjectTags(
    projectId: str, requestBody: UpdateProjectTagsRequest
) -> GenericApiResponse:
    """Update the list of project tags."""
    pass


@api("/api/{projectId}", method="post")
def updateProject(
    projectId: str, requestBody: UpdateProjectRequest
) -> GenericApiResponse:
    """Update project properties such as name and logo."""
    pass


@api("/api/{projectId}/hmackeys/{hmacId}", method="delete")
def revokeProjectHmacKey(projectId: str, hmacId: str) -> GenericApiResponse:
    """Revoke an HMAC key. Note that if you revoke the development key some services (such as automatic provisioning of devices through the serial daemon) will no longer work."""
    pass


@api("/api/{projectId}/apikeys/{apiKeyId}", method="delete")
def revokeProjectApiKey(projectId: str, apiKeyId: str) -> GenericApiResponse:
    """Revoke an API key. Note that if you revoke the development API key some services (such as automatic provisioning of devices through the serial daemon) will no longer work."""
    pass


@api("/api/{projectId}/versions/{versionId}", method="delete")
def deleteVersion(projectId: str, versionId: str) -> GenericApiResponse:
    """Delete a version. This does not delete the version from cold storage."""
    pass


@api("/api/{projectId}/ai-actions/{actionId}", method="delete")
def deleteAIAction(projectId: str, actionId: str) -> GenericApiResponse:
    """Deletes an AI Actions."""
    pass


@api("/api/{projectId}", method="delete")
def deleteProject(projectId: str) -> GenericApiResponse:
    """Remove the current project, and all data associated with it. This is irrevocable!"""
    pass


@api("/api/{projectId}/devices", method="get")
def listDevices(projectId: str) -> ListDevicesResponse:
    """List all devices for this project. Devices get included here if they connect to the remote management API or if they have sent data to the ingestion API and had the `device_id` field set."""
    pass


@api("/api/{projectId}/device/{deviceId}", method="get")
def getDevice(projectId: str, deviceId: str) -> GetDeviceResponse:
    """Retrieves a single device"""
    pass


@api("/api/{projectId}/device/{deviceId}", method="delete")
def deleteDevice(projectId: str, deviceId: str) -> GenericApiResponse:
    """Delete a device. When this device sends a new message to ingestion or connects to remote management the device will be recreated."""
    pass


@api("/api/{projectId}/device/{deviceId}/start-sampling", method="post")
def startSampling(
    projectId: str, deviceId: str, requestBody: StartSamplingRequest
) -> StartSamplingResponse:
    """Start sampling on a device. This function returns immediately. Updates are streamed through the websocket API."""
    pass


@api("/api/{projectId}/device/{deviceId}/debug-stream/inference/start", method="post")
def startDeviceInferenceDebugStream(
    projectId: str, deviceId: str
) -> StartDeviceDebugStreamResponse:
    """Start an inference debug stream for this device with inference results (and images if a camera is attached). Updates are streamed through the websocket API. A keep-alive token is returned, you'll need to ping the API (with keepDeviceDebugStreamAlive) every 10 seconds (so we know when the client is disconnected)."""
    pass


@api("/api/{projectId}/device/{deviceId}/debug-stream/snapshot/start", method="post")
def startDeviceSnapshotDebugStream(
    projectId: str, deviceId: str, requestBody: StartDeviceSnapshotDebugStreamRequest
) -> StartDeviceDebugStreamResponse:
    """Start a snapshot debug stream for this device with a current camera view. Updates are streamed through the websocket API. A keep-alive token is returned, you'll need to ping the API (with keepDeviceDebugStreamAlive) every 10 seconds (so we know when the client is disconnected)."""
    pass


@api("/api/{projectId}/device/{deviceId}/debug-stream/keep-alive", method="post")
def keepDeviceDebugStreamAlive(
    projectId: str, deviceId: str, requestBody: KeepDeviceDebugStreamAliveRequest
) -> GenericApiResponse:
    """If you have opened a debug stream, ping this interface every 10 seconds to let us know to keep the debug stream open."""
    pass


@api("/api/{projectId}/device/{deviceId}/debug-stream/stop", method="post")
def stopDeviceDebugStream(
    projectId: str, deviceId: str, requestBody: StopDeviceDebugStreamRequest
) -> GenericApiResponse:
    """If you have opened a debug stream, close it."""
    pass


@api("/api/{projectId}/device/{deviceId}/get-impulse-records", method="post")
def getImpulseRecords(
    projectId: str, deviceId: str, requestBody: GetImpulseRecordsRequest
) -> GenericApiResponse:
    """Retrieve impulse records from the device."""
    pass


@api("/api/{projectId}/devices/create", method="post")
def createDevice(
    projectId: str, requestBody: CreateDeviceRequest
) -> GenericApiResponse:
    """Create a new device. If you set `ifNotExists` to `false` and the device already exists, the `deviceType` will be overwritten."""
    pass


@api("/api/{projectId}/devices/{deviceId}/rename", method="post")
def renameDevice(
    projectId: str, deviceId: str, requestBody: RenameDeviceRequest
) -> GenericApiResponse:
    """Set the current name for a device."""
    pass


@api("/api/{projectId}/devices/{deviceId}/request-model-update", method="post")
def requestDeviceModelUpdate(projectId: str, deviceId: str) -> GenericApiResponse:
    """Trigger a model update request, this only works for devices connected to remote management server in inference mode."""
    pass


@api("/api/{projectId}/raw-data", method="get")
def listSamples(
    projectId: str,
    category: str,
    limit: str = None,
    offset: str = None,
    excludeSensors: str = None,
    labels: str = None,
    filename: str = None,
    maxLength: str = None,
    minLength: str = None,
    minFrequency: str = None,
    maxFrequency: str = None,
    signatureValidity: str = None,
    includeDisabled: str = None,
    minLabel: str = None,
    maxLabel: str = None,
    search: str = None,
    proposedActionsJobId: str = None,
) -> ListSamplesResponse:
    """Retrieve all raw data by category."""
    pass


@api("/api/{projectId}/raw-data/count", method="get")
def countSamples(
    projectId: str,
    category: str,
    labels: str = None,
    filename: str = None,
    maxLength: str = None,
    minLength: str = None,
    minFrequency: str = None,
    maxFrequency: str = None,
    signatureValidity: str = None,
    includeDisabled: str = None,
    minLabel: str = None,
    maxLabel: str = None,
    search: str = None,
) -> CountSamplesResponse:
    """Count all raw data by category."""
    pass


@api("/api/{projectId}/raw-data/label-object-detection-queue", method="get")
def getObjectDetectionLabelQueue(projectId: str) -> ObjectDetectionLabelQueueResponse:
    """Get all unlabeled items from the object detection queue."""
    pass


@api("/api/{projectId}/raw-data/label-object-detection-queue/count", method="get")
def getObjectDetectionLabelQueueCount(
    projectId: str,
) -> ObjectDetectionLabelQueueCountResponse:
    """Get count for unlabeled items from the object detection queue."""
    pass


@api("/api/{projectId}/raw-data/metadata", method="get")
def getSampleMetadata(projectId: str, category: str) -> GetSampleMetadataResponse:
    """Get metadata for all samples in a project."""
    pass


@api("/api/{projectId}/raw-data/imported-from", method="get")
def getAllImportedFrom(
    projectId: str, limit: str = None, offset: str = None
) -> GetAllImportedFromResponse:
    """Lists all data with an 'imported from' metadata key. Used to check in a data source which items are already in a project."""
    pass


@api("/api/{projectId}/raw-data/{sampleId}", method="get")
def getSample(
    projectId: str,
    sampleId: str,
    limitPayloadValues: str = None,
    cacheKey: str = None,
    impulseId: str = None,
    proposedActionsJobId: str = None,
) -> GetSampleResponse:
    """Get a sample."""
    pass


@api("/api/{projectId}/raw-data/{sampleId}/raw", method="get")
def getSampleAsRaw(projectId: str, sampleId: str) -> File:
    """Download a sample in it's original format as uploaded to the ingestion service."""
    pass


@api("/api/{projectId}/raw-data/{sampleId}/wav", method="get")
def getSampleAsAudio(
    projectId: str,
    sampleId: str,
    axisIx: str,
    sliceStart: str = None,
    sliceEnd: str = None,
    cacheKey: str = None,
) -> File:
    """Get a sample as a WAV file. This only applies to samples with an audio axis."""
    pass


@api("/api/{projectId}/raw-data/{sampleId}/image", method="get")
def getSampleAsImage(
    projectId: str,
    sampleId: str,
    afterInputBlock: str = None,
    cacheKey: str = None,
    impulseId: str = None,
) -> File:
    """Get a sample as an image file. This only applies to samples with RGBA data."""
    pass


@api("/api/{projectId}/raw-data/{sampleId}/video", method="get")
def getSampleAsVideo(
    projectId: str,
    sampleId: str,
    afterInputBlock: str = None,
    cacheKey: str = None,
    impulseId: str = None,
) -> File:
    """Get a sample as an video file. This only applies to samples with video data."""
    pass


@api("/api/{projectId}/raw-data/{sampleId}/slice", method="get")
def getSampleSlice(
    projectId: str,
    sampleId: str,
    sliceStart: str,
    sliceEnd: str = None,
    impulseId: str = None,
) -> GetSampleResponse:
    """Get a slice of a sample."""
    pass


@api("/api/{projectId}/raw-data/{sampleId}/original", method="get")
def getUncroppedDownsampledSample(
    projectId: str,
    sampleId: str,
    limitPayloadValues: str = None,
    zoomStart: str = None,
    zoomEnd: str = None,
    impulseId: str = None,
) -> GetSampleResponse:
    """Get the original, uncropped, downsampled data."""
    pass


@api("/api/{projectId}/raw-data/data-explorer/features", method="get")
def getDataExplorerFeatures(projectId: str) -> GetDataExplorerFeaturesResponse:
    """t-SNE2 output of the raw dataset"""
    pass


@api("/api/{projectId}/raw-data/data-explorer/has-features", method="get")
def hasDataExplorerFeatures(projectId: str) -> HasDataExplorerFeaturesResponse:
    """t-SNE2 output of the raw dataset"""
    pass


@api("/api/{projectId}/raw-data/data-explorer/predictions", method="get")
def getDataExplorerPredictions(projectId: str) -> DataExplorerPredictionsResponse:
    """Predictions for every data explorer point (only available when using current impulse to populate data explorer)"""
    pass


@api("/api/{projectId}/raw-data/data-explorer/settings", method="get")
def getDataExplorerSettings(projectId: str) -> GetDataExplorerSettingsResponse:
    """Get data explorer configuration, like the type of data, and the input / dsp block to use."""
    pass


@api("/api/{projectId}/raw-data/data-quality/diversity/exists", method="get")
def hasDiversityData(projectId: str) -> HasDataExplorerFeaturesResponse:
    """Determine if data diversity metrics have been calculated. To calculate these metrics, use the `calculateDataQualityMetrics` endpoint."""
    pass


@api("/api/{projectId}/raw-data/data-quality/diversity", method="get")
def getDiversityData(projectId: str) -> GetDiversityDataResponse:
    """Obtain metrics that describe the similarity and diversity of a dataset. To calculate these metrics, use the `calculateDataQualityMetrics` endpoint."""
    pass


@api("/api/{projectId}/raw-data/data-quality/label-noise/exists", method="get")
def hasLabelNoiseData(projectId: str) -> HasDataExplorerFeaturesResponse:
    """Determine if label noise metrics have been calculated. To calculate these metrics, use the `calculateDataQualityMetrics` endpoint."""
    pass


@api("/api/{projectId}/raw-data/data-quality/label-noise", method="get")
def getLabelNoiseData(projectId: str) -> GetLabelNoiseDataResponse:
    """Obtain metrics that describe potential label noise issues in the dataset. To calculate these metrics, use the `calculateDataQualityMetrics` endpoint."""
    pass


@api(
    "/api/{projectId}/raw-data/ai-actions-preview/{jobId}/proposed-changes",
    method="get",
)
def getAIActionsProposedChanges(
    projectId: str, jobId: str
) -> GetAIActionsProposedChangesResponse:
    """Get proposed changes from an AI Actions job."""
    pass


@api("/api/{projectId}/rebalance", method="post")
def rebalanceDataset(projectId: str) -> RebalanceDatasetResponse:
    """Rebalances the dataset over training / testing categories. This resets the category for all data and splits it 80%/20% between training and testing. This is a deterministic process based on the hash of the name of the data."""
    pass


@api("/api/{projectId}/raw-data/clear-all-object-detection-labels", method="post")
def clearAllObjectDetectionLabels(projectId: str) -> GenericApiResponse:
    """Clears all object detection labels for this dataset, and places all images back in the labeling queue."""
    pass


@api("/api/{projectId}/raw-data/delete-all", method="post")
def deleteAllSamples(projectId: str) -> GenericApiResponse:
    """Deletes all samples for this project over all categories. This also invalidates all DSP and learn blocks. Note that this does not delete the data from cold storage."""
    pass


@api("/api/{projectId}/raw-data/delete-all/{category}", method="post")
def deleteAllSamplesByCategory(projectId: str, category: str) -> GenericApiResponse:
    """Deletes all samples for this project over a single category. Note that this does not delete the data from cold storage."""
    pass


@api("/api/{projectId}/raw-data/{sampleId}/rename", method="post")
def renameSample(
    projectId: str, sampleId: str, requestBody: RenameSampleRequest
) -> GenericApiResponse:
    """Sets the file name of the sample. This name does not need to be unique, but it's highly recommended to do so."""
    pass


@api("/api/{projectId}/raw-data/{sampleId}/edit-label", method="post")
def editLabel(
    projectId: str, sampleId: str, requestBody: EditSampleLabelRequest
) -> GenericApiResponse:
    """Sets the label (also known as class) of the sample. Use the same label for similar types of data, as they are used during training."""
    pass


@api("/api/{projectId}/raw-data/{sampleId}/move", method="post")
def moveSample(
    projectId: str, sampleId: str, requestBody: MoveRawDataRequest
) -> GenericApiResponse:
    """Move a sample to another category (e.g. from test to training)."""
    pass


@api("/api/{projectId}/raw-data/{sampleId}/crop", method="post")
def cropSample(
    projectId: str, sampleId: str, requestBody: CropSampleRequest
) -> CropSampleResponse:
    """Crop a sample to within a new range."""
    pass


@api("/api/{projectId}/raw-data/{sampleId}/split", method="post")
def splitSampleInFrames(
    projectId: str, sampleId: str, requestBody: SplitSampleInFramesRequest
) -> Union[GenericApiResponse, StartJobResponse]:
    """Split a video sample into individual frames. Depending on the length of the video sample this will either execute immediately or return the ID of a job that will perform this action."""
    pass


@api("/api/{projectId}/raw-data/{sampleId}/find-segments", method="post")
def findSegmentsInSample(
    projectId: str, sampleId: str, requestBody: FindSegmentSampleRequest
) -> FindSegmentSampleResponse:
    """Find start and end times for all non-noise events in a sample"""
    pass


@api("/api/{projectId}/raw-data/{sampleId}/segment", method="post")
def segmentSample(
    projectId: str, sampleId: str, requestBody: SegmentSampleRequest
) -> GenericApiResponse:
    """Slice a sample into multiple segments. The original file will be marked as deleted, but you can crop any created segment to retrieve the original file."""
    pass


@api("/api/{projectId}/raw-data/{sampleId}/bounding-boxes", method="post")
def setSampleBoundingBoxes(
    projectId: str, sampleId: str, requestBody: SampleBoundingBoxesRequest
) -> GenericApiResponse:
    """Set the bounding boxes for a sample"""
    pass


@api("/api/{projectId}/raw-data/{sampleId}/structured-labels", method="post")
def setSampleStructuredLabels(
    projectId: str, sampleId: str, requestBody: SetSampleStructuredLabelsRequest
) -> GenericApiResponse:
    """Set structured labels for a sample. If a sample has structured labels the `label` column is ignored, and the sample is allowed to have multiple labels. An array of { startIndex, endIndex, label } needs to be passed in with labels for the complete sample (see `valuesCount` to get the upper bound). endIndex is _inclusive_. If you pass in an incorrect array (e.g. missing values) you'll get an error back."""
    pass


@api("/api/{projectId}/raw-data/store-segment-length", method="post")
def storeSegmentLength(
    projectId: str, requestBody: StoreSegmentLengthRequest
) -> GenericApiResponse:
    """When segmenting a sample into smaller segments, store the segment length to ensure uniform segment lengths."""
    pass


@api("/api/{projectId}/raw-data/{sampleId}/retry-processing", method="post")
def retryProcessing(projectId: str, sampleId: str) -> GenericApiResponse:
    """If a sample failed processing, retry the processing operation."""
    pass


@api("/api/{projectId}/raw-data/{sampleId}/enable", method="post")
def enableSample(projectId: str, sampleId: str) -> GenericApiResponse:
    """Enable a sample, ensuring that it is not excluded from the dataset."""
    pass


@api("/api/{projectId}/raw-data/{sampleId}/disable", method="post")
def disableSample(projectId: str, sampleId: str) -> GenericApiResponse:
    """Disable a sample, ensuring that it is excluded from the dataset."""
    pass


@api("/api/{projectId}/raw-data/{sampleId}/autolabel", method="post")
def classifyUsingAutolabel(
    projectId: str, sampleId: str, requestBody: ObjectDetectionAutoLabelRequest
) -> ObjectDetectionAutoLabelResponse:
    """Classify an image using another neural network."""
    pass


@api("/api/{projectId}/raw-data/{sampleId}/metadata", method="post")
def setSampleMetadata(
    projectId: str, sampleId: str, requestBody: SetSampleMetadataRequest
) -> GenericApiResponse:
    """Adds or updates the metadata associated to a sample."""
    pass


@api("/api/{projectId}/raw-data/{sampleId}/to-labeling-queue", method="post")
def moveToLabelingQueue(projectId: str, sampleId: str) -> GenericApiResponse:
    """Clears the bounding box labels and moves item back to labeling queue"""
    pass


@api("/api/{projectId}/raw-data/{sampleId}/propose-changes", method="post")
def setSampleProposedChanges(
    projectId: str, sampleId: str, requestBody: SetSampleProposedChangesRequest
) -> GenericApiResponse:
    """Queue up changes to an object as part of the AI Actions flow. This overwrites any previous proposed changes."""
    pass


@api("/api/{projectId}/raw-data/batch/edit-labels", method="post")
def batchEditLabels(
    projectId: str,
    category: str,
    requestBody: EditSampleLabelRequest,
    labels: str = None,
    filename: str = None,
    maxLength: str = None,
    minLength: str = None,
    minFrequency: str = None,
    maxFrequency: str = None,
    signatureValidity: str = None,
    includeDisabled: str = None,
    ids: str = None,
    excludeIds: str = None,
    minLabel: str = None,
    maxLabel: str = None,
    search: str = None,
) -> Union[GenericApiResponse, StartJobResponse]:
    """Sets the label (also known as class) of multiple samples. Depending on the number of affected samples this will either execute immediately or return the ID of a job that will perform this action in batches."""
    pass


@api("/api/{projectId}/raw-data/batch/delete", method="post")
def batchDelete(
    projectId: str,
    category: str,
    labels: str = None,
    filename: str = None,
    maxLength: str = None,
    minLength: str = None,
    minFrequency: str = None,
    maxFrequency: str = None,
    signatureValidity: str = None,
    includeDisabled: str = None,
    ids: str = None,
    excludeIds: str = None,
    minLabel: str = None,
    maxLabel: str = None,
    search: str = None,
) -> Union[GenericApiResponse, StartJobResponse]:
    """Deletes samples. Note that this does not delete the data from cold storage. Depending on the number of affected samples this will either execute immediately or return the ID of a job that will perform this action in batches."""
    pass


@api("/api/{projectId}/raw-data/batch/moveSamples", method="post")
def batchMove(
    projectId: str,
    category: str,
    requestBody: MoveRawDataRequest,
    labels: str = None,
    filename: str = None,
    maxLength: str = None,
    minLength: str = None,
    minFrequency: str = None,
    maxFrequency: str = None,
    signatureValidity: str = None,
    includeDisabled: str = None,
    ids: str = None,
    excludeIds: str = None,
    minLabel: str = None,
    maxLabel: str = None,
    search: str = None,
) -> Union[GenericApiResponse, StartJobResponse]:
    """Move multiple samples to another category (e.g. from test to training). Depending on the number of affected samples this will either execute immediately or return the ID of a job that will perform this action in batches."""
    pass


@api("/api/{projectId}/raw-data/batch/enable-samples", method="post")
def batchEnable(
    projectId: str,
    category: str,
    labels: str = None,
    filename: str = None,
    maxLength: str = None,
    minLength: str = None,
    minFrequency: str = None,
    maxFrequency: str = None,
    signatureValidity: str = None,
    includeDisabled: str = None,
    ids: str = None,
    excludeIds: str = None,
    minLabel: str = None,
    maxLabel: str = None,
    search: str = None,
) -> Union[GenericApiResponse, StartJobResponse]:
    """Enables samples, ensuring that they are not excluded from the dataset. Depending on the number of affected samples this will either execute immediately or return the ID of a job that will perform this action in batches."""
    pass


@api("/api/{projectId}/raw-data/batch/disable-samples", method="post")
def batchDisable(
    projectId: str,
    category: str,
    labels: str = None,
    filename: str = None,
    maxLength: str = None,
    minLength: str = None,
    minFrequency: str = None,
    maxFrequency: str = None,
    signatureValidity: str = None,
    includeDisabled: str = None,
    ids: str = None,
    excludeIds: str = None,
    minLabel: str = None,
    maxLabel: str = None,
    search: str = None,
) -> Union[GenericApiResponse, StartJobResponse]:
    """Disables samples, ensuring that they are excluded from the dataset. Depending on the number of affected samples this will either execute immediately or return the ID of a job that will perform this action in batches."""
    pass


@api("/api/{projectId}/raw-data/batch/add-metadata", method="post")
def batchAddMetadata(
    projectId: str,
    category: str,
    requestBody: BatchAddMetadataRequest,
    labels: str = None,
    filename: str = None,
    maxLength: str = None,
    minLength: str = None,
    minFrequency: str = None,
    maxFrequency: str = None,
    signatureValidity: str = None,
    includeDisabled: str = None,
    ids: str = None,
    excludeIds: str = None,
    minLabel: str = None,
    maxLabel: str = None,
    search: str = None,
) -> Union[GenericApiResponse, StartJobResponse]:
    """Add specific metadata for multiple samples."""
    pass


@api("/api/{projectId}/raw-data/batch/clear-metadata-by-key", method="post")
def batchClearMetadataByKey(
    projectId: str,
    category: str,
    requestBody: BatchClearMetadataByKeyRequest,
    labels: str = None,
    filename: str = None,
    maxLength: str = None,
    minLength: str = None,
    minFrequency: str = None,
    maxFrequency: str = None,
    signatureValidity: str = None,
    includeDisabled: str = None,
    ids: str = None,
    excludeIds: str = None,
    minLabel: str = None,
    maxLabel: str = None,
    search: str = None,
) -> Union[GenericApiResponse, StartJobResponse]:
    """Clears a specific metadata field (by key) for multiple samples."""
    pass


@api("/api/{projectId}/raw-data/batch/clear-metadata", method="post")
def batchClearMetadata(
    projectId: str,
    category: str,
    labels: str = None,
    filename: str = None,
    maxLength: str = None,
    minLength: str = None,
    minFrequency: str = None,
    maxFrequency: str = None,
    signatureValidity: str = None,
    includeDisabled: str = None,
    ids: str = None,
    excludeIds: str = None,
    minLabel: str = None,
    maxLabel: str = None,
    search: str = None,
) -> GenericApiResponse:
    """Clears all metadata for multiple samples."""
    pass


@api("/api/{projectId}/raw-data/track-objects", method="post")
def trackObjects(
    projectId: str, requestBody: TrackObjectsRequest
) -> TrackObjectsResponse:
    """Track objects between two samples. Source sample should have bounding boxes set."""
    pass


@api("/api/{projectId}/raw-data/data-explorer/clear", method="post")
def clearDataExplorer(projectId: str) -> GenericApiResponse:
    """Remove the current data explorer state"""
    pass


@api("/api/{projectId}/raw-data/data-explorer/settings", method="post")
def setDataExplorerSettings(
    projectId: str, requestBody: DataExplorerSettings
) -> GenericApiResponse:
    """Set data explorer configuration, like the type of data, and the input / dsp block to use."""
    pass


@api("/api/{projectId}/raw-data/data-explorer/screenshot", method="post")
def uploadDataExplorerScreenshot(
    projectId: str, requestBody: UploadImageRequest
) -> GenericApiResponse:
    """Used internally (from a data pipeline) to upload a picture of the data explorer"""
    pass


@api("/api/{projectId}/raw-data/{sampleId}", method="delete")
def deleteSample(projectId: str, sampleId: str) -> GenericApiResponse:
    """Deletes the sample. Note that this does not delete the data from cold storage."""
    pass


@api("/api/{projectId}/impulse", method="get")
def getImpulse(projectId: str, impulseId: str = None) -> GetImpulseResponse:
    """Retrieve the impulse for this project. If you specify `impulseId` then that impulse is returned, otherwise the default impulse is returned."""
    pass


@api("/api/{projectId}/impulse/all", method="get")
def getImpulseAll(projectId: str, impulseId: str = None) -> GetImpulseResponse:
    """Retrieve the impulse for this project including disabled blocks. If you specify `impulseId` then that impulse is returned, otherwise the default impulse is returned."""
    pass


@api("/api/{projectId}/impulse/blocks", method="get")
def getImpulseBlocks(projectId: str) -> GetImpulseBlocksResponse:
    """Lists all possible blocks that can be used in the impulse"""
    pass


@api("/api/{projectId}/impulses", method="get")
def getAllImpulses(projectId: str) -> GetAllImpulsesResponse:
    """Retrieve all impulse for a project"""
    pass


@api("/api/{projectId}/impulses-detailed", method="get")
def getAllDetailedImpulses(projectId: str) -> GetAllDetailedImpulsesResponse:
    """Retrieve all impulse for a project, including accuracy and performance metrics."""
    pass


@api("/api/{projectId}/download-impulses-detailed", method="get")
def downloadDetailedImpulses(projectId: str, format: str = None) -> File:
    """Download all impulse for a project, including accuracy and performance metrics, as JSON or CSV."""
    pass


@api("/api/{projectId}/impulse", method="post")
def createImpulse(
    projectId: str, requestBody: CreateImpulseRequest, impulseId: str = None
) -> CreateImpulseResponse:
    """Sets the impulse for this project.  If you specify `impulseId` then that impulse is created/updated, otherwise the default impulse is created/updated."""
    pass


@api("/api/{projectId}/impulse/new", method="post")
def createNewEmptyImpulse(projectId: str) -> CreateNewEmptyImpulseResponse:
    """Create a new empty impulse, and return the ID."""
    pass


@api("/api/{projectId}/impulse/update", method="post")
def updateImpulse(
    projectId: str, requestBody: UpdateImpulseRequest, impulseId: str = None
) -> GenericApiResponse:
    """Update the impulse for this project.  If you specify `impulseId` then that impulse is created/updated, otherwise the default impulse is created/updated."""
    pass


@api("/api/{projectId}/impulse/get-new-block-id", method="post")
def getNewBlockId(projectId: str) -> GetNewBlockIdResponse:
    """Returns an unused block ID. Use this function to determine new block IDs when you construct an impulse; so you won't accidentally re-use block IDs."""
    pass


@api("/api/{projectId}/verify-dsp-block/url", method="post")
def verifyDspBlockUrl(
    projectId: str, requestBody: VerifyDspBlockUrlRequest
) -> VerifyDspBlockUrlResponse:
    """Verify the validity of a custom DSP block"""
    pass


@api("/api/{projectId}/impulse/legacy-set-impulse", method="post")
def setLegacyImpulseStateInternal(
    projectId: str, requestBody: SetLegacyImpulseStateInternalRequest
) -> GenericApiResponse:
    """Set the complete impulse state for a project, writing impulses in the old (pre-impulse experiments) format. This completely clears out all files on FSx for this project. This is an internal API."""
    pass


@api("/api/{projectId}/impulse/{impulseId}/clone/structure", method="post")
def cloneImpulseStructure(
    projectId: str, impulseId: str, requestBody: CloneImpulseRequest
) -> CreateImpulseResponse:
    """Clones the complete structure (incl. config) of an impulse. Does not copy data."""
    pass


@api("/api/{projectId}/impulse/{impulseId}/clone/complete", method="post")
def cloneImpulseComplete(
    projectId: str, impulseId: str, requestBody: CloneImpulseRequest
) -> StartJobResponse:
    """Clones the complete impulse (incl. config and data) of an existing impulse."""
    pass


@api("/api/{projectId}/impulse", method="delete")
def deleteImpulse(projectId: str, impulseId: str = None) -> GenericApiResponse:
    """Clears the impulse and all associated blocks for this project.  If you specify `impulseId` then that impulse is cleared, otherwise the default impulse is cleared."""
    pass


@api("/api/{projectId}/dsp/{dspId}", method="get")
def getDspConfig(projectId: str, dspId: str) -> DSPConfigResponse:
    """Retrieve the configuration parameters for the DSP block. Use the impulse functions to retrieve all DSP blocks."""
    pass


@api("/api/{projectId}/dsp/{dspId}/metadata", method="get")
def getDspMetadata(
    projectId: str, dspId: str, excludeIncludedSamples: str = None
) -> DSPMetadataResponse:
    """Retrieve the metadata from a generated DSP block."""
    pass


@api("/api/{projectId}/dsp/{dspId}/raw-data/{sampleId}", method="get")
def getDspRawSample(
    projectId: str, dspId: str, sampleId: str, limitPayloadValues: str = None
) -> GetSampleResponse:
    """Get raw sample data, but with only the axes selected by the DSP block. E.g. if you have selected only accX and accY as inputs for the DSP block, but the raw sample also contains accZ, accZ is filtered out. If you pass dspId = 0 this will return a raw graph without any processing."""
    pass


@api("/api/{projectId}/dsp/{dspId}/raw-data/{sampleId}/slice", method="get")
def getDspSampleSlice(
    projectId: str, dspId: str, sampleId: str, sliceStart: str, sliceEnd: str = None
) -> GetSampleResponse:
    """Get slice of raw sample data, but with only the axes selected by the DSP block. E.g. if you have selected only accX and accY as inputs for the DSP block, but the raw sample also contains accZ, accZ is filtered out."""
    pass


@api(
    "/api/{projectId}/dsp/{dspId}/raw-data/{sampleId}/slice/run/readonly", method="get"
)
def runDspSampleSliceReadOnly(
    projectId: str, dspId: str, sampleId: str, sliceStart: str, sliceEnd: str = None
) -> DspRunResponseWithSample:
    """Get slice of sample data, and run it through the DSP block. This only the axes selected by the DSP block. E.g. if you have selected only accX and accY as inputs for the DSP block, but the raw sample also contains accZ, accZ is filtered out."""
    pass


@api("/api/{projectId}/dsp/{dspId}/features/labels", method="get")
def getDspFeatureLabels(projectId: str, dspId: str) -> DspFeatureLabelsResponse:
    """Retrieve the names of the features the DSP block generates"""
    pass


@api("/api/{projectId}/dsp/{dspId}/features/get-graph/{category}", method="get")
def dspSampleTrainedFeatures(
    projectId: str,
    dspId: str,
    featureAx1: str,
    featureAx2: str,
    featureAx3: str,
    category: str,
) -> DspTrainedFeaturesResponse:
    """Get a sample of trained features, this extracts a number of samples and their labels. Used to visualize the current training set."""
    pass


@api(
    "/api/{projectId}/dsp/{dspId}/features/get-graph/classification/{sampleId}",
    method="get",
)
def dspGetFeaturesForSample(
    projectId: str, dspId: str, sampleId: str
) -> DspSampleFeaturesResponse:
    """Runs the DSP block against a sample. This will move the sliding window (dependent on the sliding window length and the sliding window increase parameters in the impulse) over the complete file, and run the DSP function for every window that is extracted."""
    pass


@api("/api/{projectId}/dsp/{dspId}/features/importance", method="get")
def getDspFeatureImportance(projectId: str, dspId: str) -> DspFeatureImportanceResponse:
    """Retrieve the feature importance for a DSP block (only available for blocks where dimensionalityReduction is not enabled)"""
    pass


@api("/api/{projectId}/dsp-data/{dspId}/x/{category}", method="get")
def downloadDspData(projectId: str, dspId: str, category: str, raw: str = None) -> File:
    """Download output from a DSP block over all data in the training set, already sliced in windows. In Numpy binary format."""
    pass


@api("/api/{projectId}/dsp-data/{dspId}/y/{category}", method="get")
def downloadDspLabels(projectId: str, dspId: str, category: str) -> File:
    """Download labels for a DSP block over all data in the training set, already sliced in windows."""
    pass


@api("/api/{projectId}/dsp/{dspId}/get-autotuner-results", method="get")
def getAutotunerResults(projectId: str, dspId: str) -> DspAutotunerResults:
    """Get a set of parameters, found as a result of running the DSP autotuner."""
    pass


@api("/api/{projectId}/dsp-data/{dspId}/artifact/{key}", method="get")
def downloadDspArtifact(projectId: str, dspId: str, key: str) -> File:
    """Download an artifact from a DSP block for debugging. This is an internal API."""
    pass


@api("/api/{projectId}/dsp/{dspId}/performance", method="get")
def getPerformanceAllVariants(
    projectId: str, dspId: str
) -> DspPerformanceAllVariantsResponse:
    """Get estimated performance (latency and RAM) for the DSP block, for all supported project latency devices."""
    pass


@api("/api/{projectId}/dsp/{dspId}", method="post")
def setDspConfig(
    projectId: str, dspId: str, requestBody: DSPConfigRequest
) -> GenericApiResponse:
    """Set configuration parameters for the DSP block. Only values set in the body will be overwritten."""
    pass


@api("/api/{projectId}/dsp/{dspId}/clear", method="post")
def clearDspBlock(projectId: str, dspId: str) -> GenericApiResponse:
    """Clear generated features for a DSP block (used in tests)."""
    pass


@api("/api/{projectId}/dsp/{dspId}/raw-data/{sampleId}/slice/run", method="post")
def runDspSampleSlice(
    projectId: str,
    dspId: str,
    sampleId: str,
    sliceStart: str,
    requestBody: DspRunRequestWithoutFeatures,
    sliceEnd: str = None,
) -> DspRunResponseWithSample:
    """Get slice of sample data, and run it through the DSP block. This only the axes selected by the DSP block. E.g. if you have selected only accX and accY as inputs for the DSP block, but the raw sample also contains accZ, accZ is filtered out."""
    pass


@api("/api/{projectId}/dsp/{dspId}/profile", method="post")
def startProfileCustomDspBlock(
    projectId: str, dspId: str, requestBody: DspRunRequestWithoutFeaturesReadOnly
) -> StartJobResponse:
    """Returns performance characteristics for a custom DSP block (needs `hasTfliteImplementation`). Updates are streamed over the websocket API (or can be retrieved through the /stdout endpoint). Use getProfileTfliteJobResult to get the results when the job is completed."""
    pass


@api("/api/{projectId}/dsp/{dspId}/run", method="post")
def runDspOnFeaturesArray(
    projectId: str, dspId: str, requestBody: DspRunRequestWithFeatures
) -> DspRunResponse:
    """Takes in a features array and runs it through the DSP block. This data should have the same frequency as set in the input block in your impulse."""
    pass


@api("/api/{projectId}/training/{learnId}/x", method="get")
def getLearnXData(projectId: str, learnId: str) -> File:
    """Download the processed data for this learning block. This is data already processed by the signal processing blocks."""
    pass


@api("/api/{projectId}/training/{learnId}/y", method="get")
def getLearnYData(projectId: str, learnId: str) -> File:
    """Download the labels for this learning block. This is data already processed by the signal processing blocks. Not all blocks support this function. If so, a GenericApiResponse is returned with an error message."""
    pass


@api("/api/{projectId}/training/anomaly/{learnId}", method="get")
def getAnomaly(projectId: str, learnId: str) -> AnomalyConfigResponse:
    """Get information about an anomaly block, such as its dependencies. Use the impulse blocks to find the learnId."""
    pass


@api("/api/{projectId}/training/anomaly/{learnId}/metadata", method="get")
def getAnomalyMetadata(projectId: str, learnId: str) -> AnomalyModelMetadataResponse:
    """Get metadata about a trained anomaly block. Use the impulse blocks to find the learnId."""
    pass


@api("/api/{projectId}/training/anomaly/{learnId}/gmm/metadata", method="get")
def getGmmMetadata(projectId: str, learnId: str) -> AnomalyGmmMetadataResponse:
    """Get raw model metadata of the Gaussian mixture model (GMM) for a trained anomaly block. Use the impulse blocks to find the learnId."""
    pass


@api("/api/{projectId}/training/keras/{learnId}", method="get")
def getKeras(projectId: str, learnId: str) -> KerasResponse:
    """Get information about a Keras block, such as its dependencies. Use the impulse blocks to find the learnId."""
    pass


@api("/api/{projectId}/training/keras/{learnId}/metadata", method="get")
def getKerasMetadata(
    projectId: str, learnId: str, excludeLabels: str = None
) -> KerasModelMetadataResponse:
    """Get metadata about a trained Keras block. Use the impulse blocks to find the learnId."""
    pass


@api("/api/{projectId}/training/keras/{learnId}/data-explorer/features", method="get")
def getKerasDataExplorerFeatures(
    projectId: str, learnId: str
) -> GetDataExplorerFeaturesResponse:
    """t-SNE2 output of the raw dataset using embeddings from this Keras block"""
    pass


@api("/api/{projectId}/training/keras/{learnId}/download-export", method="get")
def downloadKerasExport(projectId: str, learnId: str) -> File:
    """Download an exported Keras block - needs to be exported via 'exportKerasBlock' first"""
    pass


@api("/api/{projectId}/training/keras/{learnId}/download-data", method="get")
def downloadKerasData(projectId: str, learnId: str) -> File:
    """Download the data of an exported Keras block - needs to be exported via 'exportKerasBlockData' first"""
    pass


@api("/api/{projectId}/learn-data/{learnId}/model/{modelDownloadId}", method="get")
def downloadLearnModel(projectId: str, learnId: str, modelDownloadId: str) -> File:
    """Download a trained model for a learning block. Depending on the block this can be a TensorFlow model, or the cluster centroids."""
    pass


@api("/api/{projectId}/training/anomaly/{learnId}/features/get-graph", method="get")
def anomalyTrainedFeatures(
    projectId: str, learnId: str, featureAx1: str, featureAx2: str
) -> AnomalyTrainedFeaturesResponse:
    """Get a sample of trained features, this extracts a number of samples and their features."""
    pass


@api(
    "/api/{projectId}/training/anomaly/{learnId}/features/get-graph/classification/{sampleId}",
    method="get",
)
def anomalyTrainedFeaturesPerSample(
    projectId: str, learnId: str, sampleId: str
) -> AnomalyTrainedFeaturesResponse:
    """Get trained features for a single sample. This runs both the DSP prerequisites and the anomaly classifier."""
    pass


@api("/api/{projectId}/pretrained-model", method="get")
def getPretrainedModelInfo(
    projectId: str, impulseId: str = None
) -> GetPretrainedModelResponse:
    """Receive info back about the earlier uploaded pretrained model (via `uploadPretrainedModel`) input/output tensors. If you want to deploy a pretrained model from the API, see `startDeployPretrainedModelJob`."""
    pass


@api(
    "/api/{projectId}/pretrained-model/download/{pretrainedModelDownloadType}",
    method="get",
)
def downloadPretrainedModel(
    projectId: str, pretrainedModelDownloadType: str, impulseId: str = None
) -> File:
    """Download a pretrained model file"""
    pass


@api("/api/{projectId}/training/anomaly/{learnId}", method="post")
def setAnomaly(
    projectId: str, learnId: str, requestBody: SetAnomalyParameterRequest
) -> GenericApiResponse:
    """Configure the anomaly block, such as its minimum confidence score. Use the impulse blocks to find the learnId."""
    pass


@api("/api/{projectId}/training/keras/{learnId}", method="post")
def setKeras(
    projectId: str, learnId: str, requestBody: SetKerasParameterRequest
) -> GenericApiResponse:
    """Configure the Keras block, such as its minimum confidence score. Use the impulse blocks to find the learnId."""
    pass


@api("/api/{projectId}/training/keras/{learnId}/files", method="post")
def uploadKerasFiles(
    projectId: str, learnId: str, requestBody: UploadKerasFilesRequest
) -> GenericApiResponse:
    """Replace Keras block files with the contents of a zip. This is an internal API."""
    pass


@api("/api/{projectId}/training/keras/{learnId}/addFiles", method="post")
def addKerasFiles(
    projectId: str, learnId: str, requestBody: AddKerasFilesRequest
) -> GenericApiResponse:
    """Add Keras block files with the contents of a zip. This is an internal API."""
    pass


@api("/api/{projectId}/pretrained-model/upload", method="post")
def uploadPretrainedModel(
    projectId: str, requestBody: UploadPretrainedModelRequest, impulseId: str = None
) -> StartJobResponse:
    """Upload a pretrained model and receive info back about the input/output tensors. If you want to deploy a pretrained model from the API, see `startDeployPretrainedModelJob`."""
    pass


@api("/api/{projectId}/pretrained-model/save", method="post")
def savePretrainedModelParameters(
    projectId: str, requestBody: SavePretrainedModelRequest, impulseId: str = None
) -> GenericApiResponse:
    """Save input / model configuration for a pretrained model. This overrides the current impulse. If you want to deploy a pretrained model from the API, see `startDeployPretrainedModelJob`."""
    pass


@api("/api/{projectId}/pretrained-model/test", method="post")
def testPretrainedModel(
    projectId: str, requestBody: TestPretrainedModelRequest, impulseId: str = None
) -> TestPretrainedModelResponse:
    """Test out a pretrained model (using raw features) - upload first via  `uploadPretrainedModel`. If you want to deploy a pretrained model from the API, see `startDeployPretrainedModelJob`."""
    pass


@api("/api/{projectId}/pretrained-model/profile", method="post")
def profilePretrainedModel(projectId: str, impulseId: str = None) -> StartJobResponse:
    """Returns the latency, RAM and ROM used for the pretrained model - upload first via  `uploadPretrainedModel`. This is using the project's selected latency device. Updates are streamed over the websocket API (or can be retrieved through the /stdout endpoint). Use getProfileTfliteJobResult to get the results when the job is completed."""
    pass


@api("/api/{projectId}/classify/{sampleId}", method="get")
def classifySample(
    projectId: str, sampleId: str, includeDebugInfo: str = None, impulseId: str = None
) -> ClassifySampleResponse:
    """This API is deprecated, use classifySampleV2 instead (`/v1/api/{projectId}/classify/v2/{sampleId}`). Classify a complete file against the current impulse. This will move the sliding window (dependent on the sliding window length and the sliding window increase parameters in the impulse) over the complete file, and classify for every window that is extracted."""
    pass


@api("/api/{projectId}/classify/v2/{sampleId}/raw-data/{windowIndex}", method="get")
def getSampleWindowFromCache(
    projectId: str, sampleId: str, windowIndex: str, impulseId: str = None
) -> GetSampleResponse:
    """Get raw sample features for a particular window. This is only available after a live classification job has completed and raw features have been cached."""
    pass


@api("/api/{projectId}/classify/all/result", method="get")
def getClassifyJobResult(
    projectId: str,
    featureExplorerOnly: str = None,
    variant: str = None,
    impulseId: str = None,
) -> ClassifyJobResponse:
    """Get classify job result, containing the result for the complete testing dataset."""
    pass


@api("/api/{projectId}/classify/all/result/page", method="get")
def getClassifyJobResultPage(
    projectId: str,
    limit: str = None,
    offset: str = None,
    variant: str = None,
    impulseId: str = None,
) -> ClassifyJobResponsePage:
    """Get classify job result, containing the predictions for a given page."""
    pass


@api("/api/{projectId}/classify/all/metrics", method="get")
def getClassifyMetricsAllVariants(
    projectId: str, impulseId: str = None
) -> MetricsAllVariantsResponse:
    """Get metrics, calculated during a classify all job, for all available model variants. This is experimental and may change in the future."""
    pass


@api("/api/{projectId}/classify/anomaly-gmm/{blockId}/{sampleId}", method="get")
def classifySampleByLearnBlock(
    projectId: str, sampleId: str, blockId: str
) -> ClassifySampleResponse:
    """This API is deprecated, use classifySampleByLearnBlockV2 (`/v1/api/{projectId}/classify/anomaly-gmm/v2/{blockId}/{sampleId}`) instead. Classify a complete file against the specified learn block. This will move the sliding window (dependent on the sliding window length and the sliding window increase parameters in the impulse) over the complete file, and classify for every window that is extracted."""
    pass


@api("/api/{projectId}/classify/v2/{sampleId}", method="post")
def classifySampleV2(
    projectId: str,
    sampleId: str,
    includeDebugInfo: str = None,
    variant: str = None,
    impulseId: str = None,
) -> Union[ClassifySampleResponse, StartJobResponse]:
    """Classify a complete file against the current impulse. This will move the sliding window (dependent on the sliding window length and the sliding window increase parameters in the impulse) over the complete file, and classify for every window that is extracted. Depending on the size of your file, whether your sample is resampled, and whether the result is cached you'll get either the result or a job back. If you receive a job, then wait for the completion of the job, and then call this function again to receive the results. The unoptimized (float32) model is used by default, and classification with an optimized (int8) model can be slower."""
    pass


@api("/api/{projectId}/classify/v2/{sampleId}/variants", method="post")
def classifySampleForVariants(
    projectId: str,
    sampleId: str,
    variants: str,
    includeDebugInfo: str = None,
    impulseId: str = None,
) -> Union[ClassifySampleResponseMultipleVariants, StartJobResponse]:
    """Classify a complete file against the current impulse, for all given variants. Depending on the size of your file and whether the sample is resampled, you may get a job ID in the response."""
    pass


@api("/api/{projectId}/classify/anomaly-gmm/v2/{blockId}/{sampleId}", method="post")
def classifySampleByLearnBlockV2(
    projectId: str, sampleId: str, blockId: str, variant: str = None
) -> Union[ClassifySampleResponse, StartJobResponse]:
    """Classify a complete file against the specified learn block. This will move the sliding window (dependent on the sliding window length and the sliding window increase parameters in the impulse) over the complete file, and classify for every window that is extracted. Depending on the size of your file, whether your sample is resampled, and whether the result is cached you'll get either the result or a job back. If you receive a job, then wait for the completion of the job, and then call this function again to receive the results. The unoptimized (float32) model is used by default, and classification with an optimized (int8) model can be slower."""
    pass


@api("/api/{projectId}/classify/image", method="post")
def classifyImage(
    projectId: str, requestBody: UploadImageRequest, impulseId: str = None
) -> TestPretrainedModelResponse:
    """Test out a trained impulse (using a posted image)."""
    pass


@api("/api/{projectId}/performance-calibration/status", method="get")
def getPerformanceCalibrationStatus(
    projectId: str, impulseId: str = None
) -> GetPerformanceCalibrationStatusResponse:
    """Get performance calibration status"""
    pass


@api("/api/{projectId}/performance-calibration/ground-truth", method="get")
def getPerformanceCalibrationGroundTruth(
    projectId: str, impulseId: str = None
) -> GetPerformanceCalibrationGroundTruthResponse:
    """Get performance calibration ground truth data"""
    pass


@api("/api/{projectId}/performance-calibration/raw-result", method="get")
def getPerformanceCalibrationRawResult(
    projectId: str, impulseId: str = None
) -> GetPerformanceCalibrationRawResultResponse:
    """Get performance calibration raw result"""
    pass


@api("/api/{projectId}/performance-calibration/parameter-sets", method="get")
def getPerformanceCalibrationParameterSets(
    projectId: str, impulseId: str = None
) -> GetPerformanceCalibrationParameterSetsResponse:
    """Get performance calibration parameter sets"""
    pass


@api("/api/{projectId}/performance-calibration/parameters", method="get")
def getPerformanceCalibrationSavedParameters(
    projectId: str, impulseId: str = None
) -> GetPerformanceCalibrationParametersResponse:
    """Get performance calibration stored parameters"""
    pass


@api("/api/{projectId}/performance-calibration/wav", method="get")
def getWavFile(projectId: str, impulseId: str = None) -> File:
    """Get the synthetic sample as a WAV file"""
    pass


@api("/api/{projectId}/post-processing/results", method="get")
def getPostProcessingResults(
    projectId: str, impulseId: str = None
) -> GetPostProcessingResultsResponse:
    """Get results of most recent post processing run"""
    pass


@api("/api/{projectId}/performance-calibration/parameters", method="post")
def setPerformanceCalibrationSavedParameters(
    projectId: str,
    requestBody: PerformanceCalibrationSaveParameterSetRequest,
    impulseId: str = None,
) -> GenericApiResponse:
    """Set the current performance calibration parameters"""
    pass


@api("/api/{projectId}/performance-calibration/files", method="post")
def uploadLabeledAudio(
    projectId: str,
    requestBody: PerformanceCalibrationUploadLabeledAudioRequest,
    impulseId: str = None,
) -> PerformanceCalibrationUploadLabeledAudioResponse:
    """Upload a zip files with a wav file and its Label metadata to run performance calibration on it."""
    pass


@api("/api/{projectId}/performance-calibration/clear", method="post")
def clearPerformanceCalibrationState(
    projectId: str, impulseId: str = None
) -> GenericApiResponse:
    """Deletes all state related to performance calibration (used in tests for example)."""
    pass


@api("/api/{projectId}/performance-calibration/parameters", method="delete")
def deletePerformanceCalibrationSavedParameters(
    projectId: str, impulseId: str = None
) -> GenericApiResponse:
    """Clears the current performance calibration parameters"""
    pass


@api("/api/{projectId}/jobs/post-processing", method="post")
def startPostProcessingJob(
    projectId: str, requestBody: StartPostProcessingRequest, impulseId: str = None
) -> StartJobResponse:
    """Begins post processing job"""
    pass


@api("/api/{projectId}/jobs/data-explorer-features", method="post")
def generateDataExplorerFeatures(projectId: str) -> StartJobResponse:
    """Generate features for the data explorer"""
    pass


@api("/api/{projectId}/jobs/data-quality-metrics", method="post")
def calculateDataQualityMetrics(
    projectId: str, requestBody: CalculateDataQualityMetricsRequest
) -> StartJobResponse:
    """Calculate data quality metrics for the dataset"""
    pass


@api("/api/{projectId}/jobs/retry-migrate-impulse", method="post")
def retryImpulseMigration(projectId: str) -> StartJobResponse:
    """If an impulse migration previously failed, use this function to retry the job."""
    pass


@api("/api/{projectId}/jobs/synthetic-data", method="post")
def createSyntheticDataJob(
    projectId: str, requestBody: CreateSyntheticDataRequest
) -> StartJobResponse:
    """Generate new synthetic data"""
    pass


@api("/api/{projectId}/jobs/ai-actions/{actionId}/preview", method="post")
def createPreviewAIActionsJob(
    projectId: str, actionId: str, requestBody: CreatePreviewAIActionsJobRequest
) -> StartJobResponse:
    """Do a dry-run of an AI Actions job over a subset of data. This will instruct the block to propose changes to data items (via "setSampleProposedChanges") rather than apply the changes directly."""
    pass


@api("/api/{projectId}/jobs/ai-actions/{actionId}", method="post")
def createAIActionsJob(projectId: str, actionId: str) -> StartJobResponse:
    """Run an AI Actions job over a subset of data. This will instruct the block to apply the changes directly to your dataset. To preview, use "createPreviewAIActionsJob". To set the config use `updateAIAction`."""
    pass


@api("/api/{projectId}/jobs/optimize", method="post")
def optimizeJob(projectId: str, continuationJobId: str = None) -> StartJobResponse:
    """Evaluates optimal model architecture"""
    pass


@api("/api/{projectId}/jobs/set-tuner-primary-job", method="post")
def setTunerPrimaryJob(
    projectId: str, trialId: str, requestBody: SetTunerPrimaryJobRequest
) -> StartJobResponse:
    """Sets EON tuner primary model"""
    pass


@api("/api/{projectId}/jobs/{jobId}/update", method="post")
def updateJob(
    projectId: str, jobId: str, requestBody: UpdateJobRequest
) -> GenericApiResponse:
    """Update a job."""
    pass


@api("/api/{projectId}/jobs/{jobId}/cancel", method="post")
def cancelJob(
    projectId: str, jobId: str, forceCancel: str = None
) -> GenericApiResponse:
    """Cancel a running job."""
    pass


@api("/api/{projectId}/jobs/generate-features", method="post")
def generateFeaturesJob(
    projectId: str, requestBody: GenerateFeaturesRequest
) -> StartJobResponse:
    """Take the raw training set and generate features from them. Updates are streamed over the websocket API."""
    pass


@api("/api/{projectId}/jobs/autotune-dsp", method="post")
def autotuneDspJob(projectId: str, requestBody: AutotuneDspRequest) -> StartJobResponse:
    """Autotune DSP block parameters. Updates are streamed over the websocket API."""
    pass


@api("/api/{projectId}/jobs/train/keras/{learnId}", method="post")
def trainKerasJob(
    projectId: str, learnId: str, requestBody: SetKerasParameterRequest
) -> StartJobResponse:
    """Take the output from a DSP block and train a neural network using Keras. Updates are streamed over the websocket API."""
    pass


@api("/api/{projectId}/jobs/train/anomaly/{learnId}", method="post")
def trainAnomalyJob(
    projectId: str, learnId: str, requestBody: StartTrainingRequestAnomaly
) -> StartJobResponse:
    """Take the output from a DSP block and train an anomaly detection model using K-means or GMM. Updates are streamed over the websocket API."""
    pass


@api("/api/{projectId}/jobs/train/keras/{learnId}/export", method="post")
def exportKerasBlock(projectId: str, learnId: str) -> StartJobResponse:
    """Export the training pipeline of a Keras block. Updates are streamed over the websocket API."""
    pass


@api("/api/{projectId}/jobs/train/keras/{learnId}/data", method="post")
def exportKerasBlockData(
    projectId: str, learnId: str, requestBody: ExportKerasBlockDataRequest
) -> StartJobResponse:
    """Export the data of a Keras block (already split in train/validate data). Updates are streamed over the websocket API."""
    pass


@api("/api/{projectId}/jobs/build-ondevice-model", method="post")
def buildOnDeviceModelJob(
    projectId: str,
    type: str,
    requestBody: BuildOnDeviceModelRequest,
    impulseId: str = None,
) -> StartJobResponse:
    """Generate code to run the impulse on an embedded device. When this step is complete use `downloadBuild` to download the artefacts.  Updates are streamed over the websocket API."""
    pass


@api("/api/{projectId}/jobs/build-ondevice-model/organization", method="post")
def buildOrganizationOnDeviceModelJob(
    projectId: str,
    requestBody: BuildOrganizationOnDeviceModelRequest,
    impulseId: str = None,
) -> StartJobResponse:
    """Generate code to run the impulse on an embedded device using an organizational deployment block. When this step is complete use `downloadBuild` to download the artefacts.  Updates are streamed over the websocket API."""
    pass


@api("/api/{projectId}/jobs/export/original", method="post")
def startOriginalExportJob(
    projectId: str, requestBody: ExportOriginalDataRequest
) -> StartJobResponse:
    """Export all the data in the project as it was uploaded to Edge Impulse.  Updates are streamed over the websocket API."""
    pass


@api("/api/{projectId}/jobs/export/wav", method="post")
def startWavExportJob(
    projectId: str, requestBody: ExportWavDataRequest
) -> StartJobResponse:
    """Export all the data in the project in WAV format.  Updates are streamed over the websocket API."""
    pass


@api("/api/{projectId}/jobs/retrain", method="post")
def startRetrainJob(projectId: str, impulseId: str = None) -> StartJobResponse:
    """Retrains the current impulse with the last known parameters. Updates are streamed over the websocket API."""
    pass


@api("/api/{projectId}/jobs/classify", method="post")
def startClassifyJob(
    projectId: str, requestBody: StartClassifyJobRequest, impulseId: str = None
) -> StartJobResponse:
    """Classifies all items in the testing dataset against the current impulse. Updates are streamed over the websocket API."""
    pass


@api("/api/{projectId}/jobs/performance-calibration", method="post")
def startPerformanceCalibrationJob(
    projectId: str,
    requestBody: StartPerformanceCalibrationRequest,
    impulseId: str = None,
) -> StartJobResponse:
    """Simulates real world usage and returns performance metrics."""
    pass


@api("/api/{projectId}/jobs/evaluate", method="post")
def startEvaluateJob(projectId: str, impulseId: str = None) -> StartJobResponse:
    """Evaluates every variant of the current impulse. Updates are streamed over the websocket API."""
    pass


@api("/api/{projectId}/jobs/version", method="post")
def startVersionJob(
    projectId: str, requestBody: ProjectVersionRequest
) -> StartJobResponse:
    """Create a new version of the project. This stores all data and configuration offsite. If you have access to the enterprise version of Edge Impulse you can store your data in your own storage buckets (only through JWT token authentication)."""
    pass


@api("/api/{projectId}/jobs/restore", method="post")
def startRestoreJob(
    projectId: str, requestBody: RestoreProjectRequest
) -> GenericApiResponse:
    """Restore a project to a certain version. This can only applied to a project without data, and will overwrite your impulse and all settings."""
    pass


@api("/api/{projectId}/jobs/restore/from-public", method="post")
def startRestoreJobFromPublic(
    projectId: str, requestBody: RestoreProjectFromPublicRequest
) -> GenericApiResponse:
    """Restore a project to a certain public version. This can only applied to a project without data, and will overwrite your impulse and all settings."""
    pass


@api("/api/{projectId}/jobs/versions/{versionId}/make-public", method="post")
def startMakeVersionPublicJob(projectId: str, versionId: str) -> StartJobResponse:
    """Make a version of a project public. This makes all data and state available (read-only) on a public URL, and allows users to clone this project."""
    pass


@api("/api/{projectId}/jobs/keywords-noise", method="post")
def startKeywordsNoiseJob(projectId: str) -> StartJobResponse:
    """Add keywords and noise data to a project (for getting started guide)"""
    pass


@api("/api/{projectId}/jobs/profile-tflite", method="post")
def startProfileTfliteJob(
    projectId: str, requestBody: ProfileTfLiteRequest
) -> StartJobResponse:
    """Takes in a TFLite model and returns the latency, RAM and ROM used for this model. Updates are streamed over the websocket API (or can be retrieved through the /stdout endpoint). Use getProfileTfliteJobResult to get the results when the job is completed."""
    pass


@api("/api/{projectId}/jobs/deploy-pretrained-model", method="post")
def startDeployPretrainedModelJob(
    projectId: str, requestBody: DeployPretrainedModelRequest, impulseId: str = None
) -> StartJobResponse:
    """Takes in a TFLite file and builds the model and SDK. Updates are streamed over the websocket API (or can be retrieved through the /stdout endpoint). Use getProfileTfliteJobResult to get the results when the job is completed."""
    pass


@api("/api/{projectId}/jobs/profile-tflite/{jobId}/result", method="post")
def getProfileTfliteJobResultViaPostRequest(
    projectId: str, jobId: str
) -> ProfileTfLiteResponse:
    """Get the results from a job started from startProfileTfliteJob (via a POST request)."""
    pass


@api("/api/{projectId}/jobs", method="get")
def listActiveJobs(projectId: str, rootOnly: str = None) -> ListJobsResponse:
    """Get all active jobs for this project"""
    pass


@api("/api/{projectId}/jobs/history", method="get")
def listFinishedJobs(
    projectId: str,
    startDate: str = None,
    endDate: str = None,
    limit: str = None,
    offset: str = None,
    rootOnly: str = None,
) -> ListJobsResponse:
    """Get all finished jobs for this project"""
    pass


@api("/api/{projectId}/jobs/all", method="get")
def listAllJobs(
    projectId: str,
    startDate: str = None,
    endDate: str = None,
    limit: str = None,
    offset: str = None,
    rootOnly: str = None,
    key: str = None,
    category: str = None,
) -> ListJobsResponse:
    """Get all jobs for this project"""
    pass


@api("/api/{projectId}/jobs/summary", method="get")
def getJobsSummary(projectId: str, startDate: str, endDate: str) -> JobSummaryResponse:
    """Get a summary of jobs, grouped by key. Used to report to users how much compute they've used."""
    pass


@api("/api/{projectId}/jobs/impulse-migration/status", method="get")
def getImpulseMigrationJobStatus(projectId: str) -> GetJobResponse:
    """Get the status for the multi-impulse migration job in this project. This is a separate route so public projects can access it. If no multi-impulse migration jobs are present, an error will be thrown."""
    pass


@api("/api/{projectId}/jobs/impulse-migration/stdout", method="get")
def getImpulseMigrationJobsLogs(
    projectId: str, limit: str = None, logLevel: str = None
) -> LogStdoutResponse:
    """Get the logs for the multi-impulse migration job in this project. This is a separate route so public projects can access it. If no multi-impulse migration jobs are present, an error will be thrown."""
    pass


@api("/api/{projectId}/jobs/{jobId}/status", method="get")
def getJobStatus(projectId: str, jobId: str) -> GetJobResponse:
    """Get the status for a job."""
    pass


@api("/api/{projectId}/jobs/{jobId}/stdout", method="get")
def getJobsLogs(
    projectId: str, jobId: str, limit: str = None, logLevel: str = None
) -> LogStdoutResponse:
    """Get the logs for a job."""
    pass


@api("/api/{projectId}/jobs/{jobId}/stdout/download", method="get")
def downloadJobsLogs(
    projectId: str, jobId: str, limit: str = None, logLevel: str = None
) -> None:
    """Download the logs for a job (as a text file)."""
    pass


@api("/api/{projectId}/jobs/profile-tflite/{jobId}/result", method="get")
def getProfileTfliteJobResult(projectId: str, jobId: str) -> ProfileTfLiteResponse:
    """Get the results from a job started from startProfileTfliteJob (via a GET request)."""
    pass


@api("/api/{projectId}/optimize/runs", method="get")
def listTunerRuns(projectId: str) -> ListTunerRunsResponse:
    """List all the tuner runs for a project."""
    pass


@api("/api/{projectId}/optimize/config", method="get")
def getConfig(projectId: str) -> OptimizeConfigResponse:
    """Get config"""
    pass


@api("/api/{projectId}/optimize/all-learn-blocks", method="get")
def getAllLearnBlocks(projectId: str) -> AllLearnBlocksResponse:
    """Get all available learn blocks"""
    pass


@api("/api/{projectId}/optimize/window-settings", method="get")
def getWindowSettings(projectId: str) -> WindowSettingsResponse:
    """Get window settings"""
    pass


@api("/api/{projectId}/optimize/space", method="get")
def getSpace(projectId: str) -> OptimizeSpaceResponse:
    """Search space"""
    pass


@api("/api/{projectId}/optimize/state", method="get")
def getState(projectId: str) -> OptimizeStateResponse:
    """Retrieves the EON tuner state"""
    pass


@api("/api/{projectId}/optimize/dsp-parameters", method="get")
def getDspParameters(
    projectId: str, organizationId: str, organizationDspId: str
) -> OptimizeDSPParametersResponse:
    """Retrieves DSP block parameters"""
    pass


@api("/api/{projectId}/optimize/transfer-learning-models", method="get")
def getTransferLearningModels(projectId: str) -> OptimizeTransferLearningModelsResponse:
    """Retrieves available transfer learning models"""
    pass


@api("/api/{projectId}/optimize/trial/{trialId}/stdout", method="get")
def getTrialLogs(projectId: str, trialId: str) -> LogStdoutResponse:
    """Get the logs for a trial."""
    pass


@api("/api/{projectId}/optimize//{jobId}/trial/{trialId}/end-trial", method="get")
def endTrial(projectId: str, jobId: str, trialId: str) -> GenericApiResponse:
    """End an EON trial early. This can for example be used to implement early stopping."""
    pass


@api("/api/{projectId}/optimize/{tunerCoordinatorJobId}/state", method="get")
def getTunerRunState(
    projectId: str, tunerCoordinatorJobId: str
) -> OptimizeStateResponse:
    """Retrieves the EON tuner state for a specific run."""
    pass


@api("/api/{projectId}/optimize/config", method="post")
def updateConfig(projectId: str, requestBody: OptimizeConfig) -> GenericApiResponse:
    """Update config"""
    pass


@api("/api/{projectId}/optimize/score-trial", method="post")
def scoreTrial(
    projectId: str, requestBody: TunerCreateTrialImpulse
) -> ScoreTrialResponse:
    """Score trial"""
    pass


@api("/api/{projectId}/optimize/{jobId}/create-trial", method="post")
def createTrial(
    projectId: str, jobId: str, requestBody: TunerCreateTrialImpulse
) -> GenericApiResponse:
    """Create trial"""
    pass


@api("/api/{projectId}/optimize/{jobId}/complete-search", method="post")
def completeSearch(
    projectId: str, jobId: str, requestBody: TunerCompleteSearch
) -> GenericApiResponse:
    """Complete EON tuner run and mark it as succesful"""
    pass


@api("/api/{projectId}/optimize/{tunerCoordinatorJobId}", method="post")
def updateTunerRun(
    projectId: str, tunerCoordinatorJobId: str, requestBody: UpdateTunerRunRequest
) -> GenericApiResponse:
    """Updates the EON tuner state for a specific run."""
    pass


@api("/api/{projectId}/optimize/state", method="delete")
def deleteState(projectId: str) -> GenericApiResponse:
    """Completely clears the EON tuner state for this project."""
    pass


@api("/api/{projectId}/export/get-url", method="get")
def getExportUrl(projectId: str) -> ExportGetUrlResponse:
    """Get the URL to the exported artefacts for an export job of a project."""
    pass


@api("/api/auth/discourse", method="get")
def discourse(sso: str, sig: str) -> Any:
    """Log in a user to the forum. This function is only available through a JWT token."""
    pass


@api("/api/auth/readme", method="get")
def readme() -> Any:
    """Log in a user to the docs. This function is only available through a JWT token."""
    pass


@api("/api/organizations", method="get")
def listOrganizations() -> ListOrganizationsResponse:
    """Retrieve list of organizations that a user is a part of. If authenticating using JWT token this lists all the organizations the user has access to, if authenticating using an API key, this only lists that organization."""
    pass


@api("/api/organizations/{organizationId}", method="get")
def getOrganizationInfo(organizationId: str) -> OrganizationInfoResponse:
    """List all information about this organization."""
    pass


@api("/api/organizations/{organizationId}/metrics", method="get")
def getOrganizationMetrics(
    organizationId: str,
    excludeEdgeImpulseUsers: str = None,
    projectVisibility: str = None,
) -> OrganizationMetricsResponse:
    """Get general metrics for this organization."""
    pass


@api("/api/organizations/{organizationId}/whitelabel", method="get")
def whitelabelAdminGetInfo(organizationId: str) -> GetWhitelabelResponse:
    """White label admin only API to get the white label information."""
    pass


@api("/api/organizations/{organizationId}/whitelabel/metrics", method="get")
def whitelabelAdminGetMetrics(organizationId: str) -> AdminGetMetricsResponse:
    """White label admin only API to get global metrics."""
    pass


@api("/api/organizations/{organizationId}/whitelabel/users", method="get")
def whitelabelAdminGetUsers(
    organizationId: str,
    active: str = None,
    tier: str = None,
    fields: str = None,
    sort: str = None,
    filters: str = None,
    limit: str = None,
    offset: str = None,
    search: str = None,
) -> AdminGetUsersResponse:
    """White label admin only API to get the list of all registered users."""
    pass


@api("/api/organizations/{organizationId}/whitelabel/users/{userId}", method="get")
def whitelabelAdminGetUser(organizationId: str, userId: str) -> AdminGetUserResponse:
    """White label admin only API to get information about a user."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/users/{userId}/metrics",
    method="get",
)
def whitelabelAdminGetUserMetrics(
    organizationId: str, userId: str
) -> AdminGetUserMetricsResponse:
    """White label admin only API to get marketing metrics about a user."""
    pass


@api("/api/organizations/{organizationId}/whitelabel/users/{userId}/jobs", method="get")
def whitelabelAdminGetUserJobs(
    organizationId: str, userId: str, limit: str = None, offset: str = None
) -> ListJobsResponse:
    """White label admin only  API to get the list of all project jobs for a user."""
    pass


@api("/api/organizations/{organizationId}/whitelabel/projects", method="get")
def whitelabelAdminGetProjects(
    organizationId: str,
    active: str = None,
    sort: str = None,
    filters: str = None,
    limit: str = None,
    offset: str = None,
    search: str = None,
) -> AdminListProjectsResponse:
    """White label admin only API to get the list of all projects."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/projects/{projectId}", method="get"
)
def whitelabelAdminGetProject(
    organizationId: str, projectId: str
) -> ProjectInfoResponse:
    """White label admin only API to get project information."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/projects/{projectId}/jobs",
    method="get",
)
def whitelabelAdminGetProjectJobs(
    organizationId: str, projectId: str, limit: str = None, offset: str = None
) -> ListJobsResponse:
    """White label admin only API to get the list of all jobs for a project."""
    pass


@api("/api/organizations/{organizationId}/whitelabel/organizations", method="get")
def whitelabelAdminGetOrganizations(
    organizationId: str,
    active: str = None,
    includeDeleted: str = None,
    sort: str = None,
    filters: str = None,
    limit: str = None,
    offset: str = None,
    search: str = None,
) -> AdminGetOrganizationsResponse:
    """White label admin only API to get the list of all organizations."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/organizations/{innerOrganizationId}/usage/computeTime",
    method="get",
)
def whitelabelAdminGetOrganizationComputeTimeUsage(
    organizationId: str, innerOrganizationId: str, startDate: str, endDate: str
) -> AdminGetOrganizationComputeTimeUsageResponse:
    """Get compute time usage for an organization over a period of time. This is an API only available to white label admins"""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/organizations/{innerOrganizationId}/usage/reports",
    method="get",
)
def whitelabelAdminGetOrganizationUsageReports(
    organizationId: str, innerOrganizationId: str, limit: str = None, offset: str = None
) -> AdminGetReportsResponse:
    """Get all usage reports for an organization. This is an API only available to white label admins."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/organizations/{innerOrganizationId}/usage/reports/{reportId}",
    method="get",
)
def whitelabelAdminGetOrganizationUsageReport(
    organizationId: str, innerOrganizationId: str, reportId: str
) -> AdminGetReportResponse:
    """Get a usage report for an organization. This is an API only available to white label admins."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/organizations/{innerOrganizationId}/usage/reports/{reportId}/download",
    method="get",
)
def whitelabelAdminDownloadOrganizationUsageReport(
    organizationId: str, innerOrganizationId: str, reportId: str
) -> Any:
    """Download a usage report for an organization. This is an API only available to white label admins."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/organizations/{innerOrganizationId}/exports",
    method="get",
)
def whitelabelAdminGetOrganizationExports(
    organizationId: str, innerOrganizationId: str, limit: str = None, offset: str = None
) -> GetOrganizationDataExportsResponse:
    """Get all data exports for an organization. This is an API only available to white label admins."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/organizations/{innerOrganizationId}/exports/{exportId}",
    method="get",
)
def whitelabelAdminGetOrganizationExport(
    organizationId: str, innerOrganizationId: str, exportId: str
) -> GetOrganizationDataExportResponse:
    """Get a data export for an organization. This is an API only available to white label admins."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/organizations/{innerOrganizationId}",
    method="get",
)
def whitelabelAdminGetOrganizationInfo(
    organizationId: str, innerOrganizationId: str, includeDeleted: str = None
) -> AdminOrganizationInfoResponse:
    """White label admin only API to list all information about an organization."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/organizations/{innerOrganizationId}/restore",
    method="get",
)
def whitelabelAdminRestoreOrganization(
    organizationId: str, innerOrganizationId: str
) -> GenericApiResponse:
    """White label admin only API to restore a deleted organization. All organization projects sharing the same deletion date as that of the organization will also be restored. If this is a trial organization that was never upgraded to a paid plan then the organization will be restored to its original trial state."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/organizations/{innerOrganizationId}/jobs",
    method="get",
)
def whitelabelAdminGetOrganizationJobs(
    organizationId: str, innerOrganizationId: str, limit: str = None, offset: str = None
) -> ListJobsResponse:
    """White label admin only API to get the list of all jobs for a organization."""
    pass


@api("/api/organizations/{organizationId}/test-admin", method="get")
def testOrganizationAdmin(organizationId: str) -> GenericApiResponse:
    """Test endpoint that can only be reached with admin rights."""
    pass


@api("/api/organizations/{organizationId}/projects", method="get")
def listOrganizationProjects(organizationId: str) -> ListProjectsResponse:
    """Retrieve all projects for the organization."""
    pass


@api("/api/organizations/{organizationId}/apikeys", method="get")
def listOrganizationApiKeys(organizationId: str) -> ListOrganizationApiKeysResponse:
    """Retrieve all API keys. This does **not** return the full API key, but only a portion (for security purposes)."""
    pass


@api("/api/organizations/{organizationId}/exports", method="get")
def getOrganizationDataExports(
    organizationId: str, limit: str = None, offset: str = None
) -> GetOrganizationDataExportsResponse:
    """Get all data exports for an organization."""
    pass


@api("/api/organizations/{organizationId}/exports/{exportId}", method="get")
def getOrganizationDataExport(
    organizationId: str, exportId: str
) -> GetOrganizationDataExportResponse:
    """Get a data export for an organization."""
    pass


@api("/api/organizations/{organizationId}/exports/{exportId}/download", method="get")
def downloadOrganizationDataExport(organizationId: str, exportId: str) -> Any:
    """Download a data export for an organization."""
    pass


@api("/api/organizations/create", method="post")
def createOrganization(
    requestBody: CreateOrganizationRequest,
) -> CreateOrganizationResponse:
    """Create a new organization. This is an internal API."""
    pass


@api("/api/organizations/{organizationId}", method="post")
def updateOrganization(
    organizationId: str, requestBody: UpdateOrganizationRequest
) -> GenericApiResponse:
    """Update organization properties such as name and logo."""
    pass


@api("/api/organizations/{organizationId}/trial/request-extension", method="post")
def requestEnterpriseTrialExtension(
    organizationId: str, requestBody: EnterpriseUpgradeOrTrialExtensionRequest
) -> GenericApiResponse:
    """Request an extension for an enterprise trial."""
    pass


@api("/api/organizations/{organizationId}/request-hr-block-license", method="post")
def requestEnterpriseHrBlockLicense(organizationId: str) -> GenericApiResponse:
    """Request a license required for the deployment of an impulse containing the Edge Impulse HR block."""
    pass


@api("/api/organizations/{organizationId}/limits-request", method="post")
def requestEnterpriseLimitsIncrease(
    organizationId: str, requestBody: EnterpriseLimitsIncreaseRequest
) -> GenericApiResponse:
    """Request an increase in the limits for this organization. Available limits are: users, projects, compute, storage."""
    pass


@api("/api/organizations/{organizationId}/whitelabel/deploymentTargets", method="post")
def whitelabelAdminUpdateDeploymentTargets(
    organizationId: str, requestBody: UpdateWhitelabelDeploymentTargetsRequest
) -> GenericApiResponse:
    """White label admin only API to update some or all of the deployment targets enabled for this white label."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/deploymentTargets/default",
    method="post",
)
def whitelabelAdminUpdateDefaultDeploymentTarget(
    organizationId: str, requestBody: UpdateWhitelabelDefaultDeploymentTargetRequest
) -> GenericApiResponse:
    """White label admin only API to update the default deployment target for this white label."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/deploymentOptionsOrder",
    method="post",
)
def whitelabelAdminUpdateDeploymentOptionsOrder(
    organizationId: str, requestBody: UpdateWhitelabelDeploymentOptionsOrderRequest
) -> GenericApiResponse:
    """White label admin only API to customize the order of deployment options in the deployment view for this white label."""
    pass


@api("/api/organizations/{organizationId}/whitelabel/learningBlocks", method="post")
def whitelabelAdminUpdateLearningBlocks(
    organizationId: str, requestBody: UpdateWhitelabelLearningBlocksRequest
) -> GenericApiResponse:
    """White label admin only API to update some or all of the learning blocks enabled for this white label."""
    pass


@api("/api/organizations/{organizationId}/whitelabel/theme/logo", method="post")
def whitelabelAdminUpdateThemeLogo(
    organizationId: str, requestBody: UploadAssetRequest
) -> UploadAssetResponse:
    """White label admin only API to update the white label theme logo."""
    pass


@api("/api/organizations/{organizationId}/whitelabel/theme/deviceLogo", method="post")
def whitelabelAdminUpdateThemeDeviceLogo(
    organizationId: str, requestBody: UploadAssetRequest
) -> UploadAssetResponse:
    """White label admin only API to update the white label theme device logo."""
    pass


@api("/api/organizations/{organizationId}/whitelabel/theme/colors", method="post")
def whitelabelAdminUpdateThemeColors(
    organizationId: str, requestBody: UpdateThemeColorsRequest
) -> GenericApiResponse:
    """White label admin only API to update some or all theme colors."""
    pass


@api("/api/organizations/{organizationId}/whitelabel/theme/favicon", method="post")
def whitelabelAdminUpdateThemeFavicon(
    organizationId: str, requestBody: UploadImageRequest
) -> GenericApiResponse:
    """White label admin only API to update the theme favicon."""
    pass


@api("/api/organizations/{organizationId}/whitelabel/users/{userId}", method="post")
def whitelabelAdminUpdateUser(
    organizationId: str, userId: str, requestBody: AdminUpdateUserRequest
) -> GenericApiResponse:
    """White label admin only API to update user properties."""
    pass


@api("/api/organizations/{organizationId}/whitelabel/projects", method="post")
def whitelabelAdminCreateProject(
    organizationId: str, requestBody: AdminCreateProjectRequest
) -> CreateProjectResponse:
    """Create a new free tier project. This is an API only available to white label admins."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/projects/{projectId}", method="post"
)
def whitelabelAdminUpdateProject(
    organizationId: str, projectId: str, requestBody: UpdateProjectRequest
) -> GenericApiResponse:
    """White label admin only API to update project properties."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/projects/{projectId}/apiKeys",
    method="post",
)
def whitelabelAdminAddProjectApiKey(
    organizationId: str, projectId: str, requestBody: AdminAddProjectApiKeyRequest
) -> AddApiKeyResponse:
    """White label admin only API to add an API key to a project. Add a temporary API key that can be used to make Projects API (/api/projects/{projectId}/) requests on behalf of the project admin. These API keys are not visible to the project itself and have a customizable TTL defaulting to 1 minute."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/projects/{projectId}/members",
    method="post",
)
def whitelabelAdminAddUserToProject(
    organizationId: str, projectId: str, requestBody: AdminAddProjectUserRequest
) -> GenericApiResponse:
    """White label admin only API to add a user to a project. If no user is provided, the current user is used."""
    pass


@api("/api/organizations/{organizationId}/whitelabel/development-boards", method="post")
def whitelabelAdminAddDevelopmentBoard(
    organizationId: str, requestBody: DevelopmentBoardRequest
) -> EntityCreatedResponse:
    """White label admin only API to add a development board."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/development-boards/{developmentBoardId}/image",
    method="post",
)
def whitelabelAdminUpdateDevelopmentBoardImage(
    organizationId: str, developmentBoardId: str, requestBody: UploadAssetRequest
) -> UploadAssetResponse:
    """White label admin only API to update the image of a development board."""
    pass


@api("/api/organizations/{organizationId}/whitelabel/organizations", method="post")
def whitelabelAdminCreateOrganization(
    organizationId: str, requestBody: WhitelabelAdminCreateOrganizationRequest
) -> CreateOrganizationResponse:
    """Create a new organization. This is an API only available to white label admins"""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/organizations/{innerOrganizationId}/usage/reports",
    method="post",
)
def whitelabelAdminCreateOrganizationUsageReport(
    organizationId: str, innerOrganizationId: str, startDate: str, endDate: str
) -> StartJobResponse:
    """Create a new usage report for an organization. A job is created to process the report request and the job details are returned in the response. This is an API only available to white label admins."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/organizations/{innerOrganizationId}/exports",
    method="post",
)
def whitelabelAdminCreateOrganizationExport(
    organizationId: str,
    innerOrganizationId: str,
    requestBody: AdminCreateOrganizationDataExportRequest,
) -> StartJobResponse:
    """Create a new data export for an organization. A job is created to process the export request and the job details are returned in the response. This is an API only available to white label admins."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/organizations/{innerOrganizationId}/apiKeys",
    method="post",
)
def whitelabelAdminAddOrganizationApiKey(
    organizationId: str,
    innerOrganizationId: str,
    requestBody: AdminAddOrganizationApiKeyRequest,
) -> AddApiKeyResponse:
    """White label admin only API to add an API key to an organization. Add a temporary API key that can be used to make Organizations API (/api/organizations/{organizationId}/) requests on behalf of the organization. These API keys are not visible to the organization itself and have a customizable TTL defaulting to 1 minute."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/organizations/{innerOrganizationId}/members",
    method="post",
)
def whitelabelAdminAddUserToOrganization(
    organizationId: str,
    innerOrganizationId: str,
    requestBody: AdminAddOrganizationUserRequest,
) -> GenericApiResponse:
    """White label admin only API to add a user to an organization. If no user is provided, the current user is used."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/organizations/{innerOrganizationId}",
    method="post",
)
def whitelabelAdminUpdateOrganization(
    organizationId: str,
    innerOrganizationId: str,
    requestBody: AdminUpdateOrganizationRequest,
) -> GenericApiResponse:
    """White label admin only API to update organization properties such as name and logo."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/organizations/{innerOrganizationId}/projects",
    method="post",
)
def whitelabelAdminCreateOrganizationProject(
    organizationId: str,
    innerOrganizationId: str,
    requestBody: AdminCreateProjectRequest,
) -> CreateProjectResponse:
    """White label admin only API to create a new project for an organization."""
    pass


@api("/api/organizations/{organizationId}/logo", method="post")
def uploadOrganizationLogo(
    organizationId: str, requestBody: UploadAssetRequest
) -> UploadAssetResponse:
    """Uploads and updates the organization logo"""
    pass


@api("/api/organizations/{organizationId}/header", method="post")
def uploadOrganizationHeader(
    organizationId: str, requestBody: UploadAssetRequest
) -> UploadAssetResponse:
    """Uploads and updates the organization header image"""
    pass


@api("/api/organizations/{organizationId}/apikeys", method="post")
def addOrganizationApiKey(
    organizationId: str, requestBody: AddOrganizationApiKeyRequest
) -> AddApiKeyResponse:
    """Add an API key."""
    pass


@api("/api/organizations/{organizationId}/members/add", method="post")
def addOrganizationMember(
    organizationId: str, requestBody: AddMemberRequest
) -> EntityCreatedResponse:
    """Add a member to an organization."""
    pass


@api("/api/organizations/{organizationId}/members/invite", method="post")
def inviteOrganizationMember(
    organizationId: str, requestBody: InviteOrganizationMemberRequest
) -> GenericApiResponse:
    """Invite a member to an organization."""
    pass


@api("/api/organizations/{organizationId}/members/remove", method="post")
def removeOrganizationMember(
    organizationId: str, requestBody: RemoveMemberRequest
) -> GenericApiResponse:
    """Remove a member from an organization. Note that you cannot invoke this function if only a single member is present to the organization."""
    pass


@api("/api/organizations/{organizationId}/members/{memberId}/role", method="post")
def setOrganizationMemberRole(
    organizationId: str, memberId: str, requestBody: SetMemberRoleRequest
) -> GenericApiResponse:
    """Change the role of a member in an organization."""
    pass


@api("/api/organizations/{organizationId}/members/{memberId}/datasets", method="post")
def setOrganizationMemberDatasets(
    organizationId: str, memberId: str, requestBody: SetMemberDatasetsRequest
) -> GenericApiResponse:
    """Set the datasets a guest member has access to in an organization."""
    pass


@api(
    "/api/organizations/{organizationId}/members/{memberId}/resend-invite",
    method="post",
)
def resendOrganizationMemberInvite(
    organizationId: str, memberId: str
) -> GenericApiResponse:
    """Resend an invitation to a member in an organization."""
    pass


@api("/api/organizations/{organizationId}/readme/upload-image", method="post")
def uploadOrganizationReadmeImage(
    organizationId: str, requestBody: UploadImageRequest
) -> UploadReadmeImageResponse:
    """Uploads an image to the user CDN and returns the path."""
    pass


@api("/api/organizations/{organizationId}", method="delete")
def deleteOrganization(organizationId: str) -> GenericApiResponse:
    """Remove the current organization, and all data associated with it. This is irrevocable!"""
    pass


@api("/api/organizations/{organizationId}/whitelabel/users/{userId}", method="delete")
def whitelabelAdminDeleteUser(organizationId: str, userId: str) -> GenericApiResponse:
    """White label admin only API to delete a user."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/projects/{projectId}",
    method="delete",
)
def whitelabelAdminDeleteProject(
    organizationId: str, projectId: str
) -> GenericApiResponse:
    """White label admin only API to delete a project."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/projects/{projectId}/members/{userId}",
    method="delete",
)
def whitelabelAdminRemoveUserFromProject(
    organizationId: str, projectId: str, userId: str
) -> GenericApiResponse:
    """White label admin only API to remove a user from a project."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/development-boards/{developmentBoardId}",
    method="delete",
)
def whitelabelAdminRemoveDevelopmentBoard(
    organizationId: str, developmentBoardId: str
) -> GenericApiResponse:
    """White label admin only API to remove a development board."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/organizations/{innerOrganizationId}/usage/reports/{reportId}",
    method="delete",
)
def whitelabelAdminDeleteOrganizationUsageReport(
    organizationId: str, innerOrganizationId: str, reportId: str
) -> GenericApiResponse:
    """Delete a usage report for an organization. This is an API only available to white label admins."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/organizations/{innerOrganizationId}/exports/{exportId}",
    method="delete",
)
def whitelabelAdminDeleteOrganizationExport(
    organizationId: str, innerOrganizationId: str, exportId: str
) -> GenericApiResponse:
    """Delete a data export for an organization. This is an API only available to white label admins."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/organizations/{innerOrganizationId}/members/{userId}",
    method="delete",
)
def whitelabelAdminRemoveUserFromOrganization(
    organizationId: str, innerOrganizationId: str, userId: str
) -> GenericApiResponse:
    """White label admin only API to remove a user from an organization."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/organizations/{innerOrganizationId}",
    method="delete",
)
def whitelabelAdminDeleteOrganization(
    organizationId: str, innerOrganizationId: str
) -> GenericApiResponse:
    """White label admin only API to delete an organization."""
    pass


@api("/api/organizations/{organizationId}/apikeys/{apiKeyId}", method="delete")
def revokeOrganizationApiKey(organizationId: str, apiKeyId: str) -> GenericApiResponse:
    """Revoke an API key."""
    pass


@api("/api/organizations/{organizationId}/whitelabel", method="put")
def whitelabelAdminUpdateInfo(
    organizationId: str, requestBody: UpdateWhitelabelRequest
) -> GenericApiResponse:
    """White label admin only API to update the white label information."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/development-boards/{developmentBoardId}",
    method="put",
)
def whitelabelAdminUpdateDevelopmentBoard(
    organizationId: str,
    developmentBoardId: str,
    requestBody: DevelopmentBoardRequestUpdate,
) -> GenericApiResponse:
    """White label admin only API to update a development board."""
    pass


@api(
    "/api/organizations/{organizationId}/whitelabel/organizations/{innerOrganizationId}/exports/{exportId}",
    method="put",
)
def whitelabelAdminUpdateOrganizationExport(
    organizationId: str,
    innerOrganizationId: str,
    exportId: str,
    requestBody: AdminUpdateOrganizationDataExportRequest,
) -> GenericApiResponse:
    """Update a data export for an organization. This is an API only available to white label admins."""
    pass


@api("/api/organizations/{organizationId}/buckets", method="get")
def listOrganizationBuckets(organizationId: str) -> ListOrganizationBucketsResponse:
    """Retrieve all configured storage buckets. This does not list the secret key."""
    pass


@api("/api/organizations/{organizationId}/buckets/{bucketId}", method="get")
def getOrganizationBucket(
    organizationId: str, bucketId: str
) -> GetOrganizationBucketResponse:
    """Get storage bucket details."""
    pass


@api("/api/organizations/{organizationId}/data", method="get")
def listOrganizationData(
    organizationId: str,
    dataset: str = None,
    filter: str = None,
    limit: str = None,
    offset: str = None,
) -> ListOrganizationDataResponse:
    """Lists all data items. This can be filtered by the ?filter parameter."""
    pass


@api("/api/organizations/{organizationId}/data/download", method="get")
def downloadOrganizationDataItem(
    organizationId: str, dataIds: str, dataset: str = None, filter: str = None
) -> File:
    """Download all data for selected data items. This function does not query the underlying bucket."""
    pass


@api("/api/organizations/{organizationId}/data/files", method="get")
def listOrganizationFiles(
    organizationId: str,
    dataset: str = None,
    filter: str = None,
    limit: str = None,
    offset: str = None,
) -> ListOrganizationFilesResponse:
    """Lists all files included by the filter."""
    pass


@api("/api/organizations/{organizationId}/data/{dataId}", method="get")
def getOrganizationDataItem(
    organizationId: str, dataId: str, filter: str = None
) -> GetOrganizationDataItemResponse:
    """Get a data item. This will HEAD the underlying bucket to retrieve the last file information."""
    pass


@api("/api/organizations/{organizationId}/data/{dataId}/download", method="get")
def downloadOrganizationSingleDataItem(
    organizationId: str, dataId: str, filter: str = None
) -> File:
    """Download all data for this data item."""
    pass


@api("/api/organizations/{organizationId}/data/{dataId}/files/download", method="get")
def downloadOrganizationDataFile(
    organizationId: str, dataId: str, fileName: str
) -> File:
    """Download a single file from a data item."""
    pass


@api("/api/organizations/{organizationId}/data/{dataId}/files/preview", method="get")
def previewOrganizationDataFile(
    organizationId: str, dataId: str, fileName: str
) -> File:
    """Preview a single file from a data item (same as downloadOrganizationDataFile but w/ content-disposition inline and could be truncated)."""
    pass


@api(
    "/api/organizations/{organizationId}/data/{dataId}/transformation-jobs",
    method="get",
)
def getOrganizationDataItemTransformJobs(
    organizationId: str, dataId: str, limit: str = None, offset: str = None
) -> GetOrganizationDataItemTransformJobsResponse:
    """Get all transformation jobs that ran for a data item. If limit / offset is not provided then max. 20 results are returned."""
    pass


@api("/api/organizations/{organizationId}/dataset/{dataset}", method="get")
def getOrganizationDataset(
    organizationId: str, dataset: str
) -> GetOrganizationDatasetResponse:
    """Get information about a dataset"""
    pass


@api(
    "/api/organizations/{organizationId}/dataset/{dataset}/files/download-folder",
    method="get",
)
def downloadDatasetFolder(organizationId: str, dataset: str, path: str) -> File:
    """Download all files in the given folder in a dataset, ignoring any subdirectories."""
    pass


@api("/api/organizations/{organizationId}/dataset/{dataset}/files/view", method="get")
def viewDatasetFile(organizationId: str, dataset: str, path: str) -> File:
    """View a file that's located in a dataset (requires JWT auth). File might be converted (e.g. Parquet) or truncated (e.g. CSV)."""
    pass


@api("/api/organizations/{organizationId}/buckets", method="post")
def addOrganizationBucket(
    organizationId: str, requestBody: AddOrganizationBucketRequest
) -> EntityCreatedResponse:
    """Add a storage bucket."""
    pass


@api("/api/organizations/{organizationId}/buckets/verify", method="post")
def verifyOrganizationBucket(
    organizationId: str, requestBody: VerifyOrganizationBucketRequest
) -> VerifyOrganizationBucketResponse:
    """Verify connectivity to a storage bucket and optionally list its contents. This endpoint allows you to: 1. Check if the provided bucket credentials are valid and the bucket is accessible. 2. Optionally list files in the bucket up to a specified limit. 3. Validate the bucket configuration before adding it to the organization.  The request can include details such as the bucket name, region, credentials, and listing options. The response provides information about the bucket's accessibility and, if requested, a list of files in the bucket.  Important note on verification process: - For S3-compatible storage backends: Verification is expected to be immediate. - For Azure buckets: Verification takes longer. Users are required to poll this endpoint until the connectionStatus changes from 'connecting' to 'connected'.  When dealing with Azure buckets, implement a polling mechanism to check the status periodically until it's confirmed as connected."""
    pass


@api("/api/organizations/{organizationId}/buckets/{bucketId}", method="post")
def updateOrganizationBucket(
    organizationId: str, bucketId: str, requestBody: UpdateOrganizationBucketRequest
) -> GenericApiResponse:
    """Updates storage bucket details. This only updates fields that were set in the request body. Before updating the bucket details, it is required to verify the connection using the POST /api/organizations/{organizationId}/buckets/verify endpoint.  The verification process: 1. Call the verify endpoint with the new bucket details. 2. Poll the verify endpoint until it responds with `connectionStatus: connected`. 3. If the endpoint responds with `connectionStatus: error`, the verification has failed.  Only proceed with updating the bucket details after receiving a `connected` status. The polling interval and timeout should be determined based on your application's requirements."""
    pass


@api("/api/organizations/{organizationId}/buckets/{bucketId}/verify", method="post")
def verifyExistingOrganizationBucket(
    organizationId: str,
    bucketId: str,
    requestBody: VerifyOrganizationExistingBucketRequest,
) -> VerifyOrganizationBucketResponse:
    """Verify whether we can reach a bucket before adding it."""
    pass


@api("/api/organizations/{organizationId}/data/add", method="post")
def addOrganizationDataItem(
    organizationId: str, requestBody: OrganizationAddDataItemRequest
) -> EntityCreatedResponse:
    """Add a new data item. You can add a maximum of 10000 files directly through this API. Use `addOrganizationDataFile` to add additional files."""
    pass


@api("/api/organizations/{organizationId}/data/add-folder", method="post")
def addOrganizationDataFolder(
    organizationId: str, requestBody: OrganizationAddDataFolderRequest
) -> StartJobResponse:
    """Bulk adds data items that already exist in a storage bucket. The bucket path specified should contain folders. Each folder is added as a data item in Edge Impulse."""
    pass


@api("/api/organizations/{organizationId}/data/delete", method="post")
def deleteOrganizationDataItems(
    organizationId: str, dataIds: str, dataset: str = None, filter: str = None
) -> StartJobResponse:
    """Delete all data for selected data items. This removes all data in the underlying data bucket."""
    pass


@api("/api/organizations/{organizationId}/data/clear-checklist", method="post")
def clearChecklistOrganizationDataItems(
    organizationId: str, dataIds: str, dataset: str = None, filter: str = None
) -> StartJobResponse:
    """Clear all checklist flags for selected data items."""
    pass


@api("/api/organizations/{organizationId}/data/change-dataset", method="post")
def changeDatasetOrganizationDataItems(
    organizationId: str,
    dataIds: str,
    requestBody: SetOrganizationDataDatasetRequest,
    dataset: str = None,
    filter: str = None,
) -> StartJobResponse:
    """Change the dataset for selected data items."""
    pass


@api("/api/organizations/{organizationId}/data/refresh", method="post")
def refreshOrganizationData(organizationId: str, dataset: str) -> StartJobResponse:
    """Update all data items. HEADs all underlying buckets to retrieve the last file information. Use this API after uploading data directly to S3. If your dataset has bucketId and bucketPath set then this will also remove items that have been removed from S3."""
    pass


@api("/api/organizations/{organizationId}/data/bulk-metadata", method="post")
def organizationBulkUpdateMetadata(
    organizationId: str, requestBody: OrganizationBulkMetadataRequest
) -> StartJobResponse:
    """Bulk update the metadata of many data items in one go. This requires you to submit a CSV file with headers, one of which the columns should be named 'name'. The other columns are used as metadata keys."""
    pass


@api("/api/organizations/{organizationId}/data/{dataId}", method="post")
def updateOrganizationDataItem(
    organizationId: str, dataId: str, requestBody: UpdateOrganizationDataItemRequest
) -> GenericApiResponse:
    """Update the data item metadata."""
    pass


@api("/api/organizations/{organizationId}/data/{dataId}/add", method="post")
def addOrganizationDataFile(
    organizationId: str, dataId: str, requestBody: OrganizationAddDataFileRequest
) -> GenericApiResponse:
    """Add a new file to an existing data item."""
    pass


@api("/api/organizations/{organizationId}/dataset", method="post")
def addOrganizationDataset(
    organizationId: str, requestBody: OrganizationAddDatasetRequest
) -> StartJobResponse:
    """Add a new research dataset"""
    pass


@api("/api/organizations/{organizationId}/dataset/{dataset}", method="post")
def updateOrganizationDataset(
    organizationId: str, dataset: str, requestBody: UpdateOrganizationDatasetRequest
) -> GenericApiResponse:
    """Set information about a dataset"""
    pass


@api("/api/organizations/{organizationId}/dataset/{dataset}/hide", method="post")
def hideOrganizationDataset(organizationId: str, dataset: str) -> GenericApiResponse:
    """Hide a dataset (does not remove underlying data)"""
    pass


@api("/api/organizations/{organizationId}/dataset/{dataset}/upload-link", method="post")
def createSignedUploadLinkDataset(
    organizationId: str, dataset: str, requestBody: CreateSignedUploadLinkRequest
) -> CreateSignedUploadLinkResponse:
    """Creates a signed link to securely upload data to s3 bucket directly from the client."""
    pass


@api("/api/organizations/{organizationId}/dataset/{dataset}/verify", method="post")
def verifyDataset(
    organizationId: str, dataset: str
) -> VerifyOrganizationBucketResponse:
    """Verify whether we can reach a dataset (and return some random files, used for data sources)"""
    pass


@api("/api/organizations/{organizationId}/dataset/{dataset}/files", method="post")
def listDatasetFilesInFolder(
    organizationId: str, dataset: str, requestBody: ListPortalFilesInFolderRequest
) -> ListPortalFilesInFolderResponse:
    """List all files and directories in specified prefix."""
    pass


@api(
    "/api/organizations/{organizationId}/dataset/{dataset}/files/delete", method="post"
)
def deleteDatasetFile(
    organizationId: str, dataset: str, requestBody: DeletePortalFileRequest
) -> GenericApiResponse:
    """Delete a file from a dataset"""
    pass


@api(
    "/api/organizations/{organizationId}/dataset/{dataset}/files/rename", method="post"
)
def renameDatasetFile(
    organizationId: str, dataset: str, requestBody: RenamePortalFileRequest
) -> GenericApiResponse:
    """Rename a file in a dataset"""
    pass


@api(
    "/api/organizations/{organizationId}/dataset/{dataset}/files/download",
    method="post",
)
def downloadDatasetFile(
    organizationId: str, dataset: str, requestBody: DownloadPortalFileRequest
) -> DownloadPortalFileResponse:
    """Download a file from a dataset. Will return a signed URL to the bucket."""
    pass


@api(
    "/api/organizations/{organizationId}/dataset/{dataset}/files/preview", method="post"
)
def previewDefaultFilesInFolder(
    organizationId: str, dataset: str, requestBody: PreviewDefaultFilesInFolderRequest
) -> PreviewDefaultFilesInFolderResponse:
    """Preview files and directories in a default dataset for the given prefix, with support for wildcards. This is an internal API used when starting a transformation job."""
    pass


@api("/api/organizations/{organizationId}/buckets/{bucketId}", method="delete")
def removeOrganizationBucket(organizationId: str, bucketId: str) -> GenericApiResponse:
    """Remove a storage bucket. This will render any data in this storage bucket unreachable."""
    pass


@api("/api/organizations/{organizationId}/data/{dataId}", method="delete")
def deleteOrganizationDataItem(organizationId: str, dataId: str) -> GenericApiResponse:
    """Delete a data item. This will remove items the items from the underlying storage if your dataset has "bucketPath" set."""
    pass


@api("/api/organizations/{organizationId}/data/{dataId}/download", method="delete")
def deleteOrganizationDataFile(
    organizationId: str, dataId: str, fileName: str
) -> GenericApiResponse:
    """Delete a single file from a data item."""
    pass


@api("/api/organizations/{organizationId}/create-project", method="get")
def getOrganizationCreateProjects(
    organizationId: str,
    limit: str = None,
    offset: str = None,
    includePipelineJobs: str = None,
) -> OrganizationGetCreateProjectsResponse:
    """Get list of transformation jobs."""
    pass


@api(
    "/api/organizations/{organizationId}/create-project/{createProjectId}", method="get"
)
def getOrganizationCreateProjectStatus(
    organizationId: str,
    createProjectId: str,
    transformLimit: str,
    transformOffset: str,
    selection: str = None,
) -> OrganizationCreateProjectStatusResponse:
    """Get the current status of a transformation job job."""
    pass


@api("/api/organizations/{organizationId}/create-project", method="post")
def organizationCreateProject(
    organizationId: str, requestBody: OrganizationCreateProjectRequest
) -> OrganizationCreateProjectResponse:
    """Start a transformation job to fetch data from the organization and put it in a project, or transform into new data."""
    pass


@api(
    "/api/organizations/{organizationId}/create-project/{createProjectId}",
    method="post",
)
def updateOrganizationCreateProject(
    organizationId: str,
    createProjectId: str,
    requestBody: UpdateOrganizationCreateProjectRequest,
) -> GenericApiResponse:
    """Update the properties of a transformation job."""
    pass


@api(
    "/api/organizations/{organizationId}/create-project/{createProjectId}/transform/retry",
    method="post",
)
def retryOrganizationTransform(
    organizationId: str, createProjectId: str
) -> GenericApiResponse:
    """Retry all failed transform job from a transformation job. Only jobs that have failed will be retried."""
    pass


@api(
    "/api/organizations/{organizationId}/create-project/{createProjectId}/transform/clear",
    method="post",
)
def clearOrganizationTransform(
    organizationId: str, createProjectId: str
) -> GenericApiResponse:
    """Clear all failed transform job from a create project job. Only jobs that have failed will be cleared."""
    pass


@api(
    "/api/organizations/{organizationId}/create-project/{createProjectId}/upload/retry",
    method="post",
)
def retryOrganizationUpload(
    organizationId: str, createProjectId: str
) -> GenericApiResponse:
    """Retry the upload job from a transformation job. Only jobs that have failed can be retried."""
    pass


@api(
    "/api/organizations/{organizationId}/create-project/{createProjectId}/files/{createProjectFileId}/retry",
    method="post",
)
def retryOrganizationCreateProjectFile(
    organizationId: str, createProjectId: str, createProjectFileId: str
) -> GenericApiResponse:
    """Retry a transformation action on a file from a transformation job. Only files that have failed can be retried."""
    pass


@api("/api/organizations/{organizationId}/custom-block", method="post")
def uploadCustomBlock(
    organizationId: str, requestBody: UploadCustomBlockRequest
) -> StartJobResponse:
    """Upload a zip file containing a custom transformation or deployment block."""
    pass


@api("/api/organizations/{organizationId}/new-project", method="post")
def organizationCreateEmptyProject(
    organizationId: str, requestBody: UpdateOrganizationCreateEmptyProjectRequest
) -> CreateProjectResponse:
    """Create a new empty project within an organization."""
    pass


@api("/api/organizations/{organizationId}/add-project-collaborator", method="post")
def organizationAddCollaborator(
    organizationId: str, requestBody: UpdateOrganizationAddCollaboratorRequest
) -> GenericApiResponse:
    """Add a new collaborator to a project owned by an organisation."""
    pass


@api(
    "/api/organizations/{organizationId}/create-project/{createProjectId}",
    method="delete",
)
def deleteOrganizationCreateProject(
    organizationId: str, createProjectId: str
) -> GenericApiResponse:
    """Remove a transformation job. This will stop all running jobs."""
    pass


@api(
    "/api/organizations/{organizationId}/create-project/{createProjectId}/files/{createProjectFileId}",
    method="delete",
)
def deleteOrganizationCreateProjectFile(
    organizationId: str, createProjectId: str, createProjectFileId: str
) -> GenericApiResponse:
    """Remove a file from a create project job. Only files for which no jobs are running can be deleted."""
    pass


@api("/api/organizations/{organizationId}/transformation", method="get")
def listOrganizationTransformationBlocks(
    organizationId: str,
) -> ListOrganizationTransformationBlocksResponse:
    """Retrieve all transformation blocks."""
    pass


@api("/api/organizations/{organizationId}/transformation/public", method="get")
def listPublicOrganizationTransformationBlocks(
    organizationId: str,
) -> ListPublicOrganizationTransformationBlocksResponse:
    """Retrieve all transformation blocks published by other organizations, available for all organizations."""
    pass


@api(
    "/api/organizations/{organizationId}/transformation/public/{transformationId}",
    method="get",
)
def getPublicOrganizationTransformationBlock(
    organizationId: str, transformationId: str
) -> GetPublicOrganizationTransformationBlockResponse:
    """Retrieve a transformation blocks published by other organizations, available for all organizations."""
    pass


@api(
    "/api/organizations/{organizationId}/transformation/{transformationId}",
    method="get",
)
def getOrganizationTransformationBlock(
    organizationId: str, transformationId: str
) -> GetOrganizationTransformationBlockResponse:
    """Get a transformation block."""
    pass


@api("/api/organizations/{organizationId}/deploy", method="get")
def listOrganizationDeployBlocks(
    organizationId: str,
) -> ListOrganizationDeployBlocksResponse:
    """Retrieve all deploy blocks."""
    pass


@api("/api/organizations/{organizationId}/deploy/{deployId}", method="get")
def getOrganizationDeployBlock(
    organizationId: str, deployId: str
) -> GetOrganizationDeployBlockResponse:
    """Gets a deploy block."""
    pass


@api("/api/organizations/{organizationId}/dsp", method="get")
def listOrganizationDspBlocks(organizationId: str) -> ListOrganizationDspBlocksResponse:
    """Retrieve all dsp blocks."""
    pass


@api("/api/organizations/{organizationId}/dsp/{dspId}", method="get")
def getOrganizationDspBlock(
    organizationId: str, dspId: str
) -> GetOrganizationDspBlockResponse:
    """Gets a dsp block."""
    pass


@api("/api/organizations/{organizationId}/transfer-learning", method="get")
def listOrganizationTransferLearningBlocks(
    organizationId: str,
) -> ListOrganizationTransferLearningBlocksResponse:
    """Retrieve all transfer learning blocks."""
    pass


@api(
    "/api/organizations/{organizationId}/transfer-learning/{transferLearningId}",
    method="get",
)
def getOrganizationTransferLearningBlock(
    organizationId: str, transferLearningId: str
) -> GetOrganizationTransferLearningBlockResponse:
    """Gets a transfer learning block."""
    pass


@api("/api/organizations/{organizationId}/secrets", method="get")
def listOrganizationSecrets(organizationId: str) -> ListOrganizationSecretsResponse:
    """Retrieve all secrets."""
    pass


@api("/api/organizations/{organizationId}/transformation", method="post")
def addOrganizationTransformationBlock(
    organizationId: str, requestBody: AddOrganizationTransformationBlockRequest
) -> EntityCreatedResponse:
    """Adds a transformation block."""
    pass


@api(
    "/api/organizations/{organizationId}/transformation/{transformationId}",
    method="post",
)
def updateOrganizationTransformationBlock(
    organizationId: str,
    transformationId: str,
    requestBody: UpdateOrganizationTransformationBlockRequest,
) -> GenericApiResponse:
    """Updates a transformation block. Only values in the body will be updated."""
    pass


@api(
    "/api/organizations/{organizationId}/transformation/{transformationId}/export",
    method="post",
)
def exportOrganizationTransformationBlock(
    organizationId: str, transformationId: str
) -> ExportBlockResponse:
    """Download the source code for this block."""
    pass


@api("/api/organizations/{organizationId}/deploy", method="post")
def addOrganizationDeployBlock(
    organizationId: str, requestBody: AddOrganizationDeployBlockRequest
) -> EntityCreatedResponse:
    """Adds a deploy block."""
    pass


@api("/api/organizations/{organizationId}/deploy/{deployId}", method="post")
def updateOrganizationDeployBlock(
    organizationId: str,
    deployId: str,
    requestBody: UpdateOrganizationDeployBlockRequest,
) -> GenericApiResponse:
    """Updates a deploy block. Only values in the body will be updated."""
    pass


@api("/api/organizations/{organizationId}/deploy/{deployId}/export", method="post")
def exportOrganizationDeployBlock(
    organizationId: str, deployId: str
) -> ExportBlockResponse:
    """Download the source code for this block."""
    pass


@api("/api/organizations/{organizationId}/dsp", method="post")
def addOrganizationDspBlock(
    organizationId: str, requestBody: AddOrganizationDspBlockRequest
) -> EntityCreatedResponse:
    """Adds a dsp block."""
    pass


@api("/api/organizations/{organizationId}/dsp/{dspId}", method="post")
def updateOrganizationDspBlock(
    organizationId: str, dspId: str, requestBody: UpdateOrganizationDspBlockRequest
) -> GenericApiResponse:
    """Updates a dsp block. Only values in the body will be updated."""
    pass


@api("/api/organizations/{organizationId}/dsp/{dspId}/export", method="post")
def exportOrganizationDspBlock(organizationId: str, dspId: str) -> ExportBlockResponse:
    """Download the source code for this block."""
    pass


@api("/api/organizations/{organizationId}/dsp/{dspId}/retry", method="post")
def retryOrganizationDspBlock(organizationId: str, dspId: str) -> GenericApiResponse:
    """Retry launch a dsp block."""
    pass


@api("/api/organizations/{organizationId}/transfer-learning", method="post")
def addOrganizationTransferLearningBlock(
    organizationId: str, requestBody: AddOrganizationTransferLearningBlockRequest
) -> EntityCreatedResponse:
    """Adds a transfer learning block."""
    pass


@api(
    "/api/organizations/{organizationId}/transfer-learning/{transferLearningId}",
    method="post",
)
def updateOrganizationTransferLearningBlock(
    organizationId: str,
    transferLearningId: str,
    requestBody: UpdateOrganizationTransferLearningBlockRequest,
) -> GenericApiResponse:
    """Updates a transfer learning block. Only values in the body will be updated."""
    pass


@api(
    "/api/organizations/{organizationId}/transfer-learning/{transferLearningId}/export",
    method="post",
)
def exportOrganizationTransferLearningBlock(
    organizationId: str, transferLearningId: str
) -> ExportBlockResponse:
    """Download the source code for this block."""
    pass


@api("/api/organizations/{organizationId}/secrets", method="post")
def addOrganizationSecret(
    organizationId: str, requestBody: AddOrganizationSecretRequest
) -> EntityCreatedResponse:
    """Adds a secret."""
    pass


@api(
    "/api/organizations/{organizationId}/transformation/{transformationId}",
    method="delete",
)
def deleteOrganizationTransformationBlock(
    organizationId: str, transformationId: str
) -> GenericApiResponse:
    """Deletes a transformation block."""
    pass


@api("/api/organizations/{organizationId}/deploy/{deployId}", method="delete")
def deleteOrganizationDeployBlock(
    organizationId: str, deployId: str
) -> GenericApiResponse:
    """Deletes a deploy block."""
    pass


@api("/api/organizations/{organizationId}/dsp/{dspId}", method="delete")
def deleteOrganizationDspBlock(organizationId: str, dspId: str) -> GenericApiResponse:
    """Deletes a dsp block."""
    pass


@api(
    "/api/organizations/{organizationId}/transfer-learning/{transferLearningId}",
    method="delete",
)
def deleteOrganizationTransferLearningBlock(
    organizationId: str, transferLearningId: str
) -> GenericApiResponse:
    """Deletes a transfer learning block."""
    pass


@api("/api/organizations/{organizationId}/secrets/{secretId}", method="delete")
def deleteOrganizationSecret(organizationId: str, secretId: str) -> GenericApiResponse:
    """Deletes a secret"""
    pass


@api("/api/organizations/{organizationId}/jobs", method="get")
def listActiveOrganizationJobs(
    organizationId: str, rootOnly: str = None
) -> ListJobsResponse:
    """Get all active jobs for this organization"""
    pass


@api("/api/organizations/{organizationId}/jobs/history", method="get")
def listFinishedOrganizationJobs(
    organizationId: str,
    startDate: str = None,
    endDate: str = None,
    limit: str = None,
    offset: str = None,
    rootOnly: str = None,
) -> ListJobsResponse:
    """Get all finished jobs for this organization"""
    pass


@api("/api/organizations/{organizationId}/jobs/all", method="get")
def listAllOrganizationJobs(
    organizationId: str,
    startDate: str = None,
    endDate: str = None,
    limit: str = None,
    offset: str = None,
    excludePipelineTransformJobs: str = None,
    rootOnly: str = None,
    key: str = None,
    category: str = None,
) -> ListJobsResponse:
    """Get all jobs for this organization"""
    pass


@api("/api/organizations/{organizationId}/jobs/{jobId}/status", method="get")
def getOrganizationJobStatus(organizationId: str, jobId: str) -> GetJobResponse:
    """Get the status for a job."""
    pass


@api("/api/organizations/{organizationId}/jobs/{jobId}/stdout", method="get")
def getOrganizationJobsLogs(
    organizationId: str, jobId: str, limit: str = None, logLevel: str = None
) -> LogStdoutResponse:
    """Get the logs for a job."""
    pass


@api("/api/organizations/{organizationId}/jobs/{jobId}/stdout/download", method="get")
def downloadOrganizationJobsLogs(
    organizationId: str, jobId: str, limit: str = None, logLevel: str = None
) -> None:
    """Download the logs for a job (as a text file)."""
    pass


@api("/api/organizations/{organizationId}/socket-token", method="get")
def getOrganizationSocketToken(organizationId: str) -> SocketTokenResponse:
    """Get a token to authenticate with the web socket interface."""
    pass


@api("/api/organizations/{organizationId}/jobs/{jobId}/cancel", method="post")
def cancelOrganizationJob(
    organizationId: str, jobId: str, forceCancel: str = None
) -> GenericApiResponse:
    """Cancel a running job."""
    pass


@api("/api/organizations/{organizationId}/pipelines", method="get")
def listOrganizationPipelines(
    organizationId: str, projectId: str = None
) -> ListOrganizationPipelinesResponse:
    """Retrieve all organizational pipelines"""
    pass


@api("/api/organizations/{organizationId}/pipelines/archived", method="get")
def listArchivedOrganizationPipelines(
    organizationId: str, projectId: str = None
) -> ListOrganizationPipelinesResponse:
    """Retrieve all archived organizational pipelines"""
    pass


@api("/api/organizations/{organizationId}/pipelines/{pipelineId}", method="get")
def getOrganizationPipeline(
    organizationId: str, pipelineId: str
) -> GetOrganizationPipelinesResponse:
    """Retrieve an organizational pipelines"""
    pass


@api("/api/organizations/{organizationId}/pipelines", method="post")
def createOrganizationPipeline(
    organizationId: str, requestBody: OrganizationUpdatePipelineBody
) -> EntityCreatedResponse:
    """Create an organizational pipelines"""
    pass


@api("/api/organizations/{organizationId}/pipelines/{pipelineId}", method="post")
def updateOrganizationPipeline(
    organizationId: str, pipelineId: str, requestBody: OrganizationUpdatePipelineBody
) -> GenericApiResponse:
    """Update an organizational pipelines"""
    pass


@api("/api/organizations/{organizationId}/pipelines/{pipelineId}/run", method="post")
def runOrganizationPipeline(
    organizationId: str, pipelineId: str, ignoreLastSuccessfulRun: str = None
) -> RunOrganizationPipelineResponse:
    """Run an organizational pipeline"""
    pass


@api("/api/organizations/{organizationId}/pipelines/{pipelineId}/stop", method="post")
def stopOrganizationPipeline(
    organizationId: str, pipelineId: str
) -> GenericApiResponse:
    """Stops the pipeline, and marks it as failed."""
    pass


@api("/api/organizations/{organizationId}/pipelines/{pipelineId}", method="delete")
def deleteOrganizationPipeline(
    organizationId: str, pipelineId: str
) -> GenericApiResponse:
    """Delete an organizational pipelines"""
    pass


@api("/api-usercdn", method="get")
def getUserCDNResource(path: str) -> None:
    """Proxy function to retrieve data from the user CDN. This function is only used during development."""
    pass


@api("/api/organizations/{organizationId}/campaign-dashboards", method="get")
def getOrganizationDataCampaignDashboards(
    organizationId: str,
) -> GetOrganizationDataCampaignDashboardsResponse:
    """List all data campaign dashboards"""
    pass


@api(
    "/api/organizations/{organizationId}/campaign-dashboard/{campaignDashboardId}",
    method="get",
)
def getOrganizationDataCampaignDashboard(
    organizationId: str, campaignDashboardId: str
) -> GetOrganizationDataCampaignDashboardResponse:
    """Get a data campaign dashboard"""
    pass


@api(
    "/api/organizations/{organizationId}/campaign-dashboard/{campaignDashboardId}/campaigns",
    method="get",
)
def getOrganizationDataCampaignsForDashboard(
    organizationId: str, campaignDashboardId: str
) -> GetOrganizationDataCampaignsResponse:
    """Get a list of all data campaigns for a dashboard"""
    pass


@api("/api/organizations/{organizationId}/campaigns/{campaignId}", method="get")
def getOrganizationDataCampaign(
    organizationId: str, campaignId: str
) -> GetOrganizationDataCampaignResponse:
    """Get a data campaign"""
    pass


@api("/api/organizations/{organizationId}/campaign-dashboards", method="post")
def addOrganizationDataCampaignDashboard(
    organizationId: str, requestBody: AddOrganizationDataCampaignDashboardRequest
) -> AddOrganizationDataCampaignDashboardResponse:
    """Add a new data campaign dashboard"""
    pass


@api(
    "/api/organizations/{organizationId}/campaign-dashboard/{campaignDashboardId}",
    method="post",
)
def updateOrganizationDataCampaignDashboard(
    organizationId: str,
    campaignDashboardId: str,
    requestBody: UpdateOrganizationDataCampaignDashboardRequest,
) -> GenericApiResponse:
    """Update a data campaign dashboard"""
    pass


@api(
    "/api/organizations/{organizationId}/campaign-dashboard/{campaignDashboardId}/screenshot",
    method="post",
)
def uploadDashboardScreenshot(
    organizationId: str, campaignDashboardId: str, requestBody: UploadImageRequest
) -> GenericApiResponse:
    """Used internally to upload a picture of a screenshot"""
    pass


@api("/api/organizations/{organizationId}/campaigns", method="post")
def addOrganizationDataCampaign(
    organizationId: str, requestBody: AddOrganizationDataCampaignRequest
) -> AddOrganizationDataCampaignResponse:
    """Add a new data campaign to a data campaign dashboard"""
    pass


@api("/api/organizations/{organizationId}/campaigns/{campaignId}", method="post")
def updateOrganizationDataCampaign(
    organizationId: str,
    campaignId: str,
    requestBody: UpdateOrganizationDataCampaignRequest,
) -> GenericApiResponse:
    """Update a data campaign"""
    pass


@api("/api/organizations/{organizationId}/campaigns/{campaignId}/diff", method="post")
def getOrganizationDataCampaignDiff(
    organizationId: str,
    campaignId: str,
    requestBody: OrganizationDataCampaignDiffRequest,
) -> OrganizationDataCampaignDiffResponse:
    """Get which items have changed for a data campaign. You post the data points and we'll return which data items are different in the past day."""
    pass


@api(
    "/api/organizations/{organizationId}/campaign-dashboard/{campaignDashboardId}",
    method="delete",
)
def deleteOrganizationDataCampaignDashboard(
    organizationId: str, campaignDashboardId: str
) -> GenericApiResponse:
    """Delete a data campaign dashboard"""
    pass


@api("/api/organizations/{organizationId}/campaigns/{campaignId}", method="delete")
def deleteOrganizationDataCampaign(
    organizationId: str, campaignId: str
) -> GenericApiResponse:
    """Delete a data campaign"""
    pass


@api("/api-health", method="get")
def health(requester: str = None) -> GenericApiResponse:
    """Get studio web containers health."""
    pass


@api("/api/api-health", method="get")
def apiHealth(requester: str = None) -> GenericApiResponse:
    """Get studio api containers health."""
    pass


@api("/api-feature-flags", method="get")
def getFeatureFlags() -> GetFeatureFlagsResponse:
    """Get the current global feature flags and whether they are enabled"""
    pass


@api("/api/admin/metrics", method="get")
def adminGetMetrics() -> AdminGetMetricsResponse:
    """Admin-only API to get global metrics."""
    pass


@api("/api/admin/metrics/reports", method="get")
def adminGetMetricsReports(
    limit: str = None, offset: str = None
) -> AdminGetReportsResponse:
    """Admin-only API to get global metrics reports."""
    pass


@api("/api/admin/metrics/reports/{reportId}", method="get")
def adminGetMetricsReport(reportId: str) -> AdminGetReportResponse:
    """Admin-only API to get a global metrics report."""
    pass


@api("/api/admin/metrics/reports/{reportId}/download", method="get")
def adminDownloadMetricsReport(reportId: str) -> Any:
    """Admin-only API to download a global metrics report."""
    pass


@api("/api/admin/infra/migrations", method="get")
def adminGetDataMigrations() -> AdminGetDataMigrationsResponse:
    """Admin-only API to get data migrations."""
    pass


@api("/api/admin/infra/migrations/{migrationId}", method="get")
def adminGetDataMigration(migrationId: str) -> AdminGetDataMigrationResponse:
    """Admin-only API to get a data migration."""
    pass


@api("/api/admin/infra/disallowedEmailDomains", method="get")
def adminGetDisallowedEmailDomains() -> AdminGetDisallowedEmailDomainsResponse:
    """Admin-only API to get the list of disallowed email domains."""
    pass


@api("/api/admin/infra/featureFlags", method="get")
def adminGetFeatureFlags() -> GetFeatureFlagsResponse:
    """Admin-only API to get all feature flags."""
    pass


@api("/api/admin/infra/config", method="get")
def adminGetStudioConfig() -> GetStudioConfigResponse:
    """Admin-only API to get all studio config."""
    pass


@api("/api/admin/users", method="get")
def adminGetUsers(
    active: str = None,
    tier: str = None,
    fields: str = None,
    sort: str = None,
    filters: str = None,
    limit: str = None,
    offset: str = None,
    search: str = None,
) -> AdminGetUsersResponse:
    """Admin-only API to get the list of all registered users."""
    pass


@api("/api/admin/users/{userId}", method="get")
def adminGetUser(userId: str) -> AdminGetUserResponse:
    """Admin-only API to get information about a user."""
    pass


@api("/api/admin/users/{userId}/metrics", method="get")
def adminGetUserMetrics(userId: str) -> AdminGetUserMetricsResponse:
    """Admin-only API to get marketing metrics about a user."""
    pass


@api("/api/admin/users/{userId}/jobs", method="get")
def adminGetUserJobs(
    userId: str, limit: str = None, offset: str = None
) -> ListJobsResponse:
    """Admin-only API to get the list of all project jobs for a user."""
    pass


@api("/api/admin/trials/{enterpriseTrialId}", method="get")
def adminGetTrial(enterpriseTrialId: str) -> AdminGetTrialResponse:
    """Admin-only API to get a specific enterprise trial."""
    pass


@api("/api/admin/projects", method="get")
def adminGetProjects(
    active: str = None,
    sort: str = None,
    filters: str = None,
    limit: str = None,
    offset: str = None,
    search: str = None,
) -> AdminListProjectsResponse:
    """Admin-only API to get the list of all projects."""
    pass


@api("/api/admin/projects/{projectId}", method="get")
def adminGetProject(projectId: str) -> ProjectInfoResponse:
    """Admin-only API to get project information."""
    pass


@api("/api/admin/projects/{projectId}/jobs", method="get")
def adminGetProjectJobs(
    projectId: str, limit: str = None, offset: str = None
) -> ListJobsResponse:
    """Admin-only API to get the list of all jobs for a project."""
    pass


@api("/api/admin/organizations", method="get")
def adminGetOrganizations(
    active: str = None,
    includeDeleted: str = None,
    sort: str = None,
    filters: str = None,
    limit: str = None,
    offset: str = None,
    search: str = None,
) -> AdminGetOrganizationsResponse:
    """Admin-only API to get the list of all organizations."""
    pass


@api("/api/admin/organizations/{organizationId}", method="get")
def adminGetOrganizationInfo(
    organizationId: str, includeDeleted: str = None
) -> AdminOrganizationInfoResponse:
    """Admin-only API to list all information about this organization."""
    pass


@api("/api/admin/organizations/{organizationId}/usage/computeTime", method="get")
def adminGetOrganizationComputeTimeUsage(
    organizationId: str, startDate: str, endDate: str
) -> AdminGetOrganizationComputeTimeUsageResponse:
    """Admin-only API to get compute time usage for an organization over a period of time."""
    pass


@api("/api/admin/organizations/{organizationId}/usage/reports", method="get")
def adminGetOrganizationUsageReports(
    organizationId: str, limit: str = None, offset: str = None
) -> AdminGetReportsResponse:
    """Admin-only API to get all usage reports for an organization."""
    pass


@api("/api/admin/organizations/{organizationId}/usage/reports/{reportId}", method="get")
def adminGetOrganizationUsageReport(
    organizationId: str, reportId: str
) -> AdminGetReportResponse:
    """Admin-only API to get a usage report for an organization."""
    pass


@api(
    "/api/admin/organizations/{organizationId}/usage/reports/{reportId}/download",
    method="get",
)
def adminDownloadOrganizationUsageReport(organizationId: str, reportId: str) -> Any:
    """Admin-only API to download a usage report for an organization."""
    pass


@api("/api/admin/organizations/{organizationId}/exports", method="get")
def adminGetOrganizationDataExports(
    organizationId: str, limit: str = None, offset: str = None
) -> GetOrganizationDataExportsResponse:
    """Admin-only API to get the list of all data exports for an organization."""
    pass


@api("/api/admin/organizations/{organizationId}/exports/{exportId}", method="get")
def adminGetOrganizationDataExport(
    organizationId: str, exportId: str
) -> GetOrganizationDataExportResponse:
    """Admin-only API to get a data export for an organization."""
    pass


@api("/api/admin/organizations/{organizationId}/jobs", method="get")
def adminGetOrganizationJobs(
    organizationId: str, limit: str = None, offset: str = None
) -> ListJobsResponse:
    """Admin-only API to get the list of all jobs for a organization."""
    pass


@api("/api/admin/sso", method="get")
def adminGetSSOSettings() -> AdminGetSSOSettingsResponse:
    """Admin-only API to get the SSO settings."""
    pass


@api("/api/admin/sso/{domainName}", method="get")
def adminGetSSODomainIdPs(domainName: str) -> AdminGetSSODomainIdPsResponse:
    """Admin-only API to get the list of identity providers enabled for a given domain."""
    pass


@api("/api/admin/jobs/{jobId}/details", method="get")
def adminGetJobDetails(
    jobId: str, parentType: str, includeChildrenJobs: str = None
) -> JobDetailsResponse:
    """Get the job execution details including inner jobs"""
    pass


@api("/api/admin/jobs/{jobId}/logs", method="get")
def adminGetJobsLogs(
    jobId: str, parentType: str, limit: str, offset: str
) -> JobLogsResponse:
    """Get the logs for a job."""
    pass


@api("/api/admin/jobs/{jobId}/metrics", method="get")
def adminGetJobsMetrics(jobId: str, parentType: str) -> JobMetricsResponse:
    """Get cpu/memory usage metrics, if the job is a Kubernetes job"""
    pass


@api("/api/admin/emails/{email}/verification-code", method="get")
def adminGetEmailVerificationCode(email: str) -> GetEmailVerificationCodeResponse:
    """Get the enterprise trial verification code of the specified email."""
    pass


@api("/api/admin/find-user", method="get")
def adminFindUser(query: str) -> FindUserResponse:
    """DEPRECATED. Admin-only API to find a user by username or email address."""
    pass


@api("/api/admin/users-ids", method="get")
def adminGetAllUserIds() -> AdminGetUserIdsResponse:
    """DEPRECATED. Admin-only API to get list of all users."""
    pass


@api("/api/admin/users-ids/active", method="get")
def adminGetAllActiveUserIds() -> AdminGetUserIdsResponse:
    """DEPRECATED. Admin-only API to get list of all users that have been active in the past 30 days."""
    pass


@api("/api/admin/metrics/reports", method="post")
def adminCreateMetricsReport(startDate: str, endDate: str) -> StartJobResponse:
    """Admin-only API to create a new global metrics report. A job is created to process the report request and the job details are returned in the response."""
    pass


@api("/api/admin/infra/migrations/{migrationId}", method="post")
def adminToggleDataMigration(
    migrationId: str, requestBody: AdminToggleDataMigrationRequest
) -> GenericApiResponse:
    """Admin-only API to run or pause a data migration."""
    pass


@api("/api/admin/infra/config/{configKey}", method="post")
def adminSetStudioConfig(
    configKey: str, requestBody: AdminUpdateConfigRequest
) -> GenericApiResponse:
    """Admin-only API to update a studio config item."""
    pass


@api("/api/admin/users/{userId}", method="post")
def adminUpdateUser(
    userId: str, requestBody: AdminUpdateUserRequest
) -> GenericApiResponse:
    """Admin-only API to update user properties."""
    pass


@api("/api/admin/users/{userId}/permissions", method="post")
def adminUpdateUserPermissions(
    userId: str, requestBody: AdminUpdateUserPermissionsRequest
) -> GenericApiResponse:
    """Admin-only API to update the list of permissions for a user."""
    pass


@api("/api/admin/trials", method="post")
def adminCreateTrial(
    requestBody: AdminStartEnterpriseTrialRequest,
) -> EntityCreatedResponse:
    """Admin-only API to create an enterprise trial for a user."""
    pass


@api("/api/admin/trials/{enterpriseTrialId}/upgrade", method="post")
def adminUpgradeTrial(enterpriseTrialId: str) -> GenericApiResponse:
    """Admin-only API to upgrade a specific enterprise trial to a full enterprise account."""
    pass


@api("/api/admin/projects", method="post")
def adminCreateProject(requestBody: AdminCreateProjectRequest) -> CreateProjectResponse:
    """Admin-only API to create a new free tier project."""
    pass


@api("/api/admin/projects/{projectId}", method="post")
def adminUpdateProject(
    projectId: str, requestBody: UpdateProjectRequest
) -> GenericApiResponse:
    """Admin-only API to update project properties."""
    pass


@api("/api/admin/projects/{projectId}/members", method="post")
def adminAddUserToProject(
    projectId: str, requestBody: AdminAddProjectUserRequest
) -> GenericApiResponse:
    """Admin-only API to add a user to a project. If no user is provided, the current user is used."""
    pass


@api("/api/admin/organizations", method="post")
def adminCreateOrganization(
    requestBody: AdminCreateOrganizationRequest,
) -> CreateOrganizationResponse:
    """Admin-only API to create a new organization."""
    pass


@api("/api/admin/organizations/{organizationId}", method="post")
def adminUpdateOrganization(
    organizationId: str, requestBody: AdminUpdateOrganizationRequest
) -> GenericApiResponse:
    """Admin-only API to update organization properties such as name and logo."""
    pass


@api("/api/admin/organizations/{organizationId}/restore", method="post")
def adminRestoreOrganization(organizationId: str) -> GenericApiResponse:
    """Admin-only API to restore a soft deleted organization. All organization projects sharing the same deletion date as that of the organization will also be restored. If this is a trial organization that was never upgraded to a paid plan then the organization will be restored to its original trial state."""
    pass


@api("/api/admin/organizations/{organizationId}/usage/reports", method="post")
def adminCreateOrganizationUsageReport(
    organizationId: str, startDate: str, endDate: str
) -> StartJobResponse:
    """Admin-only API to create a new usage report for an organization. A job is created to process the report request and the job details are returned in the response."""
    pass


@api("/api/admin/organizations/{organizationId}/members", method="post")
def adminAddUserToOrganization(
    organizationId: str, requestBody: AdminAddOrganizationUserRequest
) -> GenericApiResponse:
    """Admin-only API to add a user to an organization. If no user is provided, the current user is used."""
    pass


@api("/api/admin/organizations/{organizationId}/projects", method="post")
def adminCreateOrganizationProject(
    organizationId: str, requestBody: AdminCreateProjectRequest
) -> CreateProjectResponse:
    """Admin-only API to create a new project for an organization."""
    pass


@api("/api/admin/organizations/{organizationId}/exports", method="post")
def adminCreateOrganizationDataExport(
    organizationId: str, requestBody: AdminCreateOrganizationDataExportRequest
) -> StartJobResponse:
    """Admin-only API to create a new data export for an organization. A job is created to process the export request and the job details are returned in the response."""
    pass


@api("/api/admin/projects/{projectId}/add", method="post")
def adminAddUserToProjectDeprecated(projectId: str) -> GenericApiResponse:
    """DEPRECATED. Admin-only API to add the current user to a project."""
    pass


@api("/api/admin/projects/{projectId}/remove", method="post")
def adminRemoveUserFromProjectDeprecated(projectId: str) -> GenericApiResponse:
    """DEPRECATED. Admin-only API to remove the current user from a project."""
    pass


@api("/api/admin/metrics/reports/{reportId}", method="delete")
def adminDeleteMetricsReport(reportId: str) -> GenericApiResponse:
    """Admin-only API to delete a global metrics report."""
    pass


@api("/api/admin/infra/disallowedEmailDomains/{domainName}", method="delete")
def adminDeleteDisallowedEmailDomain(domainName: str) -> GenericApiResponse:
    """Admin-only API to delete an email domain from the list of disallowed email domains."""
    pass


@api("/api/admin/infra/featureFlags/{featureId}", method="delete")
def adminDisableFeature(featureId: str) -> GenericApiResponse:
    """Admin-only API to delete a feature flag. Deleting a feature flag essentially disables the feature for all users."""
    pass


@api("/api/admin/infra/config/{configKey}", method="delete")
def adminDeleteStudioConfig(configKey: str) -> GenericApiResponse:
    """Admin-only API to delete a studio config item."""
    pass


@api("/api/admin/users/{userId}", method="delete")
def adminDeleteUser(userId: str) -> StartJobResponse:
    """Admin-only API to delete a user."""
    pass


@api("/api/admin/trials/{enterpriseTrialId}", method="delete")
def adminDeleteTrial(enterpriseTrialId: str) -> GenericApiResponse:
    """Admin-only API to delete an enterprise trial."""
    pass


@api("/api/admin/projects/{projectId}", method="delete")
def adminDeleteProject(projectId: str) -> GenericApiResponse:
    """Admin-only API to delete a project."""
    pass


@api("/api/admin/projects/{projectId}/members/{userId}", method="delete")
def adminRemoveUserFromProject(projectId: str, userId: str) -> GenericApiResponse:
    """Admin-only API to remove a user from a project."""
    pass


@api("/api/admin/organizations/{organizationId}", method="delete")
def adminDeleteOrganization(
    organizationId: str, fullDeletion: str = None
) -> GenericApiResponse:
    """Admin-only API to delete an organization. If `fullDeletion` is set, it deletes the organization's identifiable information and files. Otherwise, it soft deletes the organization by setting its `delete_date` value."""
    pass


@api(
    "/api/admin/organizations/{organizationId}/usage/reports/{reportId}",
    method="delete",
)
def adminDeleteOrganizationUsageReport(
    organizationId: str, reportId: str
) -> GenericApiResponse:
    """Admin-only API to delete a usage report for an organization."""
    pass


@api("/api/admin/organizations/{organizationId}/members/{userId}", method="delete")
def adminRemoveUserFromOrganization(
    organizationId: str, userId: str
) -> GenericApiResponse:
    """Admin-only API to remove a user from an organization."""
    pass


@api("/api/admin/organizations/{organizationId}/exports/{exportId}", method="delete")
def adminDeleteOrganizationDataExport(
    organizationId: str, exportId: str
) -> GenericApiResponse:
    """Admin-only API to delete a data export for an organization."""
    pass


@api("/api/admin/sso/{domainName}", method="delete")
def adminDeleteSSODomainIdPs(domainName: str) -> GenericApiResponse:
    """Admin-only API to delete the list of identity providers for a given domain."""
    pass


@api("/api/admin/infra/disallowedEmailDomains", method="put")
def adminAddDisallowedEmailDomain(
    requestBody: AdminAddDisallowedEmailDomainRequest,
) -> GenericApiResponse:
    """Admin-only API to add an email domain to the list of disallowed email domains."""
    pass


@api("/api/admin/infra/featureFlags/{featureId}", method="put")
def adminEnableFeature(featureId: str) -> GenericApiResponse:
    """Admin-only API to set a feature flag ON. Setting a feature flag ON essentially enables the feature for all users."""
    pass


@api("/api/admin/trials/{enterpriseTrialId}", method="put")
def adminUpdateTrial(
    enterpriseTrialId: str, requestBody: AdminUpdateTrialRequest
) -> GenericApiResponse:
    """Admin-only API to update an enterprise trial."""
    pass


@api("/api/admin/organizations/{organizationId}/exports/{exportId}", method="put")
def adminUpdateOrganizationDataExport(
    organizationId: str,
    exportId: str,
    requestBody: AdminUpdateOrganizationDataExportRequest,
) -> GenericApiResponse:
    """Admin-only API to update a data export for an organization."""
    pass


@api("/api/admin/sso/{domainName}", method="put")
def adminAddOrUpdateSSODomainIdPs(
    domainName: str, requestBody: AdminAddOrUpdateSSODomainIdPsRequest
) -> GenericApiResponse:
    """Admin-only API to set the list of identity provider for a given domain."""
    pass


@api("/api-metrics", method="get")
def getPublicMetrics() -> GetPublicMetricsResponse:
    """Get information about number of projects, compute and data samples. Updated once per hour."""
    pass


@api("/api-metrics/website/pageviews", method="post")
def logWebsitePageview(requestBody: LogWebsitePageviewRequest) -> GenericApiResponse:
    """Log a website pageview. Used for website analytics."""
    pass


@api("/api-metrics/events", method="post")
def logAnalyticsEvent(requestBody: LogAnalyticsEventRequest) -> GenericApiResponse:
    """Log an analytics event."""
    pass


@api("/api/portals/{portalId}", method="get")
def getPortalInfo(portalId: str) -> PortalInfoResponse:
    """Get information about a portal"""
    pass


@api("/api/portals/{portalId}/files/view", method="get")
def viewPortalFile(portalId: str, path: str) -> File:
    """View a file that's located in an upload portal (requires JWT auth). File might be converted (e.g. Parquet) or truncated (e.g. CSV)."""
    pass


@api("/api/portals/{portalId}/upload-link", method="post")
def createSignedUploadLink(
    portalId: str, requestBody: CreateSignedUploadLinkRequest
) -> CreateSignedUploadLinkResponse:
    """Creates a signed link to securely upload data to s3 bucket directly from the client."""
    pass


@api("/api/portals/{portalId}/files", method="post")
def listPortalFilesInFolder(
    portalId: str, requestBody: ListPortalFilesInFolderRequest
) -> ListPortalFilesInFolderResponse:
    """List all files and directories in specified prefix."""
    pass


@api("/api/portals/{portalId}/files/delete", method="post")
def deletePortalFile(
    portalId: str, requestBody: DeletePortalFileRequest
) -> GenericApiResponse:
    """Delete a file from an upload portal (requires JWT auth)."""
    pass


@api("/api/portals/{portalId}/files/rename", method="post")
def renamePortalFile(
    portalId: str, requestBody: RenamePortalFileRequest
) -> GenericApiResponse:
    """Rename a file on an upload portal (requires JWT auth)."""
    pass


@api("/api/portals/{portalId}/files/download", method="post")
def downloadPortalFile(
    portalId: str, requestBody: DownloadPortalFileRequest
) -> DownloadPortalFileResponse:
    """Download a file from an upload portal (requires JWT auth). Will return a signed URL to the bucket."""
    pass


@api("/api/organizations/{organizationId}/portals", method="get")
def listOrganizationPortals(organizationId: str) -> ListOrganizationPortalsResponse:
    """Retrieve all configured upload portals."""
    pass


@api("/api/organizations/{organizationId}/portals/{portalId}", method="get")
def getOrganizationPortal(
    organizationId: str, portalId: str
) -> GetOrganizationPortalResponse:
    """Retrieve a single upload portals identified by ID."""
    pass


@api("/api/organizations/{organizationId}/portals/{portalId}/verify", method="get")
def verifyOrganizationPortal(
    organizationId: str, portalId: str
) -> VerifyOrganizationBucketResponse:
    """Retrieve a subset of files from the portal, to be used in the data source wizard."""
    pass


@api("/api/organizations/{organizationId}/portals/create", method="post")
def createOrganizationPortal(
    organizationId: str, requestBody: CreateOrganizationPortalRequest
) -> CreateOrganizationPortalResponse:
    """Creates a new upload portal for the organization."""
    pass


@api("/api/organizations/{organizationId}/portals/{portalId}/update", method="put")
def updateOrganizationPortal(
    organizationId: str, portalId: str, requestBody: CreateOrganizationPortalRequest
) -> UpdateOrganizationPortalResponse:
    """Updates an upload portal for the organization."""
    pass


@api(
    "/api/organizations/{organizationId}/portals/{portalId}/rotate-token",
    method="delete",
)
def rotateOrganizationPortalToken(
    organizationId: str, portalId: str
) -> GenericApiResponse:
    """Rotates the token for an upload portal."""
    pass


@api("/api/organizations/{organizationId}/portals/{portalId}/delete", method="delete")
def deleteOrganizationPortal(organizationId: str, portalId: str) -> GenericApiResponse:
    """Deletes an upload portal for the organization."""
    pass


@api("/api/emails/{email}/request-verification", method="post")
def requestEmailVerification(
    email: str, requestBody: RequestEmailVerificationRequest
) -> EntityCreatedResponse:
    """Request an email activation code to be sent to the specified email address."""
    pass


@api("/api/emails/verify", method="post")
def verifyEmail(requestBody: ActivateUserOrVerifyEmailRequest) -> VerifyEmailResponse:
    """Verify an email address using the specified verification code."""
    pass


@api("/api/emails/validate", method="post")
def validateEmail(requestBody: EmailValidationRequest) -> ValidateEmailResponse:
    """Validate whether an email is valid for sign up. Using an email that fails this check can result in the associated account missing communications and features that are distributed through email."""
    pass


@api("/api/emails/{emailId}", method="get")
def getEmailVerificationStatus(emailId: str) -> GetEmailVerificationStatusResponse:
    """Get the status of an email verification."""
    pass
