import folium
import branca.colormap as cm
import json
from shapely.geometry import Polygon, Point
import shapely


def get_square_json(station_dict):
    features = []
    geo_data = dict()
    for index, station_data in enumerate(list(station_dict.items())):
        station, radius, center_lat, center_lon = station_data[0], station_data[1][0], station_data[1][1], station_data[1][2]
        top = float(center_lon) + radius
        down = float(center_lon) - radius
        right = float(center_lat) + radius
        left = float(center_lat) - radius
        area = [[[top, left], [top, right], [down, right], [down, left], [top, left]]]
        type_dict = {"type": "Feature", "id": station, "properties": {"name": station}, "geometry": {"type": "Polygon", "coordinates": area}}
        features.append(type_dict)
        geo_data[station] = Polygon([(top, left), (top, right), (down, right), (down, left), (top, left)])
    all_dict = {"type": "FeatureCollection", "features": features}
    state_geo = json.dumps(all_dict)
    return geo_data, state_geo


def get_circle_json(station_dict):
    features = []
    geo_data = dict()
    for index, station_data in enumerate(list(station_dict.items())):
        station, radius, center_lat, center_lon = station_data[0], station_data[1][0], station_data[1][1], station_data[1][2]
        center = Point([center_lon, center_lat])
        circle = center.buffer(radius)  # Degrees Radius
        type_dict = {"type": "Feature", "id": station, "properties": {"name": station}, "geometry": shapely.geometry.mapping(circle)}
        features.append(type_dict)
        geo_data[station] = Polygon(shapely.geometry.mapping(circle)['coordinates'][0])

    all_dict = {"type": "FeatureCollection", "features": features}
    state_geo = json.dumps(all_dict)
    return geo_data, state_geo


def plot_choropleth(gdf, state_geo, time, type_ubike, plot_type):
    fmap = folium.Map(location=[25.0516, 121.552], zoom_start=13)  # map center
    folium.TileLayer('CartoDB positron', name="Light Map", control=False).add_to(fmap)  # base map
    folium.Choropleth(
        geo_data=state_geo,  # square or circle geojson
        data=gdf,
        name='choropleth',
        columns=['station', 'rate'],
        key_on='feature.id',
        fill_color='YlGn',
        fill_opacity=0.5,
        line_opacity=0,
        highlight=True,
        legend_name='ubike % MRT 轉換率',
        reset=True
    ).add_to(fmap)
    folium.LayerControl().add_to(fmap)

    colormap = cm.linear.YlGnBu_09
    style_function = lambda x: {"weight": 0.5,
                                'color': 'black',
                                'fillColor': colormap(x['properties']['rate']),
                                'fillOpacity': 0.5}
    highlight_function = lambda x: {'fillColor': '#000000',
                                    'color': '#000000',
                                    'fillOpacity': 0.30,
                                    'weight': 0.1}
    info = folium.features.GeoJson(
        gdf,
        style_function=style_function,
        control=False,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(fields=['station', 'rate'],
                                               aliases=['station :', 'rate (%) :'],
                                               style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"),
                                               sticky=True
                                               )
    )
    fmap.add_child(info)
    fmap.keep_in_front(info)

    # add a div on map
    legend_html = """ 
                 <div style="
                 position: fixed; 
                 bottom: 20px; left: 35px; width: 330px; height: 45px; 
                 z-index:9999; 

                 background-color:white;
                 
                 opacity: .3;

                 font-size:30px;
                 font-weight: bold;

                 ">
                 &nbsp; {title} 
                  </div> """.format(title=f'{type_ubike}_{time}', itm_txt="""<br><i style="color:{col}"></i>""")

    fmap.get_root().html.add_child(folium.Element(legend_html))
    fmap.save(f'./map/{type_ubike}_{time}_{plot_type}.html')  # save map
