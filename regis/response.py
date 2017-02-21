def generate_error_response(error):
    return {'error': {'code': error.code, 'message': error.message}}


def generate_success_response(data):
    return {'data': data}
