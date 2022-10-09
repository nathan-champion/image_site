from flask import Flask
import os

def create_app(test_config=None):
    # first, we're going to make the app
    app = Flask(__name__, instance_relative_config=True)
    # next, we'll set up 
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'site.sqlite'),
        THUMBNAIL_FOLDER="website/static/thumbnails",
        SUPPORTED_UPLOADS=["audio", "image"],
        THUMBNAIL_SIZE=(128,128),
        DEFAULT_THUMB= {'image': 'website/static/thumbnails/default/default_img.jpg', 
                        'audio': 'website/static/thumbnails/default/default_aud.jpg'},
        UPLOAD_FOLDERS={'image': 'website/static/uploads/images',
                        'audio': 'website/static/uploads/audio'},
        TIMESTAMP_HASH='md5',
        EXHIBIT_LIMIT_GALLERY=8
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import uploads
    uploads.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp, url_prefix='/auth')

    from . import site
    app.register_blueprint(site.bp)

    from . import subject
    app.register_blueprint(subject.bp, url_prefix='/nav')
    # this is here because we're referring to the home page as "index"
    # in several places in auth.py.  Without this, we'd have to call
    # <folder>.index
    app.add_url_rule('/', endpoint='index')
    # rule = ROUTE!!!
    # endpoint = FUNCTION NAME!!!
    app.add_url_rule('/upload', endpoint='upload')

    return app

