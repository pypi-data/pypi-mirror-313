

- # Slack Message Blocks Simplified Package
- ## Overview
  
  **slack_message_blocks_simplified** is a Python package that simplifies the process of creating and sending rich, structured messages to Slack channels using blocks. The package provides various classes to help you build and manage these blocks and interact with Slack's API efficiently.
- ## Installation
  ```
  pip install slack-message-blocks-simplified
  ```
- ### Prerequisites
- **Python Version**: Ensure you are using Python 3.12 or higher.
- **Dependencies**:
	- `slack_sdk` (version 3.31.0)
	- `dataclasses` (built-in for Python 3.7+)
- ## Usage
- ### Importing the Package
  
  ```
  from slack_message_blocks_simplified import  DividerBlock, HeaderBlock, ContextBlock, SectionBlock, SectionTextElement, SectionTextType, SectionAccessory, ImageBlock, RichTextBlock, SlackBlock, SlackClient
  ```
- # Initialize the Slack client and Slack Block
  ```
  slack_client = SlackClient(bot_token="xoxb-your-slack-token")
  slack_message = SlackBlock(client=slack_client)
  ```
- # Create a message
  ```
  header = HeaderBlock(title="Welcome to the Channel!")
  divider = DividerBlock()
  section = SectionBlock()
  section.change_text_element(
      element = SectionTextElement(
          SectionTextType.mrkdwn,
          "This is a *section* with some _rich text_."
      )
  )
  section.change_text_accessory(
      accessory = SectionAccessory(
          image_url= "https://example.com/image.png",
          alt_text= "Example Image"
      )
  )
  ```
- # Upload file
  ```
  slack_message.upload_file("C:/path/to/file.extension", "file.extension")
  ```
- # Post the message to a channel
  ```
  slack_message.add_blocks([header, divider, section])
  slack_message.post_message_block(channel_id="C1234567890")
  ```
- # Final code
  ```
  from slack_message_blocks_simplified import DividerBlock, HeaderBlock, ContextBlock, SectionBlock, SectionTextElement, SectionTextType, SectionAccessory, ImageBlock, RichTextBlock, SlackBlock, SlackClient
 
  slack_client = SlackClient(bot_token="xoxb-your-slack-token")
  slack_message = SlackBlock(client=slack_client)
  
  header = HeaderBlock(title="Welcome to the Channel!")
  divider = DividerBlock()
  section = SectionBlock()
  section.change_text_element(
      element = SectionTextElement(
          SectionTextType.mrkdwn,
          "This is a *section* with some _rich text_."
      )
  )
  section.change_text_accessory(
      accessory = SectionAccessory(
          image_url= "https://example.com/image.png",
          alt_text= "Example Image"
      )
  )
  
  slack_message.upload_file("C:/path/to/file.extension", "file.extension")
  
  slack_message.add_blocks([header, divider, section])
  slack_message.post_message_block(channel_id="C1234567890")
  ```




# Classes and Methods

## 1. DividerBlock
Represents a Slack divider block, used to create visual separators.

### Methods:

- **`value()`**:

  **Description**: Retrieves the structure of the divider block.  
  **Returns**:  
  - `dict[str, Any]`: A dictionary with the type set to "divider".

## 2. HeaderBlock
Represents a Slack header block, used to display a title.

### Attributes:

- `title (str | None)`: The text of the header title.

### Methods:

- **`reset_value()`**:

  **Description**: Resets the header title to `None`.  
  **Args**: None.

- **`append(title: str)`**:

  **Description**: Appends text to the existing header title.  
  **Args**:  
  - `title (str)`: Text to append to the current title.

- **`value()`**:

  **Description**: Retrieves the structure of the header block.  
  **Returns**:  
  - `dict[str, Any]`: A dictionary containing the header type and its text.

## 3. ContextBlock
Represents a Slack context block, used to display context or additional information.

### Attributes:

- `elements (list[ContextSubBlock])`: A list of elements in the context block.

### Methods:

- **`reset_value()`**:

  **Description**: Clears all elements from the context block.  
  **Args**: None.

- **`add_context_sub_blocks(context_sub_block: list[ContextSubBlock])`**:

  **Description**: Adds sub-blocks to the context block.  
  **Args**:  
  - `context_sub_block (list[ContextSubBlock])`: The sub-blocks to add.

- **`value()`**:

  **Description**: Retrieves the structure of the context block.  
  **Returns**:  
  - `dict[str, Any]`: A dictionary containing the context type and its elements.

