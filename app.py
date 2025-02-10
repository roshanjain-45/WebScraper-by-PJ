from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load data from CSV
def load_data():
    try:
        df = pd.read_csv("amazon_products.csv")
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"Error loading data: {e}")
        return []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/review", methods=["POST"])
def review():
    search_query = request.form.get("content", "").lower()
    data = load_data()
    filtered_data = [item for item in data if search_query in item["Product Name"].lower()]
    return render_template("result.html", products=filtered_data)

if __name__ == "__main__":
    app.run(debug=True)
