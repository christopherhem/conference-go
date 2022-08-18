import requests
from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY


def get_photo(city, state):
    url = "https://api.pexels.com/v1/search"
    headers = {
        "Authorization": PEXELS_API_KEY,
    }
    params = {"query": f"{city} {state}", "per_page": 1}
    res = requests.get(url, params=params, headers=headers)
    pexel_dict = res.json()

    picture_url = pexel_dict["photos"][0]["src"]["original"]
    return {"picture_url": picture_url}


def get_lat_lon(city, state):
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {"q": f"{city}, {state}, USA", "appid": OPEN_WEATHER_API_KEY}
    res = requests.get(url, params=params)
    the_json = res.json()
    lat = the_json[0]["lat"]
    lon = the_json[0]["lat"]
    return lat, lon


def get_weather(city, state):
    lat, lon = get_lat_lon(city, state)
    url = "http://api.openweathermap.org/data/2.5/weather/"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPEN_WEATHER_API_KEY,
        "units": "imperial",
    }
    res = requests.get(url, params=params)
    the_json = res.json()
    return {
        "description": the_json["weather"][0]["description"],
        "temp": the_json["main"]["temp"],
    }
