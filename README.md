# sqlalchemy-challenge

In this repository, we analyze information from a database (hawaii.sqlite) of weather stations in Hawaii and the various temperature and precipitation recordings made at those places over a range of years. We begin by unpacking our data in a python notebook for modelling and visualization with pandas. Specifically, we created a bar chart of average precipiation across our weather stations for the most recent year of recorded data and a histogram of temperature frequencies at the most active weather station for the most recent year as well along with some summary statistics for the recorded preciptation and temperatures.

After our analysis and visualization with pandas, we create a Flask app with similar functionality to the python notebook we just created. On visit, the webserver will give the list of possible routes:
  /api/v1.0/precipitation - returns the recorded preciptation for the most recent year as a dictionary with date as the key and precipitation as the value
  /api/v1.0/stations - returns a list of all stations in our dataset along with their respective information (id, name, latitude, longitude, elevation)
  /api/v1.0/tobs - returns a list of recorded temperatures from the most recent year at the most active station (USC00519281)
  /api/v1.0/<start> - returns minimum, average, and maximum recorded temperature for time period beginning at start date and going to end of dataset
  /api/v1.0/<start>/<end> - returns minimum, average, and maximum recorded temperature for time period from start date to end date
  
