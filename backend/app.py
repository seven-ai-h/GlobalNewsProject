from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# Load dummy CSV
data = pd.read_csv("dummy_data.csv")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/data")
def get_data():
    return jsonify(data.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
