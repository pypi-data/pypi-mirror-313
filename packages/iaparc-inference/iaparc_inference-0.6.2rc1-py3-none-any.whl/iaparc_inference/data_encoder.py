"""
IA Parc Inference data decoder
"""
import operator
from functools import reduce  # forward compatibility for Python 3
from typing import Any
import iaparc_inference.encoders as encoders

Error = ValueError | None


class DataEncoder():
    """
    Data Encoder
    This a read-only class that encodes the data
    """

    def __init__(self, conf: dict,):
        """
        Constructor
        Arguments:
        
        """
        self.conf = conf
        self.name = conf["name"]
        self.encoders = {}
        if "type" in self.conf and self.conf["type"] == "multimodal":
            for item in self.conf["items"]:
                self.encoders[item["name"]] = DataEncoder(item)
        if "type" in self.conf and self.conf["type"] == "json":
            self.json_images, self.json_types = self.check_json_images(self.conf["items"])
        else:
            self.json_images = []
            self.json_types = []
    
    def check_json_images(self, items: list) -> tuple[list, list]:
        elts = []
        types = []
        for item in items:
            item_name = item.get("name")
            if item_name:
                if item.get("type") in ["image", "file", "binary", "audio", "video"]:
                    elts.append([item.get("name")])
                    types.append(item.get("type"))
                elif item.get("type") == "json":
                    res, _types = self.check_json_images(item["items"])
                    if len(res) > 0:
                        for k, t in zip(res, _types):
                            new_elt = [item.get("name")]
                            new_elt.extend(k)
                            elts.append(new_elt)
                            types.append(t)
        return elts, types
    
    def encode(self, data: Any) -> tuple[bytes, str, Error]:
        """
        Decode data
        Arguments:
        data: Any
        """
        res = ''.encode()
        contentType = ""
        err = None
        if data is None:
            return res, "", ValueError("No data to encode")
        try:
            match self.conf["type"]:
                case "multimodal":
                    form_data = {}
                    if not isinstance(data, dict):
                        return res, "", ValueError("Data is not a dictionary")
                    for item in self.conf["items"]:
                        if item.get("name") in data:
                            item_name = item.get("name")
                            encoder = self.encoders[item_name]
                            res, ct , err = encoder.encode(data[item_name])
                            if err:
                                return res, "", ValueError(f"{item_name}: {str(err)}")
                            match item["type"]:
                                case "file" | "image" | "binary" | "audio" | "video":
                                    field = (f"{item_name}.bin", res, ct)
                                    form_data[item_name] = field
                                case _:
                                    form_data[item_name] = res
                    res, _ct, err = encoders.encode_multipart(form_data)
                    ct_items = _ct.split(":")
                    if len(ct_items) == 1:
                        contentType = ct_items[0].strip()
                    elif len(ct_items) > 1:
                        contentType = ct_items[1].strip()
                    else:
                        contentType = "multipart/form-data"
                case "json":
                    if len(self.json_images) > 0:
                        for entry, kind in zip(self.json_images, self.json_types):
                            tmp_data = get_by_path(data, entry)
                            if tmp_data and not isinstance(tmp_data, bytes):
                                # If it has already been encoded, skip
                                match kind:
                                    case "image":
                                        tmp_data, _ = encoders.encode_image(
                                            tmp_data)
                                    case _:
                                        tmp_data, _ = encoders.encode_file(
                                            tmp_data)
                                set_by_path(data, entry, tmp_data)
                    res, err = encoders.encode_json(data)
                    contentType = "application/json"
                case "matrix":
                    res, err = encoders.encode_json(data)
                    contentType = "application/json"
                case "file" | "binary" | "audio" | "video":
                    res, err = encoders.encode_file(data)
                    contentType = "application/octet-stream"
                case "image":
                    res, err = encoders.encode_image(data)
                    if not err:
                        contentType = f"image/{data.format.lower()}"
                    else:
                        contentType = "image/*"
                case "text" | "string":
                    res, err = encoders.encode_text(data)
                    contentType = "text/plain"

        except Exception as e:
            return res, "", ValueError(f"Error encoding data: {e}")
        return res, contentType, err


def get_by_path(root: dict, items: list[str]) -> Any:
    """Access a nested object in root by item sequence."""
    return reduce(operator.getitem, items, root)

def set_by_path(root: dict, items: list[str], value: Any):
    """Set a value in a nested object in root by item sequence."""
    get_by_path(root, items[:-1])[items[-1]] = value

def del_by_path(root: dict, items: list[str]):
    """Delete a key-value in a nested object in root by item sequence."""
    del get_by_path(root, items[:-1])[items[-1]]
