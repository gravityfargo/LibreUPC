from typing import TYPE_CHECKING
import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from libreupc.models.common import Base

if TYPE_CHECKING:
    from .user import Product


class Product(Base):
    __abstract__ = True

    source_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship("User")
