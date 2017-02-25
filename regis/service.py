from flask import Blueprint, request, jsonify
from regis.registry import Registry
from regis import error
from regis.response import generate_error_response, generate_success_response
from configparser import ConfigParser

# Configuration
config = ConfigParser()
config.read('regis.cfg')


services = Blueprint('services', __name__)

registry = Registry(host=config.get('registry', 'host'), port=config.get('registry', 'port'))

if config.get('security', 'username') is not '' and config.get('security', 'password') is not '':
    registry.set_credentials(config.get('security', 'username'), config.get('security', 'password'))

if config.get('security', 'ignore_ssl') is True:
    registry.ignore_ssl()


@services.route('/images')
def images():
    n = request.args.get('n', 10)
    last = request.args.get('last', None)

    try:
        return jsonify(generate_success_response(registry.get_images(n, last)))
    except error.ConnectionError as exception:
        return jsonify(generate_error_response(exception))


@services.route('/tags')
def tags():
    print(request.args['image'])

    return jsonify({})


@services.route('/digest', methods=['POST'])
def digest():
    pass