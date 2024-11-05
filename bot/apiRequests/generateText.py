import requests

def generateText(promt):
    prompt_data = {
        "text": f"{promt}"
    }
    error = 'Что-то пошло не так'
    response = requests.post('http://127.0.0.1:8000/api/v1/get_music_text', json=prompt_data)

    if response.status_code == 200:
        music_text = response.json().get("music_text")
        return music_text
    else:
        return error