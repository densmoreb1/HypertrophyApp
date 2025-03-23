import streamlit as st
import datetime


@st.dialog("Records")
def records(conn, user_id, meso_id, exercise_id, exercise_name):

    # most volume in one set
    query = """
            select max(weight), max(reps), date_completed
            from mesos
            where user_id = %s and completed = 1 and exercise_id = %s
            group by date_completed, exercise_id
            order by max(weight) * max(reps)
            desc limit 1
            """
    sql = conn.execute_query(query, (user_id, exercise_id))[0]
    reps = sql[1]
    weight = sql[0]
    date = datetime.datetime.strftime(sql[2], "%m/%d/%Y")

    st.write(f"### {exercise_name.capitalize()}")
    st.write(f"#### Most Volume {date}")
    st.write(f"Weight: {weight} Reps: {reps}")

    # most weight


@st.dialog("Add exercise")
def add_exercise(conn, user_id, meso_id, day_id, week_id, meso_name):

    query = "select distinct muscle_group from exercises"
    sql = conn.execute_query(query)
    groups = [u[0] for u in sql]

    group = st.selectbox("Muscle Group", groups, index=None)

    sql = conn.execute_query("select name from exercises where muscle_group = %s", (group,))
    exercise_selection = [e[0] for e in sql]
    exercise = st.selectbox("Exercise", exercise_selection, index=None, placeholder="Exercise", label_visibility="collapsed")
    if exercise:
        exercise_id = conn.execute_query("select id from exercises where name = %s", (exercise,))[0][0]

    query = "select max(order_id) from mesos where user_id = %s and meso_id = %s and day_id = %s and week_id = %s"
    max_order_id = conn.execute_query(query, (user_id, meso_id, day_id, week_id))[0][0]

    if st.button("Confirm"):
        insert_query = """
                    insert into mesos
                    (meso_id, name, user_id, completed, set_id, reps, weight, order_id, exercise_id, day_id, week_id, date_created) values
                    (%s,        %s,      %s,        %s,     %s,   %s,     %s,       %s,          %s,     %s,      %s, now())
                    """
        conn.execute_query(insert_query, (meso_id, meso_name, user_id, 0, 0, None, None, max_order_id + 1, exercise_id, day_id, week_id))
        st.rerun()


@st.dialog("Change exercise")
def change_exercise(exercise_name, exercise_id, conn, day_id, meso_id, user_id, week_id):
    group = conn.execute_query("select muscle_group from exercises where id = %s", (exercise_id,))[0][0]
    sql = conn.execute_query("select name from exercises where muscle_group = %s", (group,))
    exercise_selection = [e[0] for e in sql]

    updated_exercise = st.selectbox(f"{group.capitalize()} Exercises", exercise_selection)
    updated_exercise_id = conn.execute_query("select id from exercises where name = %s", (updated_exercise,))[0][0]

    query = """
            update mesos m
            set m.exercise_id = %s, m.weight = NULL, m.reps = NULL, m.completed = 0
            where m.day_id = %s and m.meso_id = %s and m.exercise_id = %s and user_id = %s and week_id >= %s
            """
    if st.button("Confirm"):
        conn.execute_query(query, (updated_exercise_id, day_id, meso_id, exercise_id, user_id, week_id))
        st.rerun()


@st.dialog("Exercise history")
def exercise_history(exercise_name, exercise_id, user_id, conn):
    query = """
            select distinct name, meso_id
            from mesos
            where exercise_id = %s and user_id = %s and completed = 1
            order by meso_id desc
            """
    sql = conn.execute_query(query, (exercise_id, user_id))
    for i in range(len(sql)):
        history_meso = sql[i][0]
        st.markdown(f"## <ins>{history_meso}</ins>", unsafe_allow_html=True)

        history = """
                  select distinct week_id, day_id
                  from mesos
                  where exercise_id = %s and user_id = %s and completed = 1 and name = %s
                  order by week_id desc
                  """
        history_sql = conn.execute_query(history, (exercise_id, user_id, history_meso))

        for j in range(len(history_sql)):
            history_week = history_sql[j][0]
            history_day = history_sql[j][1]
            history_reps = """
                            select reps, weight, set_id, date_completed
                            from mesos
                            where exercise_id = %s and user_id = %s and completed = 1 and name = %s and week_id = %s and day_id = %s
                            order by set_id
                            """
            history_reps_sql = conn.execute_query(history_reps, (exercise_id, user_id, history_meso, history_week, history_day))
            date = datetime.datetime.strftime(history_reps_sql[0][3], "%m/%d/%Y")

            st.write(f"### {date} Week {history_week + 1} Day {history_day + 1}")

            for h in range(len(history_reps_sql)):
                reps = history_reps_sql[h][0]
                weight = history_reps_sql[h][1]
                st.write(f"Weight: {weight} Reps: {reps}")
