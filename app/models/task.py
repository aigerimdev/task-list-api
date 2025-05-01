from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from typing import Optional
from sqlalchemy import DateTime
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    def to_dict(self):
        return {
        "id": self.id,
        "title": self.title,
        "description": self.description,
        "completed_at": self.completed_at,
        "is_complete": self.completed_at is not None # # If completed_at has a value → is_complete = True , If it's None → is_complete = False
    }
    @classmethod
    def from_dict(cls, task_data):
        new_task = cls(title=task_data["title"],
                       description=task_data["description"],
                       completed_at=task_data.get("completed_at"))
        return new_task
        