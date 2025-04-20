# app/routes.py
from flask import Blueprint, request, jsonify

def create_routes(repo):
    bp = Blueprint('api', __name__)

    @bp.route('/employees', methods=['GET'])
    def get_all():
        return jsonify(repo.get_all())

    @bp.route('/employees/<int:id>', methods=['GET'])
    def get(id):
        emp = repo.get(id)
        return jsonify(emp) if emp else ('Not Found', 404)

    @bp.route('/employees', methods=['POST'])
    def add():
        data = request.get_json()
        return jsonify(repo.add(data['name'], data['role'])), 201

    @bp.route('/employees/<int:id>', methods=['PUT'])
    def update(id):
        data = request.get_json()
        updated = repo.update(id, data['name'], data['role'])
        return jsonify(updated) if updated else ('Not Found', 404)

    @bp.route('/employees/<int:id>', methods=['DELETE'])
    def delete(id):
        repo.delete(id)
        return jsonify({'status': 'deleted'})

    return bp
