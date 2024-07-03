import tkinter as tk
from tkinter import messagebox
from string import punctuation

class FitnessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fitness App")
        
        # User information variables
        self.name = tk.StringVar()
        self.unit = tk.StringVar()
        self.weight = tk.DoubleVar()
        self.height_unit = tk.StringVar()
        self.height = tk.DoubleVar()
        self.age = tk.IntVar()
        self.gender = tk.StringVar()
        self.gain_or_lose = tk.StringVar()
        self.goal_weight = tk.DoubleVar()
        self.act_lvl = tk.DoubleVar()

        self.create_widgets()
        
    def create_widgets(self):
        # Name input
        tk.Label(self.root, text="What is your name?: ").grid(row=0, column=0)
        tk.Entry(self.root, textvariable=self.name).grid(row=0, column=1)
        
        # Weight unit input
        tk.Label(self.root, text="Preferred weight unit (Kg/Lbs): ").grid(row=1, column=0)
        tk.Entry(self.root, textvariable=self.unit).grid(row=1, column=1)
        
        # Weight input
        tk.Label(self.root, text="What is your weight?: ").grid(row=2, column=0)
        tk.Entry(self.root, textvariable=self.weight).grid(row=2, column=1)
        
        # Height unit input
        tk.Label(self.root, text="Preferred height unit (cm/m): ").grid(row=3, column=0)
        tk.Entry(self.root, textvariable=self.height_unit).grid(row=3, column=1)
        
        # Height input
        tk.Label(self.root, text="What is your height?: ").grid(row=4, column=0)
        tk.Entry(self.root, textvariable=self.height).grid(row=4, column=1)
        
        # Age input
        tk.Label(self.root, text="What is your age?: ").grid(row=5, column=0)
        tk.Entry(self.root, textvariable=self.age).grid(row=5, column=1)
        
        # Gender input
        tk.Label(self.root, text="What is your gender (male/female)?: ").grid(row=6, column=0)
        tk.Entry(self.root, textvariable=self.gender).grid(row=6, column=1)
        
        # Gain or Lose weight input
        tk.Label(self.root, text="Do you want to gain or lose weight (gain/lose)?: ").grid(row=7, column=0)
        tk.Entry(self.root, textvariable=self.gain_or_lose).grid(row=7, column=1)
        
        # Goal weight input
        tk.Label(self.root, text="What is your goal weight?: ").grid(row=8, column=0)
        tk.Entry(self.root, textvariable=self.goal_weight).grid(row=8, column=1)
        
        # Activity level input
        tk.Label(self.root, text="What is your activity level (1.2 - 2.2)?: ").grid(row=9, column=0)
        tk.Entry(self.root, textvariable=self.act_lvl).grid(row=9, column=1)
        
        # Calculate button
        tk.Button(self.root, text="Calculate", command=self.calculate).grid(row=10, columnspan=2)
        
    def calculate(self):
        try:
            name = self.name.get().strip().lower()
            if any(p in name for p in punctuation):
                raise ValueError("Name contains punctuation.")
            if name.isdigit():
                raise ValueError("Name contains numbers.")
            
            unit = self.unit.get().strip().lower()
            if unit not in ['kg', 'lbs', 'kilograms', 'kilogram', 'pounds', 'pound', 'lb', 'kgs']:
                raise ValueError("Invalid weight unit.")
            
            weight = self.weight.get()
            
            height_unit = self.height_unit.get().strip().lower()
            if height_unit not in ['cm', 'centimeter', 'centimeters', 'meters', 'meter', 'm']:
                raise ValueError("Invalid height unit.")
            
            height = self.height.get()
            age = self.age.get()
            gender = self.gender.get().strip().lower()
            if gender not in ['male', 'female']:
                raise ValueError("Invalid gender.")
            
            gain_or_lose = self.gain_or_lose.get().strip().lower()
            if gain_or_lose not in ['gain', 'lose']:
                raise ValueError("Invalid goal choice.")
            
            goal_weight = self.goal_weight.get()
            if (gain_or_lose == "gain" and goal_weight <= weight) or (gain_or_lose == "lose" and goal_weight >= weight):
                raise ValueError("Invalid goal weight.")
            
            act_lvl = self.act_lvl.get()
            if not (1.2 <= act_lvl <= 2.2):
                raise ValueError("Invalid activity level.")
            
            bmi, bmi_status = self.calculate_bmi(weight, height, unit, height_unit)
            bmr = self.calculate_bmr(gender, age, weight, height, unit, height_unit)
            tdee = round(bmr * act_lvl)
            caloric_intake = self.calculate_caloric_intake(bmr, act_lvl, gain_or_lose)
            
            result = (
                f"{name.title()}, your BMI is: {bmi:.2f} and you are: {bmi_status}\n"
                f"Your BMR is: {bmr:.2f} (calories burned at rest)\n"
                f"Your TDEE (maintenance calories): {tdee}\n"
                f"To reach your goal, you should consume: {caloric_intake} calories per day.\n"
            )
            messagebox.showinfo("Results", result)
        
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
    
    def calculate_bmi(self, weight, height, unit, height_unit):
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
    
    def calculate_bmr(self, gender, age, weight, height, unit, height_unit):
        if unit in ('lbs', 'lb', 'pound', 'pounds'):
            weight /= 2.205
        if height_unit in ('cm', 'centimeter', 'centimeters'):
            height /= 100
        if gender == "male":
            bmr = 10 * weight + 6.25 * (height * 100) - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * (height * 100) - 5 * age - 161
        return bmr
    
    def calculate_caloric_intake(self, bmr, act_lvl, gain_or_lose):
        if gain_or_lose == "gain":
            more_gain = messagebox.askyesno("Accelerated Gain", "Would you like to see accelerated weight gain?")
            return round(bmr * act_lvl * (1.25 if more_gain else 1.20))
        elif gain_or_lose == "lose":
            more_loss = messagebox.askyesno("Accelerated Loss", "Would you like to see accelerated weight loss?")
            return round(bmr * act_lvl * (0.75 if more_loss else 0.80))


if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessApp(root)
    root.mainloop()
