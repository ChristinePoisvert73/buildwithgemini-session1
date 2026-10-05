"""Image generation tool using gemini-3.1-flash-lite-image in global region."""

import os
import uuid
from typing import Any

from google import genai
from google.genai import types
from google.cloud import storage
from google.adk.tools import ToolContext

# HARDCODED PUBLIC BUCKET NAME
BUCKET_NAME = "travel-concierge-assets-qwiklabs-gcp-02-d2b5e9270243"
PROJECT_ID = "qwiklabs-gcp-02-d2b5e9270243"


async def generate_tour_postcard(
    description: str,
    tool_context: ToolContext
) -> dict[str, Any]:
    """Generates a visual travel postcard image for a walking tour or authentic local experience.

    Args:
        description: Visual description or prompt for the postcard (e.g. 'A vibrant street food stall in Tokyo with local people enjoying ramen').
        tool_context: Injected ADK tool context used to save the generated image as a session artifact.

    Returns:
        Dictionary containing the prompt, filename, and public Cloud Storage HTTPS URL of the generated image.
    """
    try:
        # Initialize GenAI client with global region and project
        genai_client = genai.Client(
            vertexai=True,
            project=PROJECT_ID,
            location="global"
        )

        # Generate image using gemini-3.1-flash-lite-image model
        response = genai_client.models.generate_content(
            model="gemini-3.1-flash-lite-image",
            contents=description,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"]
            )
        )

        # Extract image bytes
        image_bytes = None
        mime_type = "image/jpeg"

        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    image_bytes = part.inline_data.data
                    mime_type = part.inline_data.mime_type or mime_type
                    break

        if not image_bytes:
            return {"error": "No image content was returned by the generation model."}

        # Unique filename
        filename = f"postcard_{uuid.uuid4().hex[:8]}.jpg"

        # 1. Save as artifact using tool_context.save_artifact for Playground panel
        artifact_part = types.Part(
            inline_data=types.Blob(mime_type=mime_type, data=image_bytes)
        )
        await tool_context.save_artifact(
            filename=filename,
            artifact=artifact_part
        )

        # 2. Upload same bytes directly to public GCS bucket (without saving to a local file)
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(f"postcards/{filename}")
        blob.upload_from_string(image_bytes, content_type=mime_type)

        public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/postcards/{filename}"

        return {
            "status": "success",
            "prompt": description,
            "filename": filename,
            "public_url": public_url,
            "message": "Successfully generated postcard and saved to artifacts and public Cloud Storage."
        }

    except Exception as e:
        return {"error": f"Failed to generate tour postcard image: {e!s}"}
