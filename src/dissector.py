import os
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
    def __init__(self, image_path: str, model: str = "openai/gpt-4o"):
        self.image_path = image_path
        self.image_format = image_path.split(".")[-1]
        raw_token = os.getenv("GITHUB_TOKEN")
        if raw_token:
            self._token = raw_token.strip()
        else:
            self._token = None

        if not self._token:
            # This case should ideally be prevented by main.py's checks,
            # but as a safeguard for direct instantiation or other uses:
            raise ValueError("GITHUB_TOKEN was not found in environment.")
        self._model_name = model

        # Initialize client only if token is present (already guarded by the check above)
        self._client = ChatCompletionsClient(
            endpoint="https://models.github.ai/inference",
            credential=AzureKeyCredential(self._token),
        )

    def get_response(self) -> str:
        # The __init__ method now raises ValueError if token is missing,
        # so self._client should always be initialized if an instance exists.
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

    def write_response(self, dest_path: str = "./", filename: str = "response.md"):
        os.makedirs(dest_path, exist_ok=True)
        full_output_path = os.path.join(dest_path, filename)
        with open(full_output_path, "w") as f:
            f.write(self.get_response())
