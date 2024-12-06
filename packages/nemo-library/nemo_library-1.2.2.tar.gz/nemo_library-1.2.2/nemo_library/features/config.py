import configparser
import requests
import json

from nemo_library.utils.password_manager import PasswordManager

COGNITO_URLS = {
    "demo": "https://cognito-idp.eu-central-1.amazonaws.com/eu-central-1_1ZbUITj21",
    "dev": "https://cognito-idp.eu-central-1.amazonaws.com/eu-central-1_778axETqE",
    "test": "https://cognito-idp.eu-central-1.amazonaws.com/eu-central-1_778axETqE",
    "prod": "https://cognito-idp.eu-central-1.amazonaws.com/eu-central-1_1oayObkcF",
    "challenge": "https://cognito-idp.eu-central-1.amazonaws.com/eu-central-1_U2V9y0lzx",
}
COGNITO_APPCLIENT_IDS = {
    "demo": "7tvfugcnunac7id3ebgns6n66u",
    "dev": "4lr89aas81m844o0admv3pfcrp",
    "test": "4lr89aas81m844o0admv3pfcrp",
    "prod": "8t32vcmmdvmva4qvb79gpfhdn",
    "challenge": "43lq8ej98uuo8hvnoi1g880onp",
}
NEMO_URLS = {
    "demo": "https//demo.enter.nemo-ai.com",
    "dev": "http://development.enter.nemo-ai.com",
    "test": "http://test.enter.nemo-ai.com",
    "prod": "https://enter.nemo-ai.com",
    "challenge": "http://challenge.enter.nemo-ai.com",
}


class Config:

    def __init__(
        self,
        tenant=None,
        userid=None,
        password=None,
        environment=None,
        hubspot_api_token=None,
        config_file="config.ini",
    ):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.tenant = (
            self.config["nemo_library"]["tenant"] if tenant == None else tenant
        )
        self.userid = (
            self.config["nemo_library"]["userid"] if userid == None else userid
        )
        try:
            self.password = (
                self.config["nemo_library"]["password"]
                if password == None
                else password
            )
        except KeyError as e:
            pm = PasswordManager(service_name="nemo_library", username=self.userid)
            self.password = pm.get_password()

        self.environment = (
            self.config["nemo_library"]["environment"]
            if environment == None
            else environment
        )
        self.hubspot_api_token = (
            self.config["nemo_library"]["hubspot_api_token"]
            if hubspot_api_token == None
            else hubspot_api_token
        )

    def config_get_nemo_url(self):
        """
        Retrieve the Nemo URL from the configuration file.

        This function reads the `config.ini` file and retrieves the Nemo URL
        specified under the `nemo_library` section.

        Returns:
            str: The Nemo URL.
        """
        env = self.config_get_environment()
        try:
            return NEMO_URLS[env]
        except KeyError:
            raise Exception(f"unknown environment '{env}' provided")

    def config_get_tenant(self):
        """
        Retrieve the tenant information from the configuration file.

        This function reads the `config.ini` file and retrieves the tenant
        specified under the `nemo_library` section.

        Returns:
            str: The tenant information.
        """
        return self.tenant

    def config_get_userid(self):
        """
        Retrieve the user ID from the configuration file.

        This function reads the `config.ini` file and retrieves the user ID
        specified under the `nemo_library` section.

        Returns:
            str: The user ID.
        """
        return self.userid

    def config_get_password(self):
        """
        Retrieve the password from the configuration file.

        This function reads the `config.ini` file and retrieves the password
        specified under the `nemo_library` section.

        Returns:
            str: The password.
        """
        return self.password

    def config_get_environment(self):
        """
        Retrieve the environment information from the configuration file.

        This function reads the `config.ini` file and retrieves the environment
        specified under the `nemo_library` section.

        Returns:
            str: The environment information.
        """
        return self.environment

    def config_get_hubspot_api_token(self):
        """
        Retrieve the hubspot_api_token information from the configuration file.

        This function reads the `config.ini` file and retrieves the hubspot_api_token
        specified under the `nemo_library` section.

        Returns:
            str: The hubspot_api_token information.
        """
        return self.hubspot_api_token

    def connection_get_headers(self):
        """
        Retrieve headers for authentication and API requests.

        This function gets the authentication tokens using `connection_get_tokens`
        and prepares the headers needed for API requests.

        Returns:
            dict: A dictionary containing headers with the authorization token,
                content type, API version, and refresh token.
        """
        tokens = self.connection_get_tokens()
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {tokens[0]}",
            "refresh-token": tokens[2],
            "api-version": "1.0",
        }
        return headers

    def connection_get_cognito_authflow(self):
        """
        Retrieve the Cognito authentication flow type.

        This function returns the type of Cognito authentication flow to be used.

        Returns:
            str: The Cognito authentication flow type.
        """
        return "USER_PASSWORD_AUTH"

    def connection_get_cognito_url(self):
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
        env = self.config_get_environment()
        try:
            return COGNITO_URLS[env]
        except KeyError:
            raise Exception(f"unknown environment '{env}' provided")

    def connection_get_cognito_appclientid(self):
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
        env = self.config_get_environment()
        try:
            return COGNITO_APPCLIENT_IDS[env]
        except KeyError:
            raise Exception(f"unknown environment '{env}' provided")

    def connection_get_tokens(self):
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
            "USERNAME": self.config_get_userid(),
            "PASSWORD": self.config_get_password(),
        }

        data = {
            "AuthParameters": authparams,
            "AuthFlow": self.connection_get_cognito_authflow(),
            "ClientId": self.connection_get_cognito_appclientid(),
        }

        # login and get token
        response_auth = requests.post(
            self.connection_get_cognito_url(), headers=headers, data=json.dumps(data)
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
