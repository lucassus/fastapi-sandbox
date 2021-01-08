from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Todo:
    name: str
    id: Optional[int] = None
    completed_at: Optional[datetime] = None

    @property
    def is_completed(self) -> bool:
        return self.completed_at is not None
