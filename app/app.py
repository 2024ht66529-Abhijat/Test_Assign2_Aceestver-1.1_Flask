from flask import Flask, render_template, request

app = Flask(__name__)

programs = {
    'Fat Loss (FL)': {
        'workout': "Mon: 5x5 Back Squat + AMRAP<br>Tue: EMOM 20min Assault Bike<br>Wed: Bench Press + 21-15-9<br>Thu: 10RFT Deadlifts/Box Jumps<br>Fri: 30min Active Recovery",
        'diet': "3 Egg Whites + Oats Idli<br>Grilled Chicken + Brown Rice<br>Fish Curry + Millet Roti",
        'color': '#e74c3c'
    },
    'Muscle Gain (MG)': {
        'workout': "Squat, Bench, Deadlift split",
        'diet': "High calorie South Indian plan",
        'color': '#2ecc71'
    }
}

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        weight = request.form.get("weight")
        program = request.form.get("program")
        # Simple calorie calculation logic
        if program == "Fat Loss (FL)":
            calories = int(weight) * 15
        else:
            calories = int(weight) * 20
        result = f"Estimated Calories: {calories}"
    return render_template("index.html", programs=programs, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
