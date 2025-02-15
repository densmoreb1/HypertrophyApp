from helpers.connection import MySQLDatabase
import streamlit as st

conn = MySQLDatabase()

if "role" not in st.session_state:
    st.session_state.role = None


sql = conn.execute_query('select distinct name from users')
users = [s[0] for s in sql]


def login():

    st.header("Log in")
    role = st.text_input("Username")

    if role in users:
        st.session_state.role = role
        st.rerun()


def logout():
    st.session_state.role = None
    st.rerun()


role = st.session_state.role

page_dict = {}
if role in users:
    page_dict['Current'] = [st.Page('01_current/Create_Meso.py', default=True), st.Page('01_current/Current.py')]
    page_dict['Statistics'] = [st.Page('02_statistics/Previous_Workouts.py'), st.Page('02_statistics/Statistics.py')]
    page_dict['Add'] = [st.Page('03_add/Add_Exercise.py')]
    page_dict['Account'] = [st.Page(logout, title="Log out", icon=":material/logout:")]
    if role == 'brandon':
        page_dict['Account'].append(st.Page('00_settings.py', title='Settings'))

if len(page_dict) > 0:
    pg = st.navigation(page_dict)
else:
    pg = st.navigation([st.Page(login)])

pg.run()
