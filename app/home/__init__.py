from flask import Blueprint

home = Blueprint('home',
        __name__,
        template_folder='templates',
        static_folder='static',
        static_url_path='/assets',
        url_prefix='/'
)
from . import routes