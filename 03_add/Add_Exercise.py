from helpers.connection import MySQLDatabase
import streamlit as st

conn = MySQLDatabase()

st.set_page_config(page_title='Add Exercise', layout='centered')
st.write('# Add Exercise')

name = st.text_input('Exercise Name').lower()
group = st.text_input('Muscle Group').lower()
result = st.button('Create Exercise')

query = 'select name from exercises'
sql = conn.execute_query(query)
names = [u[0] for u in sql]

insert_sql = 'insert into exercises (name, muscle_group) values (%s, %s)'

if result:
    if name not in names:
        conn.execute_query(insert_sql, (name, group))
        st.toast('Exercise created')
    else:
        st.toast('Exercise already exists')
