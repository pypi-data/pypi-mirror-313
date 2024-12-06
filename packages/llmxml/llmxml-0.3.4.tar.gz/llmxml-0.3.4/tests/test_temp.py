import json
from pathlib import Path
from typing import Type, TypeVar, Union

from llmxml import XMLSafeString, generate_prompt_template, parse_xml
from pydantic import BaseModel, Field

T = TypeVar("T", bound=BaseModel)


def load_test_file(filename: str) -> str:
    """Load test file content."""
    test_dir = Path(__file__).parent / "test_files_temp"
    with open(test_dir / filename, "r") as f:
        return f.read()


def validate_parsed_model(parsed: BaseModel, model_class: Type[T]) -> None:
    """Helper function to validate parsed models"""
    assert (
        isinstance(parsed, model_class)
        or type(parsed).__name__.startswith(f"Partial{model_class.__name__}")
    ), f"Expected {model_class.__name__} or Partial{model_class.__name__}, got {type(parsed).__name__}"
    json_str = parsed.model_dump_json()
    assert json.loads(json_str), "Model should be JSON serializable"


class NewFileResponse(BaseModel):
    thinking: str = Field(..., description="The thinking to perform")
    new_file_path: str = Field(..., description="The path to the new file to create")
    file_contents: XMLSafeString = Field(
        ..., description="The contents of the new file to create"
    )


class File(BaseModel):
    new_file_path: str = Field(..., description="The path to the new file to create")
    file_contents: str = Field(
        ..., description="The contents of the new file to create"
    )


class MultiNewFileResponse(BaseModel):
    thinking: str = Field(..., description="The thinking to perform")
    files: list[File] = Field(..., description="The files to create")


class CreateFileResponse(BaseModel):
    thinking: XMLSafeString = Field(
        ..., description="The assistant's analysis and reasoning"
    )
    new_file_path: XMLSafeString = Field(..., description="The path to the new file")
    file_contents: XMLSafeString = Field(
        ..., description="The full updated file contents"
    )


class TestNewFileResponse:
    def test_complete_response(self):
        """Test parsing a complete response with multiple actions."""
        xml = load_test_file("mod_1.xml")
        result = parse_xml(CreateFileResponse, xml)

        assert isinstance(result, CreateFileResponse)
        assert result.thinking.strip() != ""
        assert "break down" in result.thinking

        assert result.new_file_path.endswith(".tsx")
        assert "page.tsx" in result.new_file_path

        assert result.file_contents.strip() != ""
        assert "bgColor" in result.file_contents

    def test_complete_response_streaming(self):
        xml = load_test_file("mod_1.xml")
        partial_content = ""
        last_valid_result = None
        for char in xml:
            partial_content += char
            result = parse_xml(NewFileResponse, partial_content)
            validate_parsed_model(result, NewFileResponse)
            last_valid_result = result

        assert last_valid_result is not None
        assert isinstance(last_valid_result, NewFileResponse)
        assert last_valid_result.thinking.strip() != ""
        assert "Chakra UI" in last_valid_result.thinking

        assert last_valid_result.new_file_path.endswith(".tsx")
        assert "page.tsx" in last_valid_result.new_file_path

        assert last_valid_result.file_contents.strip() != ""
        assert "bgColor" in last_valid_result.file_contents


from rich.console import Console

console = Console()


