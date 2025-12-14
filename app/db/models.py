from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String(64), index=True, nullable=False)
    channel = Column(String(32), index=True, default="whatsapp", nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    messages = relationship("Message", back_populates="conversation")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    direction = Column(String(8), index=True, nullable=False)  # "in" / "out"
    text = Column(Text, default="", nullable=False)
    raw = Column(Text, default="", nullable=False)  # store JSON string for now
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    conversation = relationship("Conversation", back_populates="messages")
