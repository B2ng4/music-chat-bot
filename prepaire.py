from pydub import AudioSegment
import os

def convert_to_wav(input_dir, output_dir):
    # Создаем выходную директорию, если она не существует
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Перебираем все файлы в входной директории
    for filename in os.listdir(input_dir):
        if os.path.isfile(os.path.join(input_dir, filename)) and filename.lower().endswith(('.mp3', '.ogg', '.flac', '.wav', '.aac')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.wav')

            # Загружаем аудиофайл
            audio = AudioSegment.from_file(input_path)

            # Сохраняем файл в формате .wav
            audio.export(output_path, format='wav')
            print(f"Преобразован {filename} в {output_path}")

if __name__ == "__main__":
    input_directory = "E:/dataset/traindata"  # Замените на путь к вашей директории с аудиофайлами
    output_directory = "E:/dataset2"  # Замените на путь к директории, куда будут сохранены преобразованные файлы

    convert_to_wav(input_directory, output_directory)