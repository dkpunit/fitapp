from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import pandas as pd
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workouts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise = db.Column(db.String(50), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_workout():
    exercise = request.form.get('exercise')
    sets = request.form.get('sets')
    reps = request.form.get('reps')
    weight = request.form.get('weight')
    date = request.form.get('date')

    new_workout = Workout(exercise=exercise, sets=sets, reps=reps, weight=weight, date=date)
    db.session.add(new_workout)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/results')
def results():
    workouts = Workout.query.all()
    df = pd.read_sql_table('workout', con=db.engine)
    return render_template('results.html', workouts=workouts, tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('workouts.db')
    df = pd.read_sql_query("SELECT * FROM workout", conn)
    return render_template('dashboard.html', tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)