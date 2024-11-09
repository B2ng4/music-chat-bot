from lxml import html as lxml_html
import requests
import os

response = requests.get('https://rus.hitmotop.com/')
soup = lxml_html.fromstring(response.content)

save_directory = "./music"
os.makedirs(save_directory, exist_ok=True)  # Create directory if it doesn't exist

links = soup.xpath('//a[@class="track__download-btn"]')
track_names = soup.xpath('//div[@class="track__title"]/text()')
artists = soup.xpath('//div[@class="track__desc"]/text()')

for i, link in enumerate(links):
    url = link.get("href")
    if url:
        track_name = track_names[i].strip() if i < len(track_names) else "Unknown Track"
        artist_name = artists[i].strip() if i < len(artists) else "Unknown Artist"
        filename = f"{artist_name} - {track_name}.mp3"
        file_path = os.path.join(save_directory, filename)

        print(f"Ссылка на скачивание: {url}")

        response = requests.get(url, stream=True)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Файл {filename} успешно скачан.")