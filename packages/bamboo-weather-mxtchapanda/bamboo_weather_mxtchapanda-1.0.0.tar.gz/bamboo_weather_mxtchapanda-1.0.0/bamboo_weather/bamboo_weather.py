import datetime

import requests
from pprint import pprint


class Weather:
    """
    Create a Weather Object to fetch Weather for a location based on a city name or latitude/longitude arguments.

    Usage:
       sf = Weather(city='San Francisco')
       san_fran =  Weather(lat=37.773972,lon=-122.431297)

    Methods:
        sf.current() - Get Current Weather
        sf.forecast() - Get Forecast JSON
        sf.forecast_simple() - Get a list containing an hourly forecast for the date
    """
    def __init__(self, city=None, lat=None, lon=None):
        baseurl = "https://api.weatherapi.com/v1"
        API_KEY = "9ccb15851ea4497da3a185244240412"
        query = ""
        if city:
            print(1)
            query = city
        elif lat and lon:
            query = f"{lat},{lon}"
        else:
            raise TypeError("Provide a city orr latitude and longitude arguments!")

        today = datetime.datetime.now()
        forecast_date = today + datetime.timedelta(5)
        forecast_date = forecast_date.strftime("%Y-%m-%d")

        url = f"{baseurl}/forecast.json?q={query}&days=5&key={API_KEY}&aqi=&dt={today}"
        request = requests.get(url)
        if request.status_code != 200:
            raise ValueError("Location not found!")
        self.data =request.json()


        self.city = self.data['location']['name']
        self.region = self.data['location']['region']


    def current(self):
        return self.data['current']

    def forecast(self):
        return self.data['forecast']

    def forecast_simple(self):
        forecast_data = self.forecast()['forecastday'][0]
        # output = f"Weather in {self.city}, {self.region}:\n"
        output = []
        for hour in forecast_data['hour']:
            data_list = [hour['time'], hour['temp_f'], hour['condition']['text']]
            output.append(data_list)
            # string_data = [str(item) for item in data_list ]
            # hour_stats = " ".join(string_data)
            # output +=  hour_stats + "\n"
        return output


mechsburg = Weather(city="Mechanicsburg, PA")
broc = Weather(lat=37.773972,lon=-122.431297)

pprint(broc.forecast_simple())
