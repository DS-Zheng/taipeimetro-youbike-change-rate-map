import pandas as pd
import datetime
import geopandas as gpd
from get_youbike_data import get_all_mrt_station
import plot_map

y, m, d, h = 2018, 12, 1, 0  # year, month, day, hour
time = str(datetime.datetime(y, m, d, h, 0, 0))

''' choose mrt {type mrt = in <-> ubike = return} {mrt = out <-> ubike = rent}'''

ty = 'in'
# ty = 'out'

''' choose plot type'''
# plot_type = 'circle'
plot_type = 'square'

data, station_dict, type_ubike = get_all_mrt_station(ty, time)

if plot_type == 'circle':
    geo_data, state_geo = plot_map.get_circle_json(station_dict)
else:
    geo_data, state_geo = plot_map.get_square_json(station_dict)

geo_data = pd.DataFrame.from_dict(geo_data, orient='index',
                                  columns=['geometry']).reset_index().rename(columns={'index': 'station'})
gdf = gpd.GeoDataFrame(data, geometry=geo_data['geometry'])

gdf.set_crs(epsg=4326, inplace=True)
time = time.replace(' ', "_")[:13]
gdf.to_file(f'./geojson/{type_ubike}_{time}.geojson', driver='GeoJSON')
plot_map.plot_choropleth(gdf, state_geo, time, type_ubike, plot_type)
