from typing import TYPE_CHECKING
import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from libreupc.models.common import Base

if TYPE_CHECKING:
    from .product import Product


class Answer(Base):
    content: Mapped[str] = mapped_column(String(1000))

    question_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("question.id"))
    question: Mapped[Question] = relationship("Question", back_populates="answers")

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship("User")
