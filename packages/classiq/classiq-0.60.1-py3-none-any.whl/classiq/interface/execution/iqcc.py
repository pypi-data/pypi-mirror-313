from classiq.interface.helpers.versioned_model import VersionedModel


class IQCCInitAuthData(VersionedModel):
    auth_scope_id: str
    auth_method_id: str


class IQCCInitAuthResponse(VersionedModel):
    auth_url: str
    token_id: str


class IQCCProbeAuthData(IQCCInitAuthData):
    token_id: str


class IQCCProbeAuthResponse(VersionedModel):
    auth_token: str
