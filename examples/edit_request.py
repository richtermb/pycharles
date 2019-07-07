import pycharles

CHARLES_SESSION_PATH = '../example_sessions/httpbin_post.chlsj'

if __name__ == '__main__':
    sess = pycharles.session.CharlesSession(path=CHARLES_SESSION_PATH)
    print('session has {} requests.'.format(sess.requests_count()))
    print('changing user-agent of the first request...')
    sess.query_request_with_index(0).set_header('User-Agent', 'Nokia 8110')
    sess.save('../example_sessions/edited_httpbin_request.chlsj')
