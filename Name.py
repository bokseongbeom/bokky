import pydeck as pdk
MAPBOX_API_KEY = "pk.eyJ1IjoiYm9rc2IxIiwiYSI6ImNrcTVjaWZwNzEyMzYycG12bDlud2N4dzgifQ.x9WaaDhFembOygQa1gJTcg"

geo_data = 'abc.geojson'

import geopandas as gpd
import shapely

# Shapely 형태의 데이터를 받아 내부 좌표들을 List안에 반환합니다.
def line_string_to_coordinates(line_string):
    if isinstance(line_string, shapely.geometry.linestring.LineString):
        lon, lat = line_string.xy
        return [[x, y] for x, y in zip(lon, lat)]
    elif isinstance(line_string, shapely.geometry.multilinestring.MultiLineString):
        ret = []
        for i in range(len(line_string)):
            lon, lat = line_string[i].xy
            for x, y in zip(lon, lat):
                ret.append([x, y])
        return ret

df = gpd.read_file(geo_data)
df['geometry'] = df['geometry'].apply(line_string_to_coordinates)
df = pd.DataFrame(df) # geopanadas 가 아닌 pandas 의 데이터프레임으로 꼭 바꿔줘야 합니다.
df.head()

df['정규화도로폭'] = df['도로폭'] / df['도로폭'].max()

layer = pdk.Layer(
    'PathLayer',
    df,
    get_path='geometry',
    get_width='도로폭',
    get_color='[255, 255 * 정규화도로폭, 120]',
    pickable=True,
    auto_highlight=True
)

center = [126.950, 37.495]
view_state = pdk.ViewState(
    longitude=center[0],
    latitude=center[1],
    zoom=12)

r = pdk.Deck(layers=[layer], initial_view_state=view_state)
r.show()