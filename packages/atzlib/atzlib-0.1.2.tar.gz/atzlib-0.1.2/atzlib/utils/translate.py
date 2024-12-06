import requests
import os

def translate_text(text: str, lang_code: str) -> str:
    """
    Translates the provided text into the target language using Deepl API.

    Args:
        text (str): The text to be translated.
        target_lang (str): The target language code (e.g., 'EN', 'KO').

    Returns:
        str: The translated text.
    """
    endpoint = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": os.environ.get("DEEPL"),
        "text": text,
        "target_lang": lang_code  # en, ko, ...
    }
    response = requests.post(endpoint, data=params, timeout=10)    
    return response.json()["translations"][0]["text"]