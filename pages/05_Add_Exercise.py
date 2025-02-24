from helpers.connection import MySQLDatabase
from helpers.login import login
import streamlit as st

if st.session_state.get("authentication_status"):
    authenticator = st.session_state.get("authenticator")
    authenticator.logout(location="sidebar", key="add_logout")
    authenticator.login(location="unrendered", key="add_logout")
else:
    login()

conn = MySQLDatabase()

st.write('# Add Exercise')

name = st.text_input('Exercise Name').lower()
group = st.text_input('Muscle Group').lower()
result = st.button('Create Exercise')

query = 'select name from exercises'
sql = conn.execute_query(query)
names = [u[0] for u in sql]

insert_sql = 'insert into exercises (name, muscle_group) values (%s, %s)'

if result:
    if name not in names:
        conn.execute_query(insert_sql, (name, group))
        st.toast('Exercise created')
    else:
        st.toast('Exercise already exists')
