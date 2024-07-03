from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy # type: ignore
from sqlalchemy.sql import func # type: ignore
import streamlit as st
import pandas as pd
import plotly.express as px # type: ignore
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workouts.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=func.current_date())
    exercise = db.Column(db.String(100), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Workout {self.exercise} on {self.date}>'

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        date = request.form.get('date')
        exercise = request.form.get('exercise')
        sets = request.form.get('sets')
        reps = request.form.get('reps')
        weight = request.form.get('weight')

        if not date or not exercise or not sets or not reps or not weight:
            flash('Please fill out all fields', 'danger')
        else:
            new_workout = Workout(date=datetime.datetime.strptime(date, '%Y-%m-%d'), exercise=exercise, sets=int(sets), reps=int(reps), weight=float(weight))
            db.session.add(new_workout)
            db.session.commit()
            flash('Workout added successfully', 'success')
            return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/workouts')
def workouts():
    workouts = Workout.query.order_by(Workout.date.desc()).all()
    return render_template('workouts.html', workouts=workouts)

@app.route('/delete/<int:id>')
def delete(id):
    workout = Workout.query.get_or_404(id)
    db.session.delete(workout)
    db.session.commit()
    flash('Workout deleted successfully', 'success')
    return redirect(url_for('workouts'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    workout = Workout.query.get_or_404(id)
    if request.method == 'POST':
        workout.date = datetime.datetime.strptime(request.form.get('date'), '%Y-%m-%d')
        workout.exercise = request.form.get('exercise')
        workout.sets = int(request.form.get('sets'))
        workout.reps = int(request.form.get('reps'))
        workout.weight = float(request.form.get('weight'))
        
        db.session.commit()
        flash('Workout updated successfully', 'success')
        return redirect(url_for('workouts'))
        
    return render_template('edit.html', workout=workout)

@app.route('/dashboard')
def dashboard():
    # Streamlit setup
    st.set_page_config(page_title="Fitness Dashboard", layout="wide")

    # Dashboard title
    st.title("Fitness Dashboard")

    # Welcome message
    st.write("Welcome to the Fitness Dashboard")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Analytics", "Settings"])

    # Content based on sidebar selection
    if page == "Home":
        st.subheader("Home")
        st.write("Home page content goes here...")
    elif page == "Analytics":
        st.subheader("Analytics")
        workouts = Workout.query.all()
        if workouts:
            df = pd.DataFrame([(w.date, w.exercise, w.sets, w.reps, w.weight) for w in workouts], columns=['Date', 'Exercise', 'Sets', 'Reps', 'Weight'])
            fig = px.line(df, x='Date', y='Weight', color='Exercise', title='Workout Progress Over Time')
            st.plotly_chart(fig)
        else:
            st.write("No workout data available.")
    elif page == "Settings":
        st.subheader("Settings")
        st.write("Settings page content goes here...")

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)