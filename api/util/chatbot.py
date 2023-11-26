from typing import List, Dict, Optional

import openai


class Chat:
    """
    A Chat class to interact with OpenAI's GPT model.


    This class handles sending messages to the GPT model and receiving responses.

    Attributes:
        messages (List[Dict]): A list of previous messages in the chat.
        max_tokens (int): Maximum number of tokens to generate for each response.
        api_key (str): API key for accessing OpenAI's GPT model.
        model (str): The name of the GPT model to use.
    """

    def __init__(
            self,
            api_key: str,
            max_tokens: int = 100,
            previous_messages: Optional[List[Dict]] = None,
            model: str = "gpt-3.5-turbo",
    ):
        if previous_messages is None:
            previous_messages = []
        self.messages = previous_messages
        self.max_tokens = max_tokens
        self.api_key = api_key
        self.model = model

    def send_message(self, message: str, role: str = "user") -> str:
        """
        Sends a message to the GPT model and receives a response.

        Args:
            message (str): The message to send.
            role (str, optional): The role of the message sender (e.g., "user"). Defaults to "user".
        """
        new_message = {"role": role, "content": message}
        self.messages.append(new_message)
        response = openai.ChatCompletion.create(
            api_key=self.api_key,
            model=self.model,
            messages=self.messages,
            max_tokens=self.max_tokens,
        )

        resp = response.choices[0].message
        resp_message = resp.content
        resp_role = resp.role
        self.messages.append(
            {"role": resp_role, "content": resp_message}
        )
        return resp_message

    def get_messages(self):
        """
        Retrieves all messages from the chat history.

        Returns:
            List[Dict]: A list of messages in the chat history.
        """
        return self.messages
