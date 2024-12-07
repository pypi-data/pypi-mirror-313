import logging

logger = logging.getLogger(__name__)

def parse_aspect_ratio(aspect_ratio, base_size=512):
    """
    Parse aspect ratio string and return width and height.
    Default base_size is 512.
    """
    try:
        if ":" in aspect_ratio:
            width_ratio, height_ratio = map(float, aspect_ratio.split(":"))
            width = int(base_size * width_ratio)
            height = int(base_size * height_ratio)
        else:
            width = height = base_size  # Default to square if aspect ratio is invalid
        return width, height
    except Exception:
        logger.warning("Invalid aspect ratio provided. Using default square dimensions.")
        return base_size, base_size


def get_runtime_parameters(runtime):
    """
    Adjust inference steps based on runtime.
    """
    if runtime == "short":
        return 10
    elif runtime == "medium":
        return 50
    elif runtime == "long":
        return 100
    else:
        return 50  # Default to medium
