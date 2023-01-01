import requests
import yaml
import csv
import os.path
import pandas as pd
import time
from collections import defaultdict


def get_weather_data(params):
    response = requests.get(url='https://api.openweathermap.org/data/2.5/weather?', params=params)
    return response.json()


def save_to_csv(json, path, exists):
    data_entry = defaultdict()
    data_entry['latitude'] = json['coord']['lat']
    data_entry['longitude'] = json['coord']['lon']
    data_entry['weather'] = json['weather'][0]['main']
    data_entry['description'] = json['weather'][0]['description']
    data_entry['temperature'] = json['main']['temp']
    data_entry['feels_like'] = json['main']['feels_like']
    data_entry['temp_min'] = json['main']['temp_min']
    data_entry['temp_max'] = json['main']['temp_max']
    data_entry['humidity'] = json['main']['humidity']
    data_entry['wind_speed'] = json['wind']['speed']
    data_entry['wind_deg'] = json['wind']['deg']
    data_entry['wind_gust'] = json['wind']['gust'] if 'gust' in json['wind'] else 0
    data_entry['cloud'] = json['clouds']['all']
    data_entry['timestamp'] = json['dt']
    data_entry['city_name'] = json['name']
    data_entry['rain_1h'] = json['rain']['1h'] if 'rain' in json else 0
    data_entry['rain_3h'] = json['rain']['3h'] if 'rain' in json else 0
    data_entry['snow_1h'] = json['snow']['1h'] if 'snow' in json else 0
    data_entry['snow_3h'] = json['snow']['3h'] if 'snow' in json else 0
    print(data_entry)
    with open(path, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data_entry.keys())
        if not exists:
            writer.writeheader()
    df = pd.DataFrame(data_entry, index=[0])
    df.to_csv(path, mode='a', index=False, header=False)


if __name__ == '__main__':
    while True:
        print('App awaken...')
        request_params = defaultdict()

        with open("settings.yaml") as file:
            yaml_args = yaml.safe_load(file)
            request_params['lat'] = yaml_args['request']['latitude']
            request_params['lon'] = yaml_args['request']['longitude']
            request_params['appid'] = yaml_args['request']['apiKey']
            file_path = yaml_args['data']['path']
        file_exists = os.path.isfile(file_path)
        response_json = get_weather_data(request_params)
        print('Parsed response: ')
        save_to_csv(response_json, file_path, file_exists)
        print('Request processed, going back to sleep...')
        time.sleep(3600)
