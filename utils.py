def normalize_arabic(text):
    if text is None:
        return ""
    text = str(text)
    text = text.replace('ى', 'ي')
    text = text.replace('أ', 'ا')
    text = text.replace('إ', 'ا')
    text = text.replace('آ', 'ا')
    text = text.replace('ة', 'ه')
    text = text.replace('ؤ', 'و')
    text = text.replace('ئ', 'ي')
    return text 