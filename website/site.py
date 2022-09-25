from ast import Not
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from website.auth import login_required
from website.db import get_db
from website.uploads import save_upload_and_thumbnail
from website.uploads import supports_upload
from website.uploads import is_image

bp = Blueprint('site', __name__)


@bp.route("/", methods=['GET'])
def index():
    # now we want to get the latest uploads. 
    query = "SELECT id, thumbnail_path, uploader, upload_name FROM upload ORDER BY upload_time DESC LIMIT 20"

    db = get_db()
    result = db.execute(query)
    names = {}

    for item in result.fetchall():        
        names.update({item['id']:(item["thumbnail_path"], item["uploader"], item["upload_name"])})
    return render_template("site/index.html", previews=names)


@bp.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        # check to make sure there's an upload
        upload = request.files['filename']
        thumbnail = request.files['thumbnail']
        error = None
        if upload.filename == '':
            error = "Upload does not exist."
            flash(error)
  
        if not supports_upload(upload) and error is None:
            error = "This site does not support uploaded file type."
            flash(error)

        if (thumbnail.filename != '' and
            not is_image(thumbnail)
            and error is None):
            error = "Custom thumbnail is not an image file!"
            flash(error)      

        if error is None:
            error = save_upload_and_thumbnail(upload, thumbnail)
            if error is not None:
                flash(error)
            return render_template("nav/upload.html")

    return render_template("nav/upload.html")