import functools

from flask import current_app, redirect, request


def require_https(endpoint):
    """require https transaction, if https cannot be detected reload page
    using https explicitly or raise exception

    for secure forms both GET and POST must be transmitted via https, a form
    retrieved via http which posts to https is subject to MITM attacks
    """
    @functools.wraps(endpoint)
    def require_https_wrapper(*args, **kwargs):
        """if current request is not https, redirect to same url via https"""
        current_app.logger.debug('require https {}'.format(request.headers))
        if request.is_secure:
            current_app.logger.debug("require_https: ok")
        else:
            https_url = "https://" + request.url[7:] # replace ^http://
            current_app.logger.debug('redirecting to https %s' % (https_url,))
            return redirect(https_url)
        return endpoint(*args, **kwargs)
    return require_https_wrapper

