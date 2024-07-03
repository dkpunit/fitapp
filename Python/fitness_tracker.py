import streamlit as st
import pandas as pd
from datetime import datetime
import altair as alt

# Initialize session state
if 'workout_logs' not in st.session_state:
    st.session_state.workout_logs = []
if 'current_plan' not in st.session_state:
    st.session_state.current_plan = []

# Function to generate a simple workout plan based on user input
def generate_plan(goals, experience, equipment):
    plan = []
    # Dummy logic to generate a plan
    exercises = ["Squats", "Bench Press", "Deadlift", "Overhead Press", "Bicep Curls", "Tricep Extensions", "Pull-ups", "Push-ups"]
    for exercise in exercises:
        plan.append({
            "Exercise": exercise,
            "Sets": 3 if experience == "Beginner" else 4,
            "Reps": 10 if goals == "Hypertrophy" else 5,
            "Notes": f"Use {equipment} if available."
        })
    return plan

# Sidebar for user input
st.sidebar.header("Customize Your Training Plan")
goals = st.sidebar.selectbox("Training Goals", ["Hypertrophy", "Strength", "Endurance"])
experience = st.sidebar.selectbox("Experience Level", ["Beginner", "Intermediate", "Advanced"])
equipment = st.sidebar.text_input("Available Equipment", placeholder="e.g., dumbbells, barbell, resistance bands")
generate_button = st.sidebar.button("Generate Plan")

if generate_button:
    st.session_state.current_plan = generate_plan(goals, experience, equipment)

# Display current training plan
st.header("Your Training Plan")
if st.session_state.current_plan:
    for exercise in st.session_state.current_plan:
        st.subheader(exercise["Exercise"])
        st.write(f"Sets: {exercise['Sets']}")
        st.write(f"Reps: {exercise['Reps']}")
        st.write(f"Notes: {exercise['Notes']}")

# Sidebar for logging workout
st.sidebar.header("Log Your Workout")
exercises = st.sidebar.multiselect(
    "Select Exercises",
    [ex["Exercise"] for ex in st.session_state.current_plan],
)
exercise_details = {}

for exercise in exercises:
    st.sidebar.subheader(exercise)
    sets = st.sidebar.number_input(f"Sets for {exercise}", min_value=1, step=1, key=f"{exercise}_sets")
    reps = st.sidebar.number_input(f"Reps for {exercise}", min_value=1, step=1, key=f"{exercise}_reps")
    weight = st.sidebar.number_input(f"Weight for {exercise} (lbs)", min_value=0.0, step=1.0, key=f"{exercise}_weight")
    notes = st.sidebar.text_area(f"Notes for {exercise}", placeholder="Any notes about the exercise", key=f"{exercise}_notes")
    exercise_details[exercise] = {"Sets": sets, "Reps": reps, "Weight": weight, "Notes": notes}

log_button = st.sidebar.button("Add Log")

# Add log to the workout logs list
if log_button and exercise_details:
    for exercise, details in exercise_details.items():
        st.session_state.workout_logs.append({
            "Exercise": exercise,
            "Sets": details["Sets"],
            "Reps": details["Reps"],
            "Weight": details["Weight"],
            "Notes": details["Notes"],
            "Date": datetime.now().strftime("%Y-%m-%d")
        })
    st.sidebar.success(f"Logged: {', '.join(exercise_details.keys())}")

# Convert logs to a DataFrame
logs_df = pd.DataFrame(st.session_state.workout_logs)

# Display the logs
st.header("Workout Logs")
if not logs_df.empty:
    st.table(logs_df)
else:
    st.write("No logs yet. Start by adding a workout.")

# Option to clear logs
if st.button("Clear Logs"):
    st.session_state.workout_logs = []
    st.write("Logs cleared!")

# Visualization of progress
if not logs_df.empty:
    st.header("Progress Over Time")
    progress_chart = alt.Chart(logs_df).mark_line(point=True).encode(
        x='Date:T',
        y='Weight:Q',
        color='Exercise:N',
        tooltip=['Exercise', 'Sets', 'Reps', 'Weight', 'Notes', 'Date']
    ).interactive()

    st.altair_chart(progress_chart, use_container_width=True)
