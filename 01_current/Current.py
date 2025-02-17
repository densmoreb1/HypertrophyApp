from helpers.connection import MySQLDatabase
import streamlit as st

conn = MySQLDatabase()


# Get Users to populate current meso
user_name = st.session_state.role
user_id = conn.execute_query('select id from users where name = %s', (user_name,))[0][0]


# Get Meso for the selected User
query = 'select distinct name, meso_id from mesos where user_id = %s order by meso_id desc'
sql = conn.execute_query(query, (user_id,))
mesos = [g[0] for g in sql]

if len(mesos) > 0:
    meso_name = st.selectbox('Mesos', mesos)
    meso_id = conn.execute_query('select meso_id from mesos where name = %s', (meso_name,))[0][0]
else:
    st.write('Looks you have not created a meso yet')
    st.stop()


# Get the first uncompleted workout
# Get week_id
query = 'select min(week_id) from mesos where completed = 0 and meso_id = %s'
week_id = conn.execute_query(query, (meso_id,))[0][0]

# Get day_id
query = 'select min(day_id) from mesos where completed = 0 and meso_id = %s and week_id = %s'
day_id = conn.execute_query(query, (meso_id, week_id))[0][0]


# Get the exercises
query = '''
        select distinct e.name, e.id, m.order_id
        from mesos m
        inner join exercises e on m.exercise_id = e.id
        where m.day_id = %s and m.week_id = %s and m.meso_id = %s and m.user_id = %s
        order by m.order_id
        '''
exercises = conn.execute_query(query, (day_id, week_id, meso_id, user_id))

st.write(f'## Week {week_id + 1} Day {day_id + 1}')

for i in range(len(exercises)):
    exercise_name = exercises[i][0]

    st.write(f'### {exercise_name}')

    query = '''
            select m.set_id, m.reps, m.weight, e.name, e.id, m.order_id
            from mesos m
            inner join exercises e on m.exercise_id = e.id
            where m.day_id = %s and m.week_id = %s and m.meso_id = %s and m.user_id = %s and e.name = %s
            order by m.order_id
            '''
    workout = conn.execute_query(query, (day_id, week_id, meso_id, user_id, exercise_name))
    previous = conn.execute_query(query, (day_id, week_id - 1, meso_id, user_id, exercise_name))

    for i in range(len(workout)):
        prev_reps = None
        prev_weight = None
        # if last workout exists
        if len(previous) > 0:
            # if set exists
            if i < len(previous):
                prev_reps = previous[i][1]
                prev_weight = previous[i][2]

        set_id = workout[i][0]
        reps = workout[i][1]
        weight = workout[i][2]
        exercise_id = workout[i][4]
        order_id = workout[i][5]

        completed = []
        cols = st.columns(4)
        with cols[0]:
            st.write(f'Set: {set_id + 1}')
        with cols[1]:
            weight = st.number_input('Weight',
                                     label_visibility='collapsed',
                                     placeholder=f'Weight: {prev_weight}',
                                     value=None,
                                     key=f'weight{exercise_name, set_id}',
                                     step=.5)
        with cols[2]:
            reps = st.number_input('Reps',
                                   label_visibility='collapsed',
                                   placeholder=f'Reps: {prev_reps}',
                                   value=None,
                                   key=f'reps{exercise_name, set_id}',
                                   step=1)
        with cols[3]:
            completed.append(st.checkbox('Complete', key=f'completed{exercise_name, set_id}'))

        if all(completed):
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


@st.dialog("Workout Completed")
def complete_workout():
    if st.button("View Past Workouts"):
        st.switch_page('02_statistics/Previous_Workouts.py')


if st.button('Complete Workout'):
    complete_workout()
