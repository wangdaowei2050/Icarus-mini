from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.services.llm_service import chat_with_llm
from app.db.session import SessionLocal
from app.db.models import Message as MessageModel

router = APIRouter(prefix="/api", tags=["chat"])

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]
    model: str

@router.post("/chat")
def chat(request: ChatRequest):

    latest_user_message = request.messages[-1]

    db = SessionLocal()

    try:
        user_message = MessageModel(
            role=latest_user_message.role, 
            content=latest_user_message.content
            )
        db.add(user_message)
        db.commit()
    finally:
        db.close()

    def stream_and_save():
        assistant_reply=""

        for chunk in chat_with_llm(request.messages, request.model):
            assistant_reply += chunk
            yield chunk
        db = SessionLocal()
        try:
            assistant_message = MessageModel(
                role="assistant",
                content=assistant_reply
            )
            db.add(assistant_message)
            db.commit()
        finally:
            db.close()

    return StreamingResponse(stream_and_save(), media_type="text/plain")