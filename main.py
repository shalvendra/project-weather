import utils.weather_helper as wh

"""
    Retrive latitude, longitude values of city
"""
city = input("please enter city name to get weather information: ")
latitude, longitude = wh.get_longitudeandlatitude(city)

"""
    Retrive current weather from latitude, longitude values
"""
# temp = wh.get_currentweather(latitude, longitude)
# print(f'Current temp. of gwalior is: {temp}°C')

"""
    Retrive forecasted weather from latitude, longitude values
"""
forecastedtemp = wh.get_forecastedweather(latitude, longitude)
# print(forecastedtemp)

"""
    load forecasted data into pandas to configure it.
"""
dataframe = wh.load_pasttempintopandas(forecastedtemp)
# print(dataframe)

"""
    create a simple line chart and save data in csv file.
"""
wh.visualize_tempdataingraph(dataframe, city)
