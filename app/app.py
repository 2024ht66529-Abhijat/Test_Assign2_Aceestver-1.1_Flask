
from flask import Flask, render_template, request
app = Flask(__name__)
PROGRAMS={
 'Fat Loss (FL)':{
  'workout':"Mon: Back Squat 5x5 + Core<br>Tue: EMOM 20min Assault Bike<br>Wed: Bench Press + 21-15-9<br>Thu: Deadlift + Box Jumps<br>Fri: Zone 22 Cardio 30min",
  'diet':"Breakfast: Egg Whites + Oats<br>Lunch: Grilled Chicken + Brown Rice<br>Dinner: Fish Curry + Millet Roti<br>Target: ~2000 kcal",
  'color':'#e74c3c','factor':22},
 'Muscle Gain (MG)':{
  'workout':"Squat / Bench / Deadlift Split",
  'diet':"High Calorie South Indian Plan (~3200 kcal)",
  'color':'#2ecc71','factor':35},
 'Beginner (BG)':{
  'workout':"Full Body Beginner Circuit",
  'diet':"Balanced Tamil Meals",
  'color':'#3498db','factor':26}
}
@app.route('/',methods=['GET','POST'])
def index():
 calories=None
 if request.method=='POST':
  w=float(request.form.get('weight',0))
  p=request.form.get('program')
  if w>0 and p in PROGRAMS:
   calories=int(w*PROGRAMS[p]['factor'])
 return render_template('index.html',programs=PROGRAMS,calories=calories)
if __name__=='__main__': app.run(host='0.0.0.0',port=5000)
