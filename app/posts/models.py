from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, Boolean

from app import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    content = Column(Text, nullable=False)
    posted = Column(DateTime, default=datetime.utcnow)
    category = Column(
        Enum('news', 'publication', 'tech', 'other', name='post_category'),
        default='other',
        nullable=True
    )
    is_active = Column(Boolean, nullable=False, default=True)
    author = Column(String(20), default='Anonymous')

    def __repr__(self):
        return f"<Post id={self.id} title='{self.title}'>"