#https://learn.microsoft.com/en-us/python/api/azure-ai-translation-document/azure.ai.translation.document.singledocumenttranslationclient?view=azure-python
import os
from dotenv import load_dotenv

from azure.ai.translation.document import DocumentTranslationClient, SingleDocumentTranslationClient
from azure.ai.translation.document.models import DocumentTranslateContent
from azure.core.credentials import AzureKeyCredential

# Load the environment variables from the .env file
load_dotenv()

key = os.getenv("AZURE_AI_TRANSLATOR_KEY")
endpoint = os.getenv("AZURE_AI_DOCUMENT_TRANSLATOR_ENDPOINT")

client = SingleDocumentTranslationClient(endpoint, AzureKeyCredential(key))

TEST_INPUT_FILE_NAME = os.path.abspath(
    os.path.join(os.path.abspath(__file__), "..", "../data/example-en.docx")
)

target_language = "it"
file_name = os.path.basename(TEST_INPUT_FILE_NAME)
print(f"File for translation: {file_name}")

with open(TEST_INPUT_FILE_NAME, "rb") as file:
    file_contents = file.read()

# https://learn.microsoft.com/en-us/azure/ai-services/translator/document-translation/overview
file_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
document_content = (file_name, file_contents, file_type)
document_translate_content = DocumentTranslateContent(document=document_content)

response_stream = client.document_translate(body=document_translate_content, target_language=target_language)

output_file_path = os.path.abspath(
    os.path.join(os.path.abspath(__file__), "..", "../data/Translated_example-en.docx")
)

with open(output_file_path, "wb") as output_file:
    output_file.write(response_stream)

print(f"Translated file saved to: {output_file_path}")