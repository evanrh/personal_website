from flask import Blueprint

blog = Blueprint('blog',
        __name__,
        template_folder='templates',
        static_folder='static',
        subdomain="blog"
        )

from . import routes