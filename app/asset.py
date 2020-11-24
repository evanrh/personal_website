from flask import current_app as app
from flask_assets import Bundle

def compile_static_assets(assets):
    """Create stylesheet bundles"""
    assets.auto_build = True
    assets.debug = False

    common_less_bundle = Bundle('src/less/*.less',
                                filters='less,cssmin',
                                output='dist/css/styles.css',
                                extra={'rel': 'stylesheet/less'})
    home_less_bundle = Bundle('home/less/home.less',
                                filters='less,cssmin',
                                output='dist/css/home.css',
                                extra={'rel': 'stylesheet/less'})
    blog_less_bundle = Bundle('blog/less/blog.less',
                                filters='less,cssmin',
                                output='dist/css/blog.css',
                                extra={'rel': 'stylesheet/less'})
    assets.register('common_less_bundle', common_less_bundle)
    assets.register('home_less_bundle', home_less_bundle)
    assets.register('blog_less_bundle', blog_less_bundle)
    if app.config['FLASK_ENV'] == 'development':
        common_less_bundle.build()
        home_less_bundle.build()
        blog_less_bundle.build()
    return assets