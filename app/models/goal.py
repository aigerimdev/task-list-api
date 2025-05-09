from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")
    
    @classmethod
    def from_dict(cls, goal_data):
        return cls(
            title=goal_data["title"]
        )
    
    def to_dict(self, include_tasks=False):
        goal_dict = {
            "id": self.id,
            "title": self.title
        }
        # # Add list of tasks only if requested
        if include_tasks:
            goal_dict["tasks"] = [task.to_dict(include_goal_id=True) for task in self.tasks]
        return goal_dict