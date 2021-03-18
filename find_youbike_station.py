import pandas as pd
import numpy as np

ubike_wgs = pd.read_csv('./data/ubike_wgs.csv')[['sno', 'sna', 'lat', 'lng']]
ubike_wgs = ubike_wgs.sort_values(by=['lng', 'lat']).reset_index(drop=True)

mrt_out_wgs = pd.read_csv('./data/臺北捷運車站出入口座標.csv', encoding='utf-8')
mrt_out_wgs['站點'] = mrt_out_wgs['出入口名稱'].str.split('站', expand=True)[0]


def find(station):
    temp = mrt_out_wgs[mrt_out_wgs['站點'] == station].reset_index(drop=True)  # select station
    center_lat, center_lon = np.mean(temp['緯度']), np.mean(temp['經度'])  # Calculate exits center point
    radius = 0.002  # 200m
    neighbor = []
    for x in range(len(ubike_wgs)):
        if (ubike_wgs.at[x, 'lat'] - center_lat) ** 2 + (ubike_wgs.at[x, 'lng'] - center_lon) ** 2 < radius ** 2:
            neighbor.append(ubike_wgs.at[x, 'sna'])
        # if (x-center_x)^2 + (y - center_y)^2 < radius^2 -> this ubike station in this mrt_station
    return radius, center_lat, center_lon, list(set(neighbor))

# print(ubike_wgs)
# print(mrt_out_wgs)

# (x-center_x)^2 + (y - center_y)^2 < radius^2

# dx = abs(x-center_x)
# dy = abs(y-center_y)
# R = radius

# if dx>R then
#     return false.
# if dy>R then
#     return false.
