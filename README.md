I want to find temperatures and precipitation in Hawaii for a given week between the last year of the sample,
starting in August 23, 2016 and ending August 23, 2017.  The data exists in sqlite:///Resources/hawaii.sqlite
and starts in September 2009 at 9 different observation stations around Hawaii.

```from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
total = session.query(func.count(Measurement.date)).all()
last_day = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
rows = []
for row in session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date.between('2016-08-23','2017-08-23')).all():  #.limit(15)
    rows.append(row)

    # Save the query results as a Pandas DataFrame and set the index to the date column
row_df = pd.DataFrame.from_dict(rows)
row_df = row_df.set_index("date")
row_df = row_df.sort_index()
# row_df
row_df.plot(rot=90)```
![Precipitation Bar Chart](C:\Users\Shalesh Kumbhat\Documents\sqlalchemy-challenge\precipitation.png)

Here are the number of observations at each temperation at station USC005192821 during 8/23/16 - 8/23/17.
```year_ago_day = dt.date(2017,8,23)-dt.timedelta(days=365)
row_df['date'] = pd.to_datetime(row_df['date'])
last_year_df = row_df.loc[row_df['date']>year_ago_day]
big_station_df = last_year_df.loc[last_year_df['station']==most_active]
hist = big_station_df['tobs'].hist(bins=12)
plt.xlabel("Temperature")
plt.ylabel("# of Observations") 
plt.title("Observed Temperatures at Station USC00519281")```
![Temperature Bar Chart](C:\Users\Shalesh Kumbhat\Documents\sqlalchemy-challenge\USC005192821.png)

```from flask import request

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
Station = Base.classes.station```

```def calc_temps(start_date, end_date):
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
        print(calc_temps('2012-02-28', '2012-03-05'))
```
```fig, ax = plt.subplots(figsize=plt.figaspect(2.))
xpos = 1
yerr = tmax - tmin
bar = ax.bar(xpos, tmax, yerr=yerr, alpha = 0.5, color = 'coral', align = 'center')
ax.set(ylabel = "Temp (F)", xticks = range(xpos), xticklabels = 'a', title="Trip Average Temp")
ax.margins(.2,.2)
fig.tight_layout()
fig.show()```
![Avg Temp Chart](C:\Users\Shalesh Kumbhat\Documents\sqlalchemy-challenge\AvgTemp.png)