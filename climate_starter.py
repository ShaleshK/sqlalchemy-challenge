import numpy as np
import pandas as pd
import datetime as dt
from flask import request

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
# apt-get install python3-flask
from flask import Flask, jsonify
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
#Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)
app = Flask(__name__)
@app.route('/')     #flask function that we’ll use as a decorator
def home():
	print('Server received request for "Home" page…')
	return (
        f"Welcome to the Hawaii Temperature & Precipitation API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route('/api/v1.0/precipitation')
def precipitation():
    print('Server received request for "Precipitation" page…')
    last_day = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    rows = []
    for row in session.query(Measurement.date, Measurement.prcp).filter(Measurement.date.between('2016-08-23','2017-08-23')).all():  #.limit(15)
        rows.append(row)
    session.close()
    return jsonify(rows)

@app.route('/api/v1.0/stations')
def stations():
    print('Server received request for "Stations" page…')
    results = session.query(Measurement.station,func.count(Measurement.station)).group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()
    all_stations = []
    for station,count in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["count"] = count
        all_stations.append(station_dict)
    session.close()
    return jsonify(all_stations)
   
@app.route('/api/v1.0/tobs')
def tobs():
    print('Server received request for "Temperature Observations" page…')
    year_ago_day = dt.date(2017,8,23)-dt.timedelta(days=365)
    rows = []
    for row in session.query(Measurement.prcp, Measurement.station, Measurement.tobs, Measurement.date, Measurement.id).all():
        rows.append(row)
    row_df = pd.DataFrame.from_dict(rows)
    most_active = row_df.station.value_counts().idxmax()
    # row_df['date'] = pd.to_datetime(row_df['date'])
    # last_year_df = row_df.loc[row_df['date']>year_ago_day]
    # big_station_df = last_year_df.loc[last_year_df['station']==most_active]
    # temp = big_station_df.set_index('date').T.to_dict('list')
    results = session.query(Measurement.tobs).filter(Measurement.station == most_active).filter(Measurement.date>year_ago_day).all() 
    all_tobs = list(np.ravel(results))
    session.close()
    return jsonify(all_tobs)

@app.route('/api/v1.0/<start>')
def tempobs(start):
    #     start (string): A date string in the format %Y-%m-%d
    # start_df = row_df.loc[row_df['date']>start]
    # tobs = start_df.set_index('date').T.to_dict('list')
    # return jsonify(tobs)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()
    return jsonify(results)
    #return jsonify({"error": f"Date needs to be in %Y-%m-%d format."}), 404

@app.route('/api/v1.0/<start>/<end>')
#def obstemp(start='2000-01-01', end='2999-12-31'):
def obstemp(start=None, end=None):
    #     start (string): A date string in the format %Y-%m-%d
    #     end (string): A date string in the format %Y-%m-%d

    # start  = request.args.get('start')
    # end  = request.args.get('end')

    # start_end_df = row_df[row_df.date.between(start,end)]
    # tobs = start_end_df.set_index('date').T.to_dict('list')
    # return jsonify(tobs)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    return jsonify(results)
    #return jsonify({"error": f"Date needs to be in %Y-%m-%d format."}), 404
if __name__ == "__main__":
    app.run(debug=True)

