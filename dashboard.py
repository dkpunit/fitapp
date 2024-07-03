import streamlit as st

st.title("Fitness Dashboard")

st.sidebar.header("User Input Parameters")

def user_input():
    name = st.sidebar.text_input("Name", "John Doe")
    weight = st.sidebar.number_input("Weight (kg)", min_value=0, value=70)
    height = st.sidebar.number_input("Height (cm)", min_value=0, value=175)
    age = st.sidebar.number_input("Age", min_value=0, value=25)
    gender = st.sidebar.selectbox("Gender", ("Male", "Female"))
    activity_level = st.sidebar.selectbox("Activity Level", ("Sedentary", "Lightly active", "Moderately active", "Very active", "Super active"))
    goal = st.sidebar.selectbox("Goal", ("Lose weight", "Maintain weight", "Gain weight"))
    return name, weight, height, age, gender, activity_level, goal

name, weight, height, age, gender, activity_level, goal = user_input()

st.write(f"Name: {name}")
st.write(f"Weight: {weight} kg")
st.write(f"Height: {height} cm")
st.write(f"Age: {age}")
st.write(f"Gender: {gender}")
st.write(f"Activity Level: {activity_level}")
st.write(f"Goal: {goal}")