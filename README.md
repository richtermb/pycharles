# pycharles

## usage:

1. open your desired charles session.
2. select `File > Export Session`
3. export as a JSON session file

```
> from pycharles.session import CharlesSession
> from pycharles.request import CharlesRequest

> session = CharlesSession(path=PATH)
> session.requests_count()  # return number of requests in the session file
> charles_request = session.query_request_with_index(n)  # return the nth request object in the file
> charles_request.set_header('User-Agent', 'Nokia')  # set header
> 
```

License
-------
MIT
