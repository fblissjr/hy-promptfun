# prompt_emulator.py

from typing import Literal, Optional, Union
import json
from constants import (
    CAMERA_MOVEMENTS,
    VISUAL_STYLES,
    LIGHTING_CONDITIONS,
    PROMPT_TEMPLATES
)

class HunyuanPromptEmulator:
    def __init__(self, llm_client):
        """
        Initialize with any LLM client that has a generate method.

        Args:
            llm_client: Client that implements generate(system_prompt, user_prompt)
        """
        self.llm = llm_client

    def _process_image(self, image_data: Union[str, bytes]) -> str:
        """
        Process the image data and return a textual description.

        Args:
            image_data: Image data in bytes or file path

        Returns:
            Textual description of the image
        """
        if isinstance(image_data, str):
            # Assume image_data is a file path
            with open(image_data, 'rb') as image_file:
                image_bytes = image_file.read()
        else:
            # Assume image_data is already in bytes
            image_bytes = image_data
            
        description = self._image_captioning_model(image_bytes)
        return description

    def _image_captioning_model(self, image_bytes: bytes) -> str:
        """
        Placeholder for an image captioning model.

        Args:
            image_bytes: Image data in bytes

        Returns:
            Textual description of the image
        """
        # This is a placeholder for the actual image captioning logic
        # You would replace this with your actual image captioning model
        return "Not done yet - soon, maybe"

    def _get_structured_description(self,
                                  text: str = None,
                                  image: str = None) -> dict:
        """
        Generate structured description from text or image input.
        """
        base_prompt = """
        Create a structured video description with these components:
        {
            "short_description": "Core action and subject",
            "dense_description": "Detailed scene description with motion",
            "camera_movement": "Primary camera movement",
            "style": "Visual style",
            "lighting": "Lighting conditions",
            "atmosphere": "Mood and feeling",
            "technical_details": "Professional production elements"
        }
        """

        if image:
            # Process the image to get a textual description
            image_description = self._process_image(image)
            prompt = f"{base_prompt}\nAnalyze this image description: {image_description}"
        else:
            prompt = f"{base_prompt}\nAnalyze this text: {text}"

        response = self.llm.generate(
            system_prompt=prompt,
            user_prompt=text or "Analyze the provided image"
        )

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Fallback to simple structure if JSON parsing fails
            return {
                "short_description": response,
                "dense_description": response,
                "camera_movement": "tracking shot",
                "style": "cinematic",
                "lighting": "natural lighting",
                "atmosphere": "professional"
            }

    def generate_prompt(self,
                       input_data: Union[str, bytes],
                       mode: Literal["normal", "master"] = "normal") -> str:
        """
        Generate a Hunyuan-style prompt from text or image input.

        Args:
            input_data: Text string or image data
            mode: "normal" or "master"

        Returns:
            Formatted prompt string
        """
        # Determine if input is image or text
        is_image = isinstance(input_data, bytes) or (
            isinstance(input_data, str) and
            any(input_data.lower().endswith(ext)
                for ext in ['.jpg','.png','.jpeg'])
        )

        # Get structured description
        components = self._get_structured_description(
            text=None if is_image else input_data,
            image=input_data if is_image else None
        )

        # Get template for selected mode
        template = PROMPT_TEMPLATES[mode].format(
            camera_movements=", ".join(CAMERA_MOVEMENTS),
            visual_styles=", ".join(VISUAL_STYLES),
            lighting_conditions=", ".join(LIGHTING_CONDITIONS)
        )

        # Generate final prompt
        final_prompt = self.llm.generate(
            system_prompt=template,
            user_prompt=json.dumps(components)
        )

        return final_prompt.strip()
