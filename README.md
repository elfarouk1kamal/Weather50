# Weather 50
#### Video Demo:  https://youtu.be/v2GoSL8HrbU
### Description:
##### Weather 50 is a web application created in python.
##### it allows you to access the basic information about the weather in  most cities of the world using the city name or the zip code and country code that is: 
- The current day and time
- The Temperature degree (Celsius)
- A description of the current weather
- The Wind speed (kilometer per hour)
- The Humidity
- The Pressure (Millibar)
##### and handle all the possible user errors
####
##### Data provided by [openweathermap](https://openweathermap.org/)
####
##### You can search for the weather using the city name or the country code and zip code.
####
##### The home page is very straightforward.
##### it contains a nav bar with the name and the logo of the site on the left side of the nav bar and a contact button (mailto link) on the right.
##### and the home page also contains two forms one with one field for the city name and the other with two fields for the country code and zip code.
#### The web application can handle all possible user errors as:
- Submitting an empty field
- Submitting a city name with numbers or special characters
- Submitting an incorrect city name
- Submitting a country code with numbers or special characters
- Submitting a zip code with letters or special characters
- Submitting an incorrect zip code

### Files:
#### app.py
##### The flask application that contains all the routes and the functions
#### getweather.py
##### Python module that includes the two functions that can get the weather information (byname, byzip).
##### there are more functions but they get called in the module, not in the application
#### config.ini
##### The Web application is using the config.ini file to store the API key
```
[openweathermap]
api_key= "your API key"
```

#### The site works with most cities of the world, the API supports over 200,000 cities around the world.

### How it works
##### There are two routes for getting the weather information (weatherbyname, weatherbyzip)
####
##### their mission is to take the user input and check if there are no user errors.
####
##### redirect the user to **/weather/<arg>** (arg is the city name or the country code and zip code in this format US,10001) 
####
##### **/weather/<arg>** checks if arg is a city name it will call the function getweather.byname() if not it will call the function getweather.byzip()
####
##### In both cases the function will call the API URL which will return the weather data in JSON format and return the weather information in this format using this function (weatherformat())
```
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
```
##### if something goes wrong in this function that means the error will be not found city name or not found country code or zip code 
####
##### Gettime function that return a dictionary in this specific format
```
{"time": datetime.strftime(localtime, "%H:%M"),
"day": "{}, {} {}".format(datetime.strftime(localtime, "%A"), datetime.strftime(localtime, "%B"), datetime.strftime(localtime, "%d"))}
```
##### which look like this:
```
{"time": "08:25", "day": "Monday, July 11"}
```

#### For more information about the API: [openweathermap/api](https://openweathermap.org/api)

#### Languages:
- Python
- HTML
- CSS

#### Requirements:
- flask
- requests
- datetime
- configparser


