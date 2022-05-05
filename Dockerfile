# write some code to build your image

FROM python:3.8.12

# The trained model
COPY model.joblib /model.joblib

# the code of the project which is required in order to load the model
COPY TaxiFareModel /TaxiFareModel

# the code of our API
COPY api /api

# the list of requirements
COPY requirements.txt /requirements.txt

# to install the requied dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# To specify which command the container should run once it has started
CMD uvicorn api.fast:app --root-path /predict --host 0.0.0.0
