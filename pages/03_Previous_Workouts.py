from helpers.connection import MySQLDatabase
from helpers.login import login
import streamlit as st

# Login
if st.session_state.get("authentication_status"):
    authenticator = st.session_state.get("authenticator")
    authenticator.logout(location="sidebar", key="previous_logout")
    authenticator.login(location="unrendered", key="previous_logout")
else:
    login()

conn = MySQLDatabase()


# Get the current user
if "username" in st.session_state and st.session_state["username"] is not None:
    user_name = st.session_state["username"]
    user_id = conn.execute_query("select id from users where name = %s", (user_name,))[0][0]
else:
    st.stop()


# Get Meso for the selected User
query = "select distinct name, meso_id from mesos where user_id = %s order by meso_id desc"
sql = conn.execute_query(query, (user_id,))
mesos = [g[0] for g in sql]


# Check if there are no mesos for this user
if len(mesos) > 0:
    meso_name = st.selectbox("Mesos", mesos)
    meso_id = conn.execute_query("select meso_id from mesos where name = %s", (meso_name,))[0][0]
else:
    st.write("Looks you have not created a meso yet")
    st.stop()


# Get the completed week_ids
query = "select distinct week_id from mesos where meso_id = %s and user_id = %s and completed = 1 order by week_id desc"
sql = conn.execute_query(query, (meso_id, user_id))
weeks = [d[0] + 1 for d in sql]

if len(weeks) > 0:
    week_id = st.selectbox("Week", weeks) - 1
else:
    st.write("You have not completed a workout yet")
    st.stop()


# Get the completed day_ids
query = "select distinct day_id from mesos where completed = 1 and meso_id = %s and week_id = %s and user_id = %s order by day_id"
sql = conn.execute_query(query, (meso_id, week_id, user_id))
days = [str(d[0] + 1) for d in sql]

day_tabs = st.tabs(days)

for day_id in range(len(day_tabs)):
    with day_tabs[day_id]:
        st.write(f"## Day {day_id + 1}")

        # Get the exercises
        query = """
                select distinct e.name, e.id, m.order_id
                from mesos m
                inner join exercises e on m.exercise_id = e.id
                where m.day_id = %s and m.week_id = %s and m.meso_id = %s and m.user_id = %s
                order by m.order_id
                """
        exercises = conn.execute_query(query, (day_id, week_id, meso_id, user_id))

        for i in range(len(exercises)):
            exercise_name = exercises[i][0]

            query = """
                    select m.set_id, m.reps, m.weight, e.name, e.id, m.order_id
                    from mesos m
                    inner join exercises e on m.exercise_id = e.id
                    where m.day_id = %s and m.week_id = %s and m.meso_id = %s and m.user_id = %s and e.name = %s
                    order by m.order_id
                    """
            workout = conn.execute_query(query, (day_id, week_id, meso_id, user_id, exercise_name))

            st.write(f"### {exercise_name}")

            for i in range(len(workout)):
                set_id = workout[i][0]
                reps = workout[i][1]
                weight = workout[i][2]
                name = workout[i][3]
                exercise_id = workout[i][4]
                order_id = workout[i][5]

                cols = st.columns(3)
                with cols[0]:
                    st.write(f"Set: {set_id + 1}")
                with cols[1]:
                    st.write(f"Weight: {weight}")
                with cols[2]:
                    st.write(f"Reps: {reps}")

st.write("###")
if st.button("Current Workout"):
    st.switch_page("01_Current_Workout.py")

if st.button("Add a Week"):

    max_week_id = int(conn.execute_query("select max(week_id) from mesos where user_id = %s and meso_id = %s", (user_id, meso_id))[0][0])

    query = """select distinct day_id, exercise_id, order_id, set_id
               from mesos where user_id = %s and meso_id = %s and week_id = %s
               order by day_id, order_id
            """

    workout_week = conn.execute_query(query, (user_id, meso_id, max_week_id))

    for each_day in workout_week:
        day_id = each_day[0]
        exercise_id = each_day[1]
        order_id = each_day[2]
        set_id = each_day[3]

        insert_query = """
                    insert into mesos
                    (meso_id, name, user_id, completed, completed_day, set_id, reps, weight, order_id, exercise_id, day_id, week_id, date_created) values
                    (%s,        %s,      %s,        %s,             %s,    %s,   %s,     %s,       %s,          %s,      %s,     %s,        now())
                    """
        conn.execute_query(
            insert_query, (meso_id, meso_name, user_id, 0, 0, set_id, None, None, order_id, exercise_id, day_id, max_week_id + 1)
        )

    st.toast(f"Week {max_week_id + 2} added", icon="✅")

if st.button("Delete Meso"):
    query = "delete from mesos where user_id = %s and meso_id = %s"
    conn.execute_query(query, (user_id, meso_id))
    st.toast(f"{meso_name} deleted", icon="👑")
