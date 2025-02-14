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


# Get the first uncompleted workout
query = 'select min(day_id), min(week_id) from mesos where completed = 0 and meso_id = %s and user_id = %s'
uncompleted_ids = conn.execute_query(query, (meso_id, user_id))[0]
day_id = uncompleted_ids[0]
week_id = uncompleted_ids[1]

# Get the exercises
query = '''
        select distinct e.name, e.id, m.order_id
        from mesos m
        inner join exercises e on m.exercise_id = e.id
        where m.day_id = %s and m.week_id = %s and m.meso_id = %s and m.user_id = %s
        order by m.order_id
        '''
exercises = conn.execute_query(query, (day_id, week_id, meso_id, user_id))

for i in range(len(exercises)):
    exercise_name = exercises[i][0]

    query = '''
            select m.set_id, m.reps, m.weight, e.name, e.id, m.order_id
            from mesos m
            inner join exercises e on m.exercise_id = e.id
            where m.day_id = %s and m.week_id = %s and m.meso_id = %s and m.user_id = %s and e.name = %s
            order by m.order_id
            '''
    workout = conn.execute_query(query, (day_id, week_id, meso_id, user_id, exercise_name))

    st.write(f'### {exercise_name}')

    for i in range(len(workout)):
        set_id = workout[i][0]
        reps = workout[i][1]
        weight = workout[i][2]
        name = workout[i][3]
        exercise_id = workout[i][4]
        order_id = workout[i][5]

        cols = st.columns(4)
        with cols[0]:
            st.write(f'Set: {set_id + 1}')
        with cols[1]:
            weight = st.number_input('Weight',
                                     label_visibility='collapsed',
                                     value=None,
                                     key=f'weight{exercise_name, set_id}',
                                     step=.5)
        with cols[2]:
            reps = st.number_input('Reps',
                                   label_visibility='collapsed',
                                   value=None,
                                   key=f'reps{exercise_name, set_id}',
                                   step=1)
        with cols[3]:
            completed = st.checkbox('Complete', key=f'completed{exercise_name, set_id}')

        if completed:
            query = '''
                    update mesos
                    set reps = %s, weight = %s, completed = 1, date_completed = now()
                    where set_id = %s and day_id = %s and week_id = %s and exercise_id = %s and name = %s
                    '''
            conn.execute_query(query, (reps, weight, set_id, day_id, week_id, exercise_id, meso_name))

    add_set = st.button('Add set', key=f'add{exercise_name, set_id}')
    if add_set:
        query = '''
                insert into mesos
                (meso_id, name, user_id, completed, set_id, reps, weight, order_id, exercise_id, day_id, week_id, date_created) values
                (%s,        %s,      %s,         0,     %s,    %s,    %s,       %s,          %s,     %s,      %s, now())
                '''
        conn.execute_query(query, (meso_id, meso_name, user_id, set_id + 1, reps, weight, order_id, exercise_id, day_id, week_id))
        st.toast('Inserted')
        st.rerun()

# Complete workout - navigate to previous workout page
st.write('###')
all_done = st.button('Complete Workout')
