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
    with open(r'output\outros\endereco_nao_encontrado.txt', 'w') as file:

        colors = ['red', 'blue', 'green', 'orange', 'yellow', 'purple', 'black', 'pink', 'white']
        types = ['Casa', 'Terreno', 'Apartamento', 'Área Rural', 'Outros', 'Comercial', 'Galpão', 'Garagem']
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

            color = colors[types.index(dataframe['Tipo de Imóvel'][i])]

            coordinates = get_coordinates(dataframe['Localização'][i])
            if len(coordinates) == 0:
                print('Endereço não encontrado:', dataframe['Link'][i])
                file.write(dataframe['Link'][i] + "\n")
                continue
            folium.CircleMarker(location=coordinates, color=color, fill=True, radius=8, tooltip=(f'{dataframe.iloc[i, 0]} - R$ {dataframe.iloc[i, 1]:,.2f}'), popup=dataframe['Link'][i]).add_to(map)
        
        file.close()
    save_path = r'output/mapas/map_'
    save_path = save_path + name + '.html'
    map.save(save_path)
