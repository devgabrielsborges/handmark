import os
import re
import json
import yaml
import xml.etree.ElementTree as ET
from models.json import get_json_config
from models.markdown import get_markdown_config
from models.xml import get_xml_config
from models.yaml import get_yaml_config
from providers.factory import create_provider
from model import Model


class ImageDissector:
    def __init__(
        self,
        image_path: str,
        model: Model,
        output_format: str = "markdown",
    ):
        self.image_path = image_path
        self.image_format = image_path.split(".")[-1]
        self.output_format = output_format.lower()
        self.format_config = self._get_format_config()
        self._model = model
        self._provider = create_provider(model)

    def _get_format_config(self):
        """Get configuration for the current output format using dataclasses"""
        if self.output_format == "markdown":
            return get_markdown_config()
        elif self.output_format == "json":
            return get_json_config()
        elif self.output_format == "yaml":
            return get_yaml_config()
        elif self.output_format == "xml":
            return get_xml_config()
        else:
            raise ValueError(f"Unknown output format '{self.output_format}'.")

    def _get_file_extension(self) -> str:
        """Get the file extension for the current output format."""
        return self.format_config.file_extension

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
        """Get AI response using the configured provider"""
        system_message_content = self.format_config.system_message_content
        user_message_text = self.format_config.user_message_content

        model_name = (
            self._model.ollama_model_name
            if self._model.ollama_model_name
            else self._model.name
        )

        return self._provider.get_response(
            image_path=self.image_path,
            system_message=system_message_content,
            user_message=user_message_text,
            model_name=model_name,
        )

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
            return json.dumps(
                parsed,
                indent=2 if self.format_config.pretty_print else None,
                ensure_ascii=not self.format_config.ensure_ascii,
            )
        except json.JSONDecodeError:
            # If it's not valid JSON, return as-is
            return content

    def _process_yaml_content(self, content: str) -> str:
        """Process and validate YAML content"""
        try:
            clean_content = self._strip_code_blocks(content, "yaml")
            parsed = yaml.safe_load(clean_content)
            return yaml.dump(
                parsed,
                default_flow_style=self.format_config.default_flow_style,
                allow_unicode=self.format_config.allow_unicode,
            )
        except yaml.YAMLError:
            return content

    def _process_xml_content(self, content: str) -> str:
        """Process and validate XML content"""
        try:
            clean_content = self._strip_code_blocks(content, "xml")
            root = ET.fromstring(clean_content)
            if self.format_config.pretty_print:
                ET.indent(root, space="  ")
            return ET.tostring(root, encoding="unicode")
        except ET.ParseError:
            return content

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
