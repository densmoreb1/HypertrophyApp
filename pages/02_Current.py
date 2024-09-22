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

week = st.selectbox('Week', weeks) - 1

days_query = '''
select distinct day_id from mesos where name = %s
'''
day_sql = conn.execute_query(days_query, (meso_name, ))
days = sorted([str(d[0]+1) for d in day_sql])

day_tabs = st.tabs(days)

execise_query = '''
select distinct e.name, e.id, m.order_id
from mesos m
inner join exercises e
    on m.exercise_id = e.id
where m.day_id = %s and m.week_id = %s
and m.name = %s
order by m.order_id
'''

workout_query = '''
select m.set_id, m.reps, m.weight, m.completed, m.order_id
from mesos m
inner join exercises e
    on m.exercise_id = e.id
where m.day_id = %s and m.week_id = %s and exercise_id = %s
and m.name = %s
'''

update_set_query = '''
update mesos
set reps = %s
, weight = %s
, completed = 1
, date_completed = now()
where set_id = %s and day_id = %s and week_id = %s and exercise_id = %s
and name = %s
'''

add_set_query = '''
insert into fitness.mesos
(name, user_id, completed, set_id, reps, weight, order_id
, exercise_id, day_id, week_id, date_created)
values (%s, 1, 0, %s, %s, %s, %s, %s, %s, %s, now())
'''


for i in range(len(day_tabs)):
    with day_tabs[i]:
        st.write(f'Day {i+1}')
        exercise_sql = conn.execute_query(execise_query, (i, week, meso_name))

        for exercise in range(len(exercise_sql)):
            st.write(exercise_sql[exercise][0])
            exercise_id = exercise_sql[exercise][1]

            workout_sql = conn.execute_query(workout_query,
                                             (i, week, exercise_id, meso_name))

            cols = st.columns(4)
            for j in range(len(workout_sql)):
                sets = workout_sql[j][0]
                reps = workout_sql[j][1]
                weight = workout_sql[j][2]
                completed = workout_sql[j][3]
                order_id = workout_sql[j][4]

                with cols[0]:
                    st.write(f'Set: {sets+1}')
                with cols[1]:
                    if completed == 0:
                        reps = st.number_input('Reps',
                                               label_visibility='collapsed',
                                               value=None,
                                               placeholder='Reps',
                                               key=f'reps{exercise, i, j}',
                                               step=1)
                    else:
                        st.write(f'Reps: {reps}')
                with cols[2]:
                    if completed == 0:
                        weight = st.number_input('Weight',
                                                 label_visibility='collapsed',
                                                 value=None,
                                                 placeholder='Weight',
                                                 key=f'weight{exercise, i, j}',
                                                 step=1)
                    else:
                        st.write(f'Weight: {weight}')
                with cols[3]:
                    if completed == 0:
                        c = st.button('Complete',
                                      key=f'completed{exercise, i, j}')
                        if c:
                            conn.execute_query(
                                update_set_query,
                                (reps, weight, sets, i, week,
                                 exercise_id, meso_name))
                    else:
                        st.write('Completed')

            add_set = st.button('Add set', key=f'{exercise, i}')
            if add_set:
                conn.execute_query(add_set_query,
                                   (meso_name, sets+1, weight, reps+1,
                                    order_id, exercise_id, i, week)
                                   )