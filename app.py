# import  required dependencies 
from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrape_mars

#create flask app
app = Flask(__name__)

#set up mongo 
app.config["MONGO_URI"] = "mongodb://localhost:27017/scrape_mars"
mongo = PyMongo(app)

#Route that will query Mongo Database and pass data to html
@app.route("/")
def home(): 

    # Find data
    scraped_mars_data1 = mongo.db.scraped_mars_data.find_one()

    # Return template and data
    return render_template("index.html", data=scraped_mars_data1)


 # Route will call and scrape
@app.route("/scrape")
def scrape():

    # scrape
    scraped_mars_data2 = scrape_mars.scrape_info()

    # update mongo db
    mongo.db.scraped_mars_data.update({}, scraped_mars_data2, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)  

#@app.route("/")
#def index():
    #setup mongo
 #   app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
  #  mongo=PyMongo(app)
   # # data=mongo.db.marsdict.find()
    #data = mongo.db.marsdict.find_one()
    #return render_template("index.html", data=data)


#@app.route("/scrape")
#def scrape():
    #setup mongo
 #   app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
  #  mongo=PyMongo(app)

   # data=mongo.db.marsdict
   # listings_data=scrape_mars.scrape_info()
   # print(listings_data)
   # data.update({},listings_data)
    #return redirect("/", code=302)
    


#if __name__=="__main__":
 #   app.run(debug=True)