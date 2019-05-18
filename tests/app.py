from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo 
import webscraping_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# conn = "mongodb://localhost:27017"
# client = pymongo.MongoClient(conn,ConnectTimeoutMS=30000)
# mongo = PyMongo(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

## create / Use database
# db = client.mars_db
# ## create/use collection. 
# mars_coll = db.mars_data_coll

@app.route("/")
def index():
	 # Get the data from mongodb.
    mars_info = mongo.db.mars_info.find_one()

    # return template and data
    return render_template("index.html", mars_info=mars_info)

#import python function from mars_scraping.py
from webscraping_mars import mars_scrape
# Route that will trigger scrape function.
@app.route("/scrape")
def scrape():
    mars_info = mongo.db.mars_info 
    mars_data = webscraping_mars.mars_scrape()
    mars_info.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)

# from flask import Flask, render_template, redirect
# from flask_pymongo import PyMongo
# import scrape_craigslist

# app = Flask(__name__)

# # Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/craigslist_app"
# mongo = PyMongo(app)

# # Or set inline
# # mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


# @app.route("/")
# def index():
#     listings = mongo.db.listings.find_one()
#     return render_template("index.html", listings=listings)


# @app.route("/scrape")
# def scraper():
#     listings = mongo.db.listings
#     listings_data = scrape_craigslist.scrape()
#     listings.update({}, listings_data, upsert=True)
#     return redirect("/", code=302)


# if __name__ == "__main__":
#     app.run(debug=True)

