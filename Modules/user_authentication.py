import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

def create_authenticator():
    """
    Create an authenticator object based on the configuration specified in the .streamlit/config.yaml file.

    Returns:
        authenticator: An authenticator object configured with the credentials and cookie settings from the config file.
    """
    with open(".streamlit/config.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)

        authenticator = stauth.Authenticate(
            config["credentials"],
            config["cookie"]["name"],
            config["cookie"]["key"],
            config["cookie"]["expiry_days"],
        )
    return authenticator