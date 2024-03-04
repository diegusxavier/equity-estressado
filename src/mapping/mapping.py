import googlemaps

gmaps = googlemaps.Client(key='AIzaSyCzQIxBQDxD-9apyT4gdRzcKVCgsGi1cBM')

def get_coordinates(addres):
    geocode_result = gmaps.geocodegeocode_result = gmaps.geocode(addres)
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']
    return lat, lng



