from googletrans import Translator
import asyncio


async def translation(text, language):
    translator = Translator(service_urls=[
        'translate.google.com',
        'translate.google.co.kr',
    ])

    translated = await asyncio.get_event_loop().run_in_executor(None, lambda: translator.translate(text, dest=language))

    return translated.text