from flask import Flask, render_template
import geopandas as gpd
import folium
import pandas as pd

app = Flask(__name__)

@app.route('/')
def map_view():
    gdf = gpd.read_file('data/zinke_soil.shp')

    def convert_coordinate(coordinate):
        if 'N' in coordinate:
            return float(coordinate.replace('N', ''))
        elif 'S' in coordinate:
            return -float(coordinate.replace('S', ''))
        elif 'E' in coordinate:
            return float(coordinate.replace('E', ''))
        elif 'W' in coordinate:
            return -float(coordinate.replace('W', ''))
        else:
            return float(coordinate)

    gdf['LAT'] = gdf['LAT'].apply(convert_coordinate)
    gdf['LON'] = gdf['LON'].apply(convert_coordinate)

    gdf_clean = gdf.dropna(subset=['CARBON', 'NITROGEN', 'LAT', 'LON'])

    m = folium.Map(location=[0, 0], zoom_start=2)

    for _, row in gdf_clean.iterrows():
        folium.CircleMarker(
            location=(row['LAT'], row['LON']),
            radius=5,
            color='blue' if row['NITROGEN'] < 0.5 else 'red',
            fill=True,
            fill_color='blue' if row['NITROGEN'] < 0.5 else 'red',
            fill_opacity=0.6,
            popup=f'Carbon: {row["CARBON"]}, Nitrogen: {row["NITROGEN"]}'
        ).add_to(m)

    map_path = 'templates/zinke_soil_map.html'
    m.save(map_path)
    return render_template('zinke_soil_map.html')

server = app.server

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
