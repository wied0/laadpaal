import pandas as pd
import os
import plotly.express as px

path_raw = '/Users/rubenwiedijk/PycharmProjects/VA_opdracht/dashboard/data_raw'
path_clean = '/Users/rubenwiedijk/PycharmProjects/VA_opdracht/dashboard/data_clean'

os.chdir(path_raw)

brandstof_data = pd.read_csv('brandstof_data.csv')
voertuigen_data = pd.read_csv('voertuigen_data.csv')

brandstof_voertuig = voertuigen_data.merge(brandstof_data, how='inner', on='kenteken')

dict_df = {'column': [],
           'nans': []}

column_list = brandstof_voertuig.columns
for column_name in column_list:
    dict_df['column'].append(column_name)
    percentage_nan = brandstof_voertuig.loc[:, column_name].isnull().sum() / len(brandstof_voertuig.loc[:, column_name])
    dict_df['nans'].append(percentage_nan)
    if percentage_nan > 0.2:
        brandstof_voertuig = brandstof_voertuig.drop(column_name, axis=1)

df_nans = pd.DataFrame(dict_df)
fig = px.bar(df_nans, y='column', x='nans')
fig.add_vline(x=0.2)    # Cutoff
fig.show()

brandstof_voertuig_relevant = brandstof_voertuig[['merk', 'datum_tenaamstelling','brandstofverbruik_gecombineerd', 'brandstofverbruik_stad',
                                                           'brandstofverbruik_buiten', 'brandstof_omschrijving',
                                                          'co2_uitstoot_gecombineerd', 'emissie_co2_gecombineerd_wltp',
                                                          'brandstof_verbruik_gecombineerd_wltp']].copy()

brandstof_voertuig_relevant[['brandstofverbruik_gecombineerd', 'brandstofverbruik_stad',
                             'brandstofverbruik_buiten', 'co2_uitstoot_gecombineerd',
                            'emissie_co2_gecombineerd_wltp', 'brandstof_verbruik_gecombineerd_wltp']] = brandstof_voertuig_relevant[['brandstofverbruik_gecombineerd', 'brandstofverbruik_stad',
                             'brandstofverbruik_buiten', 'co2_uitstoot_gecombineerd',
                            'emissie_co2_gecombineerd_wltp', 'brandstof_verbruik_gecombineerd_wltp']].apply(pd.to_numeric, axis = 1)


os.chdir(path_clean)
brandstof_voertuig_relevant.to_csv('brandstof_voertuig_relevant.csv', index=False)

brandstof_voertuig_relevant = pd.read_csv('brandstof_voertuig_relevant.csv')
brandstof_voertuig_relevant['datum_tenaamstelling'] = brandstof_voertuig_relevant['datum_tenaamstelling'].astype(str)


def split(string_):
    indices = [0, 4, 6]
    parts = [string_[i:j] for i, j in zip(indices, indices[1:] + [None])]
    parts = '-'.join(parts)
    return parts


brandstof_voertuig_relevant['datum_tenaamstelling'] = brandstof_voertuig_relevant['datum_tenaamstelling'].apply(split)

brandstof_voertuig_relevant['datum_tenaamstelling'] = pd.to_datetime(
    brandstof_voertuig_relevant['datum_tenaamstelling'])

brandstof_voertuig_relevant = brandstof_voertuig_relevant.sort_values('datum_tenaamstelling')

print(brandstof_voertuig_relevant)

brandstof_voertuig_Benzine = brandstof_voertuig_relevant[
    brandstof_voertuig_relevant['brandstof_omschrijving'] == 'Benzine'].drop(
    'merk', axis=1
)
brandstof_voertuig_Diesel = brandstof_voertuig_relevant[
    brandstof_voertuig_relevant['brandstof_omschrijving'] == 'Diesel'].drop(
    'merk', axis=1
)
voertuig_elektrisch = brandstof_voertuig_relevant[
    brandstof_voertuig_relevant['brandstof_omschrijving'] == 'Elektrisch'].drop(
    'merk', axis=1
)

benzine_per_month = brandstof_voertuig_Benzine.groupby(
    pd.Grouper(key='datum_tenaamstelling',
               freq='1M')).mean()
diesel_per_month = brandstof_voertuig_Diesel.groupby(
    pd.Grouper(key='datum_tenaamstelling',
               freq='1M')).mean()

diesel_per_month.dropna().to_csv('diesel_per_month.csv')
benzine_per_month.dropna().to_csv('bezine_per_month.csv')

for merk in brandstof_voertuig_relevant['merk'].unique():
    brandstof_voertuig_relevant[merk] = brandstof_voertuig_relevant['merk'] == merk

brandstof_voertuig_relevant[brandstof_voertuig_relevant.columns[9:]].astype(int)

cumsum_sales = brandstof_voertuig_relevant[brandstof_voertuig_relevant.columns[9:]].cumsum()
cumsum_sales.index = brandstof_voertuig_relevant['datum_tenaamstelling']

cumsum_sales.to_csv('cumsum_sales.csv')