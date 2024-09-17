from helpers.connection import MySQLDatabase
import streamlit as st

st.set_page_config(page_title='Current Workout', layout='centered')
conn = MySQLDatabase()

mesos_sql = conn.execute_query('select distinct name from mesos')
mesos = []

for g in mesos_sql:
    mesos.append(g[0])

meso_name = st.selectbox('Mesos', mesos)
workout_date = st.date_input('Pick a date')

# get last workout sets and reps for exercise
# if exists then use this to populate the page, if not use mesos
last_workout_query = 'select'
# loop for each exercise adding a set or reps
