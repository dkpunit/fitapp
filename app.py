from flask import Flask, request, redirect, render_template
from string import punctuation
import subprocess
import os

app = Flask(__name__)

@app.before_request
def before_request():
    if 'DYNO' in os.environ:  # Only redirect on Heroku
        if not request.is_secure:
            return redirect(request.url.replace("http://", "https://", 1), code=301)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fitapp')
def fitapp():
    return render_template('fitapp.html')

@app.route('/dashboard')
def dashboard():
    subprocess.Popen(["streamlit", "run", "dashboard.py"])
    return redirect("http://localhost:8501")

if __name__ == "__main__":
    app.run()

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Results route
@app.route('/results', methods=['POST'])
def results():
    # Your existing results logic here
    name = request.form['name'].strip().lower()
    unit = request.form['unit'].strip().lower()
    weight = float(request.form['weight'])
    height_unit = request.form['height_unit'].strip().lower()
    height = float(request.form['height'])
    age = int(request.form['age'])
    gender = request.form['gender'].strip().lower()
    gain_or_lose = request.form['goal'].strip().lower()
    goal_weight = float(request.form['goal_weight'])
    act_lvl = float(request.form['act_lvl'])

    if any(p in name for p in punctuation):
        return "Name contains punctuation."
    if name.isdigit():
        return "Name contains numbers."
    if unit not in ['kg', 'lbs', 'kilograms', 'kilogram', 'pounds', 'pound', 'lb', 'kgs']:
        return "Invalid weight unit."
    if height_unit not in ['cm', 'centimeter', 'centimeters', 'meters', 'meter', 'm']:
        return "Invalid height unit."
    if gender not in ['male', 'female']:
        return "Invalid gender."
    if gain_or_lose not in ['gain', 'lose']:
        return "Invalid goal choice."
    if (gain_or_lose == "gain" and goal_weight <= weight) or (gain_or_lose == "lose" and goal_weight >= weight):
        return "Invalid goal weight."
    if not (1.2 <= act_lvl <= 2.2):
        return "Invalid activity level."

    bmi, bmi_status = calculate_bmi(weight, height, unit, height_unit)
    bmr = calculate_bmr(gender, age, weight, height, unit, height_unit)
    tdee = round(bmr * act_lvl)
    caloric_intake = calculate_caloric_intake(bmr, act_lvl, gain_or_lose)

    return render_template('results.html', name=name, bmi=f"{bmi:.1f}", bmi_status=bmi_status, bmr=f"{bmr:.1f}", tdee=tdee, caloric_intake=caloric_intake)

def calculate_bmi(weight, height, unit, height_unit):
    if unit in ('lbs', 'lb', 'pound', 'pounds'):
        weight /= 2.205
    if height_unit in ('cm', 'centimeter', 'centimeters'):
        height /= 100
    bmi = weight / (height ** 2)
    if bmi < 16:
        return bmi, "severely underweight"
    elif 16 <= bmi < 18.5:
        return bmi, "underweight"
    elif 18.5 <= bmi < 25:
        return bmi, "healthy"
    elif 25 <= bmi < 30:
        return bmi, "overweight"
    else:
        return bmi, "obese"

def calculate_bmr(gender, age, weight, height, unit, height_unit):
    if unit in ('lbs', 'lb', 'pound', 'pounds'):
        weight /= 2.205
    if height_unit in ('cm', 'centimeter', 'centimeters'):
        height /= 100
    if gender == "male":
        bmr = 10 * weight + 6.25 * (height * 100) - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * (height * 100) - 5 * age - 161
    return bmr

def calculate_caloric_intake(bmr, act_lvl, gain_or_lose):
    if gain_or_lose == "gain":
        return round(bmr * act_lvl * 1.20)
    elif gain_or_lose == "lose":
        return round(bmr * act_lvl * 0.80)

if __name__ == "__main__":
    app.run()
