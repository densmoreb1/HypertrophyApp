from helpers.connection import MySQLDatabase
import streamlit as st

st.set_page_config(page_title='Add Exercise', layout='centered')
st.write('# Add Exercise')

conn = MySQLDatabase()

name = st.text_input('Exercise Name').lower()
group = st.text_input('Muscle Group').lower()

result = st.button('Create Exercise')

insert_sql = '''
insert into exercises (name, muscle_group)
values (%s, %s)
'''

if result:
    conn.execute_query(insert_sql, (name, group))
