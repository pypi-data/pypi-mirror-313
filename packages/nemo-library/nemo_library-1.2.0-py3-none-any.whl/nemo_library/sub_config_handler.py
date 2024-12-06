import configparser
from nemo_library.sub_password_handler import PasswordManager


class ConfigHandler:
    def __init__(
        self,
        nemo_url=None,
        tenant=None,
        userid=None,
        password=None,
        environment=None,
        hubspot_api_token=None,
        config_file="config.ini",
    ):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.nemo_url = (
            self.config["nemo_library"]["nemo_url"] if nemo_url == None else nemo_url
        )
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
        return self.nemo_url

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
