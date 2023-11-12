from typing import List, Dict, Optional

import openai


class Chat:
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
        new_message = {"role": role, "content": message}
        self.messages.append(new_message)
        try:
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
        except openai.error.OpenAIError as e:
            if isinstance(e, openai.error.AuthenticationError):
                print(f"OpenAI API request was not authorized: {e}")
            elif isinstance(e, openai.error.PermissionError):
                print(f"OpenAI API request was not permitted: {e}")
            elif isinstance(e, openai.error.RateLimitError):
                print(f"OpenAI API request exceeded rate limit: {e}")
            else:
                print(f"OpenAI API error: {e}")
            resp_role = "assistant"
            resp_message = None
            self.messages.append(
                {"role": resp_role, "content": resp_message}
            )
        return resp_message
    
    
