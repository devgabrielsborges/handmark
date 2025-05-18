import os
from dotenv import load_dotenv
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
        load_dotenv()

        self.image_path = image_path
        self.image_format = image_path.split(".")[-1]
        self._token = os.getenv("GITHUB_TOKEN")
        self._model_name = model

        self._client = ChatCompletionsClient(
            endpoint="https://models.github.ai/inference",
            credential=AzureKeyCredential(self._token),
        )

    def get_response(self) -> str:
        response = self._client.complete(
            messages=[
                SystemMessage("You are a helpful assistant that transforms handwritten images in Markdown files."),
                UserMessage(
                    content=[
                        TextContentItem(text="Give to me a Markdown of this text on the image and only this.Add a title for it, that must be the first line of the response .Do not describe the image."),
                        ImageContentItem(
                            image_url=ImageUrl.load(
                                image_file=self.image_path,
                                image_format=self.image_format,
                                detail=ImageDetailLevel.LOW)
                        ),
                    ],
                ),
            ],
            model=self._model_name

        )
        
        return response.choices[0].message.content
    
    def write_response(self, dest_path: str = "./"):
        with open(f"{dest_path}response.md", "w") as f:
            f.write(self.get_response())
