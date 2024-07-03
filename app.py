from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///workouts.db')
db = SQLAlchemy(app)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise = db.Column(db.String(50), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/results', methods=['POST'])
def results():
    exercise = request.form['exercise']
    sets = request.form['sets']
    reps = request.form['reps']
    weight = request.form['weight']
    date = request.form['date']
    new_workout = Workout(exercise=exercise, sets=sets, reps=reps, weight=weight, date=date)
    db.session.add(new_workout)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_message="Page not found"), 404

if __name__ == '__main__':
    app.run(debug=True)