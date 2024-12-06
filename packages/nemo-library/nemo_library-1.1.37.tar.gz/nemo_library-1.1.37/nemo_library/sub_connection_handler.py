import requests
import json
from nemo_library.sub_config_handler import ConfigHandler


def connection_get_headers(config: ConfigHandler):
    """
    Retrieve headers for authentication and API requests.

    This function gets the authentication tokens using `connection_get_tokens`
    and prepares the headers needed for API requests.

    Returns:
        dict: A dictionary containing headers with the authorization token,
              content type, API version, and refresh token.
    """
    tokens = connection_get_tokens(config)
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {tokens[0]}",
        "refresh-token": tokens[2],
        "api-version": "1.0",
    }
    return headers


def connection_get_cognito_authflow(config: ConfigHandler):
    """
    Retrieve the Cognito authentication flow type.

    This function returns the type of Cognito authentication flow to be used.

    Returns:
        str: The Cognito authentication flow type.
    """
    return "USER_PASSWORD_AUTH"


def connection_get_cognito_url(config: ConfigHandler):
    """
    Retrieve the Cognito URL based on the current environment.

    This function obtains the current environment using the `connection_get_environment`
    function and returns the corresponding Cognito URL. If the environment is
    not recognized, an exception is raised.

    Returns:
        str: The Cognito URL for the current environment.

    Raises:
        Exception: If the environment is unknown.
    """
    env = config.config_get_environment()
    appclient_ids = {
        "demo": "https://cognito-idp.eu-central-1.amazonaws.com/eu-central-1_1ZbUITj21",
        "dev": "https://cognito-idp.eu-central-1.amazonaws.com/eu-central-1_778axETqE",
        "test": "https://cognito-idp.eu-central-1.amazonaws.com/eu-central-1_778axETqE",
        "prod": "https://cognito-idp.eu-central-1.amazonaws.com/eu-central-1_1oayObkcF",
        "challenge": "https://cognito-idp.eu-central-1.amazonaws.com/eu-central-1_U2V9y0lzx",
    }

    try:
        return appclient_ids[env]
    except KeyError:
        raise Exception(f"unknown environment '{env}' provided")


def connection_get_cognito_appclientid(config: ConfigHandler):
    """
    Retrieve the Cognito App Client ID based on the current environment.

    This function obtains the current environment using the `connection_get_environment`
    function and returns the corresponding Cognito App Client ID. If the environment is
    not recognized, an exception is raised.

    Returns:
        str: The Cognito App Client ID for the current environment.

    Raises:
        Exception: If the environment is unknown.
    """
    env = config.config_get_environment()
    appclient_ids = {
        "demo": "7tvfugcnunac7id3ebgns6n66u",
        "dev": "4lr89aas81m844o0admv3pfcrp",
        "test": "4lr89aas81m844o0admv3pfcrp",
        "prod": "8t32vcmmdvmva4qvb79gpfhdn",
        "challenge": "43lq8ej98uuo8hvnoi1g880onp",
    }

    try:
        return appclient_ids[env]
    except KeyError:
        raise Exception(f"unknown environment '{env}' provided")


def connection_get_tokens(config: ConfigHandler):
    """
    Retrieve authentication tokens from the Cognito service.

    This function performs a login operation using Cognito and retrieves
    the authentication tokens including IdToken, AccessToken, and RefreshToken.

    Returns:
        tuple: A tuple containing the IdToken, AccessToken, and optionally the RefreshToken.

    Raises:
        Exception: If the request to the Cognito service fails.
    """
    headers = {
        "X-Amz-Target": "AWSCognitoIdentityProviderService.InitiateAuth",
        "Content-Type": "application/x-amz-json-1.1",
    }

    authparams = {
        "USERNAME": config.config_get_userid(),
        "PASSWORD": config.config_get_password(),
    }

    data = {
        "AuthParameters": authparams,
        "AuthFlow": connection_get_cognito_authflow(config),
        "ClientId": connection_get_cognito_appclientid(config),
    }

    # login and get token
    response_auth = requests.post(
        connection_get_cognito_url(config), headers=headers, data=json.dumps(data)
    )
    if response_auth.status_code != 200:
        raise Exception(
            f"request failed. Status: {response_auth.status_code}, error: {response_auth.text}"
        )
    tokens = json.loads(response_auth.text)
    id_token = tokens["AuthenticationResult"]["IdToken"]
    access_token = tokens["AuthenticationResult"]["AccessToken"]
    refresh_token = tokens["AuthenticationResult"].get(
        "RefreshToken"
    )  # Some flows might not return a RefreshToken

    return id_token, access_token, refresh_token


if __name__ == "__main__":
    config = ConfigHandler()
    print(connection_get_headers(config))
