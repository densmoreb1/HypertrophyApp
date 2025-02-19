from helpers.connection import MySQLDatabase
import streamlit as st

st.set_page_config(page_title='Create Meso', layout='wide')
conn = MySQLDatabase()

# Get the available exercises
groups_sql = conn.execute_query('select distinct muscle_group from exercises')
muscle_groups = [g[0] for g in groups_sql]


# Get the current user
user_name = st.session_state.role
user_id = conn.execute_query('select id from users where name = %s', (user_name,))[0][0]


st.write('# Create Meso')
name = st.text_input('Name of Meso').lower()
weeks = st.selectbox('Weeks', (4, 5, 6))
days = st.selectbox('Days per week', (1, 2, 3, 4, 5, 6, 7))
result = st.button('Create Meso')

cols = st.columns(days, border=True)

meso = {}
for i in range(len(cols)):
    if days >= i:
        with cols[i]:
            st.write(f'### Day {i + 1}')

            exercises_per = st.selectbox('How many exercises?', (1, 2, 3, 4, 5, 6), key=f'per{i}')

            final_exercise_list = []
            for r in range(exercises_per):
                muscle = st.selectbox(f'Exercise {r + 1}',
                                      muscle_groups,
                                      key=f'muscle{i, r}',
                                      index=None,
                                      placeholder='Muscle Group')

                sql = conn.execute_query('select name from exercises where muscle_group = %s', (muscle,))
                exercise_selection = [e[0] for e in sql]
                exercise = st.selectbox('Exercise',
                                        exercise_selection,
                                        key=f'exercise{i, r}',
                                        index=None,
                                        placeholder='Exercise',
                                        label_visibility='collapsed')

                final_exercise_list.append(exercise)

            meso[i] = final_exercise_list


if result and name != '':

    if len(conn.execute_query('select name from mesos where name = %s and user_id = %s', (name, user_id))) > 0:
        st.toast('Meso already exists with name', icon="⚠️")
        st.stop()

    meso_id = conn.execute_query('select max(meso_id) from mesos where user_id = %s', (user_id,))[0][0]
    if meso_id is None:
        meso_id = 0
    else:
        meso_id += 1

    for week_id in range(weeks):
        for day_id, value in meso.items():
            for order_id in range(len(value)):
                exercise_id = conn.execute_query('select id from exercises where name = %s', (value[order_id],))[0][0]
                insert_query = '''
                            insert into mesos
                            (meso_id, name, user_id, completed, set_id, reps, weight, order_id, exercise_id, day_id, week_id, date_created) values
                            (%s,        %s,      %s,        %s,     %s,   %s,     %s,       %s,          %s,     %s,      %s, now())
                            '''
                conn.execute_query(insert_query, (meso_id, name, user_id, 0, 0, 0, 0, order_id, exercise_id, day_id, week_id,))
    st.toast('Meso Created', icon='✅')
