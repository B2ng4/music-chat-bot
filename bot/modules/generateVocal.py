import os

VOICE_DIRECTORY = 'тут гс'

async def generateVocal(message):
    filename = "тут название гс"
    file_path = os.path.join(VOICE_DIRECTORY, filename)

    if os.path.isfile(file_path):
        return file_path
    else:
        raise FileNotFoundError(f"Voice file '{filename}' not found in directory '{VOICE_DIRECTORY}'")