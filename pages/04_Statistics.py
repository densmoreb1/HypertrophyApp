from helpers.connection import MySQLDatabase
import streamlit as st

st.set_page_config(page_title='Statistics', layout='wide')
st.write('# Statistics')

conn = MySQLDatabase()

# be able to view sets per weeks per muscle group
# view volumne of exercise over each workout
