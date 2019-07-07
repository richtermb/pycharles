from pycharles.session import CharlesSession
from pycharles.request import CharlesRequest

CHARLES_SESSION_PATH = '../example_sessions/httpbin.chlsj'

if __name__ == '__main__':
    sess = CharlesSession(path=CHARLES_SESSION_PATH)
    print('session has {} requests.'.format(sess.requests_count()))

    queried_sess = sess.query_requests_with_properties({
        'method': 'GET'
    }).query_requests_with_properties({
        'response.status': 200
    })  # chained queries for readability

    print('queried session: found {} results. \nprinting...'.format(queried_sess.requests_count()))
    queried_sess.query_request_with_index(0).print_simple_json()
