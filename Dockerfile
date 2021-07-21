FROM python:3.8-slim-buster

# Install the requirements first of all to benefit from layer caching.
COPY requirements.txt /
RUN pip install -r /requirements.txt

# Copy the code to the image...
COPY . /code
WORKDIR /code

# ...and run it
CMD [ "python", "./CoronaIncidenceChange.py" ]