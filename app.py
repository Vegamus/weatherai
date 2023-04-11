from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta
import openai

openai.api_key = ("OPENAI_API_KEY")



app = Flask(__name__)

 
def generate_city_description(city):
    prompt = f"Please provide a brief description of the city of {city}."
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

def get_local_time(offset_seconds):
    utc_time = datetime.utcnow()
    local_time = utc_time + timedelta(seconds=offset_seconds)
    return local_time

def get_weather_data(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json(), response.status_code

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form.get('city')
        weather_data, status_code = get_weather_data(city, api_key)
        if status_code == 200:
            local_time = get_local_time(weather_data['timezone'])
            city_description = get_city_description(city)
            return render_template('index.html', weather_data=weather_data, city=city, local_time=local_time, city_description=city_description)
        else:
            return render_template('index.html', error=True)
    else:
        return render_template('index.html')



def display_weather_data(weather_data):
    city = weather_data['name']
    temperature = weather_data['main']['temp']
    description = weather_data['weather'][0]['description']
    timestamp = weather_data['dt']
    timezone_offset = weather_data['timezone']
    local_time = datetime.fromtimestamp(timestamp + timezone_offset)

    print(f"City: {city}")
    print(f"Temperature: {temperature}°C")
    print(f"Weather: {description}")
    print(f"Local Date and Time: {local_time}")

def get_city_description(city):
    prompt = f"Please provide a brief description of the city along with history and popular local foods {city}."
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5,
    )

    description = response.choices[0].text.strip()
    return description


if __name__ == "__main__":
    api_key = "your_openweathermap_api_key" # Replace with your OpenWeatherMap API key
    app.run(debug=True)
