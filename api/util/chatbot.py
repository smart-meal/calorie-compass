from typing import List, Dict, Optional
import openai

class ChatError(Exception):
    def __init__(self, message, status_code=None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


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

    def send_message(self, message: str, role: str = "user"):
        try:
            if not message.strip():  # Check if the message is empty or contains only whitespace
                raise ChatError("Empty message sent")

            new_message = {"role": role, "content": message}
            self.messages.append(new_message)

            valid_model = "gpt-3.5-turbo"
            if self.model not in valid_model:
                raise ChatError(f"Invalid model specified: {self.model}")

            response = openai.ChatCompletion.create(
                api_key=self.api_key,
                model=self.model,
                messages=self.messages,
                max_tokens=self.max_tokens,
            )

            if 'choices' in response and response.choices:
                resp = response.choices[0].message
                resp_message = resp['content']
                resp_role = resp['role']
                self.messages.append({"role": resp_role, "content": resp_message})
                return resp_message
            else:
                if 'error' in response:
                    error_message = response['error']['message']
                    status_code = response['error']['code']

                    raise ChatError(f"OpenAI Error: {error_message}, HTTP Status Code: {status_code}")

        except ChatError as e:
            return f"OpenAI Error: {e.message}, HTTP Status Code: {e.status_code}"

        except Exception as e:
            return f"An error occurred: {str(e)}"
