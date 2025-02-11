from helpers.connection import MySQLDatabase
import streamlit as st

st.set_page_config(page_title='Current Workout', layout='centered')
conn = MySQLDatabase()


# Get Users to populate current meso
sql = conn.execute_query('select distinct name from users')
users = [u[0] for u in sql]

user_name = st.selectbox('Name', users)
user_id = conn.execute_query('select id from users where name = %s', (user_name,))[0][0]


# Get Meso for the selected User
query = 'select distinct name from mesos where user_id = %s'
sql = conn.execute_query(query, (user_id,))
mesos = [g[0] for g in sql]

meso_name = st.selectbox('Mesos', mesos)
meso_id = conn.execute_query('select meso_id from mesos where name = %s', (meso_name,))[0][0]


# Get the current workout
query = 'select min(day_id), min(week_id) from mesos where completed = 0'
uncompleted_ids = conn.execute_query(query)[0]

query = '''
        select m.set_id, m.reps, m.weight, m.order_id, e.name
        from mesos m
        inner join exercises e on m.exercise_id = e.id
        where m.day_id = %s and m.week_id = %s and m.meso_id = %s
        '''

res = conn.execute_query(query, (uncompleted_ids[0], uncompleted_ids[1], meso_id,))
st.write(res)
