from openai import OpenAI
import json
import time
import uuid

client = OpenAI(
    base_url="http://0.0.0.0:8080/v1",
    api_key="dummy"
)

async def generate_stream_response(request_data):
    response = client.chat.completions.create(
        model="luna-v1",
        messages=[
            {"role": "system", "content": request_data["system_prompt"]},
            {"role": "user", "content": request_data["prompt"]},
        ],
        stream=True,
    )

    chat_id = f"chatcmpl-{uuid.uuid4().hex}"
    created = int(time.time())

    # Initial role chunk
    yield (
        "data: "
        + json.dumps(
            {
                "id": chat_id,
                "object": "chat.completion.chunk",
                "created": created,
                "model": "bitnet",
                "choices": [
                    {
                        "index": 0,
                        "delta": {"role": "assistant"},
                        "finish_reason": None,
                    }
                ],
            }
        )
        + "\n\n"
    )

    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
            yield (
                "data: "
                + json.dumps(
                    {
                        "id": chat_id,
                        "object": "chat.completion.chunk",
                        "created": created,
                        "model": "bitnet",
                        "choices": [
                            {
                                "index": 0,
                                "delta": {"content": content},
                                "finish_reason": None,
                            }
                        ],
                    }
                )
                + "\n\n"
            )

    # Final chunk
    yield (
        "data: "
        + json.dumps(
            {
                "id": chat_id,
                "object": "chat.completion.chunk",
                "created": created,
                "model": "bitnet",
                "choices": [
                    {
                        "index": 0,
                        "delta": {},
                        "finish_reason": "stop",
                    }
                ],
            }
        )
        + "\n\n"
    )

    yield "data: [DONE]\n\n"

def generate_response(request_data):
    response = client.chat.completions.create(
        model="luna-v1",
        messages=[
            {"role": "system", "content": request_data['system_prompt']},
            {"role": "user", "content": request_data['prompt']}
        ],
        stream=False,
    )
    print(response.choices[0].message.content)
    return {"response": response, "type":"complete"}