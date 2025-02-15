from helpers.connection import MySQLDatabase
import streamlit as st

conn = MySQLDatabase()

# Add a user
st.write('## Add a User')
user = st.text_input('Username').lower()

query = 'select name from users'
sql = conn.execute_query(query)
names = [u[0] for u in sql]

if user != '':
    if user not in names:
        query = 'insert into users (name) values (%s)'
        conn.execute_query(query, (user,))

        query = 'select id from users where name = %s'
        id = conn.execute_query(query, (user,))[0][0]
        st.toast(f'User "{user}" was created with id of {id}')
    else:
        query = 'select id from users where name = %s'
        id = conn.execute_query(query, (user,))[0][0]
        st.toast(f'User "{user}" already exists with id of {id}')
else:
    st.stop()
