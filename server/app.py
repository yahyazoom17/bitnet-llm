from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from schemas import ChatRequestSchema
from utils import generate_response, generate_stream_response

app = FastAPI(title="Luna API v1")

async def stream_llm_response(tokens):
    for token in tokens:
        yield token

@app.post("/api/v1/chat/completions")
async def generate_response_from_llm(request_data: ChatRequestSchema):
    data = request_data.dict()
    if data['stream']:
        return StreamingResponse(
            generate_stream_response(data),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
    else:
        result = generate_response(data)
        return {"status":200, "message":"Response generated successfully!", "data":result['response']}