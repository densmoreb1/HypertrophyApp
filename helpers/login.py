from helpers.connection import MySQLDatabase
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


def login():
    with open('.streamlit/config.yml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    conn = MySQLDatabase()
    sql = conn.execute_query('select distinct name from users')
    users = [s[0] for s in sql]

    st.session_state["authenticator"] = authenticator
    st.session_state["config"] = config

    try:
        authenticator.login()
    except Exception as e:
        st.error(e)

    if st.session_state["authentication_status"]:
        authenticator.logout(location="sidebar", key="logout-demo-app-home")
    elif st.session_state["authentication_status"] is False:
        st.error("Username/password is incorrect")
