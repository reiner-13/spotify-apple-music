import os
from flask import Flask, session, redirect, url_for, request, render_template, flash
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
import sqlalchemy as sa
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from app import app, db
from app.forms import *
from app.models import *


"""Spotipy Things"""
client_id = "7cb865a7264c4d0b9e5b4c6f171582a5"
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = "http://localhost:5000/callback"
scope = "playlist-read-private playlist-modify-private"
cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=True
)
sp = Spotify(auth_manager=sp_oauth)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/callback")
def callback():
    sp_oauth.get_access_token(request.args["code"])
    return redirect(url_for("profile"))


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.platform == "spotify" and not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    playlists = sp.user_playlists(sp.me()["id"])
    create_playlist_form = CreatePlaylistForm()
    if create_playlist_form.validate_on_submit():
        playlist = Playlist(name=create_playlist_form.playlist_name.data)
        db.session.add(playlist)
        current_user.platform_username = sp.me()["id"]
        sp_playlist = sp.user_playlist_create(current_user.platform_username, playlist.name, public=False, collaborative=False, description="SAM Shared Playlist")
        db.session.commit()
        user_playlist = UserPlaylist(user_id=current_user.id, playlist_id=playlist.id, platform_id=sp_playlist["id"])
        db.session.add(user_playlist)
        db.session.commit()
        return redirect(url_for("profile"))
    

    return render_template("profile.html", create_playlist_form=create_playlist_form, playlists=playlists, username=sp.me()["id"])


@app.route("/<playlist_name>/search_songs", methods=['GET'])
@login_required
def search_songs(playlist_name):
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    if request.method == 'GET':
        data = request.args
        search_text = data.get("song_search") if data.get("song_search") is not None else "roundabout" # else "": this is default value, could personalize based off other playlists or something
        search_results = sp.search(q=search_text, limit=20, type="track")
        #track_id = search_results["tracks"]["items"][idx]["uri"]
    return render_template("add_songs.html", playlist_name=playlist_name, search_text=search_text, search_results=search_results)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("profile"))
    login_form = LoginForm()
    create_acc_form = CreateAccountForm()

    if login_form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == login_form.username.data)
        )
        if user is None or not user.check_password(login_form.password.data):
            flash("Invalid username or password.")
            return redirect(url_for("login"))
        login_user(user, remember=login_form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for("profile")
        return redirect(next_page)

    if create_acc_form.validate_on_submit():
        user = User(username=create_acc_form.username.data, first_name=create_acc_form.first_name.data, last_name=create_acc_form.last_name.data, platform=create_acc_form.platform.data)
        user.set_password(create_acc_form.password1.data)
        db.session.add(user)
        db.session.commit()
        flash("Created user account.")
        login_user(user)
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for("profile")
        return redirect(next_page)
    return render_template("login.html", login_form=login_form, create_acc_form=create_acc_form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))