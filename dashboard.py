import streamlit as st
import pandas as pd
import sqlite3

st.title('Fitness Tracker Dashboard')

# Connect to SQLite database
conn = sqlite3.connect('workouts.db')
df = pd.read_sql_query("SELECT * FROM workout", conn)

st.write("## Workouts Data")
st.dataframe(df)

st.write("## Summary Statistics")
st.write(df.describe())

# Visualizations
st.write("## Visualizations")
chart = st.bar_chart(df[['exercise', 'weight']].groupby('exercise').mean())