import pandas as pd
from geopy.geocoders import Nominatim

#reading data from csv
data = pd.read_csv('/Users/hemantchaudhary/Downloads/Residex.csv')

#initializing geolocator
geolocator = Nominatim(user_agent = 'xyz')

#function to get coordinates
def get_coordinates(DataFrame):
    DataFrame['shift_city'] = DataFrame['city'].shift(1)

    #creating empty latitude and longitude column
    DataFrame['latitude'] = None
    DataFrame['longitude'] = None

    for index, row in DataFrame.iterrows():
        if pd.isna(row['shift_city']) or row['city'] != row['shift_city']:
            DataFrame.loc[index, 'longitude'] = geolocator.geocode(row['city']).longitude, 
            DataFrame.loc[index, 'latitude'] = geolocator.geocode(row['city']).latitude
        else:
            DataFrame.loc[index, 'longitude'] = DataFrame.loc[index - 1, 'longitude']
            DataFrame.loc[index, 'latitude'] = DataFrame.loc[index - 1, 'latitude']

    DataFrame = DataFrame.drop('shift_city', axis = 1)
    return DataFrame

x = get_coordinates(data)
print(x.head())
    