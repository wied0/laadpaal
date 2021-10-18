import pandas as pd
import requests
import os

#! pip install plotly
import plotly.express as px


response = requests.get("https://opendata.rdw.nl/resource/m9d7-ebf2.json?$limit=413000")
voertuigen_data = pd.DataFrame.from_dict(response.json())

response = requests.get("https://opendata.rdw.nl/resource/8ys7-d773.json?$limit=413000")
brandstof_data = pd.DataFrame.from_dict(response.json())

path_raw = '/Users/rubenwiedijk/PycharmProjects/VA_opdracht/dashboard/data_raw'
path_clean = '/Users/rubenwiedijk/PycharmProjects/VA_opdracht/dashboard/data_clean'

os.chdir(path_raw)

key = '91b8563b-459b-4816-9417-2e3860f1f3e4'
url = ' https://api.openchargemap.io/v3/poi/?output=json&countrycode=NL&maxresults=11063&compact=true&verbose=false'

json_data = requests.get(url, params={'key': key}).json()
laadpaallocaties = pd.DataFrame.from_dict(json_data)

laadpaallocaties.to_csv('laadpaallocaties.csv', index=False)
brandstof_data.to_csv('voertuigen_data.csv', index=False)
voertuigen_data.to_csv('brandstof_data.csv', index=False)