from dataclasses import dataclass, field
from typing import Any

from .slack_client import SlackClient
from .slack_base_elements import BaseBlock, ContextSubBlock, RichTextList, RichTextSection, SectionTextElement, SectionAccessory

@dataclass
class DividerBlock(BaseBlock):
    """
    Divider block class.

    Represents a Slack divider block, used to create visual separators.
    """

    def value(self) -> dict[str, Any]:
        """
        Retrieves the structure of the divider block.

        Returns:
            dict[str, Any]: A dictionary with the type set to "divider".
        """
        return {
			"type": "divider"
		}
    
@dataclass
class HeaderBlock(BaseBlock):
    """
    Header block class.

    Represents a Slack header block, used to display a title.

    Attributes:
        title (str): The text of the header title.
    """
    title: str|None = None

    def reset_value(self) -> None:
        """
        Resets the header title to None.
        """
        self.title = None
    
    def append(self, *, title: str) -> None:
        """
        Adds text to the existing header title.

        Args:
            title (str): Text to append to the current title.
        """
        self.title = f"{self.title} {title}" if self.title is not None else title

    def value(self) -> dict[str, Any]:
        """
        Retrieves the structure of the header block.

        Returns:
            dict[str, Any]: A dictionary containing the header type and its text.
        """
        return {
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": self.title,
				"emoji": True
			}
		}

@dataclass
class ContextBlock(BaseBlock):
    """
    Context block class.

    Represents a Slack context block, used to display context or additional information.

    Attributes:
        elements (list[ContextSubBlock]): A list of elements in the context block.
    """
    elements: list[ContextSubBlock] = field(default_factory=list)

    def reset_value(self) -> None:
        """
        Clears all elements from the context block.
        """
        self.elements = []

    def add_context_sub_blocks(self, *, context_sub_block: list[ContextSubBlock]) -> None:
        """
        Adds sub-blocks to the context block.

        Args:
            context_sub_block (list[ContextSubBlock]): The sub-blocks to add.
        """
        self.elements.extend(context_sub_block)

    
    def value(self) -> dict[str, Any]:
        """
        Retrieves the structure of the context block.

        Returns:
            dict[str, Any]: A dictionary containing the context type and its elements.
        """
        return {
            "type": "context",
            "elements": [
                element.value() for element in self.elements
            ]
        }

@dataclass
class SectionBlock(BaseBlock):
    """
    Section block class.

    Represents a Slack section block, used to display text and optional accessories.

    Attributes:
        element (SectionTextElement | None): The main content of the section.
        accessory (SectionAccessory | None): An optional accessory for the section.
    """
    element: SectionTextElement|None = None
    accessory: SectionAccessory|None = None

    def reset_value(self) -> None:
        """
        Resets the section content and accessory to None.
        """
        self.element = None
        self.accessory = None

    def change_text_element(self, *, element: SectionTextElement) -> None:
        """
        Updates the content of the section.

        Args:
            element (SectionTextElement): The new text element for the section.
        """
        self.element = element

    def change_text_accessory(self, *, accessory: SectionAccessory) -> None:
        """
        Updates the accessory of the section.

        Args:
            accessory (SectionAccessory): The new accessory for the section.
        """
        self.accessory = accessory
    
    def value(self) -> dict[str, Any]:
        """
        Retrieves the structure of the section block.

        Returns:
            dict[str, Any]: A dictionary containing the section type, text, and optional accessory.

        Raises:
            ValueError: If the element attribute is None.
        """
        if self.element is None:
            raise ValueError("element attribute must not be None")

        return {
            "type": "section",
            "text": self.element.value(),
            "accessory": self.accessory.value()
            } if self.accessory is not None else {
                "type": "section",
                "text": self.element.value(),
            }

