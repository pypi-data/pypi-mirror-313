import pandas as pd
import streamlit as st
from gdstdatatable import gd_datatable

# Test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run custom_datatable/example.py`


def init_df():
    ids = list(range(1, 8))
    selecteds = [False for i in ids]
    names = [f"name{i}" for i in ids]
    desc = [f"desc{i}" for i in ids]

    raw_data = {"id": ids, "select": selecteds, "desc": desc, "name": names}
    df = pd.DataFrame(raw_data, columns=["select", "id", "desc", "name"])
    return df


def apply_action(action, df):
    if action["action"] != "edit":
        return df
    else:
        id = action["id"]
        column = action["colName"]
        value = action["value"]
        df.loc[df["id"] == id, column] = value
        return df


if "df" not in st.session_state:
    st.session_state.df = init_df()

if "action_id" not in st.session_state:
    st.session_state.action_id = 0


@st.fragment
def show_df():
    action = gd_datatable(
        st.session_state.df,
        id_column="id",
        column_specs=[
            {"name": "select", "width": 50, "editable": True},
            {"name": "name", "grow": 2, "editable": True},
            {"name": "desc", "grow": 2},
            {"name": "view", "width": 60},
        ],
        add_view_column=True,
        width=800,
        action_id=st.session_state.action_id,
        key="datatable",
    )

    if action:
        print("action=", action)
        st.write("action:", action)
        if action["actionId"] > st.session_state.action_id:
            st.session_state.df = apply_action(action, st.session_state.df)
            st.session_state.action_id = action["actionId"]
            print("df=", st.session_state.df)
        else:
            print(
                "already applied actionId=",
                action["actionId"],
                "session.action_id=",
                st.session_state.action_id,
            )


show_df()
