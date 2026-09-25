from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

# Load trained ML model
model = joblib.load("house_price_model.pkl")


@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    error = None

    # Keep user-entered values
    area = ""
    bedrooms = ""
    age = ""

    if request.method == "POST":

        try:
            area = request.form["area"]
            bedrooms = request.form["bedrooms"]
            age = request.form["age"]

            # Convert values for prediction
            area_value = float(area)
            bedrooms_value = int(bedrooms)
            age_value = float(age)

            # Input validation
            if area_value <= 0:
                error = "Area must be greater than 0."

            elif bedrooms_value <= 0:
                error = "Bedrooms must be at least 1."

            elif age_value < 0:
                error = "Property age cannot be negative."

            else:
                # Make prediction
                prediction = model.predict(
                    [[area_value, bedrooms_value, age_value]]
                )[0]

                prediction = round(prediction, 2)

        except ValueError:
            error = "Please enter valid numbers."

    return render_template(
        "index.html",
        prediction=prediction,
        error=error,
        area=area,
        bedrooms=bedrooms,
        age=age
    )

if __name__ == "__main__":
    app.run()