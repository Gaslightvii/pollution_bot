import datetime
from httplib2 import Http
import json
from pytz import timezone
import requests


def send():
# Messages to be sent
    inside = "Please stay indoors."
    outside = "You can go outside."
    message = "Please await further instructions."

    # Runs get pollution function
    pollution, updated = get_pollution()

    # If pollution too high, send message inside
    if pollution == 0:
        message = message
        send_message(message, pollution, updated)

    elif pollution > 150:
        message = inside
        send_message(message, pollution, updated)

    # If pollution is ok, send message outside
    else:
        message = outside
        send_message(message, pollution, updated)



def send_message(message, pollution, updated):

    # URL of Google Space
    url = "https://chat.googleapis.com/v1/spaces/AAAAhYDOgMA/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=5EzFKnnkYjv8cR5EfSpkL99v-PvBkOMlQGX9kAf7UsA"

    # Message to be sent
    app_message = {"text": (message) +
                   "\nThe pollution AQI is: " + str(pollution) +
                   "\nData updated: " + (updated)}

    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    http_obj = Http()
    response = http_obj.request(
    uri=url,
    method="POST",
    headers=message_headers,
    body=json.dumps(app_message),
        )


def get_pollution():
    api_key = '643c4650-c5ca-4703-b82b-76cd09ef5b11'
    endpoint_url = 'https://device.iqair.com/v3/5f4c6806972145c5b069d362'

    headers = {'Authorization': f'Bearer {api_key}'}  # Include the API key in the headers
    response = requests.get(endpoint_url, headers=headers)

    if response.status_code == 200:
        # If success, process the data
        data = response.json()  # Assuming the response is in JSON format

        pretty_json = json.dumps(data, indent=4)  # Use 4 spaces for indentation
        # Extract the current aqius
        pollution = data["current_measurement"]["aqius"]

        # Extract the time stamp
        updated = data["current_measurement"]["ts"]

        # Parse the UTC time string
        utc_time = datetime.datetime.fromisoformat(updated)

        # Create a timezone object for Bangkok (ICT)
        bangkok_timezone = timezone("Asia/Bangkok")

        # Localize the UTC time to Bangkok time
        bangkok_time = utc_time.astimezone(bangkok_timezone)
        updated = (bangkok_time.strftime("%H:%M"))

    else:
        pollution = 0
        updated = "Data not found"


    # Return the AQI value and the time it was updated
    return pollution, updated

send()


