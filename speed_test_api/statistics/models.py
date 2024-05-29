from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Statistic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Float, nullable=False)
    accuracy = db.Column(db.Float, nullable=False)
    wpm = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Statistic {self.id}>'