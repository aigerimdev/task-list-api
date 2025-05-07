from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from typing import Optional
from sqlalchemy import DateTime
from datetime import datetime

class Task(db.Model): # specificheskii model dlya sql
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    # completed_at: Mapped[datetime] = mapped_column(nullable=True)
    # completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    
    @classmethod
    def from_dict(cls, task_data): # task_data = dictionary data
        return cls(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=task_data.get("completed_at")  # will be None if null
        )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            # "is_complete": self.completed_at is not None
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }