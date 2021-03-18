# 利用Geojson與folium製作臺北捷運與youbike分時轉換率熱區圖

##  Abstract
透過公開資料將臺北捷運分時進出站統計數據與youbike公共自行車租用紀錄做轉換率的計算，首先透過捷運站個出口的座標找尋附近的youbike場站，之後透過創建.geojson搭配folium Choropleth產生分時熱區圖，將臺北捷運與youbike的轉換率視覺化。


## Data Source
- [臺北捷運各站分時進出量統計](http://163.29.157.32:8080/fi/dataset/98d67c29-464a-4003-9f78-b1cbb89bff59)
- [臺北捷運車站出入口座標](https://data.taipei/#/dataset/detail?id=cfa4778c-62c1-497b-b704-756231de348b)
- [臺北市自行車租借紀錄](https://data.taipei/#/dataset/detail?id=9d9de741-c814-450d-b6bb-af8c438f08e5)


