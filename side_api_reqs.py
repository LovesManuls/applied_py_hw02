# FROM HW01 STREAMLIT

from config import OPEN_WEATHER_API
import httpx

## Weathers
async def get_lat_long_async(city_name, api_key, client):
    base_url = f"http://api.openweathermap.org/geo/1.0/direct"
    params = {
        'q': city_name,
        'appid': api_key,
    }
    response = await client.get(base_url, params=params)
    if response.status_code == 200:
        response = response.json()[0]
        return response['lat'], response['lon']
    else:
        return {"error": response.status_code}


async def get_weather_data_async(lat, lon, api_key, client):
    base_url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': lat,  # широта
        'lon': lon,  # долгота
        'appid': api_key,
        'units': 'metric',
    }
    response = await client.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()['main']['temp']  # just temperature in float
    else:
        return -1


async def access_one_city_temperature(city_name, api_key=OPEN_WEATHER_API):
    async with httpx.AsyncClient() as client:
        lat, lon = await get_lat_long_async(city_name, api_key, client)
        temp = await get_weather_data_async(lat, lon, api_key, client)
        if temp == -1:
            return None
        else:
            return temp

## Foods

