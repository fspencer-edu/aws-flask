from flask import Flask
from routes import journal_bp
from services.db import init_db


def create_app():
    app = Flask(__name__)
    app.register_blueprint(journal_bp)

    with app.app_context():
        init_db()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)