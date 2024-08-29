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

    playlists : so.WriteOnlyMapped["UserPlaylist"] = so.relationship(
        back_populates="users"
    )

    def __repr__(self):
        return f"<User {self.username}>"
    
class Playlist(db.Model):
    id : so.Mapped[int] = so.mapped_column(primary_key=True)
    name : so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    spotify_id : so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    apple_music_id : so.Mapped[str] = so.mapped_column(sa.String(64), index=True)

    users : so.WriteOnlyMapped["UserPlaylist"] = so.relationship(
        back_populates="playlists"
    )

    def __repr__(self):
        return f"<Playlist {self.name}>"

class UserPlaylist(db.Model):
    id : so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id : so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    playlist_id : so.Mapped[int] = so.mapped_column(sa.ForeignKey(Playlist.id), index=True)


