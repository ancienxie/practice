from flask import Blueprint, request, jsonify
from .models import db, Statistic

bp = Blueprint('statistics', __name__)

@bp.route('/add', methods=['POST'])
def add_statistic():
    data = request.json
    if not all(k in data for k in ("time", "accuracy", "wpm")):
        return jsonify({"error": "Missing data"}), 400

    new_stat = Statistic(time=data["time"], accuracy=data["accuracy"], wpm=data["wpm"])
    db.session.add(new_stat)
    db.session.commit()
    return jsonify({"message": "Statistic added"}), 201

@bp.route('/get', methods=['GET'])
def get_statistics():
    stats = Statistic.query.all()
    results = [
        {"time": stat.time, "accuracy": stat.accuracy, "wpm": stat.wpm} for stat in stats
    ]
    return jsonify(results), 200