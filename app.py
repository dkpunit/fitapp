from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workouts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise = db.Column(db.String(80), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_workout():
    exercise = request.form['exercise']
    sets = int(request.form['sets'])
    reps = int(request.form['reps'])
    weight = int(request.form['weight'])
    date_str = request.form['date']
    date = datetime.strptime(date_str, '%Y-%m-%d').date()  # Convert string to date
    new_workout = Workout(exercise=exercise, sets=sets, reps=reps, weight=weight, date=date)
    db.session.add(new_workout)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/results')
def results():
    with db.engine.connect() as connection:  # Correct way to use the engine with pandas
        df = pd.read_sql_table('workout', con=connection)
    return render_template('results.html', tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)