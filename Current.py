from helpers.connection import MySQLDatabase
import streamlit as st

st.set_page_config(page_title='Current Workout', layout='centered')
conn = MySQLDatabase()

mesos_sql = conn.execute_query('select distinct name from mesos')
mesos = [g[0] for g in mesos_sql]

meso_name = st.selectbox('Mesos', mesos)

weeks_query = '''
select distinct week_id from mesos where name = %s
'''
weeks_sql = conn.execute_query(weeks_query, (meso_name, ))
weeks = sorted([d[0]+1 for d in weeks_sql])

week = st.selectbox('Week', weeks)

days_query = '''
select distinct day_id from mesos where name = %s
'''
day_sql = conn.execute_query(days_query, (meso_name, ))
days = sorted([str(d[0]+1) for d in day_sql])

day_tabs = st.tabs(days)

query = '''
select m.set_id, m.reps, m.weight, m.order_id, e.name, m.day_id, m.week_id
from mesos m
inner join exercises e
    on m.exercise_id = e.id
where m.day_id = %s and m.week_id = %s
order by m.order_id
'''

for i in range(len(day_tabs)):
    with day_tabs[i]:
        st.write(f'Day {i+1}')
        workout_sql = conn.execute_query(query, (i, week,))
        st.write(workout_sql)