@dataclass
class ImageBlock(BaseBlock):
    """
    Image block class.

    Represents a Slack image block, used to display an image with optional title and alternative text.

    Attributes:
        image_url (str | None): The URL of the image.
        title (str | None): The title of the image block (optional).
        alt_text (str | None): The alternative text for the image.
        is_markdown (bool): Indicates whether the title is in Markdown format.
    """
    image_url: str|None = None
    title: str | None = None
    alt_text: str|None = None
    is_markdown: bool = False

    def reset_value(self) -> None:
        """
        Resets all properties of the image block to their default state.
        """
        self.image_url = None
        self.title = None
        self.alt_text = None
        self.is_markdown = False

    def change_values(self, *, image_url: str|None = None, title: str | None = None, alt_text: str|None = None, is_markdown: bool|None = None) -> None:
        """
        Updates the properties of the image block.

        Args:
            image_url (str | None): The URL of the image.
            title (str | None): The title of the image block.
            alt_text (str | None): The alternative text for the image.
            is_markdown (bool | None): Whether the title is in Markdown format.
        """
        self.image_url = image_url if image_url is not None else self.image_url
        self.title = title if title is not None else self.title
        self.alt_text = alt_text if alt_text is not None else self.alt_text
        self.is_markdown = is_markdown if is_markdown is not None else self.is_markdown

    def value(self) -> dict[str, Any]:
        """
        Retrieves the structure of the image block.

        Returns:
            dict[str, Any]: A dictionary containing the image block details.

        Raises:
            ValueError: If the image_url attribute is None.
        """
        if self.image_url is None:
            raise ValueError("image_url attribute cannot be None.")
        
        result: dict[str, Any]
        
        if self.title is not None:
            result = {
                "type": "image",
                "title": {
                    "type": "mrkdwn" if self.is_markdown else "plain_text",
                    "text": self.title
                },
                "image_url": self.image_url,
            }
        else:
            result =  {
                "type": "image",
                "image_url": self.image_url,
            }
        if self.alt_text is not None:
            result["alt_text"] = self.alt_text
        return result

@dataclass
class RichTextBlock(BaseBlock):
    """
    Rich text block class.

    Represents a Slack rich text block, used for more complex formatting and layout.

    Attributes:
        sections (list[RichTextList | RichTextSection]): A list of rich text sections and lists.
    """
    sections: list[RichTextList|RichTextSection] = field(default_factory=list)

    def reset_value(self) -> None:
        """
        Clears all sections from the rich text block.
        """
        self.sections = []
    
    def add_sections_and_lists(self, *, elements: list[RichTextList|RichTextSection]):
        """
        Adds sections and lists to the rich text block.

        Args:
            elements (list[RichTextList | RichTextSection]): A list of rich text sections and lists to add.
        """
        self.sections.extend(elements)

    def value(self) -> dict[str, Any]:
        """
        Retrieves the structure of the rich text block.

        Returns:
            dict[str, Any]: A dictionary containing the rich text block details.
        """
        return {
            "type": "rich_text",
            "elements": [
                element.value() for element in self.sections
            ]
        }

@dataclass
class SlackBlock:
    """
    Slack block class.

    Represents a message block to be sent via Slack, which includes text, rich blocks, and files.

    Attributes:
        client (SlackClient): The Slack client used for API communication.
        text (str): The main text content of the message.
        blocks (list[dict[str, Any]]): A list of structured blocks for the message.
        files (list[str]): A list of file URLs to be attached to the message.
    """
    client: SlackClient
    text: str = ""
    blocks: list[BaseBlock] = field(default_factory=list)
    files: list[str] = field(default_factory=list)

    def add_blocks(self, blocks: list[BaseBlock]) -> None:
        """
        Adds multiple structured blocks to the Slack message.

        Args:
            blocks (list[BaseBlock]): A list of block objects to add.
        """
        self.blocks.extend(blocks)

    def upload_file(self, *, file_path: str, filename: str | None = None) -> None:
        """
        Uploads a file to Slack and stores its permalink.

        Args:
            file_path (str): The local path of the file to upload.
            filename (str | None): An optional custom filename for the uploaded file.
        """
        upload = self.client.upload(file= file_path, filename= filename) # type: ignore
        self.files.append(f"<{upload['file']['permalink']}>")

    def add_message(self, *, new_text: str) -> None:
        """
        Appends additional text to the current message.

        Args:
            new_text (str): The text to append to the existing message.
        """
        self.text = f"{self.text}{new_text}"
    
    def change_message(self, *, new_text: str) -> None:
        """
        Replaces the existing message text with new content.

        Args:
            new_text (str): The new text for the message.
        """
        self.text = new_text

    def reset_message(self) -> None:
        """
        Clears the message text.
        """
        self.text = ""

    def post_message_block(self, *, channel_id: str) -> None:
        """
        Sends the message block to a specified Slack channel.

        Args:
            channel_id (str): The ID of the Slack channel where the message will be posted.
        """
        blocks_repr: list[dict[str, Any]] = []
        for block in self.blocks:
            blocks_repr.append(
                block.value() 
            )
        concatenated_files: str = '\n'.join(self.files)
        self.client.post_message_block(
            channel_id=channel_id,
            blocks=blocks_repr,
            text=f"{self.text} \n {concatenated_files}"
        )


