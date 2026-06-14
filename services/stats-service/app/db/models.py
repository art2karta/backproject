from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from app.db.database import Base


class UserEvent(Base):
    __tablename__ = "user_events"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, nullable=False)

    email = Column(String, nullable=False)

    event_type = Column(String, nullable=False)

    created_at = Column(DateTime, nullable=False)