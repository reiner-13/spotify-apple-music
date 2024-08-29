from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    __tablename__ = "user_table"
    id : so.Mapped[int] = so.mapped_column(primary_key=True)
    username : so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    first_name : so.Mapped[str] = so.mapped_column(sa.String(64))
    last_name : so.Mapped[str] = so.mapped_column(sa.String(64))
    password_hash : so.Mapped[Optional[str]] = so.mapped_column(sa.String(265))

    playlists : so.Mapped[list["UserPlaylist"]] = so.relationship(
        back_populates="user"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"
    
class Playlist(db.Model):
    __tablename__ = "playlist_table"
    id : so.Mapped[int] = so.mapped_column(primary_key=True)
    name : so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    spotify_id : so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    apple_music_id : so.Mapped[str] = so.mapped_column(sa.String(64), index=True)

    users : so.Mapped[list["UserPlaylist"]] = so.relationship(
        back_populates="playlist"
    )

    def __repr__(self):
        return f"<Playlist {self.name}>"

class UserPlaylist(db.Model):
    __tablename__ = "userplaylist_table"
    user_id : so.Mapped[int] = so.mapped_column(sa.ForeignKey("user_table.id"), primary_key=True)
    playlist_id : so.Mapped[int] = so.mapped_column(sa.ForeignKey("playlist_table.id"), primary_key=True)

    user : so.Mapped["User"] = so.relationship(back_populates="playlists")
    playlist : so.Mapped["Playlist"] = so.relationship(back_populates="users")

    def __repr__(self):
        return f"<UserPlaylist U:{self.user_id}, P:{self.playlist_id}>"

