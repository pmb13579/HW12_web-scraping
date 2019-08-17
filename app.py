from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/U12_db"
mongo = PyMongo(app)

@app.route("/")
def index():
    scraping1 = mongo.db.scraping1.find_one()
#    scraping1 = "desrtyecd"
    print ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    print(scraping1)
    return render_template("index.html", scraping1=scraping1)


@app.route("/scrape")
def scraper():
    scrape_mars.scrape()
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
