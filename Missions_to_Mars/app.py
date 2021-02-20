# Import Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Initialize App
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

#### ROUTES ####
@app.route("/")
def echo():
    data = mongo.db.data.find_one()
    return render_template("index.html", data=data)

@app.route("/scrape")
def scrape():
    mars_data = mongo.db.data
    new_data = scrape_mars.scrape()
    mars_data.update({}, new_data, upsert=True)
    return redirect("/", code=302)
#### END ROUTES ####

if __name__ == "__main__":
    app.run(debug=True)