from typing import Union

import pytesseract
from pdf2image import convert_from_bytes, convert_from_path


def pdf_image_to_text(input_data: Union[str, bytes]) -> str:
    """
    Converts a PDF that contains images to text using OCR.

    Args:
        input_data (Union[str, bytes]): The file path to the PDF or a bytes-like object
            of the PDF content.

    Returns:
        str: The extracted text from the PDF.
    """

    # Check if the input is a file path (str) or bytes, and
    # convert PDF to images accordingly
    if isinstance(input_data, str):
        images = convert_from_path(input_data)
    elif isinstance(input_data, bytes):
        images = convert_from_bytes(input_data)
    else:
        raise ValueError("input_data must be a file path (str) or bytes-like object")

    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)

    return text
