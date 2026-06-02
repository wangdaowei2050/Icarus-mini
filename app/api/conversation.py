from fastapi import APIRouter
from pydantic import BaseModel

from app.db.session import SessionLocal
from app.repositories.conversation_repository import create_conversation, get_conversations, get_conversation

from app.repositories.message_repository import get_messages_by_conversation

router = APIRouter(prefix="/api/conversations", tags=["conversations"])

class CreateConversationRequest(BaseModel):
    title: str = "新会话"

@router.post("")
def create(request: CreateConversationRequest):
    db = SessionLocal()

    try:
        conversation = create_conversation(db, title=request.title)

        return {
            "id": conversation.id,
            "title": conversation.title,
            "created_at": conversation.created_at
        }
    finally:
        db.close()

@router.get("")
def list_conversations():
    db = SessionLocal()
    try:
        conversations = get_conversations(db)
        return [
            {
                "id": conversation.id,
                "title": conversation.title,
                "created_at": conversation.created_at
            }
            for conversation in conversations
        ]
    finally:
        db.close()

@router.get("/{conversation_id}")
def get_conversation_detail(conversation_id: int):
    db = SessionLocal()
    try:
        conversation = get_conversation(db, conversation_id)

        if conversation is None:
            return {"error": "Conversation not found"}
        
        messages = get_messages_by_conversation(db, conversation_id)

        return {
            "id": conversation.id,
            "title": conversation.title,
            "created_at": conversation.created_at,
            "messages": [
                {
                    "id": message.id,
                    "role": message.role,
                    "content": message.content,
                    "created_at": message.created_at
                }
                for message in messages
            ]
        }
    finally:
        db.close()
    


    