## 4. SectionBlock
Represents a Slack section block, used to display text and optional accessories.

### Attributes:

- `element (SectionTextElement | None)`: The main content of the section.
- `accessory (SectionAccessory | None)`: An optional accessory for the section.

### Methods:

- **`reset_value()`**:

  **Description**: Resets the section content and accessory to `None`.  
  **Args**: None.

- **`change_text_element(element: SectionTextElement)`**:

  **Description**: Updates the content of the section.  
  **Args**:  
  - `element (SectionTextElement)`: The new text element for the section.

- **`change_text_accessory(accessory: SectionAccessory)`**:

  **Description**: Updates the accessory of the section.  
  **Args**:  
  - `accessory (SectionAccessory)`: The new accessory for the section.

- **`value()`**:

  **Description**: Retrieves the structure of the section block.  
  **Returns**:  
  - `dict[str, Any]`: A dictionary containing the section type, text, and optional accessory.  
  **Raises**:  
  - `ValueError`: If the `element` attribute is `None`.

## 5. ImageBlock
Represents a Slack image block, used to display an image with optional title and alternative text.

### Attributes:

- `image_url (str | None)`: The URL of the image.
- `title (str | None)`: The title of the image block (optional).
- `alt_text (str | None)`: The alternative text for the image.
- `is_markdown (bool)`: Indicates whether the title is in Markdown format.

### Methods:

- **`reset_value()`**:

  **Description**: Resets all properties of the image block to their default state.  
  **Args**: None.

- **`change_values(image_url: str | None = None, title: str | None = None, alt_text: str | None = None, is_markdown: bool | None = None)`**:

  **Description**: Updates the properties of the image block.  
  **Args**:  
  - `image_url (str | None)`: The new URL of the image.  
  - `title (str | None)`: The new title for the image block.  
  - `alt_text (str | None)`: The new alternative text for the image.  
  - `is_markdown (bool | None)`: Whether the title should be in Markdown format.

- **`value()`**:

  **Description**: Retrieves the structure of the image block.  
  **Returns**:  
  - `dict[str, Any]`: A dictionary containing the image block details.  
  **Raises**:  
  - `ValueError`: If the `image_url` attribute is `None`.

## 6. RichTextBlock
Represents a Slack rich text block, used for more complex formatting and layout.

### Attributes:

- `sections (list[RichTextList | RichTextSection])`: A list of rich text sections and lists.

### Methods:

- **`reset_value()`**:

  **Description**: Clears all sections from the rich text block.  
  **Args**: None.

- **`add_sections_and_lists(elements: list[RichTextList | RichTextSection])`**:

  **Description**: Adds sections and lists to the rich text block.  
  **Args**:  
  - `elements (list[RichTextList | RichTextSection])`: A list of rich text sections and lists to add.

- **`value()`**:

  **Description**: Retrieves the structure of the rich text block.  
  **Returns**:  
  - `dict[str, Any]`: A dictionary containing the rich text block details.

## 7. SlackBlock
Represents a message block to be sent via Slack, which includes text, rich blocks, and files.

### Attributes:

- `client (SlackClient)`: The Slack client used for API communication.
- `text (str)`: The main text content of the message.
- `blocks (list[dict[str, Any]])`: A list of structured blocks for the message.
- `files (list[str])`: A list of file URLs to be attached to the message.

### Methods:

- **`add_blocks(blocks: list[BaseBlock])`**:

  **Description**: Adds multiple structured blocks to the Slack message.  
  **Args**:  
  - `blocks (list[BaseBlock])`: A list of block objects to add.

- **`upload_file(file_path: str, filename: str | None = None)`**:

  **Description**: Uploads a file to Slack and stores its permalink.  
  **Args**:  
  - `file_path (str)`: The local path of the file to upload.  
  - `filename (str | None)`: An optional custom filename for the uploaded file.

- **`add_message(new_text: str)`**:

  **Description**: Appends additional text to the current message.  
  **Args**:  
  - `new_text (str)`: The text to append to the existing message.

- **`change_message(new_text: str)`**:

  **Description**: Replaces the existing message text with new content.  
  **Args**:  
  - `new_text (str)`: The new text that will replace the current message content.

- **`reset_message()`**:

  **Description**: Clears the message text.  
  **Args**: None.

- **`post_message_block(channel_id: str)`**:

  **Description**: Sends the message block to a specified Slack channel.  
  **Args**:  
  - `channel_id (str)`: The ID of the Slack channel where the message will be posted.

