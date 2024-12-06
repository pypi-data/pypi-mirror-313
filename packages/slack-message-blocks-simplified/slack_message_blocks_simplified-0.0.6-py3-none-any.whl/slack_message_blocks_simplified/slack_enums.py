from enum import Enum

class ContextSubBlockType(Enum):
    image = "image"
    plain_text = "plain_text"
    mrkdwn = "mrkdwn"

class RichTextSectionType(Enum):
    rich_text_section = "rich_text_section"
    rich_text_preformatted = "rich_text_preformatted"
    rich_text_quote = "rich_text_quote"

class RichTextElementStyle(Enum):
    bold = "bold"
    italic = "italic"
    strike = "strike"

class RichTextElementType(Enum):
    text = "text"
    emoji = "emoji"
    link = "link"

class RichTextListType(Enum):
    bullet = "bullet"
    ordered = "ordered"

class SectionTextType(Enum):
    plain_text = "plain_text"
    mrkdwn = "mrkdwn"