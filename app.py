from flask import Flask, render_template, request
import numpy as np
import pickle

app = Flask(__name__)

# Load stacking model (KNN + DT + Naive Bayes)
with open("diabeties.pkl", "rb") as f:
    model = pickle.load(f)


@app.route("/", methods=["GET", "POST"])
def diabetes():

    if request.method == "POST":

        features = [
            float(request.form["HighBP"]),
            float(request.form["HighChol"]),
            float(request.form["CholCheck"]),
            float(request.form["BMI"]),
            float(request.form["Smoker"]),
            float(request.form["Stroke"]),
            float(request.form["HeartDiseaseorAttack"]),
            float(request.form["PhysActivity"]),
            float(request.form["Fruits"]),
            float(request.form["Veggies"]),
            float(request.form["HvyAlcoholConsump"]),
            float(request.form["AnyHealthcare"]),
            float(request.form["NoDocbcCost"]),
            float(request.form["GenHlth"]),
            float(request.form["MentHlth"]),
            float(request.form["PhysHlth"]),
            float(request.form["DiffWalk"]),
            float(request.form["Sex"]),
            float(request.form["Age"]),
        ]

        final_features = np.array(features).reshape(1, -1)
        prediction = model.predict(final_features)[0]

        if prediction == 1:
            result = "High Risk of Diabetes"
        else:
            result = "Low Risk of Diabetes"

        return render_template("index.html", prediction_text=result)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)