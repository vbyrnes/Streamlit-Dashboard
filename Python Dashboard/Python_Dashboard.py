# @Project:  Python Dashboard w/ Streamlit



import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import altair as alt

#######################################
# PAGE SETUP
#######################################

st.set_page_config(page_title="Email Dashboard", page_icon=":bar_chart:", layout="wide")

st.title("Email Dashboard")
st.markdown("v1.0")

#######################################
# DATA LOADING
#######################################



df=pd.read_excel(io="totals.xlsx",
        engine="openpyxl",
        usecols="A:F",
        nrows=13)
 

st.dataframe(df)

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
Month = st.sidebar.multiselect(
    "Select the Month:",
    options=df["month"].unique(),
    default=df["month"].unique()
)

filtered_df =  df.query("month == @Month")

df.reset_index()
df.dropna()
# ---- MAINPAGE ----
st.title(":email: Blocked Emails")
st.markdown("##")

chart_data = pd.DataFrame(filtered_df, columns=["blocked", "received", "delivered","spam","month"])

st.bar_chart(chart_data, x=("month"), y=("blocked", "received", "delivered","spam"),stack=False)



b=st.altair_chart(alt.Chart(chart_data).transform_fold(
  ["blocked", "received", "delivered","spam"],
  as_=["_", "value"]
).mark_bar().encode(
  x=alt.X("_:N", sort=None),
  y=alt.Y("value:Q", sort=None),
  column=alt.Column("month:N", sort=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
))


actions = ["blocked", "received", "delivered","spam"] # or df_users_community.columns[3:]

st.plotly_chart(px.bar(chart_data, x='month', y=actions, 
             labels={'variable':'action', 'value':'count'}, 
             barmode='group', title='**Double Click To Reset Graph').update_layout(xaxis={'categoryorder': 'array'}))

st.plotly_chart(px.line(chart_data, x='month', y=actions, 
             labels={'variable':'action', 'value':'count'}, 
              title='**Double Click To Reset Graph').update_layout(xaxis={'categoryorder': 'array'}))

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
