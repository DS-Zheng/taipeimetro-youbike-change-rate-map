import pandas as pd

# Read Data
df = pd.read_csv('./data/臺北捷運每日分時各站OD流量統計資料_201812.csv',
                 delim_whitespace=True, error_bad_lines=False).iloc[1:-1]
# Create datetime column
df['time'] = df['日期'] + ' ' + df['時段'].astype('str').str.strip().str.zfill(2)
df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H')

# Calculate in & out static data and export
df['人次'] = df['人次'].astype('int')
df_in = df.groupby(['time', '進站']).sum().reset_index()
df_in.rename(columns={'進站': '站點'}).to_csv('./data/in.csv', index=False, encoding='utf-8-sig')

df_out = df.groupby(['time', '出站']).sum().reset_index()
df_out.rename(columns={'出站': '站點'}).to_csv('./data/out.csv', index=False, encoding='utf-8-sig')
