# FLASK_APP=flask_app flask run
# FLASK_APP=flask_app FLASK_DEBUG=1 flask run

from flask import Flask

def create_app():
    app = Flask(__name__)

    from flask_app.views.home_views import home_bp
    from flask_app.views.about_views import about_bp
    from flask_app.views.predict_views import predict_bp
    from flask_app.views.reference_view import reference_bp
    app.register_blueprint(home_bp)
    app.register_blueprint(about_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(reference_bp)

    return app

if __name__ == "__main__":
  app = create_app()
  app.run()