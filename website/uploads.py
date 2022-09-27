from email.mime import audio, base, image
from math import factorial
from sqlite3 import Timestamp
from flask import (
    g, current_app, session, url_for
)

from pathlib import Path

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from website.db import get_db
from website.utils import get_centered_rectangle, get_mimetype_type
from website.utils import get_timestamp_hash
from website.utils import get_timestamp_now

from PIL import Image

import click

import os


class UploadData(object):

    def __init__(self, uploader, thumbnail, upload):
        super(UploadData, self).__init__()

        self.uploader = uploader
        self.t_filename = self.compose_filename(thumbnail)
        self.u_filename = self.compose_filename(upload)
        self.time = get_timestamp_now()
        self.time_hash = get_timestamp_hash(self.time, current_app.config['TIMESTAMP_HASH'])
        self.mimetype = upload.mimetype

    def get_time_hashed_name(self):
        return f"{self.time_hash}_{self.u_filename}"


    def compose_filename(self, fileStorage: FileStorage):
        if fileStorage.filename == '':
            return ''
        # secure filename
        return secure_filename(fileStorage.filename)


    def get_filename_without_suffix(self):
        return Path(self.u_filename).stem



def supports_upload(upload: FileStorage):
    for type in current_app.config['SUPPORTED_UPLOADS']:
        if upload.mimetype.find(type) != -1:
            return True
    return False


def save_upload_and_thumbnail(upload: FileStorage, thumbnail: FileStorage):   
    upload_data = UploadData(session.get('user_id'), thumbnail, upload)
    try:
        thumb_path = save_thumbnail(upload, thumbnail, upload_data.time_hash)   
        upload_path = save_upload(upload, upload_data.time_hash)

        if (upload_path is not None and thumb_path is not None):
            write_upload_to_database(upload_data, upload_path.as_posix(), thumb_path.as_posix())
    except:
        if thumb_path is None:
            return "There was a problem saving your thumbnail!"
        elif upload_path is None:
            return "There was a problem saving your upload!"
        else:
            return "There was a problem saving your upload data to the database!"
    
    return None      

        
def write_upload_to_database(upload: UploadData, upload_path, thumb_path):
    print("Writing to database")
    db = get_db()
    db.execute(
        "INSERT INTO upload (uploader, upload_path, thumbnail_path, upload_name, kind, upload_time) VALUES(?, ?, ?, ?, ?, ?)",
        (upload.uploader, upload_path, thumb_path, upload.get_filename_without_suffix(), upload.mimetype, upload.time ) 
    )
    db.commit()


def is_image(file_storage: FileStorage):
    if file_storage.mimetype.find('image/') != -1:
        return True
    return False


def save_thumbnail(upload: FileStorage, thumbnail: FileStorage, timestamp_hash):
    if thumbnail.filename == '':
        if is_image(upload):
            thumbnail = upload
        else:  
            tp = str(current_app.config['DEFAULT_THUMB'][get_mimetype_type(upload.mimetype)])  
            return Path('/'.join(tp.split('/')[2:]))

    s_name = secure_filename(thumbnail.filename)
    base_path = current_app.config['THUMBNAIL_FOLDER'] 
    thumb_path = Path(base_path) / f"{timestamp_hash}_{s_name[0:s_name.rindex('.')]}.jpg"
    
    with Image.open(thumbnail) as image:
        region = get_centered_rectangle(image.width, image.height)            
        temp = image.convert('RGB').crop(region)
        temp.thumbnail(current_app.config['THUMBNAIL_SIZE'])
        temp.save(thumb_path, 'JPEG')
        temp.close()

    thumbnail.stream.seek(0, 0)
    return Path(*thumb_path.parts[2:])


def save_upload(upload: FileStorage, timestamp_hash):
    upload_type = get_mimetype_type(upload.mimetype)
    s_name = secure_filename(upload.filename)
    base_path = current_app.config['UPLOAD_FOLDERS'][upload_type]
    upload_path = Path(base_path) / f"{timestamp_hash}_{s_name}"
    upload.save(upload_path)

    return Path(*upload_path.parts[2:])


@click.command('wipe-uploads')
def wipe_uploads_command():
    base_dir = Path(os.getcwd())
    audio_dir = Path(base_dir) / current_app.config['UPLOAD_FOLDERS']['audio']
    image_dir = Path(base_dir) / current_app.config['UPLOAD_FOLDERS']['image']
    thumbs_dir = Path(base_dir) / current_app.config['THUMBNAIL_FOLDER']
    __remove_all_files__(audio_dir)
    __remove_all_files__(image_dir)
    __remove_all_files__(thumbs_dir)    

    click.echo("Wiped upload folders")


def __remove_all_files__(directory):
    just_files = [f for f in os.listdir(directory) if os.path.isfile(directory / f)]
    for file in just_files:
        os.remove(directory / file)
    

def init_app(app):
    app.cli.add_command(wipe_uploads_command)
