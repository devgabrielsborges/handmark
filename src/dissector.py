import os
import re
import json
import yaml
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Any
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
    def __init__(
        self,
        image_path: str,
        model: str = "microsoft/Phi-3.5-vision-instruct",
        output_format: str = "markdown",
    ):
        self.image_path = image_path
        self.image_format = image_path.split(".")[-1]
        self.output_format = output_format.lower()
        self._load_config()

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

    def _load_config(self) -> None:
        """Load configuration from config.json file"""
        config_path = Path(__file__).parent.parent / "config" / "config.json"
        try:
            with open(config_path, "r") as f:
                self.config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"Could not load config file: {e}")

        if self.output_format not in self.config["output_formats"]:
            available_formats = list(self.config["output_formats"].keys())
            raise ValueError(
                f"Unknown output format '{self.output_format}'. "
                f"Available formats: {available_formats}"
            )

    def _get_format_config(self) -> Dict[str, Any]:
        """Get configuration for the current output format"""
        return self.config["output_formats"][self.output_format]

    def _sanitize_filename(self, name: str) -> str:
        """Converts a string to a safe filename with the appropriate extension."""
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

        extension = self._get_file_extension()
        return f"{name}{extension}"

    def get_response(self) -> str:
        format_config = self._get_format_config()
        system_message_content = format_config["system_message_content"]
        user_message_text = format_config["user_message_content"]

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

    def _process_content(self, raw_content: str) -> str:
        """Process the raw content based on the output format"""
        if self.output_format == "markdown":
            return raw_content
        elif self.output_format == "json":
            return self._process_json_content(raw_content)
        elif self.output_format == "yaml":
            return self._process_yaml_content(raw_content)
        elif self.output_format == "xml":
            return self._process_xml_content(raw_content)
        else:
            return raw_content

    def _process_json_content(self, content: str) -> str:
        """Process and validate JSON content"""
        try:
            clean_content = self._strip_code_blocks(content, "json")
            parsed = json.loads(clean_content)
            format_config = self._get_format_config()
            return json.dumps(
                parsed,
                indent=2 if format_config.get("pretty_print", True) else None,
                ensure_ascii=not format_config.get("ensure_ascii", False),
            )
        except json.JSONDecodeError:
            # If it's not valid JSON, return as-is
            return content

    def _process_yaml_content(self, content: str) -> str:
        """Process and validate YAML content"""
        try:
            clean_content = self._strip_code_blocks(content, "yaml")
            parsed = yaml.safe_load(clean_content)
            format_config = self._get_format_config()
            return yaml.dump(
                parsed,
                default_flow_style=format_config.get("default_flow_style", False),
                allow_unicode=format_config.get("allow_unicode", True),
            )
        except yaml.YAMLError:
            return content

    def _process_xml_content(self, content: str) -> str:
        """Process and validate XML content"""
        try:
            clean_content = self._strip_code_blocks(content, "xml")
            root = ET.fromstring(clean_content)
            format_config = self._get_format_config()
            if format_config.get("pretty_print", True):
                ET.indent(root, space="  ")
            return ET.tostring(root, encoding="unicode")
        except ET.ParseError:
            return content

    def _get_file_extension(self) -> str:
        """Get the file extension for the current format"""
        format_config = self._get_format_config()
        return format_config["file_extension"]

    def _strip_code_blocks(self, content: str, format_type: str) -> str:
        """Strip markdown code blocks from content if present"""
        lines = content.strip().splitlines()

        # Check if content is wrapped in code blocks
        if len(lines) >= 2:
            first_line = lines[0].strip()
            last_line = lines[-1].strip()

            code_block_markers = [
                f"```{format_type}",
                f"```{format_type.upper()}",
                "```",
            ]

            if (
                any(first_line.startswith(marker) for marker in code_block_markers)
                and last_line == "```"
            ):
                # Remove first and last lines (code block markers)
                return "\n".join(lines[1:-1])

        return content

    def write_response(
        self, dest_path: str = "./", fallback_filename: str = None
    ) -> str:
        raw_content = self.get_response()
        processed_content = self._process_content(raw_content)

        if fallback_filename is None:
            extension = self._get_file_extension()
            fallback_filename = f"response{extension}"

        final_filename_to_use = fallback_filename

        if processed_content:
            if self.output_format == "markdown":
                lines = processed_content.splitlines()
                if lines:
                    title_candidate = lines[0].strip()
                    if title_candidate.startswith("#"):
                        title_candidate = title_candidate.lstrip("#").strip()
                    if title_candidate:
                        derived_filename = self._sanitize_filename(title_candidate)
                        if derived_filename:
                            final_filename_to_use = derived_filename

            elif self.output_format in ["json", "yaml"]:
                try:
                    content_to_parse = self._strip_code_blocks(
                        processed_content, self.output_format
                    )

                    if self.output_format == "json":
                        data = json.loads(content_to_parse)
                    else:
                        data = yaml.safe_load(content_to_parse)

                    if isinstance(data, dict) and "title" in data:
                        title = data["title"]
                        if title and isinstance(title, str):
                            derived_filename = self._sanitize_filename(title)
                            if derived_filename:
                                final_filename_to_use = derived_filename
                except (json.JSONDecodeError, yaml.YAMLError):
                    pass

            elif self.output_format == "xml":
                try:
                    content_to_parse = self._strip_code_blocks(
                        processed_content, self.output_format
                    )
                    root = ET.fromstring(content_to_parse)

                    # First, try to find a title element
                    title_elem = root.find(".//title")
                    title_text = None

                    if title_elem is not None and title_elem.text:
                        title_text = title_elem.text.strip()
                    else:
                        # Fallback: try to extract meaningful content
                        # Look for content element and use first few words
                        content_elem = root.find(".//content")
                        if content_elem is not None and content_elem.text:
                            content_text = content_elem.text.strip()
                            if content_text:
                                # Use first 3-5 words as title
                                words = content_text.split()[:4]
                                title_text = " ".join(words)

                        # If still no title, use the root element's first text content
                        if not title_text:
                            for elem in root.iter():
                                if elem.text and elem.text.strip():
                                    words = elem.text.strip().split()[:3]
                                    title_text = " ".join(words)
                                    break

                    if title_text:
                        derived_filename = self._sanitize_filename(title_text)
                        if derived_filename:
                            final_filename_to_use = derived_filename

                except ET.ParseError:
                    pass

        os.makedirs(dest_path, exist_ok=True)
        full_output_path = os.path.join(dest_path, final_filename_to_use)

        with open(full_output_path, "w", encoding="utf-8") as f:
            f.write(processed_content if processed_content else "")

        return full_output_path
