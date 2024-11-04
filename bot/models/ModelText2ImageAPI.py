import json
import time
import requests


class Text2ImageAPI:

        def __init__(self, url, api_key, secret_key):
            self.URL = url
            self.AUTH_HEADERS = {
                'X-Key': f'Key {api_key}',
                'X-Secret': f'Secret {secret_key}',
            }

        def get_model(self):
            response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
            data = response.json()
            print("Response data:", data)
            return data[0]['id']

        def generate(self, prompt, model, images=1, width=1024, height=1024):
            params = {
                "type": "GENERATE",
                "style": "UHD",
                "numImages": images,
                "width": width,
                "height": height,
                "negativePromptUnclip": "Размытость"
                                        "Грубые пропорции"
                                        "Деформированный,"
                                        "Без мягких линий и размытости"
                                        "Избегай мягких текстур и кругов",
                "generateParams": {
                    "query": f"{prompt}"
                }
            }

            data = {
                'model_id': (None, model),
                'params': (None, json.dumps(params), 'application/json')
            }
            response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
            data = response.json()
            return data['uuid']

        def check_generation(self, request_id, attempts=10, delay=10):
            while attempts > 0:
                response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
                data = response.json()
                if data['status'] == 'DONE':
                    return data['images']

                attempts -= 1
                time.sleep(delay)

        def download_image(self, url, file_path):
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(file_path, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                return file_path
            return None