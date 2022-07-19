import requests
from datetime import datetime, timedelta
from configparser import ConfigParser

# import the api key
config = ConfigParser()
config.read("config.ini")
api_key = config["openweathermap"]["api_key"]


def byzip(arg):
    zipcode = zipcodeformat(arg, "1")
    countrycode = zipcodeformat(arg, "2")
    api_url = f"https://api.openweathermap.org/data/2.5/weather?zip={zipcode},{countrycode}&appid={api_key}"
    return weatherformat(requests.get(api_url).json())


def byname(city):
    api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    return weatherformat(requests.get(api_url).json())


def weatherformat(weather):

    return {
            "city": weather["name"],
            "country": weather["sys"]["country"],
            "temp": convert(weather["main"]["temp"], "k:c"),
            "humidity": weather["main"]["humidity"],
            "pressure" : weather["main"]["pressure"],
            "description": weather["weather"][0]["description"],
            "time": Gettime(weather["timezone"])["time"],
            "day": Gettime(weather["timezone"])["day"],
            "wind_speed": convert(weather["wind"]["speed"], "m/s:km/h")
            }
    
    
def convert(value, mode):
    if mode == "k:c":
        return round(value - 273.15)
    elif mode == "c:k":
        return round(value + 273.15)
    elif mode == "m/s:km/h":
        return round((value *18)/5)


def Gettime(timezone):

    ''' takes the timezone which it is the shift in seconds from UTC and returns the current day and time '''

    offset = timedelta(seconds=timezone)
    utc = datetime.utcnow()
    localtime = utc + offset

    # return a dictionary in specific format
    return {"time": datetime.strftime(localtime, "%H:%M"),"day": "{}, {} {}".format(datetime.strftime(localtime, "%A"), datetime.strftime(localtime, "%B"), datetime.strftime(localtime, "%d"))}


def zipcodeformat(arg, mode):

    ''' takes a parameter should be in this format "US,10001"
        and returns the country code "US" or the zip code "10001" '''

    if mode == "1":
        zipcode = ""
        iszip = False
        for i in arg:
            if i == ",":
                iszip = True
                continue

            if iszip:
                zipcode += i
        return zipcode

    if mode == "2":
        countrycode = ""
        for i in arg:
            if i == ",":
                return countrycode
            countrycode += i