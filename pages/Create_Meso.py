from helpers.connection import MySQLDatabase
import streamlit as st

st.set_page_config(page_title='Create Meso', layout='wide')

conn = MySQLDatabase('root', 'remote22', '172.17.0.2', 'fitness')

groups_sql = conn.execute_query('SELECT DISTINCT muscle_group FROM exercises')
groups = []

for g in groups_sql:
    groups.append(g[0])

exercise_query = 'SELECT name FROM exercises WHERE muscle_group = %s'

st.write('# Create Meso')

days = st.selectbox('Days per week', (1, 2, 3, 4, 5, 6, 7))
cols = st.columns(days)

for i in range(len(cols)):
    if days >= i:
        with cols[i]:
            st.write(f'Day {i+1}')
            muscle = st.selectbox('Muscle Group', (groups), key=i)
            exercise_sql = conn.execute_query(exercise_query, (muscle,))
            exercises = []
            for e in exercise_sql:
                exercises.append(e[0])

            st.selectbox('Exercise', (exercises), key=f'exercise{i}')
