from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from src.models.base import Base
from src.models.utils import generate_uuid


class SnippetsOrm(Base):
    __tablename__ = "snippets"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    title: Mapped[str] = mapped_column(String(100))
    code: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
