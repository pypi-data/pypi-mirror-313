from PIL import Image
import requests
from together import Together
import os
import logging

logger = logging.getLogger(__name__)

# Ensure output folder exists
OUTPUT_FOLDER = os.path.abspath("output_files")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# The Celery app will be initialized externally and injected here
def register_tasks(celery):
    """
    Register tasks with an external Celery instance.
    """
    @celery.task(name="omni_photo_lib.generate_image_task")
    def generate_image_task(
        model_name,
        prompt,
        steps,
        width,
        height,
        num_images,
        image_url=None,
        mask_url=None,
        task_type=None,
        style=None,
        seed=None,
    ):
        """
        Celery task to generate images using Together API.
        """
        try:
            # Replace 'YOUR_API_KEY' with a dynamic value from environment variables
            client = Together(api_key="7c0df69e207dce0a688cc91caaec8fd3a097e50aaa3ed4b640c6cf133e4f67df")

            # Build request payload
            request_payload = {
                "model": model_name,
                "width": width,
                "height": height,
                "steps": steps,
                "prompt": prompt,
                "n": num_images,
                "style": style,
                "seed": seed,
            }

            # Add specific parameters for task type
            if task_type == "depth_to_image" and image_url:
                request_payload["image_url"] = image_url
            elif task_type == "inpainting" and image_url and mask_url:
                request_payload["image_url"] = image_url
                request_payload["mask_url"] = mask_url

            # Generate images
            response = client.images.generate(**request_payload)

            # Save generated images locally
            image_paths = []
            if hasattr(response, "data") and isinstance(response.data, list):
                for idx, img_data in enumerate(response.data):
                    if hasattr(img_data, "url"):
                        output_path = os.path.join(
                            OUTPUT_FOLDER, f"{task_type}_output_{idx}.png"
                        )
                        img = Image.open(requests.get(img_data.url, stream=True).raw)
                        img.save(output_path)
                        image_paths.append(output_path)
                    else:
                        raise ValueError("Missing 'url' in API response")

            return image_paths
        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            return str(e)

    return generate_image_task
