import os
from getpass import getuser

_token_cache_enabled_ = True
_azure_auth_enabled_ = True
_azure_tenant_id_ = os.getenv("EIGEN_INGENUITY_TENANT_ID", "74efa022-e6d6-42ad-bc15-edc76c525bde")
_azure_client_id_ = os.getenv("EIGEN_INGENUITY_CLIENT_ID", "c2b9aa13-e178-4dde-bc2c-b6cc4c8391d2")
_azure_client_secret_ = os.getenv("EIGEN_INGENUITY_CLIENT_SECRET", None)
_api_token_value_ = os.getenv("EIGEN_INGENUITY_API_TOKEN", False)
_auth_scope_ = os.getenv("EIGEN_INGNEUITY_AUTH_SCOPE","user_impersonation")


def clear_auth_token_cache():
    """
    Delete any cached tokens for the current signed in user

    Args:
        None

    Returns:
        None
    """
    if os.path.exists(os.path.dirname(__file__) + f'/.azure/{getuser()}_cache.bin'):
        os.remove(os.path.dirname(__file__) + f'/.azure/{getuser()}_cache.bin')

def disable_auth_token_cache(state=True):
    """
    Prevent the program from creating/using/updating the token cache when authenticating with Azure. Note that this will not delete any existing tokens, for this see clear_auth_token_cache()

    Args:
        None

    Returns:
        None
    """
    global _token_cache_enabled_
    _token_cache_enabled_ = not state

def disable_azure_auth(state=True):
    """
    Skip all azure authentication steps, note that this will cause an error if querying a protected resource (Disabling this is not necessarily necessary, it will not cause errors).

    Args:
        None

    Returns:
        None
    """
    global _azure_auth_enabled_
    _azure_auth_enabled_ = not state

def set_azure_tenant_id(id):
    """
    Set the ID of the Azure tenant of the eigenserver. This value is required for Azure authentication, but the use of the TENANTID environmental variable can be used as an alternative way of setting it.

    Args:
        id: The ID of your tenant in Azure. This can be found at portal.azure.com.(Default points to our DEMO Instance)

    Returns:
        None
    """
    global _azure_tenant_id_
    _azure_tenant_id_ = id

def set_azure_client_id(id):
    """
    Set the Client ID of the App registration for the eigenserver. This value required for Azure authentication, but the use of the EIGEN_INGENUITY_TENANT_ID environmental variable can be used as an alternative way of setting it.

    Args:
        id: The ID of your service principal in Azure. This can be found at portal.azure.com. (Default points to our DEMO Instance)

    Returns:
        None
    """
    global _azure_client_id_
    _azure_client_id_ = id

def set_azure_client_secret(secret):
    """
    Set the Client ID of the App registration for the eigenserver. This value required for Azure authentication via CLIENT_CREDENTIALS flow, but not for the USER_CREDENTIALS flow, but the use of the EIGEN_INGENUITY_CLIENT_SECRET environmental variable can be used as an alternative way of setting it.

    Args:
        secret: The value of the client secret of your service principal in Azure. This can be found at portal.azure.com. (Default points to our DEMO Instance)

    Returns:
        None
    """
    global _azure_client_secret_
    _azure_client_secret_ = secret

def set_api_token(token):
    """
    Set the API token for the eigenserver. This value is required to access our secured endpoints, but the use of the EIGEN_INGENUITY_API_TOKEN environmental variable can be used as an alternative way of setting it.

    Args:
        token: The value of your api token. This can be found at {TBA}.

    Returns:
        None
    """
    global _api_token_value_
    _api_token_value_ = token

def set_auth_scope(scope):
    """
    Set the Scope to be requested from the Azure App registration. This is only required if your IT has implemented a non-standard scope.
    This value must match the one configured in the eigen dashboards app registration in your Azure, if you are unsure of what is should be, ask yoeu system administrator. The use of the EIGEN_INGENUITY_AUTH_SCOPE environmental variable can be used as an alternative way of setting it.

    Args:
        scope: The value of the required scope. Defaults to 'user_impersonation'.

    Returns:
        None
    """
    global _auth_scope_
    _auth_scope_ = scope
