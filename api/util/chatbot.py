from typing import List, Dict, Optional
import openai
from api.util.log import logger


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
            return resp_message
        
        except openai.error.OpenAIError as e:
            # First remvoing the user message as it could be one of the reasons the error was caused.
            #  So it is safe to remove that from conversation history.
            self.messages.pop()
            error_resp_message = "There was an error, please try again"
            if isinstance(e, openai.error.AuthenticationError):
                logger.error("OpenAI API request was not authorized: %s",e)

            elif isinstance(e, openai.error.PermissionError):
                logger.errort("OpenAI API request was not permitted: %s",e)

            elif isinstance(e, openai.error.RateLimitError):
                logger.error("OpenAI API request exceeded rate limit: %s",e)
                error_resp_message = "You have sent too many requests or your message is too long."

            elif isinstance(e, openai.error.InvalidRequestError):
                logger.error("OpenAI API request is invalid: %s",e)
                error_resp_message = "The request is invalid please try again with a different request"

            elif isinstance(e, openai.error.Timeout):
                logger.error("OpenAI API request Timed out: %s",e)
                error_resp_message = "Your request timed out, please check your connection or try again after some time"

            elif isinstance(e, openai.error.ServiceUnavailableError):
                logger.error("OpenAI API request service is unavailable: %s",e)
                error_resp_message = "The service is currently unavailable please try again after some time."
            else:
                logger.error("OpenAI API error: %s",e)
            
            # No need to append to the conversation history if there's any error, the user will just get 
            # the error message and can send the request again based on the error.
            
            return error_resp_message
        

    def get_messages(self):
        return self.messages
