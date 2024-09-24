from helpers.connection import MySQLDatabase
import streamlit as st
import pandas as pd

st.set_page_config(page_title='Statistics', layout='centered')
st.write('# Statistics')

conn = MySQLDatabase()

user_sql = conn.execute_query('select distinct name from users')
users = [u[0] for u in user_sql]

user_name = st.selectbox('Name', users)
user_id = conn.execute_query('select id from users where name = %s',
                             (user_name,))[0][0]

groups_sql = conn.execute_query('select distinct muscle_group from exercises')
muscle_groups = [g[0] for g in groups_sql]
muscle_groups = st.multiselect('Muscle Groups', muscle_groups)

sets_query = '''
select
    e.muscle_group,
    count(m.set_id) AS set_count,
    row_number() over (partition by e.muscle_group,
                        m.meso_id order by m.week_id) AS week_rank
from mesos m
inner join exercises e on m.exercise_id = e.id
inner join users u on m.user_id = u.id
where m.completed = 1
    and u.id = %s
group by e.muscle_group, m.meso_id, m.week_id
'''

sets_sql = conn.execute_query(sets_query, (user_id,))

df = pd.DataFrame(sets_sql, columns=['muscle_group', 'set_count', 'week'])

for muscle in muscle_groups:
    st.write(muscle.capitalize())
    df = df[df['muscle_group'] == muscle]
    st.line_chart(df, x='week', y='set_count')

# view volumne of exercise over each workout
