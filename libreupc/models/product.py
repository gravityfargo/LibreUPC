import uuid

# from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# from typing import TYPE_CHECKING


# if TYPE_CHECKING:
#     from .user import Product


class Product(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    # source_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    # user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    # user: Mapped[User] = relationship("User")
