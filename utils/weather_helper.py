import os
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd
import requests


def get_longitudeandlatitude(city: str) -> float:
    """
    Fetch longitude and latitude of a city using CityAPI.

    Parms
        city : string
            city in string.
    Return
        lon : float
            Longitude in decimal degrees.
        lat : float
            Latitude in decimal degrees.
    """
    url = f"https://api.cityapi.org/v1/cities?search={city}"
    response = requests.get(url)
    data = response.json()  # data is a list of dicts

    if len(data) > 0:
        records = []
        for item in data["data"]:  # har element ek dictionary hai
            if item["name"].lower() == city.lower():
                records.append(item)

        if records:
            result = records[0]
            latitude = result["latitude"]
            longitude = result["longitude"]
            return latitude, longitude
        else:
            print("City not found in results:", city)
            return None
    else:
        print("No data found for:", city)
        return None


def get_currentweather(lat: float, lon: float) -> float:
    """
    Fetch longitude and latitude of a city using CityAPI.

    Parms
        lon : float
            Longitude in decimal degrees.
        lat : float
            Latitude in decimal degrees.
    Return
        Temperature
    """

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m,relative_humidity_2m"
    response = requests.get(url)
    data = response.json()
    return data["current"]["temperature_2m"]


def get_forecastedweather(lat: float, lon: float) -> str:
    """
    Fetch 7-day forecasted temperature using Open-Meteo API.

    Parms
        lon : float
            Longitude in decimal degrees.
        lat : float
            Latitude in decimal degrees.
    Return
        7 days data in JSON string
    """
    # Calculate dates
    today = datetime.now()
    week_ago = today - timedelta(days=7)

    # Format dates for API (YYYY-MM-DD)
    start_date = week_ago.strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min"
    )
    response = requests.get(url)
    data = response.json()
    return data


def load_pasttempintopandas(data: str) -> pd.DataFrame:
    """
    Convert forecasted daily temperature data into a pandas DataFrame.

    Parameters
    ----------
    data : dict
        A dictionary containing weather forecast data with a 'daily' key.
        The 'daily' key should include:
        - 'time': list of date strings
        - 'temperature_2m_max': list of maximum temperature values
        - 'temperature_2m_min': list of minimum temperature values

    Returns
    -------
    pandas.DataFrame
        A DataFrame with columns:
        - 'date' (datetime64): Converted date values
        - 'max_temp' (float): Maximum daily temperature
        - 'min_temp' (float): Minimum daily temperature

    Notes
    -----
    - Date strings are converted to pandas datetime objects.
    - Temperature values are converted to numeric types.
    - Useful for further analysis or visualization of daily temperature forecasts.
    """
    # Extract the daily data
    daily_data = data["daily"]

    # Create a DataFrame
    df = pd.DataFrame(
        {
            "date": daily_data["time"],
            "max_temp": daily_data["temperature_2m_max"],
            "min_temp": daily_data["temperature_2m_min"],
        }
    )

    df["date"] = pd.to_datetime(df["date"])  # Convert date strings to datetime
    df["max_temp"] = pd.to_numeric(df["max_temp"])  # Convert max_temp strings to number
    df["min_temp"] = pd.to_numeric(df["min_temp"])

    # 3. Calculate average
    df["avg_temp"] = (df["max_temp"] + df["min_temp"]) / 2

    return df


def visualize_tempdataingraph(df: pd.DataFrame, city):
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(df["date"], df["max_temp"], marker="o", label="Max Temp")
    plt.plot(df["date"], df["min_temp"], marker="o", label="Min Temp")

    # Add labels and title
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.title(f"{city} Weather - Past 7 Days")
    plt.legend()

    # Rotate x-axis labels for readability
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot to image
    plt.savefig(f"resources/img/{city}_weather_chart.png")

    # Create data folder if it doesn't exist
    if not os.path.exists("resources/files"):
        os.makedirs("resources/files")

    # Save to CSV
    df.to_csv(f"resources/files/{city}_weather.csv", index=False)
    print(f"Data saved to resources/{city}_weather.csv")
