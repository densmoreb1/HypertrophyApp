from helpers.connection import MySQLDatabase
import streamlit as st

st.set_page_config(page_title='Current Workout', layout='centered')
conn = MySQLDatabase()

mesos_sql = conn.execute_query('select distinct name from mesos')
mesos = [g[0] for g in mesos_sql]

meso_name = st.selectbox('Mesos', mesos)

# select from table and populate
# maybe use streamlit tabs
# create an add set button that will insert sets
