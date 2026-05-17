from helpers.connection import MySQLDatabase
from helpers.login import login
import streamlit as st

st.write("# Create Template")

# Login
if st.session_state.get("authentication_status"):
    authenticator = st.session_state.get("authenticator")
    if authenticator:
        authenticator.logout(location="sidebar", key="create_logout")
        authenticator.login(location="unrendered", key="create_login")
else:
    login()

conn = MySQLDatabase()


# Get the current user
if "username" in st.session_state and st.session_state["username"] is not None:
    user_name = st.session_state["username"]
    user_id = conn.execute_query("select id from users where name = %s", (user_name,))[
        0
    ][0]
else:
    st.stop()


name = st.text_input("Name of Template").lower()
days = st.selectbox("Days per week", (1, 2, 3, 4, 5, 6, 7))
edit_template = None

button_cols = st.columns([1, 7])
with button_cols[0]:
    create = st.button("Create Template")
with button_cols[1]:
    # Get Meso for the selected User
    query = "select distinct name from templates"
    sql = conn.execute_query(query)
    templates = [g[0] for g in sql]

    if len(templates) > 0:
        edit_template = st.checkbox("Edit Template ")

groups_sql = conn.execute_query(
    "select distinct muscle_group from exercises order by muscle_group", params=None
)
muscle_groups = [g[0] for g in groups_sql]

template_name = None
if edit_template:
    template_name = st.selectbox("Past Templates", templates)
else:
    meso_name = None

if not template_name:
    meso = {}
    cols = st.columns(days, border=True)
    for i in range(len(cols)):
        if days >= i:
            with cols[i]:
                st.write(f"### Day {i + 1}")

                exercises_per = st.selectbox(
                    label="How many exercises?",
                    options=(1, 2, 3, 4, 5, 6, 7, 8, 9),
                    key=f"per{i}{name}",
                )

                final_exercise_list = []
                for r in range(exercises_per):
                    muscle = st.selectbox(
                        label=f"Muscle {r + 1}",
                        options=muscle_groups,
                        index=None,
                        key=f"muscle{i}{r}{name}",
                        placeholder="Muscle Group",
                    )

                    final_exercise_list.append(muscle)

                    meso[i] = final_exercise_list
else:
    query = """
            select name, day_id, muscle_group, order_id
            from templates
            where name = %s
            """
    current_template = conn.execute_query(query, (template_name,))

    st.write(current_template)

    meso = {}
    cols = st.columns(len(current_template), border=True)
    for i in range(len(cols)):
        with cols[i]:
            st.write(f"### Day {i + 1}")

            exercises_per = st.selectbox(
                label="How many exercises?",
                options=(1, 2, 3, 4, 5, 6, 7, 8, 9),
                index=len(current_template[i]),
                key=f"per{i}{name}",
            )


if create and name != "":
    previous_templates = conn.execute_query(
        "select name from templates where name = %s", (name,)
    )
    if len(previous_templates) > 0:
        st.toast("Template already exists with name", icon="⚠️")
        st.stop()

    for day_id, value in meso.items():
        for order_id in range(len(value)):
            query = """
                INSERT INTO templates
                (
                    name,
                    day_id,
                    muscle_group,
                    order_id,
                    date_created
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    NOW()
                )
                """
            conn.execute_query(query, (name, day_id, value[order_id], order_id))

    st.toast("Template Created", icon="✅")
