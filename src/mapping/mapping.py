import googlemaps
import folium
import pandas as pd

gmaps = googlemaps.Client(key='AIzaSyCzQIxBQDxD-9apyT4gdRzcKVCgsGi1cBM')

def get_coordinates(addres):
    geocode_result = gmaps.geocode(addres)
    # if geocode_result:
    lat = geocode_result[0]['geometry']['location']['lat']
    lon = geocode_result[0]['geometry']['location']['lng']
    print(lat, lon)
    # else:
    #     print('No results found for the given address:', addres)
    return lat, lon
    

def plot_map(dataframe, nome):
    lat, lon = get_coordinates(dataframe['Localização'][0])
    map = folium.Map(location=[lat, lon], zoom_start=12)

    for i in range(dataframe.shape[0]):
        lat, lon = get_coordinates(dataframe['Localização'][i])
        print(i, dataframe['Localização'][i])
        folium.CircleMarker(location=[lat, lon], fill=True, radius=8, tooltip=(f'Valor do leilão: R$ {dataframe.iloc[i, 0]}')).add_to(map)
        if i == 80:
            break
    map.save(f'output//map_{nome}.html')

dataframe = pd.read_excel('output\leilaoimoveis.xlsx')
plot_map(dataframe, 'fortaleza-ce')