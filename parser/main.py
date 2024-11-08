from LxmlSoup import LxmlSoup
import requests
import os


html = requests.get('https://rus.hitmotop.com/').text #Тут ставим какой сайт парсим
soup = LxmlSoup(html)
save_directory = "./music"


links = soup.find_all('a', class_='track__download-btn')#Тут нужно выбрать селектор
for i, link in enumerate(links):

    url = link.get("href")
    print(f"Ссылка на скачивание: {url}")


    if url:
        response = requests.get(url, stream=True)
        filename = f"downloaded_music_{i + 1}.mp3"
        file_path = os.path.join(save_directory, filename)

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Файл {filename} успешно скачан.")