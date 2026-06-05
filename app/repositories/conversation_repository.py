from sqlalchemy.orm import Session
from app.db.models import Conversation

def create_conversation(db: Session, title: str = "新会话"):
    conversation = Conversation(title=title)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

def get_conversations(db: Session):
    return db.query(Conversation).order_by(Conversation.created_at.desc()).all()

def get_conversation(db: Session, conversation_id: int):
    return db.query(Conversation).filter(Conversation.id == conversation_id).first()

def update_conversation_title(db: Session, conversation_id: int, title: str):
    conversation = get_conversation(db, conversation_id)
    if conversation is None:
        return None
    conversation.title = title
    db.commit()
    db.refresh(conversation)
    return conversation

def delete_conversation(db: Session, conversation_id: int):
    conversation = get_conversation(db, conversation_id)
    if conversation is None:
        return False
    db.delete(conversation)
    db.commit()
    return conversation



