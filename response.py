
class Error:
    CONNECTION_ERROR = (1000, "ConnectionError")

def generate_error_response(error):
    return {'error': {'code': error[0], 'message': error[1]}}

def generate_success_response(data):
    return {'data': data}