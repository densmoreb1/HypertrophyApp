from helpers.connection import MySQLDatabase
import streamlit as st

st.set_page_config(page_title='Create Meso', layout='wide')
conn = MySQLDatabase()

groups_sql = conn.execute_query('select distinct muscle_group from exercises')
muscle_groups = [g[0] for g in groups_sql]
meso = {}
exercise_query = 'select name from exercises where muscle_group = %s'

st.write('# Create Meso')

name = st.text_input('Name of Meso').lower()

weeks = st.selectbox('Weeks', (4, 5, 6))
days = st.selectbox('Days per week', (1, 2, 3, 4, 5, 6, 7))

result = st.button('Create Meso')

if result and name == '':
    st.warning('Enter name', icon="⚠️")

cols = st.columns(days)

for i in range(len(cols)):
    if days >= i:
        with cols[i]:
            st.write(f'### Day {i+1}')

            exercises_per = st.selectbox(
                'How many exercises?', (1, 2, 3, 4, 5, 6), key=f'per{i}')

            final_exercise_list = []

            for r in range(exercises_per):
                muscle = st.selectbox(f'#### Muscle Group {r+1}',
                                      (muscle_groups),
                                      key=f'muscle{i, r}')
                exercise_sql = conn.execute_query(exercise_query, (muscle,))
                exercise_selection = [e[0] for e in exercise_sql]
                exercise = st.selectbox(
                    'Exercise', (exercise_selection), key=f'exercise{i, r}')

                final_exercise_list.append(exercise)

            meso[i] = final_exercise_list


exercise_id_query = '''
select id
from fitness.exercises
where name = %s
'''

insert_query = '''
insert into fitness.mesos
(name, user_id, set_id, reps, weight, order_id
, exercise_id, day_id, week_id, date_created)
values (%s, %s, %s, %s, %s, %s, %s, %s, %s, now())
'''

if result and name != '':

    for week_id in range(weeks):
        for day_id, value in meso.items():
            for order_id in range(len(value)):
                exercise_id = conn.execute_query(
                    exercise_id_query, (value[order_id],))[0][0]
                res = conn.execute_query(
                    insert_query,
                    (name, 1, 0, 0, 0, order_id, exercise_id, day_id, week_id,)
                )
        print(res)
