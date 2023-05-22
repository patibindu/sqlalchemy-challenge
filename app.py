# Import the dependencies.

from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# View all of the classes that automap found
Base.classes.keys()

# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """Home Route to list all my route paths"""
    return(
        f"Welcome to Hawaii Weather API<br/>"
        f"Available Routes: <br>"
        f"/api/v1.0/Precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tob<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end><br>"
        f"note: start and end must be dates in YYYYMMDD format with"
    )

# Precipitation Route
@app.route("/api/v1.0/Precipitation")
def prcp_output():
    """Return Precipitation for the last 12 months in json format"""

    # Calculate the date one year from the last date in data set.

    year_ago = dt.datetime(2017,8,23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    prcp_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()
    prcp_query

    # Close Session
    session.close()

    precip = {date: prcp for date, prcp in prcp_query}

    #return jsonify version of precip
    return  jsonify(precip)

#Station Route
@app.route("/api/v1.0/stations")
def station_output():
    """Return list of all stations"""
    all_stations_results = session.query(Station.station).all()

    # Close Session
    session.close()

    # convert list of tuples into normal list
    all_stations = list (np.ravel(all_stations_results))

    #return jsonify version of 
    return jsonify(all_stations)

# Temperature Route
@app.route("/api/v1.0/tob")
def temp_output():
    """ return temp's for the last year for most active station"""
    # Calculate the date one year from the last date in data set.
    year_ago = dt.datetime(2017,8,23) - dt.timedelta(days=365)

    # Query the last 12 months of temperature observation data for this station and plot the results as a histogram
    most_active_station_query = session.query(Measurement.tobs).\
                            filter(Measurement.station == 'USC00519281').\
                            filter(Measurement.date >= year_ago).all()

    # Close Session
    session.close()

    #unravel results
    temperatures = list(np.ravel(most_active_station_query))

    # return array of temp for last year for station USC00519281
    return jsonify(temperatures = temperatures)

    # start and start end routes for temp's for USC00519281
   # @app.route("/api/v1.0/<start>")
   # def temp start():
   #     """ """



if __name__ == "__main__":
    app.run(debug = True)