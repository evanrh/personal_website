from app import create_app, db
from app.models import User, Post, Category, PageView

app = create_app()
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Category': Category, 'PageView': PageView}
