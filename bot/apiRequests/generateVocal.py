import requests


def generateVocal(prompt):
    prompt_data = {
        "text": prompt
    }
    error_message = 'Что-то пошло не так'

    response = requests.post('http://127.0.0.1:8000/api/v1/get_vocal', json=prompt_data)

    if response.status_code == 200:
        url_music = response.json().get("path_ti_vocal")
        if url_music:
            return url_music
        else:
            return error_message
    else:
        return f"{error_message}: {response.status_code} - {response.text}"