import json

import requests


class CharlesRequest(object):
    """Represents a single Charles request object.

    The underlying request can be accessed and modified using the instance methods.

    Parameters
    ----------
    request: the raw dict that represents a Charles request
        It is recommended to pass in an existing request that can be found in the Charles session.
    """

    def __init__(self, request_dict):
        self.request_dict = request_dict

    def execute(self):
        return requests.request(
            self.request_dict['method'],
            self.request_dict['host'] if self.request_dict['path'] is None else self.request_dict['host'] + \
                                                                                self.request_dict['path'],

        )

    def get_url(self):
        _scheme = self.request_dict['scheme']
        _resource = self.request_dict['host'] if self.request_dict['path'] is None else self.request_dict['host'] + \
                                                                                        self.request_dict['path']
        return '{}://{}'.format(_scheme, _resource)

    def diff(self, other):
        """Find the differences between instance and another request

        Parameters
        ----------
        other: the other request

        Returns
        -------
        keys: list of keys with differences
        """
        return 0

    def print_simple_json(self):
        """Displays only necessary information"""
        try:
            print(json.dumps({
                'method': self.request_dict['method'],
                'url': self.get_url(),
                'status': self.request_dict['response']['status']
            }, indent=4))
        except KeyError:
            print(json.dumps({
                'method': self.request_dict['method'],
                'url': self.get_url(),
                'status': None
            }, indent=4))


    def print_all_json(self):
        print(json.dumps(self.request, indent=4))
