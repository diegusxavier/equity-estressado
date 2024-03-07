import googlemaps
import folium

gmaps = googlemaps.Client(key='AIzaSyCzQIxBQDxD-9apyT4gdRzcKVCgsGi1cBM')

def get_coordinates(addres):
    geocode_result = gmaps.geocode(addres)
    if geocode_result:
        lat = geocode_result[0]['geometry']['location']['lat']
        lon = geocode_result[0]['geometry']['location']['lng']
        coordinates = [lat, lon]
        # print(coordinates)
        return lat, lon
    else:
        # print('Não encontrado:', addres)
        return []
    
    

def plot_map(dataframe, name):
    collors = ['red', 'blue', 'green', 'orange', 'yellow', 'purple', 'black', 'pink', 'white']
    types = []
    i = 0
    while True:
        if i == dataframe.shape[0]:
            print('Nenhum endereço encontrado.')
            return '-1'
        coordinates = get_coordinates(dataframe['Localização'][i])
        if len(coordinates) != 0:
            map = folium.Map(location=coordinates, zoom_start=12)
            break
        i += 1

    for i in range(dataframe.shape[0]):
        coordinates = get_coordinates(dataframe['Localização'][i])
        if len(coordinates) == 0:
            print('Endereço não encontrado:', dataframe['Link'][i])
            continue
        folium.CircleMarker(location=coordinates, fill=True, radius=8, tooltip=(f'Valor do leilão: R$ {dataframe.iloc[i, 1]:,.2f}'), popup=dataframe['Link'][i]).add_to(map)
    map.save(f'output//mapas//map_{name}.html')

