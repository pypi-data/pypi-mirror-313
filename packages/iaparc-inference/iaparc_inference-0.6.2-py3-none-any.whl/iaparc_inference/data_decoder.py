"""
IA Parc Inference data handler
"""
import os
import io
import logging
import logging.config
from typing import Any
import iaparc_inference.decoders as decoders

Error = ValueError | None

LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=LEVEL,
    force=True,
    format="%(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
LOGGER = logging.getLogger("Inference")
LOGGER.propagate = True


def decode(raw: bytes, content_type: str, conf: dict) -> tuple[Any, Error]:
    if conf["type"] == "multimodal":
        raw_items, error = decoders.decode_multipart(
            raw, conf["items"], content_type)
        result = {}
        for item in conf["items"]:
            item_data = raw_items.get(item["name"])
            if item_data:
                result[item["name"]], error = _decode(item_data, item["type"])
                if error:
                    LOGGER.error(f"Error decoding {item['name']}: {error}")
                    return None, error
        return result, None
    else:
        return _decode(raw, conf["type"])

def _decode(raw, kind) -> tuple[Any, Error]:
    """
    Decode data
    """
    match kind:
        case "integer":
            return decoders.decode_int(raw)
        case "boolean":
            return decoders.decode_bool(raw)
        case "number":
            return decoders.decode_float(raw)
        case "file" | "binary" | "audio" | "video":
            return decoders.decode_file(raw)
        case "text" | "string":
            return decoders.decode_text(raw)
        case "image":
            return decoders.decode_image(raw)
        case "json" | "matrix" | "array":
            return decoders.decode_json(raw)
        case _:
            return raw, ValueError(f"Unsupported data type: {kind}")

