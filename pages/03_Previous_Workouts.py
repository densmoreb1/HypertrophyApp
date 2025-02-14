from helpers.connection import MySQLDatabase
import streamlit as st

st.set_page_config(page_title='Previous Workouts', layout='centered')
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


# Get the completed week_ids
query = 'select distinct week_id from mesos where name = %s and completed = 1 order by week_id'
sql = conn.execute_query(query, (meso_name, ))
weeks = [d[0] + 1 for d in sql]

week_id = st.selectbox('Week', weeks) - 1

# Get the completed day_ids
query = 'select distinct day_id from mesos where name = %s and completed = 1 order by day_id'
sql = conn.execute_query(query, (meso_name, ))
days = [str(d[0] + 1) for d in sql]

day_tabs = st.tabs(days)

for day_id in range(len(day_tabs)):
    with day_tabs[day_id]:
        st.write(f'## Day {day_id + 1}')

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

                cols = st.columns(3)
                with cols[0]:
                    st.write(f'Set: {set_id + 1}')
                with cols[1]:
                    st.write(f'Weight: {weight}')
                with cols[2]:
                    st.write(f'Reps: {reps}')
