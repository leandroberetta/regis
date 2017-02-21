from flask import Blueprint, request, jsonify
from registry import Registry

services = Blueprint('services', __name__)
registry = Registry()


@services.route('/images')
def images():
    return jsonify(registry.get_images())


@services.route('/tags', methods=['POST', 'DELETE'])
def tags():
    payload = request.json()

    if request.method == 'POST':
        print(payload)
    elif request.method == 'DELETE':
        print(payload)


@services.route('/digest', methods=['POST'])
def digest():
    pass