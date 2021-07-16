import requests
import pandas as pd

# url to use
url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?'

# setting input parameters for earthquake selection
print('Imput required information for your selection: ')

start_time = input('Start time (YYYY-MM-DD): ')
end_time = input('End time (YYYY-MM-DD): ')
lat = input('Latitude: ')
long = input('Longitude: ')
radius_km = input('Radius of selected area in km: ')
number_of_features_to_show = int(input('Number of earthquakes to display sorted by magnitude: '))
print('')

# getting data in json format
data_json = requests.get(url,
                        headers={
                            'Accept': 'application/json'
                        },
                        params={
                            'format': 'geojson',
                            'starttime': start_time,
                            'endtime': end_time,
                            'latitude': lat,
                            'longitude': long,
                            'maxradiuskm': radius_km,
                        }
                        ).json()

# sorting by magnintude and taking desired number of entities
data_json_top_n_by_magnitude = list(
                                    sorted(
                                        data_json['features'],
                                        key=lambda x: x['properties']['mag'],
                                        reverse=True
                                          )
                                    )[:number_of_features_to_show]

# selecting the option how to display the selected data
answer = input(f'Type "all" to print all {number_of_features_to_show} features, type "one" to see certain position: ')
if answer == 'all':
    print('')
    data = []
    column_names = ['Location', 'Magnitude']
    for i in data_json_top_n_by_magnitude:
        data.append([i['properties']['place'].split(' ')[-1], i['properties']['mag']])
    df = pd.DataFrame(data, columns=column_names)
    print(df)
else:
    print('')
    display = True
    while display:
        answer = input('Type "finish" to finish displaying the data, type desired position of selected earthquakes you want to display: ')
        print('')
        if answer == 'finish':
            display = False
        else:
            answer = int(answer)
            print(f'Position {answer} of earthquakes by magnitude: ')
            print(
                'Location: {}'.format(data_json_top_n_by_magnitude[answer]['properties']['place'].split(' ')[-1])
            )
            print(
                'Magnitude: {}'.format(data_json_top_n_by_magnitude[answer]['properties']['mag'])
            )
            print('')