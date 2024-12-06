import argparse
import logging
import os
import tempfile

from flask import Flask, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.middleware.profiler import ProfilerMiddleware

log = logging.getLogger(__name__)

# FLASKAPP_ARGPARSE_DEFAULTS can be useful when testing custom FlaskAppArgParser implementations:
#   args = StrikeReportsArgParser.parse_args(['--port', '9999'])
#   expect = argparse.Namespace(port=9999, **FLASKAPP_ARGPARSE_DEFAULTS)
#   self.assertEqual(args, expect)
FLASKAPP_ARGPARSE_DEFAULTS = {
    'config': None,
    'debug': False,
    'https': False,
    'ssl_key': '',
    'ssl_crt': '',
    'profiler': False,
    'proxy_fix': False,
}

FlaskAppArgParser = argparse.ArgumentParser(description="Arg parser for configured_app()")
FlaskAppArgParser.add_argument("--config", type=str,
                                help="string path to config module: myapp.config)")
FlaskAppArgParser.add_argument("--host", type=str, help="host")
FlaskAppArgParser.add_argument("--port", type=int, required=True, help="port")
FlaskAppArgParser.add_argument("--debug", action="store_true", default=False,
                                help="put app into debug mode")
# app should be behind https terminus, in case not..
FlaskAppArgParser.add_argument("--https", action="store_true", default=False,
                                help="listen via https")
FlaskAppArgParser.add_argument("--ssl-key", default="")
FlaskAppArgParser.add_argument("--ssl-crt", default="")
# options to enable Flask extensions
FlaskAppArgParser.add_argument("--profiler", action="store_true", default=False)
FlaskAppArgParser.add_argument("--proxy-fix", action="store_true", default=False)


def configured_app(import_name, debug=False, config_module=None,
                   profiler=False, proxy_fix=False, sqlalchemy=False,
                   **flask_kwargs):
    """instantiate a Flask app

    for details see https://flask.palletsprojects.com/en/2.0.x/api/#flask.Flask

     * import_name: the name of your app package
     * debug: put flask app into debug mode
     * config_module: python module path to load config from
     * profiler: bool. activate flask.contrib.profiler.ProfilerMiddleware
     * proxy_fix: bool. activate werkzeug.contrib.fixers.ProxyFix

    Environment variables supported:

    FLASKAPP_CONFIG envvar module, values will override those in config_module
    """
    app = Flask(import_name, **flask_kwargs)
    app.secret_key = os.urandom(24)
    if sqlalchemy:
        # stop noisy warnings
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if debug:
        app.debug = debug
        if sqlalchemy:
            app.config['SQLALCHEMY_ECHO'] = True

    if config_module:
        app.config.from_object(config_module)
    if os.getenv("FLASKAPP_CONFIG", False):
        # do not fail silently if configured file cannot be loaded
        app.config.from_envvar("FLASKAPP_CONFIG", silent=False)

    # enable profiling?
    if profiler:
        pstat_dir = tempfile.mkdtemp()
        log.debug("PROFILER writing pstat files to {}".format(pstat_dir))
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, profile_dir=pstat_dir)

    # Do not enable the ProxyFix without reading & understanding the manual
    # https://werkzeug.palletsprojects.com/en/2.1.x/middleware/proxy_fix/
    if proxy_fix:
        app.wsgi_app = ProxyFix(app.wsgi_app)

    @app.route('/heartbeat')
    def heartbeat():
        return jsonify({"{}-server".format(import_name): "ok"})

    return app

