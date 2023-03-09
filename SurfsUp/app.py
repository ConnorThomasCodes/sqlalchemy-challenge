import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, or_, and_

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"Precipitation data from 2016-08-24 to 2017-08-23<br/><br/>"
        f"/api/v1.0/stations<br/>"
        f"List of weather stations in dataset<br/><br/>"
        f"/api/v1.0/tobs<br/>"
        f"Temperature observations for the previous year at weather station USC00519281<br/><br/>"
        f"/api/v1.0/&ltstart&gt<br/>"
        f"Min, avg, and max temperature for all dates after start date (i.e. start = 2015-04-01)<br/><br/>"
        f"/api/v1.0/&ltstart&gt/&ltend&gt<br/>"
        f"Min, avg, and max temperature for all dates between start and end date (i.e. start = 2015-04-01, end = 2015-07-20)"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    most_recent=session.query(Measurement, Measurement.date).order_by(Measurement.date.desc()).limit(1).all()[0][1]
    new_date = pd.to_datetime(most_recent)+pd.DateOffset(years=-1)
    d = new_date.to_pydatetime()
    queries = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= d).all()
    query_dict = dict(queries)
    return jsonify(query_dict)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    queries = session.query(Station.station,Station.name,Station.longitude,Station.latitude,Station.elevation).all()
    stations = []
    for station in queries:
        station_dict = {}
        station_dict["Station ID"] = station[0]
        station_dict["Name"] = station[1]
        station_dict["Longitude"] = station[2]
        station_dict["Latitidue"] = station[3]
        station_dict["Elevation"] = station[4]
        stations.append(station_dict)
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    most_recent=session.query(Measurement, Measurement.date).order_by(Measurement.date.desc()).limit(1).all()[0][1]
    new_date = pd.to_datetime(most_recent)+pd.DateOffset(years=-1)
    d = new_date.to_pydatetime()
    most_active = session.query(Measurement.station,func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()[0][0]
    queries = session.query(Measurement.tobs).filter(and_(Measurement.date >= d,Measurement.station == most_active)).all()
    return jsonify([x[0] for x in queries])

@app.route("/api/v1.0/<start>")
def s_range(start):
    session = Session(engine)
    queries = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    sdict = {}
    for Tmin, Tavg, Tmax in queries:
        sdict["Minimum Temperature"] = Tmin
        sdict["Average Temperature"] = Tavg
        sdict["Maximum Temperature"] = Tmax
    return jsonify(sdict)

@app.route("/api/v1.0/<start>/<end>")
def se_range(start,end):
    session = Session(engine)
    queries = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(and_(Measurement.date >= start,Measurement.date <= end)).all()
    sedict = {}
    for Tmin, Tavg, Tmax in queries:
        sedict["Minimum Temperature"] = Tmin
        sedict["Average Temperature"] = Tavg
        sedict["Maximum Temperature"] = Tmax
    return jsonify(sedict)

if __name__ == '__main__':
    app.run(debug=True)