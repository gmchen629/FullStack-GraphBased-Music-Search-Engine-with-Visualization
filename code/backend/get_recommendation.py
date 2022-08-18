import numpy as np
import pandas as pd
from tqdm import tqdm
from audio_feature_extractor import find_song
import csv

def get_recommendations(song_data, song_name, song_year = None, top_k = 5):
    distances = []
    song_name_list = song_data.name.str.lower().tolist()
    song_year_list = song_data.year.tolist()
    if song_year is not None:
        if song_name.lower() in song_name_list and song_year in song_year_list:
            target_song = song_data[(song_data.name.str.lower() == song_name.lower())].iloc[0]
            print(target_song)
            remaining_data = song_data[song_data.name.str.lower() != song_name.lower()]
        else:
            remaining_data = song_data
            target_song = find_song(song_name.lower(), song_year, top_k)
    else:
        if song_name.lower() in song_name_list:
            target_song = song_data[(song_data.name.str.lower() == song_name.lower())].iloc[0]
            print(target_song)
            remaining_data = song_data[song_data.name.str.lower() != song_name.lower()]
        else:
            remaining_data = song_data
            target_song = find_song(song_name.lower(), song_year, top_k)


    #TODO: fix get recommendation from new spotify data
    for remain_song in tqdm(remaining_data.values):
        dist = 0
        for col in np.arange(np.shape(remaining_data)[1]):
            if type(remain_song[col]) != float: #indeces of non-numerical columns
                continue
            dist += np.absolute(float(target_song[col]) - float(remain_song[col])) #calculating the manhettan distances between numerical features

        distances.append(dist)

    remaining_data['distance'] = distances
    remaining_data = remaining_data.sort_values('distance')
    remaining_data['url'] = "https://open.spotify.com/track/" + remaining_data['id']

    columns = ['artists', 'name', 'year', 'release_date', 'id', 'url']

    return remaining_data[columns][:top_k]

def data_export(file_name, name_l, year_l, id_l, data):
    with open(file_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['music_id', 'music_name', 'release_year', 'r_top5'])
        for i in range(150):
            res = get_recommendations(data, name_l[i], year_l[i], top_k=5)
            res_l = res['id'].tolist()
            writer.writerow([id_l[i], name_l[i], year_l[i], str(res_l)])

        r = get_recommendations(data, 'Attention', 2018, top_k=5)
        r_l = r['id'].tolist()
        writer.writerow(['5cF0dROlMOK5uNZtivgu50', 'Attention', 2018, r_l])

        r = get_recommendations(data, 'Rock Of Ages', 1951, top_k=5)
        r_l = r['id'].tolist()
        writer.writerow(['4oE2phffF2dL7OE5Pdqqlf', 'Rock Of Ages', 1951, r_l])

        r = get_recommendations(data, 'Alaniara', 1930, top_k=5)
        r_l = r['id'].tolist()
        writer.writerow(['44i8kWhXwKOcxXWNkW1IIc', 'Alaniara', 1930, r_l])

        r = get_recommendations(data, 'Mi Zitas Polla', 1930, top_k=5)
        r_l = r['id'].tolist()
        writer.writerow(['3YMO5NbZ1EdRPfgOcemwOa', 'Mi Zitas Polla', 1930, r_l])

        r = get_recommendations(data, 'Eternamente', 1958, top_k=5)
        r_l = r['id'].tolist()
        writer.writerow(['2d1UMVCRESE0KgLpmljWmX', 'Eternamente', 1958, r_l])

        r = get_recommendations(data, 'Double Trouble - Take 3', 1956, top_k=5)
        r_l = r['id'].tolist()
        writer.writerow(['4TNlYnjBBKjbx4y6VWYhaP', 'Double Trouble - Take 3', 1956, r_l])

if __name__ == '__main__':
    data = pd.read_csv("data/music_data.csv")
    name_l = data['name'].tolist()
    year_l = data['year'].tolist()
    id_l = data['id'].tolist()
    # r = get_recommendations(data, 'Danny Boy', 1921, top_k=5)
    # print(r['id'])
    # print(r['name'])
    # print(r['year'])

    data_export('data/r_result.csv', name_l, year_l, id_l, data)