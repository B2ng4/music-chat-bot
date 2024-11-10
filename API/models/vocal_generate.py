
from datetime import datetime
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav

preload_models()

async def vocal_get_wav(text:str, text_temp = 0.7, waveform_temp = 0.85) -> str:
    """Функция для преобразования текста в вокал
        Вход: текст,
        Вывод: путь до wav файла
    """
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    text_prompt = "♪"  + text + "♪"
    audio_array = generate_audio(text_prompt,  text_temp = text_temp, waveform_temp  = waveform_temp)
    path_audio = "C:/Users/makst/Documents/GitHub/music-chat-bot/API/" + current_time + ".wav"
    # save audio to disk
    write_wav(path_audio, SAMPLE_RATE, audio_array)
    return path_audio