#
# This file is necessary to make this directory a package.

from zope.app.wsgi.testlayer import http as _http

from zope.app.file.testing import AppFileLayer


def http(query_str, *args, **kwargs):
    wsgi_app = AppFileLayer.make_wsgi_app()
    kwargs.setdefault('handle_errors', False)
    return _http(wsgi_app, query_str, *args, **kwargs)
