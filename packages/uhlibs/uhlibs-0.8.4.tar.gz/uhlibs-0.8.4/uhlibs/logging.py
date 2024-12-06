import logging

def enable_http_logging():
    # These two lines enable debugging at httplib level (requests->urllib3->http.client)
    # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS
    import http.client as http_client
    http_client.HTTPConnection.debuglevel = 1
    # up the verbosity of requests library's http activity
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

