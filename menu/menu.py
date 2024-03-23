import streamlit as st

def authenticated_menu():
    """
    Show a navigation menu for authenticated users.

    This function displays a navigation menu in the sidebar for authenticated users. It includes links to the home page,
    dashboard, and data management pages. It also includes a logout widget.

    Parameters:
        None

    Returns:
        None
    """
    st.sidebar.page_link("Home.py", label="Home")
    if st.session_state.authentication_status is True:
        st.sidebar.page_link("pages/dashboard.py", label="Dashboard")
        st.sidebar.page_link("pages/data_management.py", label="Gerência de Dados")
        st.session_state['user_management'].logout_widget()


def unauthenticated_menu():
    """
    Show a navigation menu for unauthenticated users.

    This function displays a navigation menu in the sidebar for unauthenticated users.
    The menu includes a link to the "home.py" page with the label "Login".

    Parameters:
        None

    Returns:
        None
    """
    st.sidebar.page_link("home.py", label="Login")


def menu():
    """
    Determine if a user is logged in or not, then show the correct navigation menu.

    If the user is not logged in or the authentication status is False or None, the unauthenticated menu will be shown.
    Otherwise, the authenticated menu will be shown.
    """
    if "authentication_status" not in st.session_state or st.session_state.authentication_status is False or st.session_state.authentication_status is None:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    """
    Redirect users to the main page if not logged in, otherwise continue to render the navigation menu.
    """
    if "authentication_status" not in st.session_state or st.session_state.authentication_status is False or st.session_state.authentication_status is None:
        st.switch_page("home.py")
    menu()