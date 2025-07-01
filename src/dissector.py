import os
import re
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import (
    SystemMessage,
    UserMessage,
    TextContentItem,
    ImageContentItem,
    ImageUrl,
    ImageDetailLevel,
)
from azure.core.credentials import AzureKeyCredential


class ImageDissector:
    def __init__(self, image_path: str, model: str = "microsoft/Phi-3.5-vision-instruct"):
        self.image_path = image_path
        self.image_format = image_path.split(".")[-1]
        raw_token = os.getenv("GITHUB_TOKEN")
        if raw_token:
            self._token = raw_token.strip()
        else:
            self._token = None

        if not self._token:
            raise ValueError("GITHUB_TOKEN was not found in environment.")
        self._model_name = model

        self._client = ChatCompletionsClient(
            endpoint="https://models.github.ai/inference",
            credential=AzureKeyCredential(self._token),
        )

    def _sanitize_filename(self, name: str) -> str:
        """Converts a string to a safe filename."""
        if not name:
            return ""

        name = name.strip()
        if not name:
            return ""

        name = name.lower()

        name = re.sub(r"[\s.,!?;:'\"(){}\[\]\\/|<>*?]+", "_", name)
        name = re.sub(r"[^a-z0-9_]+", "_", name)
        name = re.sub(r"_+", "_", name)
        name = name.strip("_")

        if not name:
            return ""

        return f"{name}.md"

    def get_response(self) -> str:
        system_message_content = (
            "You are a helpful assistant that transforms "
            "handwritten images in Markdown files."
        )
        user_message_text = (
            "Give to me a Markdown of this text on the image and only this."
            "Add a title for it, that must be the first line of the response ."
            "Do not describe the image."
        )
        response = self._client.complete(
            messages=[
                SystemMessage(content=system_message_content),
                UserMessage(
                    content=[
                        TextContentItem(text=user_message_text),
                        ImageContentItem(
                            image_url=ImageUrl.load(
                                image_file=self.image_path,
                                image_format=self.image_format,
                                detail=ImageDetailLevel.LOW,
                            )
                        ),
                    ],
                ),
            ],
            model=self._model_name,
        )

        return response.choices[0].message.content

    def write_response(
        self, dest_path: str = "./", fallback_filename: str = "response.md"
    ) -> str:
        markdown_content = self.get_response()

        final_filename_to_use = fallback_filename

        if markdown_content:
            lines = markdown_content.splitlines()
            if lines:
                title_candidate = lines[0].strip()
                if title_candidate:
                    derived_filename = self._sanitize_filename(title_candidate)
                    if derived_filename:
                        final_filename_to_use = derived_filename

        os.makedirs(dest_path, exist_ok=True)
        full_output_path = os.path.join(dest_path, final_filename_to_use)

        with open(full_output_path, "w") as f:
            f.write(markdown_content if markdown_content else "")

        return full_output_path
