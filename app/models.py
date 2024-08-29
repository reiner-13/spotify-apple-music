from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class User(db.Model):
    id : so.Mapped[int] = so.mapped_column(primary_key=True)
    username : so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    first_name : so.Mapped[str] = so.mapped_column(sa.String(64))
    last_name : so.Mapped[str] = so.mapped_column(sa.String(64))
    password_hash : so.Mapped[Optional[str]] = so.mapped_column(sa.String(265))

    def __repr__(self):
        return f"<User {self.username}>"