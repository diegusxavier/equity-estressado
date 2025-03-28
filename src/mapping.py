import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

locator = Nominatim(user_agent="myGeocoder")
geocode = RateLimiter(locator.geocode, min_delay_seconds=1, error_wait_seconds=10)


def get_coordinates(address, city, state):

    complete_address = f"{address}, {city}, {state}"
    location = locator.geocode(complete_address)
    if location:
        lat = location.latitude
        lon = location.longitude
        return lat, lon
    else:
        # print('Não encontrado:', addres)
        return []
    
    
def format_address(address):
    address = address.replace('.', '')
    if ',' in address:
        street = address.split(',')[0].strip()
        not_street = address.split(',')[1].strip()
        not_street = not_street.split()
        for element in not_street:
            if element.isnumeric():
                number = element
                break
    else:
        street = address.strip()
        number = ''
    format_address = street + ' ' + number
    return format_address
    

def plot_map(dataframe, name):

    state = name.split('-')[-1]
    city = name[0:-3].replace('-', ' ')

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
            formated_address = format_address(dataframe['Localização'][i])

            color = colors[types.index(dataframe['Tipo de Imóvel'][i])]

            coordinates = get_coordinates(formated_address, city, state)
            if len(coordinates) == 0:
                print('Endereço não encontrado:', dataframe['Link'][i])
                file.write(dataframe['Link'][i] + "\n")
                continue
            folium.CircleMarker(location=coordinates, color=color, fill=True, radius=8, tooltip=(f'{dataframe.iloc[i, 0]} - R$ {dataframe.iloc[i, 1]:,.2f}'), popup=dataframe['Link'][i]).add_to(map)
        
        file.close()
    save_path = r'output/mapas/map_'
    save_path = save_path + name + '.html'
    map.save(save_path)
