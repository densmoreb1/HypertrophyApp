from helpers.connection import MySQLDatabase
import streamlit as st
import datetime

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


@st.dialog('Change exercise')
def change_exercise(exercise_name, exercise_id):
    group = conn.execute_query('select muscle_group from exercises where id = %s', (exercise_id,))[0][0]
    sql = conn.execute_query('select name from exercises where muscle_group = %s', (group,))
    exercise_selection = [e[0] for e in sql]

    updated_exercise = st.selectbox(f'{group.capitalize()} Exercises', exercise_selection)
    updated_exercise_id = conn.execute_query('select id from exercises where name = %s', (updated_exercise, ))[0][0]

    query = '''
            update mesos m
            set m.exercise_id = %s
            where m.day_id = %s and m.week_id = %s and m.meso_id = %s and m.exercise_id = %s
            '''
    if st.button('Confirm'):
        conn.execute_query(query, (updated_exercise_id, day_id, week_id, meso_id, exercise_id))
        st.rerun()


@st.dialog('Exercise history')
def exercise_history(exercise_name, exercise_id):
    query = '''
            select distinct name, meso_id
            from mesos
            where exercise_id = %s and user_id = %s and completed = 1
            order by meso_id desc
            '''
    sql = conn.execute_query(query, (exercise_id, user_id))
    for i in range(len(sql)):
        history_meso = sql[i][0]
        st.write(f'## {history_meso}')

        history = '''
                select distinct week_id, day_id, date_completed
                from mesos
                where exercise_id = %s and user_id = %s and completed = 1 and name = %s
                order by date_completed desc
                '''
        history_sql = conn.execute_query(history, (exercise_id, user_id, history_meso))

        for j in range(len(history_sql)):
            history_week = history_sql[j][0]
            history_day = history_sql[j][1]
            st.write(f'### Week {history_week + 1} Day {history_day + 1}')
            history_reps = '''
                            select reps, weight
                            from mesos
                            where exercise_id = %s and user_id = %s and completed = 1 and name = %s and week_id = %s and day_id = %s
                            order by date_completed desc
                            '''
            history_reps_sql = conn.execute_query(history_reps, (exercise_id, user_id, history_meso, history_week, history_day))
            for h in range(len(history_reps_sql)):
                reps = history_reps_sql[h][0]
                weight = history_reps_sql[h][1]
                st.write(f'Weight: {weight} Reps: {reps}')


# Main Page
for i in range(len(exercises)):
    exercise_name = exercises[i][0]
    exercise_id = exercises[i][1]

    query = '''
            select m.set_id, m.reps, m.weight, e.name, e.id, m.order_id
            from mesos m
            inner join exercises e on m.exercise_id = e.id
            where m.day_id = %s and m.week_id = %s and m.meso_id = %s and e.name = %s and m.user_id = %s
            order by m.order_id
            '''
    workout = conn.execute_query(query, (day_id, week_id, meso_id, exercise_name, user_id))
    previous = conn.execute_query(query, (day_id, week_id - 1, meso_id, exercise_name, user_id))

    # Formatting with columns
    exercise_cols = st.columns([2, 1])
    with exercise_cols[0]:
        st.write(f'### {exercise_name}')
    with exercise_cols[1]:
        button_cols = st.columns([1, 2])
        with button_cols[0]:
            if st.button('Replace', key=f'swap{exercise_name}'):
                change_exercise(exercise_name, exercise_id)
        with button_cols[1]:
            if st.button('History', key=f'history{exercise_name}'):
                exercise_history(exercise_name, exercise_id)

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

    # Formatting with columns
    set_cols = st.columns([2, 15])
    with set_cols[0]:
        add_set = st.button('Add set', key=f'add{exercise_name, set_id}')
    with set_cols[1]:
        remove_set = None
        # Don't remove last set
        if set_id != 0:
            remove_set = st.button('Remove set', key=f'remove{exercise_name, set_id}')

    if remove_set:
        query = '''
                delete from mesos
                where set_id = %s and day_id = %s and week_id = %s and exercise_id = %s and name = %s
                '''
        conn.execute_query(query, (set_id, day_id, week_id, exercise_id, meso_name))
        st.rerun()

    if add_set:
        query = '''
                insert into mesos
                (meso_id, name, user_id, completed, set_id, reps, weight, order_id, exercise_id, day_id, week_id, date_created) values
                (%s,        %s,      %s,         0,     %s,    %s,    %s,       %s,          %s,     %s,      %s, now())
                '''
        conn.execute_query(query, (meso_id, meso_name, user_id, set_id + 1, reps, weight, order_id, exercise_id, day_id, week_id))
        st.rerun()


# Complete workout - navigate to previous workout page
st.write('###')


@st.dialog("Workout Completed")
def complete_workout():
    if st.button("View Past Workouts"):
        st.switch_page('02_statistics/Previous_Workouts.py')


if st.button('Complete Workout'):
    complete_workout()
