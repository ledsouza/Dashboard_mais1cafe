import streamlit as st
from streamlit.testing.v1 import AppTest

# TODO: Add tests for the pages.

def test_home_no_interaction():
    """
    Test case to verify the behavior of the home page when there is no user interaction.
    """
    at = AppTest.from_file("home.py")
    at.run()
    assert at.session_state["authentication_status"] is None
    assert not at.exception

def test_home_invalid_password():
    """
    Test case to verify the behavior of the home page when an invalid password is entered.
    """
    at = AppTest.from_file("home.py")
    at.run()
    at.text_input[1].set_value("invalid password")
    at.button[0].click()
    at.run()
    assert at.session_state["authentication_status"] is False
    assert not at.exception

def test_home_valid_password():
    """
    Test case to verify the behavior of the home page when a valid password is entered.
    """
    at = AppTest.from_file("home.py")
    at.run()
    user = st.secrets['login_credential']['user']
    password = st.secrets['login_credential']['password']
    at.text_input[0].set_value(user)
    at.text_input[1].set_value(password)
    at.button[0].click()
    at.run()
    assert at.session_state["authentication_status"] is True
    assert not at.exception
