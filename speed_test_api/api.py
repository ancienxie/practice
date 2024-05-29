from flask import Flask
from statistics.models import db
from statistics.routes import bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(bp, url_prefix='/api/statistics')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)