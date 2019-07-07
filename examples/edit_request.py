import pycharles

PATH = '../example_sessions/httpbin.chlsj'

if __name__ == '__main__':
    sess = pycharles.session.CharlesSession(path=PATH)
    print('session has {} requests.'.format(sess.requests_count()))
    queried_sess = sess.query_requests_with_properties({
        'request.sizes.headers': 242
    })
    print('queried session has {} requests.'.format(queried_sess.requests_count()))
    # print(queried_sess)
    queried_sess.query_request_with_index(0).print_simple_json()