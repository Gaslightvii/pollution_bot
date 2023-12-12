from json import dumps
from httplib2 import Http
import requests
from bs4 import BeautifulSoup
import re



def send():
# Messages to be sent
    inside = "Please stay indoors. "
    outside = "Please go outdoors. "
    message = "Please await further instructions. "

    # Runs get pollution function
    pollution = get_pollution()

    # If pollution to high, send message inside
    if pollution > 150:
        message = inside
        send_message(message, pollution)
    # If pollution is ok, send message outside
    else:
        message = outside
        send_message(message, pollution)



def send_message(message, pollution):

    # URL of Google Space
    url = "https://chat.googleapis.com/v1/spaces/XXXX/messages?key=XXXX"
    
    # Message to be sent
    app_message = {"text": (message) +
                   "\nThe pollution AQI is: " + str(pollution)}

    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    http_obj = Http()
    response = http_obj.request(
    uri=url,
    method="POST",
    headers=message_headers,
    body=dumps(app_message),
        )


def get_pollution():
    # Make a request to the website
    aqi = requests.get("https://www.iqair.com/thailand/bangkok/king-s-college-international-school-bangkok")

    # Parse the HTML response
    soup = BeautifulSoup(aqi.content, "html.parser")

    # Find the AQI element
    aqi_element = soup.find("div", class_="aqi-value")

    # Extract the AQI value
    aqi_value = aqi_element.text

    # Strip non integer values
    aqi_value = strip_non_integers(aqi_value)

    # Return the AQI value
    return int(aqi_value)



def strip_non_integers(string):
  return re.sub(r"[^\d]", "", string)


send()
