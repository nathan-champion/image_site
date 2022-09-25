from flask import (
    Blueprint, render_template
)

from website.db import get_db

bp = Blueprint('subject', __name__, url_prefix='/nav')

@bp.route("/exhibit/<name>", methods=['GET'])
def exhibit(name):
    
    db = get_db()
    exhibit = db.execute("SELECT upload_path, kind, thumbnail_path FROM upload WHERE id = ?", (name,)).fetchone()
    path = exhibit['upload_path']
    kind = exhibit['kind']
    thumbnail = exhibit['thumbnail_path']
    print(path)
    print(kind)
    
    return render_template("nav/exhibit.html", path=path, kind=kind, thumbnail=thumbnail)


def get_upload_type_from_filename(filename: str):
    parts = filename.split('/')
    if len(parts) > 2:
        return parts[1]
    else:
        return ''