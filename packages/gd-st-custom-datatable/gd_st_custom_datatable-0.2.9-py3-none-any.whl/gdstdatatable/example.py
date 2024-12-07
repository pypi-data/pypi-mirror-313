import pandas as pd
import streamlit as st
from copy import copy
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
    result = df
    if "action" in action:
        if action["actionId"] > st.session_state.action_id:
            if action["action"] == "edit":
                id = action["id"]
                column = action["colName"]
                value = action["value"]
                df.loc[df["id"] == id, column] = value
                print(
                    "apply action ",
                    df,
                    action["actionId"],
                    st.session_state.datatable["actionId"],
                )
                result = df
            st.session_state.action_id = action["actionId"]
        else:
            print("skip action", action["actionId"], st.session_state.action_id)
    return result


if "df" not in st.session_state:
    st.session_state.df = init_df()

if "action_id" not in st.session_state:
    st.session_state.action_id = 0


def show_df():
    print("show_df", st.session_state.action_id)
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
        debug=True,
    )

    if action:
        print("action=", action)
        st.write("action:", action)
        st.session_state.df = apply_action(action, st.session_state.df)


def update_select():
    print(st.session_state.select_all)
    st.session_state.df.loc[:, "select"] = st.session_state.select_all
    print(f"get actionId {st.session_state.action_id}")
    st.session_state.action_id += 1
    print(f"set actionId {st.session_state.action_id}")


left, right = st.columns([1, 1])
with left:
  checked = st.checkbox("select all", key="select_all", on_change=update_select)
with right:
  if st.button("delete"):
      print(st.session_state.df)
      st.session_state.df = st.session_state.df.loc[
          st.session_state.df.loc[:, "select"] == False, :
      ]
      print(st.session_state.df)
      st.session_state.action_id += 1
show_df()
