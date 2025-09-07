from flask import Flask, render_template, request
import requests
import os 
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

api_key = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ja"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"cod": "error", "message": str(e)}
    
@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    icon = None
    city = None

    if request.method == "POST":
        city = request.form["city"]
        weather_data = get_weather(city)

        if weather_data.get("cod") == 200:
            weather_main = weather_data["weather"][0]["main"]
            icon_map = {
                "Clear": "images/sun.png",
                "Clouds": "images/cloud.png",
                "Rain": "images/rain.png",
                "Snow": "images/snow.png",
                "Drizzle": "images/drizzle.png",
                "Thunderstorm": "images/thunder.png",
            }
            icon = icon_map.get(weather_main, None)

    return render_template("index.html", city=city, weather_data=weather_data, icon=icon)

if __name__== "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)