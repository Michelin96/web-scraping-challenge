from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/marsmission_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find data from the mongo database
    all_info = mongo.db.marsmission.find_one()

    # Return template and data
    return render_template("index.html", marsinfo=all_info)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    #Make a shortcut to the database
    marsmission = mongo.db.marsmission
    # Run the scrape function
    mars_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    marsmission.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
 