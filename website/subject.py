from flask import (
    Blueprint, render_template
)

from website.db import get_db

bp = Blueprint('subject', __name__, url_prefix='/nav')

@bp.route("/exhibit/<name>", methods=['GET'])
def exhibit(name):  
    db = get_db()
    exhibit = db.execute("SELECT upload_path, kind, thumbnail_path, upload_name, uploader FROM upload WHERE id = ?", (name,)).fetchone()
    path = exhibit['upload_path']
    kind = exhibit['kind']
    thumbnail = exhibit['thumbnail_path']
    name = exhibit['upload_name']
    author = exhibit['uploader']
    
    return render_template("nav/exhibit.html", path=path, kind=kind, thumbnail=thumbnail, name=name, author=author)


@bp.route("/user/<name>", methods=['GET'])
def user_page(name):
    db = get_db()
    thumbnails = []
    exhibits = db.execute("SELECT thumbnail_path, upload_name, id FROM upload WHERE uploader = ? ORDER BY upload_time DESC LIMIT 20", (name,))
    for item in exhibits.fetchall():
        thumbnails.append((item['thumbnail_path'], item['upload_name'], item['id']))

    return render_template("nav/user.html", name=name, thumbnails=thumbnails) 