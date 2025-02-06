
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
    include_sentence_length = True
    to_language = ["it"]
    input_text_elements = [InputTextItem(text="The answer lies in machine translation. This is a test.")]

    response = trc.translate(
        content=input_text_elements, to=to_language, include_sentence_length=include_sentence_length
    )
    translation = response[0] if response else None

    if translation:
        detected_language = translation.detected_language
        if detected_language:
            print(
                f"Detected languages of the input text: {detected_language.language} with score: {detected_language.score}."
            )
        for translated_text in translation.translations:
            print(f"Text was translated to: '{translated_text.to}' and the result is: '{translated_text.text}'.")
            if translated_text.sent_len:
                print(f"Source Sentence length: {translated_text.sent_len.src_sent_len}")
                print(f"Translated Sentence length: {translated_text.sent_len.trans_sent_len}")

except HttpResponseError as exception:
    if exception.error is not None:
        print(f"Error Code: {exception.error.code}")
        print(f"Message: {exception.error.message}")