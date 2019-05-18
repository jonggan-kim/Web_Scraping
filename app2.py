# Import Dependencies 
from flask import Flask, render_template,redirect
from flask_pymongo import PyMongo
import webscraping_mars2
import os


app= Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"

mongo = PyMongo(app)

# Create route that renders index.html template and finds documents from mongo
@app.route("/")

def home():

    mars_info =mongo.db.mars_info.find_one()
    return render_template("index.html", mars_info=mars_info)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 

    # Run scrapped functions
    mars_info = mongo.db.mars_info
    mars_data = webscraping_mars2.scrape_mars_news()
    mars_data = webscraping_mars2.scrape_mars_image()
    mars_data = webscraping_mars2.scrape_mars_facts()
    mars_data = webscraping_mars2.scrape_mars_weather()
    mars_data = webscraping_mars2.scrape_mars_hemispheres()
    mars_data = webscraping_mars2.scrape_mars_datetime()
    mars_info.update({}, mars_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)

