import streamlit as st

st.write('# Create Meso')


days = st.selectbox('Days per week', (1, 2, 3, 4, 5, 6, 7))
cols = st.columns(days)

if days >= 1:
    with cols[0]:
        st.write('Day 1')
        st.selectbox('Muscle Group', ('Chest', 'Back', 'Triceps',
                     'Biceps', 'Shoulders', 'Quads', 'Calves', 'Abs', 'Hams'),
                     key=1)

if days >= 2:
    with cols[1]:
        st.write('Day 2')
        st.selectbox('Muscle Group', ('Chest', 'Back', 'Triceps',
                     'Biceps', 'Shoulders', 'Quads', 'Calves', 'Abs', 'Hams'),
                     key=2)

if days >= 3:
    with cols[2]:
        st.write('Day 3')
        st.selectbox('Muscle Group', ('Chest', 'Back', 'Triceps',
                     'Biceps', 'Shoulders', 'Quads', 'Calves', 'Abs', 'Hams'),
                     key=3)

if days >= 4:
    with cols[3]:
        st.write('Day 4')
        st.selectbox('Muscle Group', ('Chest', 'Back', 'Triceps',
                     'Biceps', 'Shoulders', 'Quads', 'Calves', 'Abs', 'Hams'),
                     key=4)

if days >= 5:
    with cols[4]:
        st.write('Day 5')
        st.selectbox('Muscle Group', ('Chest', 'Back', 'Triceps',
                     'Biceps', 'Shoulders', 'Quads', 'Calves', 'Abs', 'Hams'),
                     key=5)

if days >= 6:
    with cols[5]:
        st.write('Day 6')
        st.selectbox('Muscle Group', ('Chest', 'Back', 'Triceps',
                     'Biceps', 'Shoulders', 'Quads', 'Calves', 'Abs', 'Hams'),
                     key=6)

if days >= 7:
    with cols[6]:
        st.write('Day 7')
        st.selectbox('Muscle Group', ('Chest', 'Back', 'Triceps',
                     'Biceps', 'Shoulders', 'Quads', 'Calves', 'Abs', 'Hams'),
                     key=7)
