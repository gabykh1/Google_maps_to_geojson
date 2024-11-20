import pandas as pd
import re
from shapely.geometry import Point
import geopandas as gpd
import os
import folium
import webbrowser


current_dir = os.path.dirname(__file__)
data_file = os.path.join(current_dir, '..', 'data', 'google.csv')

df = pd.read_csv(data_file)
df.rename(columns={df.columns[0]: 'url'}, inplace=True) # change url column name

df_cleaned = df.dropna(subset='url').reset_index(drop=True) # drom nan and reset index

def extract_coordinates(url):
    match = re.search(r"!3d([-0-9.]+)!4d([-0-9.]+)", url)
    if match:
        latitude = float(match.group(1))
        longitude = float(match.group(2))
        return latitude, longitude
    return None, None

df_cleaned[['lat', 'lon']] = df_cleaned['url'].apply(
    lambda url: pd.Series(extract_coordinates(url))
)
# print(df_cleaned.head())

df_cleaned['geom'] = df_cleaned.apply(
    lambda row: Point(row['lon'], row['lat']), axis=1
)

# print(df_cleaned.head())

gdf = gpd.GeoDataFrame(df_cleaned, geometry='geom')

gdf.set_crs(epsg=4326, inplace=True)

gdf.to_file('layer.geojson', driver='GeoJSON')