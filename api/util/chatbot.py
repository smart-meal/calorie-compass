from typing import List, Dict, Optional

from openai import OpenAI

client = OpenAI()

from api import config
from api.chat.model import Message
from api.user.service import get_user_by_id  # Import the required function to get user profile



class Chat:
    def __init__(
            self,
            api_key: str,
            max_tokens: int = 300,
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
        new_message = {"role": role, "content": message}
        self.messages.append(new_message)
        response = client.chat.completions.create(
        model=self.model,
        messages=self.messages,
        max_tokens=self.max_tokens)

        resp = response.choices[0].message
        resp_message = resp.content
        resp_role = resp.role
        self.messages.append(
            {"role": resp_role, "content": resp_message}
        )
        return resp_message

    def get_messages(self):
        return self.messages


def get_chat_from_messages(previous_messages: List[Message], api_key: str = config.OPENAI_API_KEY):
    converted_messages = [
        {"content": m.text, "role": m.type.value} for m in previous_messages
    ]
    return Chat(previous_messages=converted_messages, api_key=api_key)
