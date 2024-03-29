from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def home():
    mars = mongo.db.mars.find_one()

    return render_template("index.html", mars_data=mars)

@app.route("/scrape")
def scrape():

    mars = mongo.db.mars
    scraped_mars_data = scrape_mars.scrape_news()
    scraped_mars_data = scrape_mars.scrape_featured_image()
    scraped_mars_data = scrape_mars.scrape_facts()
    scraped_mars_data = scrape_mars.scrape_weather()
    scraped_mars_data = scrape_mars.scrape_hemispheres()
    mars.update({}, scraped_mars_data, upsert=True)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)