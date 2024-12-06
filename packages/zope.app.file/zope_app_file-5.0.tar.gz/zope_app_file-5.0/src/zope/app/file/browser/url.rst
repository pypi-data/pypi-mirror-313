Special URL handling for DTML pages
===================================

When an HTML File page containing a head tag is visited, without a
trailing slash, the base href isn't set.  When visited with a slash,
it is:

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.contentType', 'text/html'),
  ...     ('UPDATE_SUBMIT', 'Add'),
  ...     ('add_input_name', 'file.html')],
  ...    [('field.data', '', b'', 'application/octet-stream')])
  >>> print(http(b"""
  ... POST /+/zope.app.file.File%%3D HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... Content-Type: %b
  ... Referer: http://localhost:8081/+/zope.app.file.File=
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 303 See Other
  ...

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.contentType', 'text/html'),
  ...     ('field.data', b'<html>\n<head></head>\n<body>\n<a href="eek.html">Eek</a>\n</body>\n</html>'),
  ...     ('UPDATE_SUBMIT', 'Change')])
  >>> print(http(b"""
  ... POST /file.html/edit.html HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... Content-Type: %b
  ... Referer: http://localhost:8081/file.html/edit.html
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 200 Ok
  ...

  >>> print(http(b"""
  ... GET /file.html HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... """))
  HTTP/1.1 200 Ok
  ...
  <html>
  <head></head>
  <body>
  <a href="eek.html">Eek</a>
  </body>
  </html>


  >>> print(http(b"""
  ... GET /file.html/ HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... """))
  HTTP/1.1 200 Ok
  ...
  <html>
  <head>
  <base href="http://localhost/file.html" />
  </head>
  <body>
  <a href="eek.html">Eek</a>
  </body>
  </html>
