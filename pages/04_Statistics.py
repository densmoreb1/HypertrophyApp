from helpers.connection import MySQLDatabase
import streamlit as st
import pandas as pd

st.set_page_config(page_title='Statistics', layout='centered')
st.write('# Statistics')

conn = MySQLDatabase()

groups_sql = conn.execute_query('select distinct muscle_group from exercises')
muscle_groups = [g[0] for g in groups_sql]

muscle_groups = st.multiselect('Muscle Groups', muscle_groups)

sets_query = '''
SELECT
    e.muscle_group,
    COUNT(m.set_id) AS set_count,
    ROW_NUMBER() OVER (PARTITION BY e.muscle_group, m.meso_id ORDER BY m.week_id) AS week_rank
FROM mesos m
JOIN exercises e ON m.exercise_id = e.id
where m.completed = 1
GROUP BY e.muscle_group, m.meso_id, m.week_id
'''

# for each muscle make a plot for sets per week orderded by comeplted time
sets_sql = conn.execute_query(sets_query)

df = pd.DataFrame(sets_sql, columns=['muscle_group', 'set_count', 'week'])

for muscle in muscle_groups:
    st.write(muscle.capitalize())
    df = df[df['muscle_group'] == muscle]
    st.line_chart(df, x='week', y='set_count')

# view volumne of exercise over each workout
