"""Video generation tool using gemini-omni-flash-preview in global region."""

import base64
import os
import uuid
from typing import Any

from google import genai
from google.genai import types
from google.cloud import storage
from google.adk.tools import ToolContext

# HARDCODED PUBLIC BUCKET NAME AND GCP PROJECT ID
BUCKET_NAME = "travel-concierge-assets-qwiklabs-gcp-02-d2b5e9270243"
PROJECT_ID = "qwiklabs-gcp-02-d2b5e9270243"


async def generate_tour_video(
    description: str,
    tool_context: ToolContext
) -> dict[str, Any]:
    """Generates a short preview video for a walking tour, scenic spot, or local experience using Google's Omni model.

    Args:
        description: Visual description or prompt for the video (e.g. 'A 3-second cinematic preview of a walking tour through Tokyo street food alley').
        tool_context: Injected ADK tool context used to save the generated video as a session artifact.

    Returns:
        Dictionary containing the prompt, filename, and public Cloud Storage HTTPS URL of the generated video.
    """
    try:
        # Initialize GenAI client with global region and project
        genai_client = genai.Client(
            vertexai=True,
            project=PROJECT_ID,
            location="global"
        )

        # Generate video using gemini-omni-flash-preview via Interactions API
        interaction = genai_client.interactions.create(
            model="gemini-omni-flash-preview",
            input=description
        )

        video_bytes = None
        mime_type = "video/mp4"

        if hasattr(interaction, "output_video") and interaction.output_video and interaction.output_video.data:
            raw_data = interaction.output_video.data
            if isinstance(raw_data, str):
                video_bytes = base64.b64decode(raw_data)
            else:
                video_bytes = raw_data

        if not video_bytes:
            return {"error": "No video content was returned by the Omni generation model."}

        # Unique filename
        filename = f"tour_video_{uuid.uuid4().hex[:8]}.mp4"

        # 1. Save as artifact using tool_context.save_artifact for Playground panel
        artifact_part = types.Part(
            inline_data=types.Blob(mime_type=mime_type, data=video_bytes)
        )
        await tool_context.save_artifact(
            filename=filename,
            artifact=artifact_part
        )

        # 2. Upload same bytes directly to public GCS bucket (without saving to a local file)
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(f"videos/{filename}")
        blob.upload_from_string(video_bytes, content_type=mime_type)

        public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/videos/{filename}"

        return {
            "status": "success",
            "prompt": description,
            "filename": filename,
            "public_url": public_url,
            "message": "Successfully generated tour video and saved to artifacts and public Cloud Storage."
        }

    except Exception as e:
        return {"error": f"Failed to generate tour video: {e!s}"}
