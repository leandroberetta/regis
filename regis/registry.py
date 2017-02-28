import requests
import json
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

    def get_url(self, path=None):
        url = 'http'

        if self.username is not None:
            url = 'https'

        if path is None:
            return '{0}://{1}:{2}/v2'.format(url, self.host, self.port)
        return '{0}://{1}:{2}/v2/{3}'.format(url, self.host, self.port, path)

    @error.exception_aware_context
    def get_images(self, n=10, last=None):
        catalog_response = requests.get(self.get_url('_catalog'),
                                        **self.http_params,
                                        params=self.get_pagination(n,last))

        catalog_data = self.get_data_or_throw_error(catalog_response)
        link = self.get_next_link(catalog_response.headers)

        return catalog_data['repositories'], link

    @error.exception_aware_context
    def get_tags(self, image):
        tags_response = requests.get(self.get_url('{0}/tags/list'.format(image)),
                                     **self.http_params)

        tags_data = self.get_data_or_throw_error(tags_response)

        return tags_data['tags'] if tags_data['tags'] else []

    @error.exception_aware_context
    def get_manifests(self, image, tag):
        manifests_response = requests.get(self.get_url('{0}/manifests/{1}'.format(image, tag)), **self.http_params)
        manifests_data = self.get_data_or_throw_error(manifests_response)

        digest = None
        if 'Docker-Content-Digest' in manifests_response.headers:
            digest = manifests_response.headers['Docker-Content-Digest']

        return {'manifests': manifests_data, 'digest': digest}

    @error.exception_aware_context
    def delete_tag(self, image, digest):
        requests.delete(self.get_url('{0}/manifests/{1}'.format(image, digest)), **self.http_params)

    @staticmethod
    def get_pagination(n, last):
        if last is None:
            return {'n': n}
        return {'n': n, 'last': last}

    @staticmethod
    def get_next_link(headers):
        if 'Link' in headers:
            try:
                link = headers['Link']
                parts = link.split('?')
                parts = parts[1].split('>')

                return '?' + parts[0]
            except IndexError:
                raise error.IntegrityError()
            #return re.search('</v2/_catalog(.*?)>', headers['Link']).group(1)
        return None

    @staticmethod
    def get_data_or_throw_error(response):
        if response.status_code == 404:
            raise error.NotFoundError()

        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            raise error.NotFoundError()

