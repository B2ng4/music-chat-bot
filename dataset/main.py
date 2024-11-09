from yandex_music import Client
import os
import json

client = Client().init()
folder_path = 'parser/music'
arr_data = []


def get_album_genre_by_track_name(track_name):
    search_result = client.search(track_name)

    if search_result.best and search_result.best.type == 'track':
        best_track = search_result.best.result
        if best_track.albums:
            album_id = best_track.albums[0].id
            album = client.albums_with_tracks(album_id)
            return album.genre
    return None

for filename in os.listdir(folder_path):
    track_name = os.path.splitext(filename)[0]
    genre = get_album_genre_by_track_name(track_name)
    data = {}
    data['name'] = track_name
    data['genre'] = genre
    arr_data.append(data)


with open('dataset.json', 'w', encoding='utf-8') as file:
    print(arr_data)
    json.dump(arr_data, file, ensure_ascii=False)