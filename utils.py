import textract

def extract_text_from_pdf(file):
    text = textract.process(file, method='pdfminer').decode('utf-8')
    return text


def extract_text_from_docx(file):
    text = textract.process(file).decode('utf-8')
    return text