import os
import requests
import json
from yandex_music import Client


client = Client('y0_AgAAAABizlx0AAG8XgAAAAEXuFpeAABxnbJiPFlMVKzbUrxRoHAfRe8baw').init()
folder_path = 'C:/Users/makst/Documents/GitHub/music-chat-bot/parser/music'
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

def get_track_id_by_name(track_name):
    search_result = client.search(track_name)
    if search_result.best and search_result.best.type == 'track':
        return search_result.best.result.id
    return None

def download_file(url, destination):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(destination, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded lyrics to {destination}")
    except Exception as e:
        print(f"Error downloading file: {e}")


for filename in os.listdir(folder_path):
    track_name = os.path.splitext(filename)[0]


    genre = get_album_genre_by_track_name(track_name)
    track_id = get_track_id_by_name(track_name)


    if track_id is None:
        print(f"Track ID not found for '{track_name}'. Skipping...")
        continue


    text = client.tracks_lyrics(track_id)


    download_file(text.download_url, "textfile.txt")


    with open("textfile.txt", "r", encoding="utf-8") as book:
        content = book.read()


    data = {
        'name': track_name,
        'genre': genre,
        'text': content.strip()
    }


    arr_data.append(data)


if os.path.exists("textfile.txt"):
    os.remove("textfile.txt")


with open('dataset.json', 'w', encoding='utf-8') as file:
    print(arr_data)
    json.dump(arr_data, file, ensure_ascii=False, indent=4)

print("Data collection complete. Check 'dataset.json' for results.")