from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo 
import webscraping_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn,ConnectTimeoutMS=30000)
## create / Use database
db = client.mars_db
## create/use collection. 
collection = db.mars_data_collection

@app.route("/")
def index():
	 # Get the data from mongodb.
    mars_data = collection.find_one()
    
    # return template and data
    return render_template("index.html", mars_data=mars_data)

#import python function from mars_scraping.py
from webscraping_mars import mars_scrape
# Route that will trigger scrape function.
@app.route("/scrape")
def scraper():
     
    mars_data = mars_scrape()
    collection.update({"id":1}, {"$set": mars_data}, upsert=True)
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
