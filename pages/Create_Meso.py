from helpers.connection import MySQLDatabase
import streamlit as st

st.set_page_config(page_title='Create Meso', layout='wide')

conn = MySQLDatabase('root', 'remote22', '172.17.0.2', 'fitness')

groups_sql = conn.execute_query('SELECT DISTINCT muscle_group FROM exercises')
muscle_groups = []

for g in groups_sql:
    muscle_groups.append(g[0])

exercise_query = 'SELECT name FROM exercises WHERE muscle_group = %s'

st.write('# Create Meso')

your_name = st.text_input('Your Name')
name = st.text_input('Name of Meso')

days = st.selectbox('Days per week', (1, 2, 3, 4, 5, 6, 7))
cols = st.columns(days)

meso = {}

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
                exercise_selection = []
                for e in exercise_sql:
                    exercise_selection.append(e[0])
                exercise = st.selectbox(
                    'Exercise', (exercise_selection), key=f'exercise{i, r}')

                final_exercise_list.append(exercise)

            meso[i] = final_exercise_list

result = st.button('Create Meso')

exercise_id_sql = '''
select id
from fitness.exercises
where name = %s
'''

user_id_sql = '''
select id
from fitness.users
where name = %s
'''

insert_sql = '''
insert into fitness.mesos
(name, user_id, exercise_id, day_id, date_started)
values (%s, %s, %s, %s, now())
'''

if result:
    user_id = conn.execute_query(user_id_sql, (your_name, ))[0][0]

    for key, value in meso.items():
        for i in value:
            exercise_id = conn.execute_query(exercise_id_sql, (i,))[0][0]
            res = conn.execute_query(insert_sql,
                                     (name, user_id, exercise_id, key,))

        print(res)
