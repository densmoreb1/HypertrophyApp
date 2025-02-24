import streamlit as st


def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("pages/01_Create_Meso.py", label="Create Meso")
    st.sidebar.page_link("pages/02_Current.py", label="Current Workout")
    st.sidebar.page_link("pages/03_Previous_Workouts.py", label="Previous Workouts")
    st.sidebar.page_link("pages/04_Statistics.py", label="Statistics")
    st.sidebar.page_link("pages/05_Add_Exercise.py", label="Add Exercise")
    if 'admin' in st.session_state.roles:
        st.sidebar.page_link("pages/06_Settings.py")


def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("login.py", label="Log in")


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if len(st.session_state.roles) == 0:
        unauthenticated_menu()
        return
    authenticated_menu()
