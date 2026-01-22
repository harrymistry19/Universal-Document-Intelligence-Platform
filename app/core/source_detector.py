import os
import mimetypes

def detect_source(input_value):
    if input_value.startswith("http"):
        return "url"          # default: static
    elif os.path.isfile(input_value):
        mime, _ = mimetypes.guess_type(input_value)
        if mime:
            if "pdf" in mime:
                return "pdf"
            if "image" in mime:
                return "image"
    raise ValueError("Unsupported input source")
