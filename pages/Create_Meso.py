from helpers.connection import MySQLDatabase
import streamlit as st

conn = MySQLDatabase('root', 'remote22', '172.17.0.2', 'fitness')

groups_sql = conn.execute_query('SELECT DISTINCT muscle_group FROM exercises')
groups = []

for g in groups_sql:
    groups.append(g[0])

exercise_query = 'SELECT name FROM exercises WHERE muscle_group = %s'

st.write('# Create Meso')

days = st.selectbox('Days per week', (1, 2, 3, 4, 5, 6, 7))
cols = st.columns(days)

if days >= 1:
    with cols[0]:
        st.write('Day 1')
        muscle = st.selectbox('Muscle Group', (groups), key=1)
        exercise = conn.execute_query(exercise_query, (muscle,))[0]
        st.selectbox('Exercise', (exercise))

if days >= 2:
    with cols[1]:
        st.write('Day 2')
        st.selectbox('Muscle Group', (groups), key=2)

if days >= 3:
    with cols[2]:
        st.write('Day 3')
        st.selectbox('Muscle Group', (groups), key=3)

if days >= 4:
    with cols[3]:
        st.write('Day 4')
        st.selectbox('Muscle Group', (groups), key=4)

if days >= 5:
    with cols[4]:
        st.write('Day 5')
        st.selectbox('Muscle Group', (groups), key=5)

if days >= 6:
    with cols[5]:
        st.write('Day 6')
        st.selectbox('Muscle Group', (groups), key=6)

if days >= 7:
    with cols[6]:
        st.write('Day 7')
        st.selectbox('Muscle Group', (groups), key=7)
