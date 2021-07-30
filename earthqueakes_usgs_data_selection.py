import requests
import pandas as pd

# url to use
url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?'

# setting input parameters for earthquake selection
print('Input required information for your selection: ')

empty = True
while empty:
    start_time = input('Start time (YYYY-MM-DD): ')
    end_time = input('End time (YYYY-MM-DD): ')
    lat = input('Latitude using decimals: ')
    long = input('Longitude using decimals: ')
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
        if not df.empty:
            print(df)
            empty = False
        else:
            print('No earthquakes are found. Try another inputs.')
            print('')
    else:
        print('')
        if data_json_top_n_by_magnitude:
            display = True
            while display:
                answer = input('Type "finish" to finish displaying the data, type desired position of selected earthquakes you want to display: ')
                print('')
                if answer == 'finish':
                    display = False
                else:
                    print(f'Number of found earthquakes: {len(data_json_top_n_by_magnitude)}')
                    answer = int(answer)
                    if answer <= (len(data_json_top_n_by_magnitude)):
                        print(f'Position {answer} of earthquakes by magnitude: ')
                        print('')
                        print(
                            'Location: {}'.format(data_json_top_n_by_magnitude[answer-1]['properties']['place'].split(' ')[-1])
                        )
                        print(
                            'Magnitude: {}'.format(data_json_top_n_by_magnitude[answer-1]['properties']['mag'])
                        )
                        print('')
                    else:
                        print('Number of found earthquakes is smaller than input position. Please type smaller position.')
                        print('')
            empty = False
        else:
            print('No earthquakes are found. Try another inputs.')
            print('')
