File objects
============

Adding Files
------------

You can add File objects from the common tasks menu in the ZMI.

  >>> result = http(b"""
  ... GET /@@contents.html HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... """)
  >>> "http://localhost/@@+/action.html?type_name=zope.app.file.File" in str(result)
  True

Let's follow that link.

  >>> print(http(b"""
  ... GET /@@+/action.html?type_name=zope.app.file.File HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... """, handle_errors=False))
  HTTP/1.1 303 See Other
  Content-Length: ...
  Location: http://localhost/+/zope.app.file.File=
  <BLANKLINE>

The file add form lets you specify the content type, the object name, and
optionally upload the contents of the file.

  >>> print(http(b"""
  ... GET /+/zope.app.file.File= HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... """))
  HTTP/1.1 200 Ok
  Content-Length: ...
  Content-Type: text/html;charset=utf-8
  <BLANKLINE>
  ...
      <title>Z3: +</title>
  ...
  ...
    <form action="http://localhost/+/zope.app.file.File%3D"
          method="post" enctype="multipart/form-data">
      <h3>Add a File</h3>
      ...<input class="textType" id="field.contentType"
                name="field.contentType" size="20" type="text" value="" />...
      ...<input class="fileType" id="field.data" name="field.data" size="20"
                type="file" />...
        <div class="controls"><hr />
          <input type="submit" value="Refresh" />
          <input type="submit" value="Add"
                 name="UPDATE_SUBMIT" />
          &nbsp;&nbsp;<b>Object Name</b>&nbsp;&nbsp;
          <input type="text" name="add_input_name" value="" />
        </div>
  ...
    </form>
  ...

Binary Files
------------

