from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the database model
class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise = db.Column(db.String(50), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    workouts = Workout.query.all()
    return render_template('index.html', workouts=workouts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        exercise = request.form['exercise']
        sets = request.form['sets']
        reps = request.form['reps']
        weight = request.form['weight']
        new_workout = Workout(exercise=exercise, sets=sets, reps=reps, weight=weight)
        db.session.add(new_workout)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete(id):
    workout = Workout.query.get_or_404(id)
    db.session.delete(workout)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    workout = Workout.query.get_or_404(id)
    if request.method == 'POST':
        workout.exercise = request.form['exercise']
        workout.sets = request.form['sets']
        workout.reps = request.form['reps']
        workout.weight = request.form['weight']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', workout=workout)

@app.route('/dashboard')
def dashboard():
    workouts = Workout.query.all()
    df = pd.DataFrame([(w.exercise, w.sets, w.reps, w.weight, w.date) for w in workouts],
                      columns=['Exercise', 'Sets', 'Reps', 'Weight', 'Date'])
    
    if not df.empty:
        fig = px.bar(df, x='Date', y='Weight', color='Exercise', barmode='group')
        graph_html = fig.to_html(full_html=False)
    else:
        graph_html = ''

    return render_template('dashboard.html', graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)