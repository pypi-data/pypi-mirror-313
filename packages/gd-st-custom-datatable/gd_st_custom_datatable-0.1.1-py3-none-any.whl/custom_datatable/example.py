import pandas as pd
import streamlit as st
from custom_datatable import custom_datatable

# Test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run custom_datatable/example.py`


def init_df():
    ids = list(range(1, 8))
    selecteds = [False for i in ids]
    names = [f"name{i}" for i in ids]

    raw_data = {"id": ids, "select": selecteds, "name": names}
    df = pd.DataFrame(raw_data, columns=["select", "id", "name"])
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


@st.fragment
def show_df():
    action = custom_datatable(
        st.session_state.df,
        id_column="id",
        hides=["id"],
        editables=["select", "name"],
        column_width={"select": 50, "name": 150, "view": 70},
        add_view_column=True,
    )

    if action:
        print("action=", action)
        st.write("action:", action)
        st.session_state.df = apply_action(action, st.session_state.df)
        print("df=", st.session_state.df)


show_df()
