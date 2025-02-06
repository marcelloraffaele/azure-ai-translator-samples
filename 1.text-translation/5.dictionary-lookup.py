
import os
from dotenv import load_dotenv

from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError

# Load the environment variables from the .env file
load_dotenv()

key = os.getenv("AZURE_AI_TRANSLATOR_KEY")
endpoint = os.getenv("AZURE_AI_TRANSLATOR_ENDPOINT")
region = os.getenv("AZURE_AI_TRANSLATOR_REGION")


credential = TranslatorCredential(key, region)
trc = TextTranslationClient(endpoint=endpoint, credential=credential)

try:
    from_language = "en"
    to_language = "it"
    input_text_elements = [InputTextItem(text="fly")]

    response = trc.lookup_dictionary_entries(
        content=input_text_elements, from_parameter=from_language, to=to_language
    )
    dictionary_entry = response[0] if response else None

    if dictionary_entry:
        print(f"For the given input {len(dictionary_entry.translations)} entries were found in the dictionary.")
        for translation in dictionary_entry.translations:
            print(f"Display Target: {translation.display_target}")
            print(f"Back Translations: {[bt.display_text for bt in translation.back_translations]}")

except HttpResponseError as exception:
    if exception.error is not None:
        print(f"Error Code: {exception.error.code}")
        print(f"Message: {exception.error.message}")
    raise