# Additional Classes

## 1. BaseBlock
Base class for Slack blocks, providing a template for implementing different types of Slack blocks.

### Methods:

- **`reset_value()`**:

  **Description**: Resets the value of the block to its default state.  
  **Raises**:  
  - `NotImplementedError`: If the method is not implemented by subclasses.

- **`value()`**:

  **Description**: Retrieves the dictionary representation of the block.  
  **Returns**:  
  - `dict[str, Any]`: A dictionary representation of the block.  
  **Raises**:  
  - `NotImplementedError`: If the method is not implemented by subclasses.

## 2. ContextSubBlock
Represents a context sub-block for Slack messages.

### Attributes:

- `type (ContextSubBlockType)`: The type of the context block (e.g., text or image).  
- `text (str | None)`: Text content for the block, if applicable.  
- `image_url (str | None)`: Image URL for the block, if applicable.  
- `alt_text (str | None)`: Alternate text for the image, if applicable.

### Methods:

- **`value()`**:

  **Description**: Retrieves the dictionary representation of the context sub-block.  
  **Returns**:  
  - `dict[str, Any]`: A dictionary with the context block's type and elements.  
  **Raises**:  
  - `ValueError`: If required attributes for the block type are missing.

## 3. RichTextElement
Represents a rich text element within a Slack block.

### Attributes:

- `type (RichTextElementType)`: The type of the rich text element (e.g., text, emoji, link).  
- `text (str | None)`: Text content of the element, if applicable.  
- `styles (list[RichTextElementStyle] | None)`: A list of styles applied to the element, if applicable.  
- `name (str | None)`: Name for emoji elements, if applicable.  
- `url (str | None)`: URL for link elements, if applicable.

### Methods:

- **`value()`**:

  **Description**: Retrieves the dictionary representation of the rich text element.  
  **Returns**:  
  - `dict[str, Any]`: A dictionary with the element's type and attributes.  
  **Raises**:  
  - `ValueError`: If required attributes for the element type are missing.

## 4. RichTextSection
Represents a rich text section containing multiple rich text elements.

### Attributes:

- `type (RichTextSectionType)`: The type of the rich text section.  
- `elements (list[RichTextElement])`: A list of rich text elements in this section.

### Methods:

- **`add_rich_text_elements(rich_text_element: list[RichTextElement])`**:

  **Description**: Adds rich text elements to the section.  
  **Args**:  
  - `rich_text_element (list[RichTextElement])`: A list of rich text elements to add.

- **`value()`**:

  **Description**: Retrieves the dictionary representation of the rich text section.  
  **Returns**:  
  - `dict[str, Any]`: A dictionary with the section's type and elements.

## 5. RichTextList
Represents a list of rich text sections in a Slack block.

### Attributes:

- `type (RichTextListType)`: The style of the list (e.g., numbered, bulleted).  
- `elements (list[RichTextSection])`: A list of rich text sections in this list.

### Methods:

- **`add_rich_text_sections(rich_text_sections: list[RichTextSection])`**:

  **Description**: Adds rich text sections to the list.  
  **Args**:  
  - `rich_text_sections (list[RichTextSection])`: A list of rich text sections to add.  
  **Raises**:  
  - `ValueError`: If any section does not match the type required for the list.

- **`value()`**:

  **Description**: Retrieves the dictionary representation of the rich text list.  
  **Returns**:  
  - `dict[str, Any]`: A dictionary with the list's type, style, and elements.

## 6. SectionTextElement
Represents a text element within a section block.

### Attributes:

- `type (SectionTextType)`: The type of text (e.g., plain_text or mrkdwn).  
- `text (str)`: The content of the text.

### Methods:

- **`value()`**:

  **Description**: Retrieves the dictionary representation of the section text element.  
  **Returns**:  
  - `dict[str, Any]`: A dictionary with the text element's type and content.

## 7. SectionAccessory
Represents an accessory for a section block, such as an image.

### Attributes:

- `image_url (str)`: The URL of the image.  
- `alt_text (str)`: Alternate text for the image.

### Methods:

- **`value()`**:

  **Description**: Retrieves the dictionary representation of the section accessory.  
  **Returns**:  
  - `dict[str, Any]`: A dictionary with the accessory's type, image URL, and alternate text.


---

If you'd like to contribute to this project, please fork the repository and submit a pull request. All contributions are welcome!

## License

This project is licensed under the MIT License.