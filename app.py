import getweather
from requests import get
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

@app.route("/")
def index():

    ip = request.remote_addr
    city = Getcity(ip) # City could be None
    return render_template("index.html", city=city) 


@app.route("/weatherbyname", methods=["GET", "POST"])
def weatherbyname():

    city = request.form.get("city")

    # check if the user submited a empty field
    if not city:
        return render_template('apology.html', apology="You have to submit a city name")

    # Chech if the user does not submit any numbers or special characters in the city name field
    if not iscityname(city):
        return render_template('apology.html', apology="City name can't contain any numbers or special characters")

    
    return redirect(url_for("weather", arg = city, mode = "1"))


@app.route("/weatherbyzip", methods=["GET", "POST"])
def weatherbyzip():
    
    # Check if the user submited one of the fields empty
    if not request.form.get("country_code") or not request.form.get("zip_code"):
        return render_template('apology.html', apology="You have to submit the country code and the zip code")

    # Check if the user does not submit any letters or special characters in the zip code field
    if not request.form.get("zip_code").isdigit():
        return render_template('apology.html', apology="Zip code can't contain any letters or special characters")

    # Chech if the user does not submit any numbers or special characters in the country code field
    if not request.form.get("country_code").isalpha():
        return render_template('apology.html', apology="Invalid country code")

    # Send the country code and the zip code to "/weather" in this format: "US,10001"
    return redirect(url_for("weather", arg = "{},{}".format(request.form.get("country_code").upper(), request.form.get("zip_code"))))


@app.route("/weather/<arg>", methods=["GET", "POST"])
def weather(arg):

    # If the argument is alphabatic deal with it as city name
    if iscityname(arg):
        city = arg
        try:
            weatherdetails = getweather.byname(city)
        except:
            return render_template('apology.html', apology="city not found!")
        return render_template("weather.html", weather=weatherdetails)

    # If not deal with it as country code and city name
    else:
        try:
            weatherdetails = getweather.byzip(arg)
        except:
            return render_template('apology.html', apology="Zip code not found!")
        return render_template("weather.html", weather=weatherdetails)


# If there is no argument redirect to home page
@app.route("/weather/")
def redirectindex():
    return redirect("/")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('apology.html', apology="page not found, try again"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('apology.html', apology="oops, something went wrong"), 500


def Getcity(ip):

    ''' get the user locatin using the user ip address '''
    try:
        location = get(f"http://ip-api.com/json/{ip}?fields=status,message,city")
    except:
        return None
    if location.json()["status"] == "fail":
        return None

    # return the user city name
    return location.json()["city"]


def iscityname(arg):

    # Check if the arg is city name 
    # city name can only contains letters and white spaces 
    for i in arg:
        if not i.isalpha():
            if not i.isspace():
                return False
    return True
            
