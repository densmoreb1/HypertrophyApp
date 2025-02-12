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
query = 'select min(day_id), min(week_id) from mesos where completed = 0 and meso_id = %s and user_id = %s'
uncompleted_ids = conn.execute_query(query, (meso_id, user_id))[0]

query = '''
        select m.set_id, m.reps, m.weight, e.name, m.order_id
        from mesos m
        inner join exercises e on m.exercise_id = e.id
        where m.day_id = %s and m.week_id = %s and m.meso_id = %s and m.user_id = %s
        order by m.order_id
        '''

exercises = conn.execute_query(query, (uncompleted_ids[0], uncompleted_ids[1], meso_id, user_id))


for exercise in exercises:
    set_id = exercise[0]
    reps = exercise[1]
    weight = exercise[2]
    name = exercise[3]

    st.write(f'### {name}')
    cols = st.columns(4)
    with cols[0]:
        st.write(f'Set: {set_id + 1}')
    with cols[1]:
        weight = st.number_input('Weight',
                                 label_visibility='collapsed',
                                 value=None,
                                 key=f'weight{exercise, set_id}',
                                 step=.5)
    with cols[2]:
        reps = st.number_input('Reps',
                               label_visibility='collapsed',
                               value=None,
                               key=f'reps{exercise, set_id}',
                               step=1)
    with cols[3]:
        c = st.checkbox('Complete', key=f'completed{exercise, set_id}')
        if c:
            s = {'weight': weight, 'reps': reps}

    add_set = st.button('Add set', key=f'add{exercise, set_id}')
    if add_set:
        st.popover('Inserted')
