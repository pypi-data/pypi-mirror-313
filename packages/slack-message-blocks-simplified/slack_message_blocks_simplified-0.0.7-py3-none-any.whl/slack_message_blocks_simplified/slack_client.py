from io import IOBase
from typing import Any
from dataclasses import dataclass

import slack_sdk

@dataclass
class SlackClient:
    """
    A client for interacting with Slack's API, allowing posting of messages and uploading of files.

    Attributes:
        bot_token (str): The token used for authenticating the bot with Slack's API.

    Methods:
        _client(): Internal method to initialize and return a Slack WebClient instance.
        post_message_block(channel_id: str, blocks: Any | None, text: str = ""): Posts a message with optional blocks to a specific Slack channel.
        upload(file: str | bytes | IOBase | None, filename: str | None): Uploads a file to Slack, optionally with a specified filename.
    """

    bot_token: str

    def _client(self):
        """
        Initializes and returns a Slack WebClient instance using the provided bot token.

        Returns:
            slack_sdk.WebClient: A Slack WebClient instance authenticated with the bot token.
        """
        return slack_sdk.WebClient(self.bot_token)

    def post_message_block(self, channel_id: str, blocks: Any | None, text: str = ""):
        """
        Posts a message to a specified Slack channel with optional formatting blocks.

        Args:
            channel_id (str): The ID of the Slack channel where the message will be posted.
            blocks (Any | None): A structured block of formatting options to include in the message.
            text (str, optional): The plain text content of the message. Defaults to an empty string.

        Notes:
            The method sends a message to the specified Slack channel. If `blocks` are provided, 
          they define the formatting and structure of the message.
        """
        self._client().chat_postMessage(channel=channel_id, text=text, blocks=blocks)  # type: ignore

    def upload(self, file: str | bytes | IOBase | None, filename: str | None):
        """
        Uploads a file to Slack, optionally specifying the filename.

        Args:
            file (str | bytes | IOBase | None): The file to upload. It can be a path, bytes, or an IO stream.
            filename (str | None): The name to use for the file in Slack. If None, Slack determines the name.

        Returns:
            dict: The response from Slack's API after the file upload.

        Notes:
            The method uploads a file to Slack using the files_upload_v2 API. It supports different types of file inputs.
        """
        return self._client().files_upload_v2(file=file, filename=filename)  # type: ignore
