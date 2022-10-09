from flask import (
    Blueprint, render_template, request, session, current_app
)

from website.db import get_db


bp = Blueprint('subject', __name__)


@bp.route("/exhibit/<id>", methods=['GET', 'POST'])
def exhibit(id):  
    db = get_db()
    exhibit = db.execute("SELECT a.upload_path, a.kind, a.thumbnail_path, a.upload_name, a.uploader, b.featured FROM upload a, user b WHERE a.id = ? AND b.username = a.uploader", (id,)).fetchone()

    if request.method == 'POST':
        try:
            make_featured = request.form['to-feature']
            db.execute("UPDATE user SET featured = ? WHERE username = ?", (make_featured, exhibit['uploader'],))
            db.commit()
            exhibit = db.execute("SELECT a.upload_path, a.kind, a.thumbnail_path, a.upload_name, a.uploader, b.featured FROM upload a, user b WHERE a.id = ? AND b.username = a.uploader", (id,)).fetchone()
        except:
            pass
    
    return render_template("nav/exhibit.html", path=exhibit['upload_path'], kind=exhibit['kind'], thumbnail=exhibit['thumbnail_path'], name=exhibit['upload_name'], author=exhibit['uploader'], featured=exhibit['featured'], id=id)


@bp.route("/user/<name>", methods=['GET'])
def user_page(name):
    
    db = get_db()
    thumbnails = []
    featured = db.execute("SELECT thumbnail_path, upload_name, id FROM upload WHERE id = (SELECT featured FROM user WHERE username = ?)", (name,)).fetchone()
    exhibits = db.execute("SELECT thumbnail_path, upload_name, id FROM upload WHERE uploader = ? ORDER BY upload_time DESC LIMIT 8", (name,))
    for item in exhibits.fetchall():
        thumbnails.append((item['thumbnail_path'], item['upload_name'], item['id']))

    return render_template("nav/user.html", name=name, thumbnails=thumbnails, featured=featured) 


@bp.route("/gallery/<name>", methods=['GET'])
@bp.route("/gallery/<name>/<page>", methods=['GET'])
def gallery(name, page=0):
    db = get_db()
    print(page)
    count = db.execute("SELECT COUNT(id) from upload WHERE uploader = ?", (name,)).fetchone()[0]
    
    limit = current_app.config['EXHIBIT_LIMIT_GALLERY']
    offset = int(page) * limit
    
    
    if count - offset < limit:
        limit = count - offset


    print(f"offset is {offset}")
    print(f"limit is {limit}")
    exhibits = db.execute("SELECT thumbnail_path, upload_name, id FROM upload WHERE uploader = ? ORDER BY upload_time DESC LIMIT ? OFFSET ?", (name, limit, offset,)).fetchall()

    return render_template("nav/gallery.html", exhibits=exhibits, offset=offset, limit=limit, count=count, page=page, name=name)