"""
IA Parc Inference encoders
"""
from PIL.Image import Image
from io import BytesIO, StringIO

Error = ValueError | None

## Data encoders
def encode_file(file: BytesIO) -> tuple[bytes, Error]:
    """
    Encode file to bytes
    Arguments:
    file: BytesIO
    """
    if not file:
        return ''.encode(), ValueError("No data to encode")
    if not isinstance(file, BytesIO):
        return ''.encode(), ValueError("Data is not a file")
    try:
        data = file.read()
    except Exception as e:
        return ''.encode(), ValueError(f"Error encoding file: {e}")
    return data, None

def encode_image(img: Image) -> tuple[bytes, Error]:
    """
    Encode image to bytes
    Arguments:
    img: PIL Image
    """
    from PIL import Image
    data = ''.encode()
    if img is None:
        return data, ValueError("No data to encode")
    try:
        buf = BytesIO()
        img.save(buf, format=img.format)
        data = buf.getvalue()
    except Exception as e:
        return data, ValueError(f"Error encoding image: {e}")    
    return data, None

def encode_text(text: str) -> tuple[bytes, Error]:
    """
    Encode text to bytes
    Arguments:
    text: str
    """
    data = ''.encode()    
    if not isinstance(text, str):
        return data, ValueError("Data is not a string")
    try:
        data = text.encode("utf-8")
    except Exception as e:
        return data, ValueError(f"Error encoding text: {e}")
    return data, None

def encode_json(in_data: dict) -> tuple[bytes, Error]:
    """
    Encode json to bytes
    Arguments:
    in_data: dict
    """
    data = ''.encode()
    from json_tricks import dumps
    if in_data is None:
        return data, ValueError("No data to encode")
    try:
        s_data = dumps(in_data)
        data = str(s_data).encode("utf-8")                
    except Exception as e:
        return data, ValueError(f"Error encoding json: {e}")
    return data, None

def encode_numpy(in_data: dict) -> tuple[bytes, Error]:
    """
    Encode numpy to bytes
    Arguments:
    in_data: dict
    """
    return encode_json(in_data)

def encode_multipart(data: dict) -> tuple[bytes, str, Error]:
    """
    Encode multi-part data to bytes
    Arguments:
    data: dict
    """
    body = ''.encode()
    if data is None:
        return body, "", ValueError("No data to encode")
    try:
        from urllib3 import encode_multipart_formdata
        body, header = encode_multipart_formdata(data)
    except Exception as e:
        return body, "", ValueError(f"Error encoding multi-part data: {e}")
    return body, header, None

