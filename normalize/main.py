from pydub import AudioSegment

def match_target_dBFS(sound, target_dBFS):
    dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(dBFS)

def apply_compression(sound):
    # Применяем компрессию (примерный метод)
    return sound.compress_dynamic_range()

def apply_equalization(sound):
    # Применяем эквалайзер (примерный метод)
    # Увеличиваем частоты 3-5 кГц для ясности вокала
    return sound.high_pass_filter(300).low_pass_filter(3000)

# Загружаем аудиофайл
sound = AudioSegment.from_file("test.wav", "wav")

print('Текущая dBFS:', round(sound.dBFS, 1))
normalized_dBFS = -10.0
print('Нормализуем к', normalized_dBFS, '\n')

# Нормализуем звук
normalized_sound = match_target_dBFS(sound, normalized_dBFS)

# Применяем эффекты
compressed_sound = apply_compression(normalized_sound)
final_sound = apply_equalization(compressed_sound)

# Экспортируем финальный звук
final_sound.export("Нормализация.wav", format="wav")

print('Всё сделано, капитан!')