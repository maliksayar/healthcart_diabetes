# from flask import Flask, render_template, request
# import numpy as np
# import pickle

# app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     if request.method == 'GET':
#         return render_template('index.html')
#     elif request.method == 'POST':
#         with open('heart_disease_RFC.pkl', 'rb') as model_file:
#             model = pickle.load(model_file)
        
#         # Extract features from the heart disease prediction form with float type casting
#         # Medical History & Risk Factors
#         HighBP = float(request.form['HighBP'])
#         HighChol = float(request.form['HighChol'])
#         CholCheck = float(request.form['CholCheck'])
#         BMI = float(request.form['BMI'])
#         Smoker = float(request.form['Smoker'])
#         Stroke = float(request.form['Stroke'])
#         Diabetes = float(request.form['Diabetes'])
        
#         # Lifestyle & Physical Activity
#         PhysActivity = float(request.form['PhysActivity'])
#         Fruits = float(request.form['Fruits'])
#         Veggies = float(request.form['Veggies'])
#         HvyAlcoholConsump = float(request.form['HvyAlcoholConsump'])
        
#         # Healthcare Access & Health Status
#         AnyHealthcare = float(request.form['AnyHealthcare'])
#         NoDocbcCost = float(request.form['NoDocbcCost'])
#         GenHlth = float(request.form['GenHlth'])
#         MentHlth = float(request.form['MentHlth'])
#         PhysHlth = float(request.form['PhysHlth'])
#         DiffWalk = float(request.form['DiffWalk'])
        
#         # Demographics
#         Sex = float(request.form['Sex'])
#         Age = float(request.form['Age'])
        
#         # Create feature array
#         features = np.array([[HighBP, HighChol, CholCheck, BMI, Smoker, Stroke, Diabetes,
#                             PhysActivity, Fruits, Veggies, HvyAlcoholConsump,
#                             AnyHealthcare, NoDocbcCost, GenHlth, MentHlth, PhysHlth, DiffWalk,
#                             Sex, Age]])
        
#         # Make prediction
#         prediction = model.predict(features)
        
#         # if prediction[0]==1:
#         #     result="You have heart disease"
#         # else:
#         #     result="You do not have heart disease"
        
#         # Render result template with prediction
#         return render_template('index.html', prediction=prediction)
    
#     else:
#         # If the request method is not GET or POST, render the index page
#         return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_URL = "https://jarvis0852-diabetes_prediction_ai_ml.hf.space/predict"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html', prediction=None)

    elif request.method == 'POST':
        try:
            data = {}

            # Gender — string field
            data['gender'] = request.form['gender']
            if data['gender'] not in ['Female', 'Male', 'Other']:
                return render_template('index.html', prediction=None, error="Invalid value for Gender.")

            # Age
            data['age'] = float(request.form['age'])
            if not 0 <= data['age'] <= 120:
                return render_template('index.html', prediction=None, error="Age must be between 0 and 120.")

            # Binary fields (0 or 1)
            binary_fields = ['hypertension', 'heart_disease']
            for field in binary_fields:
                value = float(request.form[field])
                if value not in [0, 1]:
                    return render_template('index.html', prediction=None, error=f"Invalid value for {field}. Must be 0 or 1.")
                data[field] = value

            # Smoking history — string field
            data['smoking_history'] = request.form['smoking_history']
            if data['smoking_history'] not in ['never', 'No Info', 'current', 'former', 'ever', 'not current']:
                return render_template('index.html', prediction=None, error="Invalid value for Smoking History.")

            # BMI
            data['bmi'] = float(request.form['bmi'])
            if not 10 <= data['bmi'] <= 70:
                return render_template('index.html', prediction=None, error="BMI must be between 10 and 70.")

            # HbA1c Level
            data['HbA1c_level'] = float(request.form['HbA1c_level'])
            if not 3.0 <= data['HbA1c_level'] <= 15.0:
                return render_template('index.html', prediction=None, error="HbA1c Level must be between 3.0 and 15.0.")

            # Blood Glucose Level
            data['blood_glucose_level'] = float(request.form['blood_glucose_level'])
            if not 50 <= data['blood_glucose_level'] <= 400:
                return render_template('index.html', prediction=None, error="Blood Glucose Level must be between 50 and 400.")

            # Call Hugging Face API
            response = requests.post(API_URL, json=data, timeout=30)

            if response.status_code == 200:
                result = response.json()
                prediction = [result.get('prediction', 0)]  # Pass as list for template compatibility
                return render_template('index.html', prediction=prediction, error=None)
            else:
                return render_template('index.html', prediction=None, error="Prediction service unavailable")

        except ValueError:
            return render_template('index.html', prediction=None, error="Please enter valid numbers for all fields.")
        except Exception as e:
            return render_template('index.html', prediction=None, error=f"Error: {str(e)}")

    else:
        return render_template('index.html', prediction=None)


if __name__ == '__main__':
    app.run(debug=True)
