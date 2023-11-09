from api import create_app
from api.util.chatbot import set_api_key 
import os

set_api_key(os.getenv("OPENAI_API_KEY"))

app = create_app()
app.run()
