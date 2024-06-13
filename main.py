from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.songs import Song

main = Blueprint("main", __name__)

@main.route("/")
@login_required
def index():
    songs = Song.query.all()
    return render_template("songs.html", songs=songs, name=current_user.name)