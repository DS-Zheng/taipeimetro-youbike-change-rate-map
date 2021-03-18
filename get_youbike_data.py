import pandas as pd
import find_youbike_station

data = pd.read_csv('./data/201812.csv')
df_rent = pd.DataFrame(data.groupby(['rent_time', 'rent_station']).size(), columns=['rent_size']).reset_index()
df_return = pd.DataFrame(data.groupby(['return_time', 'return_station']).size(), columns=['return_size']).reset_index()


def get_size(temp, station):
    # get each station static data
    if temp == 'rent':
        return df_rent[df_rent['rent_station'] == station].reset_index(drop=True)
    else:
        return df_return[df_return['return_station'] == station].reset_index(drop=True)


def cal_data(temp, station_list):
    # Calculate near station static data
    df = pd.DataFrame()
    for station in station_list:
        df = df.append(get_size(temp, station))
    if temp == 'rent':
        return df.groupby(['rent_time']).sum().reset_index().rename(columns={'rent_time': 'time', 'rent_size': 'size'})
    else:
        return df.groupby(['return_time']).sum().reset_index().rename(columns={'return_time': 'time', 'return_size': 'size'})


def get_all_mrt_station(ty, time):  #get mrt all station near youbike static Data
    # ty -> in or out (mrt) time -> datetime
    # read mrt data
    # if mrt type = in -> youbike = return
    # if mrt type = out -> youbike = rent
    print(time)
    if ty == 'in':
        df = pd.read_csv('./data/in.csv')
        type_ubike = 'return'
    else:
        df = pd.read_csv('./data/out.csv')  # read mrt data
        type_ubike = 'rent'
    station_list = list(df['站點'].unique())  # get all station
    station_dict = {}
    data = pd.DataFrame()
    for index, station in enumerate(station_list):
        print(station)
        radius, center_lat, center_lon, neighbor = find_youbike_station.find(station)  # get station near range info
        select = df[df['站點'] == station].reset_index()  # select mrt data
        t = select[select['time'] == time].index.tolist()[0]  # get time index
        if len(neighbor) > 0:  # if station near have youbike station
            station_dict[station] = [radius, center_lat, center_lon]  # save station range
            df_ubike = cal_data(type_ubike, neighbor)  # get youbike data
            select = select.merge(df_ubike, on=['time'], how='left').fillna(0)  # merge youbike data & mrt data
            data.at[index, 'time'] = time
            data.at[index, 'station'] = station
            data.at[index, 'rate'] = select.at[t, 'size'] / select.at[t, '人次']  # change rate

    return data.reset_index(drop=True), station_dict, type_ubike
