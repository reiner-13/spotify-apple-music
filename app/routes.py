import os
from flask import Flask, session, redirect, url_for, request, render_template, flash
from flask_mysqldb import MySQL

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

from app import app
from app.forms import *
#from user import User

"""Database Things"""
app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")
mysql = MySQL(app)

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
def home():
    return render_template("home.html")



@app.route("/callback")
def callback():
    sp_oauth.get_access_token(request.args["code"])
    return redirect(url_for("home"))


@app.route("/profile", methods=['GET', 'POST'])
def profile():
    return render_template("profile.html")


@app.route("/<playlist_name>/search_songs", methods=['GET'])
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


@app.route("/login")
def login():
    login_form = LoginForm()
    create_acc_form = CreateAccountForm()
    cursor = mysql.connection.cursor()

    if login_form.validate_on_submit():
        username = request.form["username"]
        password = request.form["password"]
        result = cursor.execute(f"SELECT * FROM users WHERE Username='{username}' AND Password='{password}';")
        if result > 0:
            data = cursor.fetchall()
            user_id = data[0][0]
            first_name = data[0][1]
            last_name = data[0][2]
            username = data[0][3]
            password = data[0][4]
            #current_user = User(user_id, first_name, last_name, username, password)
        else:
            print("ERROR")
    if create_acc_form.validate_on_submit():
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        username = request.form["username"]
        password = request.form["password"]
        cursor.execute(f"INSERT INTO users (FirstName, LastName, Username, Password) VALUES ('{first_name}', '{last_name}', '{username}', '{password}');")
        mysql.connection.commit()
        print("Successfully inserted into DB.")
    return render_template("login.html", login_form=login_form, create_acc_form=create_acc_form)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))