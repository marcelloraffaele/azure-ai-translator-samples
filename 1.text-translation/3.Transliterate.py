
import os
from dotenv import load_dotenv

from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError
import json

# Load the environment variables from the .env file
load_dotenv()

key = os.getenv("AZURE_AI_TRANSLATOR_KEY")
endpoint = os.getenv("AZURE_AI_TRANSLATOR_ENDPOINT")
region = os.getenv("AZURE_AI_TRANSLATOR_REGION")


credential = TranslatorCredential(key, region)
trc = TextTranslationClient(endpoint=endpoint, credential=credential)

try:
    language = "zh-Hans"
    from_script = "Hans"
    to_script = "Latn"
    input_text_elements = [InputTextItem(text="这是个测试。")]

    response = trc.transliterate(
        content=input_text_elements,
        language=language,
        from_script=from_script,
        to_script=to_script)

    transliteration = response[0] if response else None

    if transliteration:
        print(
            f"Input text was transliterated to '{transliteration.script}' script. Transliterated text: '{transliteration.text}'."
        )

except HttpResponseError as exception:
    if exception.error is not None:
        print(f"Error Code: {exception.error.code}")
        print(f"Message: {exception.error.message}")
    raise