Let us upload a binary file.

  >>> hello_txt_gz = (
  ...     b'\x1f\x8b\x08\x08\xcb\x48\xea\x42\x00\x03\x68\x65\x6c\x6c\x6f\x2e'
  ...     b'\x74\x78\x74\x00\xcb\x48\xcd\xc9\xc9\xe7\x02\x00\x20\x30\x3a\x36'
  ...     b'\x06\x00\x00\x00')

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.contentType', 'application/octet-stream'),
  ...     ('UPDATE_SUBMIT', 'Add'),
  ...     ('add_input_name', '')],
  ...    [('field.data', 'hello.txt.gz', hello_txt_gz, 'application/x-gzip')])
  >>> print(http(b"""
  ... POST /+/zope.app.file.File%%3D HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... Content-Type: %b
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 303 See Other
  Content-Length: ...
  Content-Type: text/html;charset=utf-8
  Location: http://localhost/@@contents.html
  <BLANKLINE>
  ...

Since we did not specify the object name in the form, Zope 3 will use the
filename.

  >>> response = http(b"""
  ... GET /hello.txt.gz HTTP/1.1
  ... """)
  >>> print(response)
  HTTP/1.1 200 Ok
  Content-Length: 36
  Content-Type: application/octet-stream
  <BLANKLINE>
  ...

Let's make sure the (binary) content of the file is correct

  >>> response.getBody() == hello_txt_gz
  True

Also, lets test a (bad) filename with full path that generates MS Internet Explorer,
Zope should process it successfully and get the actual filename. Let's upload the
same file with bad filename.

  >>> test_gz = (
  ...   b'\x1f\x8b\x08\x08\xcb\x48\xea\x42\x00\x03\x68\x65\x6c\x6c\x6f\x2e'
  ...   b'\x74\x78\x74\x00\xcb\x48\xcd\xc9\xc9\xe7\x02\x00\x20\x30\x3a\x36'
  ...   b'\x06\x00\x00\x00')
  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.contentType', 'application/octet-stream'),
  ...     ('UPDATE_SUBMIT', 'Add'),
  ...     ('add_input_name', '')],
  ...    [('field.data', 'c:\\windows\\test.gz', test_gz, 'application/x-gzip')])
  >>> print(http(b"""
  ... POST /+/zope.app.file.File%%3D HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... Content-Type: %b
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 303 See Other
  Content-Length: ...
  Content-Type: text/html;charset=utf-8
  Location: http://localhost/@@contents.html
  <BLANKLINE>
  ...

The file should be saved as "test.gz", let's check it name and contents.

  >>> response = http(b"""
  ... GET /test.gz HTTP/1.1
  ... """)
  >>> print(response)
  HTTP/1.1 200 Ok
  Content-Length: 36
  Content-Type: application/octet-stream
  <BLANKLINE>
  ...


  >>> response.getBody() == test_gz
  True

Text Files
----------

Let us now create a text file.

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.contentType', 'text/plain'),
  ...     ('UPDATE_SUBMIT', 'Add'),
  ...     ('add_input_name', 'sample.txt')],
  ...    [('field.data', '', b'', 'application/octet-stream')])
  >>> print(http(b"""
  ... POST /+/zope.app.file.File%%3D HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... Content-Type: %b
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 303 See Other
  Content-Length: ...
  Content-Type: text/html;charset=utf-8
  Location: http://localhost/@@contents.html
  <BLANKLINE>
  ...

The file is initially empty, since we did not upload anything.

  >>> print(http(b"""
  ... GET /sample.txt HTTP/1.1
  ... """))
  HTTP/1.1 200 Ok
  Content-Length: 0
  Content-Type: text/plain
  Last-Modified: ...
  <BLANKLINE>

Since it is a text file, we can edit it directly in a web form.

  >>> print(http(b"""
  ... GET /sample.txt/edit.html HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... """, handle_errors=False))
  HTTP/1.1 200 Ok
  Content-Length: ...
  Content-Type: text/html;charset=utf-8
  <BLANKLINE>
  ...
      <title>Z3: sample.txt</title>
  ...
      <form action="http://localhost/sample.txt/edit.html"
            method="post" enctype="multipart/form-data">
        <div>
          <h3>Change a file</h3>
  ...<input class="textType" id="field.contentType" name="field.contentType"
            size="20" type="text" value="text/plain"  />...
  ...<textarea cols="60" id="field.data" name="field.data" rows="15" ></textarea>...
  ...
          <div class="controls">
            <input type="submit" value="Refresh" />
            <input type="submit" name="UPDATE_SUBMIT"
                   value="Change" />
          </div>
  ...
      </form>
  ...

Files of type text/plain without any charset information can contain UTF-8 text.
So you can use ASCII text.

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.contentType', 'text/plain'),
  ...     ('field.data', 'This is a sample text file.\n\nIt can contain US-ASCII characters.'),
  ...     ('UPDATE_SUBMIT', 'Change')])
  >>> print(http(b"""
  ... POST /sample.txt/edit.html HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... Content-Type: %b
  ...
  ... %b
  ... """ % (content_type, content), handle_errors=False))
  HTTP/1.1 200 Ok
  Content-Length: ...
  Content-Type: text/html;charset=utf-8
  <BLANKLINE>
  ...
      <title>Z3: sample.txt</title>
  ...
      <form action="http://localhost/sample.txt/edit.html"
            method="post" enctype="multipart/form-data">
        <div>
          <h3>Change a file</h3>
  <BLANKLINE>
          <p>Updated on ...</p>
  <BLANKLINE>
        <div class="row">
  ...<input class="textType" id="field.contentType" name="field.contentType"
            size="20" type="text" value="text/plain"  />...
        <div class="row">
  ...<textarea cols="60" id="field.data" name="field.data" rows="15"
  >This is a sample text file.
  <BLANKLINE>
  It can contain US-ASCII characters.</textarea></div>
  ...
          <div class="controls">
            <input type="submit" value="Refresh" />
            <input type="submit" name="UPDATE_SUBMIT"
                   value="Change" />
          </div>
  ...
      </form>
  ...

Here's the file

  >>> print(http(b"""
  ... GET /sample.txt HTTP/1.1
  ... """))
  HTTP/1.1 200 Ok
  Content-Length: ...
  Content-Type: text/plain
  Last-Modified: ...
  <BLANKLINE>
  This is a sample text file.
  <BLANKLINE>
  It can contain US-ASCII characters.


Non-ASCII Text Files
--------------------

We can also use non-ASCII charactors in text file.

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.contentType', 'text/plain'),
  ...     ('field.data', 'This is a sample text file.\n\nIt can contain non-ASCII(UTF-8) characters, e.g. \u263B (U+263B BLACK SMILING FACE).'),
  ...     ('UPDATE_SUBMIT', 'Change')])
  >>> print(http(b"""
  ... POST /sample.txt/edit.html HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... Content-Type: %b
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 200 Ok
  Content-Length: ...
  Content-Type: text/html;charset=utf-8
  <BLANKLINE>
  ...
      <title>Z3: sample.txt</title>
  ...
      <form action="http://localhost/sample.txt/edit.html"
            method="post" enctype="multipart/form-data">
        <div>
          <h3>Change a file</h3>
  <BLANKLINE>
          <p>Updated on ...</p>
  <BLANKLINE>
        <div class="row">
  ...<input class="textType" id="field.contentType" name="field.contentType"
            size="20" type="text" value="text/plain"  />...
        <div class="row">
  ...<textarea cols="60" id="field.data" name="field.data" rows="15"
  >This is a sample text file.
  <BLANKLINE>
  It can contain non-ASCII(UTF-8) characters, e.g. ... (U+263B BLACK SMILING FACE).</textarea></div>
  ...
          <div class="controls">
            <input type="submit" value="Refresh" />
            <input type="submit" name="UPDATE_SUBMIT"
                   value="Change" />
          </div>
  ...
      </form>
  ...

Here's the file

  >>> response = http(b"""
  ... GET /sample.txt HTTP/1.1
  ... """)
  >>> print(response)
  HTTP/1.1 200 Ok
  Content-Length: ...
  Content-Type: text/plain
  Last-Modified: ...
  <BLANKLINE>
  This is a sample text file.
  <BLANKLINE>
  It can contain non-ASCII(UTF-8) characters, e.g. ... (U+263B BLACK SMILING FACE).

  >>> u'\u263B' in response.getBody().decode('UTF-8')
  True

And you can explicitly specify the charset. Note that the browser form is always UTF-8.

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.contentType', 'text/plain; charset=ISO-8859-1'),
  ...     ('field.data', 'This is a sample text file.\n\nIt now contains Latin-1 characters, e.g. \xa7 (U+00A7 SECTION SIGN).'),
  ...     ('UPDATE_SUBMIT', 'Change')])
  >>> print(http(b"""
  ... POST /sample.txt/edit.html HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... Content-Type: %b
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 200 Ok
  Content-Length: ...
  Content-Type: text/html;charset=utf-8
  <BLANKLINE>
  ...
      <title>Z3: sample.txt</title>
  ...
      <form action="http://localhost/sample.txt/edit.html"
            method="post" enctype="multipart/form-data">
        <div>
          <h3>Change a file</h3>
  <BLANKLINE>
          <p>Updated on ...</p>
  <BLANKLINE>
        <div class="row">
  ...<input class="textType" id="field.contentType" name="field.contentType"
            size="20" type="text" value="text/plain; charset=ISO-8859-1"  />...
        <div class="row">
  ...<textarea cols="60" id="field.data" name="field.data" rows="15"
  >This is a sample text file.
  <BLANKLINE>
  It now contains Latin-1 characters, e.g. ... (U+00A7 SECTION SIGN).</textarea></div>
  ...
          <div class="controls">
            <input type="submit" value="Refresh" />
            <input type="submit" name="UPDATE_SUBMIT"
                   value="Change" />
          </div>
  ...
      </form>
  ...

Here's the file

  >>> response = http(b"""
  ... GET /sample.txt HTTP/1.1
  ... """)
  >>> print(response)
  HTTP/1.1 200 Ok
  Content-Length: ...
  Content-Type: text/plain; charset=ISO-8859-1
  Last-Modified: ...
  <BLANKLINE>
  This is a sample text file.
  <BLANKLINE>
  It now contains Latin-1 characters, e.g. ... (U+00A7 SECTION SIGN).

Body is actually encoded in ISO-8859-1, and not UTF-8

  >>> response.getBody().splitlines()[-1].decode('latin-1')
  'It now contains Latin-1 characters, e.g. \xa7 (U+00A7 SECTION SIGN).'

The user is not allowed to specify a character set that cannot represent all
the characters.

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.contentType', 'text/plain; charset=US-ASCII'),
  ...     ('field.data', 'This is a slightly changed sample text file.\n\nIt now contains Latin-1 characters, e.g. \xa7 (U+00A7 SECTION SIGN).'),
  ...     ('UPDATE_SUBMIT', 'Change')])
  >>> print(http(b"""
  ... POST /sample.txt/edit.html HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... Content-Type: %b
  ...
  ... %b
  ... """ % (content_type, content), handle_errors=False))
  HTTP/1.1 200 Ok
  Content-Length: ...
  Content-Type: text/html;charset=utf-8
  <BLANKLINE>
  ...
      <title>Z3: sample.txt</title>
  ...
      <form action="http://localhost/sample.txt/edit.html"
            method="post" enctype="multipart/form-data">
        <div>
          <h3>Change a file</h3>
  <BLANKLINE>
          <p>The character set you specified (US-ASCII) cannot encode all characters in text.</p>
  <BLANKLINE>
        <div class="row">
  ...<input class="textType" id="field.contentType" name="field.contentType" size="20" type="text" value="text/plain; charset=US-ASCII"  />...
        <div class="row">
  ...<textarea cols="60" id="field.data" name="field.data" rows="15" >This is a slightly changed sample text file.
  <BLANKLINE>
  It now contains Latin-1 characters, e.g. ... (U+00A7 SECTION SIGN).</textarea></div>
  ...
          <div class="controls">
            <input type="submit" value="Refresh" />
            <input type="submit" name="UPDATE_SUBMIT"
                   value="Change" />
          </div>
  ...
      </form>
  ...

Likewise, the user is not allowed to specify a character set that is not supported by Python.

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.contentType', 'text/plain; charset=I-INVENT-MY-OWN'),
  ...     ('field.data', 'This is a slightly changed sample text file.\n\nIt now contains just ASCII characters.'),
  ...     ('UPDATE_SUBMIT', 'Change')])
  >>> print(http(b"""
  ... POST /sample.txt/edit.html HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... Content-Type: %b
  ...
  ... %b
  ... """ % (content_type, content), handle_errors=False))
  HTTP/1.1 200 Ok
  Content-Length: ...
  Content-Type: text/html;charset=utf-8
  <BLANKLINE>
  ...
      <title>Z3: sample.txt</title>
  ...
      <form action="http://localhost/sample.txt/edit.html"
            method="post" enctype="multipart/form-data">
        <div>
          <h3>Change a file</h3>
  <BLANKLINE>
          <p>The character set you specified (I-INVENT-MY-OWN) is not supported.</p>
  <BLANKLINE>
        <div class="row">
  ...<input class="textType" id="field.contentType" name="field.contentType" size="20" type="text" value="text/plain; charset=I-INVENT-MY-OWN"  />...
        <div class="row">
  ...<textarea cols="60" id="field.data" name="field.data" rows="15" >This is a slightly changed sample text file.
  <BLANKLINE>
  It now contains just ASCII characters.</textarea></div>
  ...
          <div class="controls">
            <input type="submit" value="Refresh" />
            <input type="submit" name="UPDATE_SUBMIT"
                   value="Change" />
          </div>
  ...
      </form>
  ...

If you trick Zope and upload a file with a content type that does not
match the file contents, you will not be able to access the edit view:

  >>> print(http(b"""
  ... GET /hello.txt.gz/@@edit.html HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... """, handle_errors=True))
  HTTP/1.1 200 Ok
  Content-Length: ...
  Content-Type: text/html;charset=utf-8
  <BLANKLINE>
  ...
     <li>The character set specified in the content type (UTF-8) does not match file content.</li>
  ...

Non-ASCII Filenames
-------------------

Filenames are not restricted to ASCII.

  >>> björn_txt_gz = (
  ...     b'\x1f\x8b\x08\x08\xcb\x48\xea\x42\x00\x03\x68\x65\x6c\x6c\x6f\x2e'
  ...     b'\x74\x78\x74\x00\xcb\x48\xcd\xc9\xc9\xe7\x02\x00\x20\x30\x3a\x36'
  ...     b'\x06\x00\x00\x00')
  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.contentType', 'application/octet-stream'),
  ...     ('UPDATE_SUBMIT', 'Add'),
  ...     ('add_input_name', '')],
  ...    [('field.data', 'björn.txt.gz', björn_txt_gz, 'application/x-gzip')])
  >>> print(http(b"""
  ... POST /+/zope.app.file.File%%3D HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... Content-Type: %b
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 303 See Other
  Content-Length: ...
  Content-Type: text/html;charset=utf-8
  Location: http://localhost/@@contents.html
  <BLANKLINE>
  ...

Since we did not specify the object name in the form, Zope 3 will use the
filename.

  >>> response = http(b"""
  ... GET /bj%C3%B6rn.txt.gz HTTP/1.1
  ... """)
  >>> print(response)
  HTTP/1.1 200 Ok
  Content-Length: 36
  Content-Type: application/octet-stream
  Last-Modified: ...
  <BLANKLINE>
  ...
