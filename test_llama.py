from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="dummy"
)

stream = client.chat.completions.create(
    model="bitnet",
    messages=[
        {"role": "system", "content": "You are Luna, a helpful assistant created by Yahya at LunaLabs organization."},
        {"role": "user", "content": "Tell me about yourself"}
    ],
    stream=True,
)

full_text = ""

for chunk in stream:
    delta = chunk.choices[0].delta.content or ""
    print(delta, end="", flush=True)
    full_text += delta

print("\n\nFinal Response:", full_text)