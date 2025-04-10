from typing import Dict


def get_content_type(params: Dict[str, str]) -> str:
    """Checks the content type (image, audio, or text) in the parameters."""

    media_type = params.get("MediaContentType0", "")
    if not isinstance(media_type, str):
        raise TypeError("The value of 'MediaContentType0' must be a string.")

    if media_type.startswith("image/"):
        return "image"
    if media_type.startswith("audio/"):
        return "audio"
    return "text"
