from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db
from typing import Optional
from sqlalchemy import DateTime
from datetime import datetime

class Task(db.Model): # specificheskii model dlya sql
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")
    
    @classmethod
    def from_dict(cls, task_data): # task_data = dictionary data
        return cls(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=task_data.get("completed_at")  # will be None if null
        )

    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "title": self.title,
    #         "description": self.description,
    #         "is_complete": self.completed_at is not None
    #         # "completed_at": self.completed_at.isoformat() if self.completed_at else None
    #     }
    def to_dict(self, include_goal_id=False):
        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }
        if include_goal_id:
            task_dict["goal_id"] = self.goal_id
        return task_dict