from openai import OpenAI

client = OpenAI(
    api_key = "sk-t4Mv9tJa0ftMCcKqKMAlqJmq3x5Da83Pk4U4Jq2M98C57GZG",
    base_url = "https://api.pro365.top/v1",
)

completion = client.chat.completions.create(
    model= "gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, please say hello"}
    ]
)

print(completion)