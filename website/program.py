from datetime import datetime, timezone
from hashlib import md5
import hashlib
import sqlite3
import time
from flask import Flask
from flask import render_template
from flask import request
from flask import session
from markupsafe import escape
from werkzeug.utils import secure_filename
from pathlib import Path
from PIL import Image
import json


def show_thumbnails_page():
    t = Path("static/thumbs")
    uploaded_images = []
    for file in t.iterdir():
        uploaded_images.append(str(file.with_suffix('').name.split('thumbnail_')[1]))

    return render_template("uploaded.html", uploaded_images=uploaded_images)


@app.route("/images/<name>")
def show_picture(name):
    
    escaped_name = escape(name)
    root_json_path = Path("static/data")
    img_json_path = Path(root_json_path / f"{escaped_name}.json")
    json_file = open(img_json_path)

    json_data = json.load(json_file)
    image_data = ImageData(**json_data)
    image_path = f"pics/{image_data.image_name}"

    # probably not going to work, as this is probably time on the server
    upload_timestamp = datetime.fromtimestamp(image_data.upload_time)
    now = time.time()
    offset = datetime.fromtimestamp(image_data.upload_time) - datetime.utcfromtimestamp(image_data.upload_time)
    upload_timestamp = upload_timestamp + offset
    return render_template("image_page.html", image_path=image_path, timestamp=upload_timestamp)