class TestMultiNewFileResponse:
    def test_complete_response(self):
        """Test parsing a complete response with multiple actions."""
        xml = load_test_file("multiple_new_files.xml")
        result = parse_xml(MultiNewFileResponse, xml)

        assert result.thinking.strip() != ""
        assert "Chakra UI" in result.thinking

        assert result.files[0].new_file_path.endswith(".tsx")
        assert "app/components/Header.tsx" in result.files[0].new_file_path

        assert result.files[0].file_contents.strip() != ""
        assert "use client" in result.files[0].file_contents
        assert "direction" in result.files[0].file_contents

    def test_complete_response_streaming(self):
        xml = load_test_file("multiple_new_files.xml")
        partial_content = ""
        last_valid_result = None
        for char in xml:
            partial_content += char
            result = parse_xml(MultiNewFileResponse, partial_content)
            if result is not None:
                validate_parsed_model(result, MultiNewFileResponse)
                last_valid_result = result

        assert last_valid_result is not None
        assert isinstance(last_valid_result, MultiNewFileResponse)
        assert last_valid_result.thinking.strip() != ""
        assert "Chakra UI" in last_valid_result.thinking

        assert last_valid_result.files[0].new_file_path.endswith(".tsx")
        assert "app/components/Header.tsx" in last_valid_result.files[0].new_file_path

        assert last_valid_result.files[0].file_contents.strip() != ""
        assert "use client" in last_valid_result.files[0].file_contents
        assert "direction" in last_valid_result.files[0].file_contents


class SectionEdit(BaseModel):
    original_code_section: XMLSafeString = Field(
        ..., description="The original code section"
    )
    new_code_section: XMLSafeString = Field(..., description="The new code section")


class FullFileContents(BaseModel):
    file_contents: XMLSafeString = Field(
        ..., description="The full file contents to edit"
    )


class EditFileResponse(BaseModel):
    thinking: XMLSafeString = Field(..., description="The thinking to perform")
    num_sections_to_modify: int = Field(
        ..., description="The number of sections to modify"
    )
    edits: list[Union[SectionEdit, FullFileContents]] = Field(
        ..., description="The inline_edits to make to the file"
    )
    command_to_run: Union[str, None] = Field(
        ..., description="The command to run to update the file"
    )


class TestEditFileResponse:
    def test_mixed_edits(self):
        xml = load_test_file("mixed_edits.xml")
        result = parse_xml(EditFileResponse, xml)

        assert isinstance(result, EditFileResponse)
        assert "landing page with multiple sections" in result.thinking
        assert result.num_sections_to_modify == 1
        assert result.edits is not None
        assert isinstance(result.edits[0], FullFileContents)
        assert result.edits[0].file_contents.strip() != ""
        assert "import { Box" in result.edits[0].file_contents
        assert len(result.edits) == 1

    def test_mixed_edits_streaming(self):
        xml = load_test_file("mixed_edits.xml")
        partial_content = ""
        last_valid_result = None
        for char in xml:
            partial_content += char
            result = parse_xml(EditFileResponse, partial_content)
            validate_parsed_model(result, EditFileResponse)
            last_valid_result = result

        assert last_valid_result is not None
        assert isinstance(last_valid_result, EditFileResponse)
        assert "landing page with multiple sections" in last_valid_result.thinking
        assert last_valid_result.num_sections_to_modify == 1
        assert last_valid_result.edits is not None
        assert len(last_valid_result.edits) == 1

    def test_full_edit(self):
        xml = load_test_file("full_edit.xml")
        result = parse_xml(EditFileResponse, xml)

        assert result.thinking.strip() != ""
        assert result.num_sections_to_modify == 1
        assert result.edits is not None
        assert isinstance(result.edits[0], FullFileContents)
        assert result.edits[0].file_contents.strip() != ""
        assert "Idk lol" in result.command_to_run

    def test_full_edit_streaming(self):
        xml = load_test_file("full_edit.xml")
        partial_content = ""
        last_valid_result = None
        for char in xml:
            partial_content += char
            result = parse_xml(EditFileResponse, partial_content)
            if result is not None:
                validate_parsed_model(result, EditFileResponse)
                last_valid_result = result

        assert last_valid_result is not None
        assert isinstance(last_valid_result, EditFileResponse)
        assert last_valid_result.thinking.strip() != ""
        assert last_valid_result.num_sections_to_modify == 1
        assert last_valid_result.edits[0].file_contents.strip() != ""
        assert "Idk lol" in last_valid_result.command_to_run


class TestPrompting:
    def test_prompt_template(self):
        result = generate_prompt_template(EditFileResponse)
        print(result)


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v"])
