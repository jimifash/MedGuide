from translate import Translator

def trans_text(text, language):
    """Help  translate user texts to user's preferred language"""
    translator = Translator(to_lang = language)
    translation = translator.translate(text)

    return translation