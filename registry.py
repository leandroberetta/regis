import requests
import error


class Registry:

    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port

        self.username = None
        self.password = None
        self.ssl = False

        self.http_params = {'verify': self.ssl,
                            'headers': {'Accept': 'application/vnd.docker.distribution.manifest.v2+json'}}

    def set_credentials(self, username, password):
        self.username = username
        self.password = password

        self.http_params['auth'] = (self.username, self.password)

    def ignore_ssl(self):
        self.ssl = False
        self.http_params['verify'] = self.ssl

    def set_ssl_certificate(self, ssl_cert_path):
        self.ssl = ssl_cert_path
        self.http_params['verify'] = self.ssl

    def get_url(self, path):
        url = 'http'

        if self.username is not None:
            url = 'https'

        return '{0}://{1}:{2}/v2/{3}'.format(url, self.host, self.port, path)

    def get_images(self):
        """
        Returns a list of Docker images stored in a private Registry.

        :return: List of images.
        :raises: error.ConnectionError
        """

        try:
            catalog = requests.get(self.get_url('_catalog'), **self.http_params).json()

            return catalog['repositories']
        except requests.exceptions.ConnectionError:
            raise error.ConnectionError()
