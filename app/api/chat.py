from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.services.llm_service import chat_with_llm
from app.db.session import SessionLocal
from app.db.models import Message as MessageModel
from app.repositories.message_repository import save_message, get_messages_by_conversation
from app.repositories.conversation_repository import get_conversation, update_conversation_title


from app.schemas.chat import ChatMessage
from app.agent.agent_runtime import run_agent

router = APIRouter(prefix="/api", tags=["chat"])

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    conversation_id: int
    message: str
    model: str

@router.post("/chat")
def chat(request: ChatRequest):

    def stream_and_save():

        assistant_reply=""
        db = SessionLocal()
        
        try:
            history_messages = get_messages_by_conversation(db, request.conversation_id)

            save_message(
                db=db,
                conversation_id=request.conversation_id,
                role="user",
                content=request.message
            )

            conversation = get_conversation(db, request.conversation_id)
            if conversation and conversation.title == "新会话":
                update_conversation_title(db, request.conversation_id, request.message.strip()[:20])

            messages_for_llm = []
            for message in history_messages:
                messages_for_llm.append(
                    ChatMessage(
                        role=message.role,
                        content=message.content
                    )
                )

            messages_for_llm.append(
                    ChatMessage(
                        role="user",
                        content=request.message
                    )
            )

            for chunk in run_agent(messages_for_llm, request.model):
                assistant_reply += chunk
                yield chunk

            save_message(
                db=db,
                conversation_id=request.conversation_id,
                role="assistant",
                content=assistant_reply
            )
        
        finally:
            db.close()

    return StreamingResponse(stream_and_save(), media_type="text/plain")