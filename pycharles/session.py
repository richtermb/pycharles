import request

import json


class CharlesSession(object):
    """Charles session object, initialized with a path to the file.

    At its core, the session is a list of request objects, which makes it easy to fool around with.
    """

    def __init__(self, request_list=list(), path=None):
        if len(request_list) == 0 and path is not None:
            with open(path, 'r') as f:
                self._all_requests = [request.CharlesRequest(r) for r in json.load(f)]
        elif len(request_list) > 0 and path is None:
            self._all_requests = [request.CharlesRequest(r) for r in request_list]
        else:
            self.fail('only one initialization parameter should be specified')

    def requests_count(self):
        return len(self._all_requests)

    def query_request_with_index(self, index):
        """Query and return the request at the specified index.

                Parameters
                ----------
                index: int

                Returns
                -------
                the query result as a charles request.
                """
        return self._all_requests[index]

    def query_requests_with_properties(self, properties):
        def _request_key_matches_query(r, k, v):
            if k[-1] == '.':
                self.fail('cannot end property key with \'.\'')

            if not k.__contains__('.'):
                return r[k] == v

            nested_keys = k.split('.')  # will *always* be at least 2 keys in length
            property_value = r[nested_keys[0]] # enumerate once
            for nested_key in nested_keys[1:]:
                property_value = property_value[nested_key]

            return property_value == v

        """Query and return requests with the defined properties in a CharlesSession object.

        Parameters
        ----------
        properties: dict with properties to query.
            example: {
                        "host": "httpbin.org",
                        "ssl.protocol": "TLSv1.2"
                     }

        Returns
        -------
        result: the query result as a new session.
            if the example is used as an argument, all requests using TLSv1.2 with the host httpbin.org will be returned
        """

        result = list()

        for charles_request in [_charles_request for _charles_request in self._all_requests]:
            for k, v in properties.items():
                if _request_key_matches_query(charles_request.request_dict, k, v):
                    result.append(charles_request.request_dict)

        return CharlesSession(request_list=result)

    def fail(self, msg):
        print('CharlesSession instance failed with error: {}'.format(msg))
        exit(-1)

    def print_json(self):
        print(json.dumps(self._all_requests, indent=4))
