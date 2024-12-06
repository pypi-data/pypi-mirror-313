from dataclasses import dataclass, field
from typing import Any

from .slack_enums import (
    ContextSubBlockType,
    RichTextElementStyle,
    RichTextElementType,
    RichTextListType,
    RichTextSectionType,
    SectionTextType,
)


@dataclass
class BaseBlock:
    """
    Base class for Slack blocks.

    Provides a template for implementing different types of Slack blocks.
    """

    def reset_value(self) -> None:
        """
        Resets the value of the block to its default state.

        Raises:
            NotImplementedError: If the method is not implemented by subclasses.
        """
        raise NotImplementedError("Subclasses should implement this method")

    def value(self) -> dict[str, Any]:
        """
        Retrieves the dictionary representation of the block.

        Returns:
            dict: Dictionary representation of the block.

        Raises:
            NotImplementedError: If the method is not implemented by subclasses.
        """
        raise NotImplementedError("Subclasses should implement this method")

@dataclass
class ContextSubBlock:
    """
    Represents a context sub-block for Slack messages.

    Attributes:
        type (ContextSubBlockType): The type of the context block (e.g., text or image).
        text (str|None): Text content for the block, if applicable.
        image_url (str|None): Image URL for the block, if applicable.
        alt_text (str|None): Alternate text for the image, if applicable.
    """
    type: ContextSubBlockType
    text: str|None = None
    image_url: str|None = None
    alt_text: str|None = None

    def value(self) -> dict[str, Any]:
        """
        Retrieves the dictionary representation of the context sub-block.

        Returns:
            dict: Dictionary with the context block's type and elements.

        Raises:
            ValueError: If required attributes for the block type are missing.
        """
        if self.type in {ContextSubBlockType.plain_text, ContextSubBlockType.mrkdwn} and self.text is None:
            raise ValueError("Text attribute is required for plain_text or mrkdwn types.")
        elif self.type == ContextSubBlockType.image and (self.image_url is None or self.alt_text is None):
            raise ValueError("image_url and alt_text attributes are required for image type.")

        match self.type:
            case ContextSubBlockType.image:
                return {"type": self.type.value, "image_url": self.image_url, "alt_text": self.alt_text}
            case ContextSubBlockType.mrkdwn | ContextSubBlockType.plain_text:
                return {"type": self.type.value, "text": self.text}


@dataclass
class RichTextElement:
    """
    Represents a rich text element within a Slack block.

    Attributes:
        type (RichTextElementType): The type of the rich text element (e.g., text, emoji, link).
        text (str|None): Text content of the element, if applicable.
        styles (list[RichTextElementStyle]|None): A list of styles applied to the element, if applicable.
        name (str|None): Name for emoji elements, if applicable.
        url (str|None): URL for link elements, if applicable.
    """

    type: RichTextElementType
    text: str | None = None
    styles: list[RichTextElementStyle] | None = None
    name: str | None = None
    url: str | None = None

    def value(self) -> dict[str, Any]:
        """
        Retrieves the dictionary representation of the rich text element.

        Returns:
            dict: Dictionary with the element's type and attributes.

        Raises:
            ValueError: If required attributes for the element type are missing.
        """
        if self.type == RichTextElementType.text and self.text is None:
            raise ValueError("Text attribute is required for text type.")
        elif self.type == RichTextElementType.emoji and self.name is None: 
            raise ValueError("Name attribute is required for emoji type.")
        elif self.type == RichTextElementType.link and self.url is None: 
            raise ValueError("URL attribute is required for link type.")

        match self.type:
            case RichTextElementType.text:
                return {
                    "type": self.type.value,
                    "text": self.text,
                    "style": {style.value: True for style in self.styles} if self.styles else {},
                }
            case RichTextElementType.emoji:
                return {"type": self.type.value, "name": self.name}
            case RichTextElementType.link:
                result: dict[str, Any] = {
                    "type": self.type.value,
                    "url": self.url,
                    "style": {style.value: True for style in self.styles} if self.styles else {},
                }
                if self.text:
                    result["text"] = self.text
                return result


@dataclass
class RichTextSection:
    """
    Represents a rich text section containing multiple rich text elements.

    Attributes:
        type (RichTextSectionType): The type of the rich text section.
        elements (list[RichTextElement]): A list of rich text elements in this section.
    """

    type: RichTextSectionType
    elements: list[RichTextElement] = field(default_factory=list)

    def add_rich_text_elements(self, *, rich_text_element: list[RichTextElement]) -> None:
        """
        Adds rich text elements to the section.

        Args:
            rich_text_element (list[RichTextElement]): A list of rich text elements to add.
        """
        self.elements.extend(rich_text_element)

    def value(self) -> dict[str, Any]:
        """
        Retrieves the dictionary representation of the rich text section.

        Returns:
            dict: Dictionary with the section's type and elements.
        """
        return {
            "type": self.type.value,
            "elements": [element.value() for element in self.elements],
        }


@dataclass
class RichTextList:
    """
    Represents a list of rich text sections in a Slack block.

    Attributes:
        type (RichTextListType): The style of the list (e.g., numbered, bulleted).
        elements (list[RichTextSection]): A list of rich text sections in this list.
    """

    type: RichTextListType
    elements: list[RichTextSection] = field(default_factory=list)

    def add_rich_text_sections(self, *, rich_text_sections: list[RichTextSection]) -> None:
        """
        Adds rich text sections to the list.

        Args:
            rich_text_sections (list[RichTextSection]): A list of rich text sections to add.

        Raises:
            ValueError: If any section does not match the type required for the list.
        """
        for section in rich_text_sections:
            if section.type != RichTextSectionType.rich_text_section:
                raise ValueError("Only rich text sections with a type of RichTextSectionType.rich_text_section can be added to a RichTextList.")
        self.elements.extend(rich_text_sections)

    def value(self) -> dict[str, Any]:
        """
        Retrieves the dictionary representation of the rich text list.

        Returns:
            dict: Dictionary with the list's type, style, and elements.
        """
        return {
            "type": "rich_text_list",
            "style": self.type.value,
            "elements": [section.value() for section in self.elements],
        }


@dataclass
class SectionTextElement:
    """
    Represents a text element within a section block.

    Attributes:
        type (SectionTextType): The type of text (e.g., plain_text or mrkdwn).
        text (str): The content of the text.
    """

    type: SectionTextType
    text: str

    def value(self) -> dict[str, Any]:
        """
        Retrieves the dictionary representation of the section text element.

        Returns:
            dict: Dictionary with the text element's type and content.
        """
        return {
            "type": self.type.value,
            "text": self.text,
        }


@dataclass
class SectionAccessory:
    """
    Represents an accessory for a section block, such as an image.

    Attributes:
        image_url (str): The URL of the image.
        alt_text (str): Alternate text for the image.
    """

    image_url: str
    alt_text: str

    def value(self) -> dict[str, Any]:
        """
        Retrieves the dictionary representation of the section accessory.

        Returns:
            dict: Dictionary with the accessory's type, image URL, and alternate text.
        """
        return {
            "type": "image",
            "image_url": self.image_url,
            "alt_text": self.alt_text,
        }
