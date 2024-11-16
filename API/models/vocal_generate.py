import subprocess

from datetime import datetime


async def vocal_get_wav(text:str) -> str:
    command = [
        "python",
        r"DiffSinger\\synthesize.py",
        "--text",
        f"{text}",
        "--model",
        "shallow",
        "--restore_step",
        "320000",
        "--mode",
        "single",
        "--dataset",
        "Ruspeech"
    ]
    try:
        # Используем subprocess.run для выполнения команды
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # Выводим стандартный вывод команды, если она выполнилась успешно
        print("Стандартный вывод:")
        print(result.stdout)

    except subprocess.CalledProcessError as e:
            # Обрабатываем ошибки, если команда завершилась с ошибкой
            print(f"Ошибка выполнения команды: {e}")
            print("Стандартный вывод ошибки:")
            print(e.stderr)
    except Exception as e:
        # Обрабатываем другие исключения
        print(f"Произошла ошибка: {e}")

    return f'{text}.wav'

























