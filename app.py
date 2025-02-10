from flask import Flask, render_template, request
from scraper import scrape_amazon

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/review", methods=["POST"])
def review():
    search_query = request.form.get("content", "").strip()
    
    if not search_query:
        return render_template("result.html", products=[], error="Please enter a valid product name.")

    products = scrape_amazon(search_query)  # Fetch new data for each search

    if not products:
        return render_template("result.html", products=[], error=f"No results found for '{search_query}'.")

    return render_template("result.html", products=products)

if __name__ == "__main__":
    app.run(debug=True)
