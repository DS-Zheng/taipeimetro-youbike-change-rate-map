import pandas as pd
import datetime
import geopandas as gpd

''' 
Prepare Data
can do one time to create data 
and then can comment it (line 10 ~ 21)
'''
# df_mrt = pd.read_csv('./data/臺北捷運每日分時各站OD流量統計資料_201812.csv', delim_whitespace=True, error_bad_lines=False, low_memory=False).iloc[1:-1]
# df_mrt['人次'] = df_mrt['人次'].astype('int')
# df_in = df_mrt.groupby(['日期', '時段', '進站']).sum().reset_index()
# for i in range(len(df_in)):
#     df_in.at[i, 'time'] = datetime.datetime(int(df_in.at[i, '日期'][:4]), int(df_in.at[i, '日期'][5:7]), int(df_in.at[i, '日期'][8:10]), int(df_in.at[i, '時段']), 0, 0)
# df_in = df_in.rename(columns={'進站': '站點'})
# df_in.to_csv('./data/in.csv', index=False, encoding='utf-8-sig')
# df_out = df_mrt.groupby(['日期', '時段', '出站']).sum().reset_index()
# for i in range(len(df_out)):
#     df_out.at[i, 'time'] = datetime.datetime(int(df_out.at[i, '日期'][:4]), int(df_out.at[i, '日期'][5:7]), int(df_out.at[i, '日期'][8:10]), int(df_out.at[i, '時段']), 0, 0)
# df_out = df_out.rename(columns={'出站': '站點'})
# df_out.to_csv('./data/out.csv', index=False, encoding='utf-8-sig')


import find_ubike_station
from create_ubike_dataset import cal_data
import plot_map

y, m, d, h = 2018, 12, 1, 0  # year, month, day, hour

''' choose mrt {type mrt = in <-> ubike = return} {mrt = out <-> ubike = rent}'''
ty = 'in'
# ty = 'out'

''' choose plot type'''
plot_type = 'circle'
# plot_type = 'square'

if ty == 'in':
    df = pd.read_csv('./data/in.csv')
    type_ubike = 'return'
else:
    df = pd.read_csv('./data/out.csv')
    type_ubike = 'rent'

station_list = list(df['站點'].unique())

time = str(datetime.datetime(y, m, d, h, 0, 0))
print(time)
station_dict = {}
data = pd.DataFrame()
for index, station in enumerate(station_list):
    print(station)
    radius, center_lat, center_lon, neighbor = find_ubike_station.find(station)
    select = df[df['站點'] == station].reset_index()
    t = select[select['time'] == time].index.tolist()[0]
    if len(neighbor) > 0:
        station_dict[station] = [radius, center_lat, center_lon]
        df_ubike = cal_data(type_ubike, neighbor)
        select = select.merge(df_ubike, on=['time'], how='left').fillna(0)
        data.at[index, 'station'] = station
        data.at[index, 'rate'] = select.at[t, 'size'] / select.at[t, '人次']
data = data.reset_index(drop=True)

if plot_type == 'circle':
    geo_data, state_geo = plot_map.get_circle_json(station_dict)
else:
    geo_data, state_geo = plot_map.get_square_json(station_dict)
geo_data = pd.DataFrame.from_dict(geo_data, orient='index',
                                  columns=['geometry']).reset_index().rename(columns={'index': 'station'})
gdf = gpd.GeoDataFrame(data, geometry=geo_data['geometry'])
gdf.set_crs(epsg=4326, inplace=True)
print(gdf)
time = time.replace(' ', "_")[:13]
gdf.to_file(f'./geojson/{type_ubike}_{time}.geojson', driver='GeoJSON')
plot_map.plot_choropleth(gdf, state_geo, time, type_ubike, plot_type)
