import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

class UserAuthentication:
    """
    A class that handles user authentication.

    Attributes:
        authenticator: An authenticator object configured with the credentials and cookie settings from the config file.
        name: The name of the authenticated user.
        authentication_status: The authentication status of the user.
        username: The username of the authenticated user.
    """

    def __init__(self):
        self.authenticator = self.create_authenticator()
        self.name, self.authentication_status, self.username = self.authenticator.login("Login", "main")

    def create_authenticator(self):
        """
        Create an authenticator object based on the configuration specified in the .streamlit/config.yaml file.

        Returns:
            authenticator: An authenticator object configured with the credentials and cookie settings from the config file.
        """
        with open(".streamlit/config.yaml", encoding='utf-8') as file:
            config = yaml.load(file, Loader=SafeLoader)

            authenticator = stauth.Authenticate(
                config["credentials"],
                config["cookie"]["name"],
                config["cookie"]["key"],
                config["cookie"]["expiry_days"],
            )
        return authenticator

    def logout(self):
        """
        Logs out the authenticated user.
        """
        self.authenticator.logout("Logout", "sidebar")