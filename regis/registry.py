import requests
import re
from regis import error


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

    def get_images(self, n=10, last=None):
        try:
            catalog_response = requests.get(self.get_url('_catalog'),
                                            **self.http_params,
                                            params=self.get_pagination(n,last))

            catalog_data = catalog_response.json()
            link = self.get_next_link(catalog_response.headers)

            return catalog_data['repositories'], link
        except requests.exceptions.ConnectionError:
            raise error.ConnectionError()
        except AttributeError:
            raise error.IntegrityError()

    @staticmethod
    def get_pagination(n, last):
        if last is None:
            return {'n': n}
        return {'n': n, 'last': last}

    @staticmethod
    def get_next_link(headers):
        if 'Link' in headers:
            return re.search('</v2/_catalog(.*?)>', headers['Link']).group(1)
        return None