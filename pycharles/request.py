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
        self.index = -1

    def set_header(self, name, value):
        """Set the value for a specified header. If the header exists, this method will overwrite it.
        If not, the header will be added.

        Parameters
        ----------
        name: the header name
        value: the value you would like to set
        """
        header_index = 0
        for header_dict in self.request_dict['request']['header']['headers']:
            if header_dict['name'].lower() == name.lower():
                self.request_dict['request']['header']['headers'][header_index]['value'] = value  # gross
                return
            header_index += 1
        self.request_dict['request']['header']['headers'].append({
            'name': name,
            'value': value
        })

    def get_header(self, name):
        """Get the value for a specified header

        Parameters
        ----------
        name: the header name

        Returns
        -------
        value: the value of the header.
        """

        header_index = 0
        for header_dict in self.request_dict['request']['header']['headers']:
            if header_dict['name'].lower() == name.lower():
                return self.request_dict['request']['header']['headers'][header_index]['value']
            header_index += 1
        return None

    def execute(self):
        """Execute the request using the requests module

        Returns
        -------
        request: the requests module request object.
        """

        headers = dict()
        for header in self.request_dict['request']['header']['headers']:
            headers[header['name']] = header['value']

        return requests.request(
            self.request_dict['method'],
            self.get_url(),
            headers=headers,
            data=self.request_dict['request']['body']['text']
        )

    def get_url(self):
        """Format URL

        Returns
        -------
        url: the complete URL of the request
        """

        _scheme = self.request_dict['scheme']
        _host_path = self.request_dict['host'] if self.request_dict['path'] is None else self.request_dict['host'] + \
                                                                                        self.request_dict['path']
        return '{}://{}'.format(_scheme, _host_path)

    def diff(self, other):
        """Find the differences between instance and another request

        Parameters
        ----------
        other: the other request

        Returns
        -------
        keys: differences
        """
        this_set = set(self.request_dict.items())
        other_set = set(other.items())

        return this_set - other_set

    def print_simple_json(self):
        """Displays only necessary information
        For requests with method 'CONNECT', getting the status will throw a KeyError, so we handle that below.
        """
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
        print(json.dumps(self.request_dict, indent=4))
