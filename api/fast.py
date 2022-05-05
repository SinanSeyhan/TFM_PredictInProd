from datetime import date
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
import pytz
from sklearn.linear_model import LinearRegression
import uvicorn


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def index():
    return {"greeting": "Hello world"}


@app.get("/predict")
def predict(pickup_datetime, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, passenger_count):
    '''

    '''

    # create a datetime object from the user provided datetime
    pickup_datetime = "2021-05-30 10:12:00"
    pickup_datetime = datetime.strptime(pickup_datetime, "%Y-%m-%d %H:%M:%S")

    # localize the user datetime with NYC timezone
    eastern = pytz.timezone("US/Eastern")
    localized_pickup_datetime = eastern.localize(pickup_datetime, is_dst=None)

    # localize the datetime to UTC
    utc_pickup_datetime = localized_pickup_datetime.astimezone(pytz.utc)

    formatted_pickup_datetime = utc_pickup_datetime.strftime("%Y-%m-%d %H:%M:%S UTC")

    # Get the params in a dictionary
    dict_res = {
        'key': '2013-07-06 17:18:00.000000119',
        'pickup_datetime': formatted_pickup_datetime,
        'pickup_longitude': np.float(pickup_longitude),
        'pickup_latitude': np.float(pickup_latitude),
        'dropoff_longitude': np.float(dropoff_longitude),
        'dropoff_latitude': np.float(dropoff_latitude),
        'passenger_count': np.int(passenger_count)
    }

    # Create the dataframe from the dict
    X_test = pd.DataFrame([dict_res])

    # Load the ML model
    model = joblib.load('model.joblib', 'r')

    # Make prediction
    fare = {'fare': np.float(model.predict(X_test))}
    return fare
