from connector.generated import (
    CapabilityName,
    OAuthCredential,
    ValidateCredentialsRequest,
    ValidateCredentialsResponse,
    ValidatedCredentials,
)
from connector.oai.integration import DescriptionData, Integration
from connector.oai.modules.oauth_module_types import OAuthSettings


async def test_scopes_for_capabilities():
    """Test if scopes are set for each implemented capability."""
    app_id = "test"
    integration = Integration(
        app_id=app_id,
        version="0.1.0",
        auth=OAuthCredential,
        oauth_settings=OAuthSettings(
            authorization_url="https://test.com/authorize",
            token_url="https://test.com/token",
            scopes={
                CapabilityName.VALIDATE_CREDENTIALS: "test",
            },
        ),
        description_data=DescriptionData(user_friendly_name="test_scopes.py", categories=[]),
        exception_handlers=[],
        handle_errors=True,
    )

    @integration.register_capability(CapabilityName.VALIDATE_CREDENTIALS)
    async def validate_credentials(args: ValidateCredentialsRequest) -> ValidateCredentialsResponse:
        return ValidateCredentialsResponse(
            response=ValidatedCredentials(
                valid=True,
                unique_tenant_id="test",
            ),
        )

    for capability in integration.capabilities:
        assert integration.oauth_settings and integration.oauth_settings.scopes is not None
        if capability.value not in [
            "get_authorization_url",
            "handle_authorization_callback",
            "refresh_access_token",
        ]:
            assert capability.value in integration.oauth_settings.scopes
