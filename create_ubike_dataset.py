import pandas as pd

data = pd.read_csv('./data/201812.csv')


def get_size(temp, station):
    if temp == 'rent':
        df_rent = pd.DataFrame(data.groupby(['rent_time', 'rent_station']).size(), columns=['rent_size']).reset_index()
        return df_rent[df_rent['rent_station'].isin([station])].reset_index(drop=True)
    else:
        df_return = pd.DataFrame(data.groupby(['return_time', 'return_station']).size(), columns=['return_size']).reset_index()
        return df_return[df_return['return_station'].isin([station])].reset_index(drop=True)

def cal_data(temp, station_list):
    df = pd.DataFrame()
    for station in station_list:
        df = df.append(get_size(temp, station))
    if temp == 'rent':
        return df.groupby(['rent_time']).sum().reset_index().rename(columns={'rent_time': 'time', 'rent_size': 'size'})
    else:
        return df.groupby(['return_time']).sum().reset_index().rename(columns={'return_time': 'time', 'return_size': 'size'})

