from flask import Blueprint

blog = Blueprint('blog',
        __name__,
        template_folder='templates',
        static_folder='static',
        url_prefix="/blog"
        )

from . import routes