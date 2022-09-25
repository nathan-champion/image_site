from datetime import datetime
import hashlib

def get_timestamp_now():
    return int(round(datetime.utcnow().timestamp()))


def get_timestamp_hash(timestamp, algorithm):
    return hashlib.new(algorithm, str(timestamp).encode()).hexdigest()


def get_mimetype_type(mimetype: str):
    return mimetype[0:mimetype.index('/')]


def get_mimetype_subtype(mimetype: str):
    return mimetype[mimetype.index('/')+1:]


def get_centered_rectangle(width, height):
    left = 0
    top = 0
    right = width
    bottom = height
    if width > height:
        left = (width / 2) - (height / 2)
        right = (width / 2) + (height / 2)
    else:
        top = (height / 2) - (width / 2)
        bottom = (height / 2) + (width / 2)
            
    return (left, top, right, bottom)

