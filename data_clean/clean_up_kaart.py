#!/usr/bin/env python
# coding: utf-8

# In[22]:

import pandas as pd
import numpy as np
import os


path_raw = '/Users/rubenwiedijk/PycharmProjects/VA_opdracht/dashboard/data_raw'
path_clean = '/Users/rubenwiedijk/PycharmProjects/VA_opdracht/dashboard/data_clean'

os.chdir(path_raw)


laadpaaldata = pd.read_csv('schone_laadpaaldata.csv')
voertuigen_data = pd.read_csv('voertuigen_data.csv')
laadpaallocaties = pd.read_csv('laadpaallocaties.csv')

laadpaaldata['Started'] = pd.to_datetime(laadpaaldata['Started'], errors='coerce')
laadpaaldata['Ended'] = pd.to_datetime(laadpaaldata['Ended'], errors='coerce')

# missing values droppen

laadpaaldata = laadpaaldata.dropna()

# alles waar het verschil tussen 'Ended' en 'Started' droppen

laadpaaldata = laadpaaldata[laadpaaldata['Ended'] - laadpaaldata['Started'] >= '0 days 00:00:00']

# alles waar 'ConnectedTime' en 'ChargeTime' minder is dan 0 droppen
laadpaaldata_dt = laadpaaldata[laadpaaldata['ConnectedTime'] >= 0]
laadpaaldata_dt = laadpaaldata[laadpaaldata['ChargeTime'] >= 0]

variables_of_intrest = ['AddressLine1', 'Town', 'StateOrProvince', 'Postcode', 'Latitude', 'Longitude']


def get_geo_data(dict_, variables_of_intrest):
    values = []
    for variable in variables_of_intrest:
        if variable in dict_.keys():
            if dict_[variable] == "":
                values.append(np.NaN)
            else:
                values.append(dict_[variable])
        else:
            values.append(np.NaN)
    return values


geo_data = []
for index, row in laadpaallocaties.iterrows():
    values = get_geo_data(eval(row['AddressInfo']), variables_of_intrest=variables_of_intrest)
    geo_data.append(values)

geo_df = pd.DataFrame(geo_data, columns=variables_of_intrest).dropna()
print(geo_df)

"""os.chdir(path_clean)
geo_df.to_csv('geo_df.csv', index=False)
laadpaaldata_dt.to_csv('laadpaaldata_dt.csv', index=False)"""