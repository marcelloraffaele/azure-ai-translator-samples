
import os
from dotenv import load_dotenv

from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import  DictionaryExampleTextItem, DictionaryExampleItem
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
    input_text_elements = [DictionaryExampleTextItem(text="fly", translation="volare")]

    response = trc.lookup_dictionary_examples(
        content=input_text_elements, from_parameter=from_language, to=to_language
    )
#DictionaryExampleItem
    print("normalizedSource= ", response[0].normalized_source)
    print("normalizedTarget= ", response[0].normalized_target)

    dictionary_entry = response[0] if response else None

    if dictionary_entry:
        print(f"For the given input {len(dictionary_entry.examples)} entries were found in the dictionary.")
        
        for example in dictionary_entry.examples:
            print(
                f"Example: '{example.target_prefix}{example.target_term}{example.target_suffix}'."
            )

except HttpResponseError as exception:
    if exception.error is not None:
        print(f"Error Code: {exception.error.code}")
        print(f"Message: {exception.error.message}")
raise