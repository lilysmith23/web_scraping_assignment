from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    mars_data = mongo.db.mars_dict.collection.find_one()
    return render_template("index.html", mars=mars_data)


@app.route("/scrape")
def scrape():
    
    #run scape function:
    mars_dict=scrape_mars.scrape_info()

    #update mongo database:
    mongo.db.mars_dict.collection.update({}, mars_dict, upsert=True)
    
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)