
import os
import asyncio
from gigachat import GigaChat
from dotenv import load_dotenv

load_dotenv()
GIGACHAT_TOKEN = os.getenv("GIGACHAT_TOKEN")


def clean_text(text: str) -> str:
    """
         Функция для очистки текста песни от лишних элементов
        input:  text (str): Исходный текст песни
        output:  str: Очищенный текст песни
        """
    # Список слов для удаления
    words_to_remove = ['Конечно, вот примерный текст для трех куплетов:', 'Надеюсь, этот текст поможет вам завершить вашу песню!', '---']

    # Разбиваем текст на строки
    lines = text.split('\n')

    # Очищаем строки
    cleaned_lines = []
    for line in lines:
        # Убираем начальные и конечные пробелы
        line = line.strip()

        # Пропускаем пустые строки
        if not line:
            continue

        # Пропускаем строки, содержащие слова из списка words_to_remove
        skip_line = False
        for word in words_to_remove:
            if word in line:
                skip_line = True
                break
        if skip_line:
            continue

        # Убираем звездочки
        line = line.replace('*', '')

        # Добавляем очищенную строку
        cleaned_lines.append(line)

    # Соединяем строки обратно с переносом строки
    return '\n'.join(cleaned_lines)


async def music_text_generate(prompt:str)->str:
    """
    Функция для написания текста песни с помощью  нейросети Gigachat
    input: prompt
    output: music_text
    """

    giga = GigaChat(
        credentials=GIGACHAT_TOKEN,
        verify_ssl_certs=False, model="GigaChat")
    response = giga.chat(
        f"{prompt} -> Это наброски для текста песни, дополни, чтобы получились полноценные слова песни. Должно  быть не менее 3х куплетов! Не выводи ничего лишнего, кроме самого текста песни и нумерации куплетов!")
    response = response.choices[0].message.content
    return  clean_text(response) #очищаем вывод



#////////////////////////////// ДЛЯ ТЕСТА ///////////////////////////////////////////////

# async def main():
#     result = await music_text_generate("Дождь, ожидание холод, боль, снова я расколот")
#     print(result)
#
# # Запускаем асинхронную функцию
# if __name__ == "__main__":
#     asyncio.run(main())