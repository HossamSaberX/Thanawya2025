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

def format_student_result(row):
    if not row:
        return None
    row_dict = dict(row)
    total_degree = row_dict.get('degree', 0)
    is_pass = total_degree >= 160
    return {
        'رقم الجلوس': row_dict.get('seating_no', 'N/A'),
        'الاسم': row_dict.get('name', 'N/A'),
        'الدرجة': total_degree,
        'student_case_desc': 'ناجح' if is_pass else 'راسب'
    }