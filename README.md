# 利用Geojson與folium製作臺北捷運與youbike分時轉換率熱區圖

##  Abstract
透過公開資料將臺北捷運分時進出站統計數據與youbike公共自行車租用紀錄做轉換率的計算，首先透過捷運站個出口的座標找尋附近的youbike場站，之後透過創建.geojson搭配folium Choropleth產生分時熱區圖，將臺北捷運與youbike的轉換率視覺化

## Data Source
- [臺北捷運各站分時進出量統計](http://163.29.157.32:8080/fi/dataset/98d67c29-464a-4003-9f78-b1cbb89bff59)
- [臺北捷運車站出入口座標](https://data.taipei/#/dataset/detail?id=cfa4778c-62c1-497b-b704-756231de348b)
- [臺北市自行車租借紀錄](https://data.taipei/#/dataset/detail?id=9d9de741-c814-450d-b6bb-af8c438f08e5)

## Data Prepare
```python
df_mrt = pd.read_csv('./data/臺北捷運每日分時各站OD流量統計資料_201812.csv',
                     delim_whitespace=True, error_bad_lines=False, low_memory=False).iloc[1:-1]
df_mrt['人次'] = df_mrt['人次'].astype('int')
df_in = df_mrt.groupby(['日期', '時段', '進站']).sum().reset_index()
for i in range(len(df_in)):
    df_in.at[i, 'time'] = datetime.datetime(
        int(df_in.at[i, '日期'][:4]), int(df_in.at[i, '日期'][5:7]), int(df_in.at[i, '日期'][8:10]), int(df_in.at[i, '時段']), 0, 0)
df_in = df_in.rename(columns={'進站': '站點'})
df_in.to_csv('./data/in.csv', index=False, encoding='utf-8-sig')
df_out = df_mrt.groupby(['日期', '時段', '出站']).sum().reset_index()
for i in range(len(df_out)):
    df_out.at[i, 'time'] = datetime.datetime(
        int(df_out.at[i, '日期'][:4]), int(df_out.at[i, '日期'][5:7]), int(df_out.at[i, '日期'][8:10]), int(df_out.at[i, '時段']), 0, 0)
df_out = df_out.rename(columns={'出站': '站點'})
df_out.to_csv('./data/out.csv', index=False, encoding='utf-8-sig')
```
