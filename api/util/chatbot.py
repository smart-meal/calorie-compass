import openai


def chatgpt_api(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100
    )

    model_reply = response['choices'][0]['message']['content']
    return model_reply

def set_api_key(api_key):
    openai.api_key = api_key