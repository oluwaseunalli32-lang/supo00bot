from sqlalchemy import BigInteger, String, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
import enum
from database import Base

class ResponseMode(enum.Enum):
    AUTO = "auto"
    MANUAL = "manual"
    AI = "ai"

class Customer(Base):
    __tablename__ = "customers"
    
    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(255))
    current_mode: Mapped[ResponseMode] = mapped_column(SQLEnum(ResponseMode), default=ResponseMode.AI)

class ConversationLog(Base):
    __tablename__ = "conversation_logs"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("customers.tg_id"))
    role: Mapped[str] = mapped_column(String(50))  # 'user', 'assistant', 'admin'
    content: Mapped[str] = mapped_column(Text)
