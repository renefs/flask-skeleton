import os
from webassets import Bundle

from extensions import assets
_basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def register_assets():

    assets.load_path = [
        os.path.join(os.path.dirname(__file__)),
    ]

    assets.register(
        'js_all',
        Bundle(
               './node_modules/jquery/dist/jquery.min.js',
               './semantic/dist/semantic.min.js',
               './public/js/main.js',
               output='js/packed.js')
    )

    assets.register(
        'css_all',
        Bundle(
            './semantic/dist/semantic.min.css',
            './public/css/style.css',
            output='css/packed.css')
    )