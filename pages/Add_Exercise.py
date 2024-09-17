from helpers.connection import MySQLDatabase
import streamlit as st

st.write('# Add Exercise')

conn = MySQLDatabase('root', 'remote22', '172.17.0.2', 'fitness')

name = st.text_input('Exercise Name').lower()
group = st.text_input('Muscle Group').lower()

result = st.button('Create Exercise')

insert_sql = '''
insert into fitness.exercises (name, muscle_group)
values (%s, %s)
'''

if result:
    conn.execute_query(insert_sql, (name, group))
