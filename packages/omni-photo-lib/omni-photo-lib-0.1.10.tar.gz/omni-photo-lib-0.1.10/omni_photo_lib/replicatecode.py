import replicate
import base64
import os

def process_image_and_mask(image_path, mask_path, prompt):
    """
    Process an image and mask with the replicate API.

    Args:
        image_path (str): Path to the image file.
        mask_path (str): Path to the mask file.
        prompt (str): Prompt for the API.

    Returns:
        list: A list of output file-like objects from the API.
    """
    # Fetch the API token from the environment
    REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
    if not REPLICATE_API_TOKEN:
        raise ValueError("Please set the REPLICATE_API_TOKEN in your environment variables or .env file.")

    # Set the token for replicate
    replicate.Client(api_token=REPLICATE_API_TOKEN)

    # Encode image and mask to base64
    with open(image_path, 'rb') as img_file:
        image_data = base64.b64encode(img_file.read()).decode('utf-8')
    with open(mask_path, 'rb') as mask_file:
        mask_data = base64.b64encode(mask_file.read()).decode('utf-8')

    # Prepare input for replicate API
    input_data = {
        "mask": f"data:application/octet-stream;base64,{mask_data}",
        "image": f"data:application/octet-stream;base64,{image_data}",
        "prompt": prompt,
    }

    # Call the replicate API
    output = replicate.run("black-forest-labs/flux-fill-dev", input=input_data)
    return output
