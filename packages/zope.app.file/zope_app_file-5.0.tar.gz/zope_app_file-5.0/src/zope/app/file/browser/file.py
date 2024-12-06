##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""File views.

"""

from datetime import datetime

import zope.contenttype.parse
import zope.datetime
import zope.event
from zope.contenttype import guess_content_type
from zope.dublincore.interfaces import IDCTimes
from zope.exceptions.interfaces import UserError
from zope.schema import Text

from zope import lifecycleevent
from zope.app.file.file import File
from zope.app.file.i18n import ZopeMessageFactory as _
from zope.app.file.interfaces import IFile


__docformat__ = 'restructuredtext'


class FileView:

    request = None
    context = None

    def show(self):
        """Sets various headers if the request is present and returns the
        data of the file. If the "If-Modified-Since" header is set and
        the context is adaptable to IDCTimes, data is only returned if
        the modification date of the context is newer than the date in the
        "If-Modified-Since" header
        >>> from zope.publisher.browser import BrowserView, TestRequest
        >>> class FileTestView(FileView, BrowserView): pass
        >>> import pytz
        >>> class MyFile(object):
        ...     contentType = 'text/plain'
        ...     data = b"data of file"
        ...     modified = datetime(2006,1,1,tzinfo=pytz.utc)
        ...     def getSize(self):
        ...         return len(self.data)

        >>> aFile = MyFile()
        >>> request = TestRequest()
        >>> view = FileTestView(aFile,request)
        >>> view.show() == MyFile.data
        True
        >>> request.response.getHeader('Content-Type')
        'text/plain'
        >>> request.response.getHeader('Content-Length')
        '12'

        If the file is adaptable to IDCTimes the "Last-Modified" header is also
        set.

        >>> request.response.getHeader('Last-Modified') is None
        True

        For the test we just declare that our file provides
        IZopeDublinCore
        >>> from zope.dublincore.interfaces import IZopeDublinCore
        >>> from zope.interface import directlyProvides
        >>> directlyProvides(aFile,IZopeDublinCore)
        >>> request = TestRequest()
        >>> view = FileTestView(aFile,request)
        >>> view.show() == MyFile.data
        True
        >>> request.response.getHeader('Last-Modified')
        'Sun, 01 Jan 2006 00:00:00 GMT'

        If the "If-Modified-Since" header is set and is newer a 304
        status is returned and the value is empty.

        >>> modified = datetime(2007,12,31,tzinfo=pytz.utc)
        >>> modHeader = zope.datetime.rfc1123_date(
        ...     zope.datetime.time(modified.isoformat()))
        >>> request = TestRequest(IF_MODIFIED_SINCE=modHeader)

        >>> view = FileTestView(aFile,request)
        >>> view.show() == b''
        True
        >>> request.response.getStatus()
        304

        An invalid value for that header is ignored.
        >>> request = TestRequest(IF_MODIFIED_SINCE="Not Valid")

        >>> view = FileTestView(aFile,request)
        >>> view.show() == MyFile.data
        True

        """

        if self.request is not None:
            self.request.response.setHeader('Content-Type',
                                            self.context.contentType)
            self.request.response.setHeader('Content-Length',
                                            self.context.getSize())
        try:
            modified = IDCTimes(self.context).modified
        except TypeError:
            modified = None
        if modified is None or not isinstance(modified, datetime):
            return self.context.data

        header = self.request.getHeader('If-Modified-Since', None)
        lmt = zope.datetime.time(modified.isoformat())
        if header is not None:
            header = header.split(';')[0]
            try:
                mod_since = int(zope.datetime.time(header))
            except zope.datetime.SyntaxError:
                mod_since = None
            if mod_since is not None:
                if lmt <= mod_since:
                    self.request.response.setStatus(304)
                    return b''
        self.request.response.setHeader('Last-Modified',
                                        zope.datetime.rfc1123_date(lmt))

        return self.context.data


def cleanupFileName(filename):
    return filename.split('\\')[-1].split('/')[-1]


class FileUpdateView:

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def errors(self):
        form = self.request.form
        if "UPDATE_SUBMIT" in form:
            filename = getattr(form["field.data"], "filename", None)
            contenttype = form.get("field.contentType")
            if filename:
                filename = cleanupFileName(filename)
                if not contenttype:
                    contenttype = guess_content_type(filename)[0]
                if not form.get("add_input_name"):
                    form["add_input_name"] = filename
            return self.update_object(form["field.data"], contenttype)
        return ''


class FileAdd(FileUpdateView):
    """View that adds a new File object based on a file upload.

    >>> class FauxAdding(object):
    ...     def add(self, content):
    ...         self.content = content
    ...     def nextURL(self):
    ...         return 'next url'

    >>> from zope.publisher.browser import TestRequest
    >>> from io import BytesIO
    >>> sio = BytesIO(b"some data")
    >>> sio.filename = 'abc.txt'

    Let's make sure we can use the uploaded file name if one isn't
    specified by the user, and can use the content type when
    specified.

    >>> request = TestRequest(form={'field.data': sio,
    ...                             'field.contentType': 'text/foobar',
    ...                             'UPDATE_SUBMIT': 'Add'})
    >>> adding = FauxAdding()
    >>> view = FileAdd(adding, request)
    >>> view.errors()
    ''
    >>> adding.content.contentType
    'text/foobar'
    >>> adding.content.data == b'some data'
    True
    >>> request.form['add_input_name']
    'abc.txt'

    Now let's guess the content type, but also use a provided file
    name for adding the new content object:

    >>> request = TestRequest(form={'field.data': sio,
    ...                             'field.contentType': '',
    ...                             'add_input_name': 'splat.txt',
    ...                             'UPDATE_SUBMIT': 'Add'})
    >>> adding = FauxAdding()
    >>> view = FileAdd(adding, request)
    >>> view.errors()
    ''
    >>> adding.content.contentType
    'text/plain'
    >>> request.form['add_input_name']
    'splat.txt'

    """

    def update_object(self, data, contenttype):
        f = File(data, contenttype)
        zope.event.notify(lifecycleevent.ObjectCreatedEvent(f))
        self.context.add(f)
        self.request.response.redirect(self.context.nextURL())
        return ''


class FileUpload(FileUpdateView):
    """View that updates an existing File object with a new upload.
        Fires an ObjectModifiedEvent.


    >>> from zope.publisher.browser import TestRequest
    >>> from io import BytesIO
    >>> sio = BytesIO(b"some data")
    >>> sio.filename = 'abc.txt'

    Before we instanciate the request, we need to make sure that the
    ``IUserPreferredLanguages`` adapter exists, so that the request's
    locale exists.  This is necessary because the ``update_object``
    method uses the locale formatter for the status message:

    >>> from zope import component as ztapi
    >>> from zope.publisher.browser import BrowserLanguages
    >>> from zope.publisher.interfaces.http import IHTTPRequest
    >>> from zope.i18n.interfaces import IUserPreferredLanguages
    >>> ztapi.provideAdapter(
    ...     BrowserLanguages, (IHTTPRequest,), IUserPreferredLanguages)

    We install an event logger so we can see the events generated:

    >>> def eventLog(event):
    ...     print('ModifiedEvent:', event.descriptions[0].attributes)
    >>> zope.event.subscribers.append(eventLog)

    Let's make sure we can use the uploaded file name if one isn't
    specified by the user, and can use the content type when
    specified.


    >>> request = TestRequest(form={'field.data': sio,
    ...                             'field.contentType': 'text/foobar',
    ...                             'UPDATE_SUBMIT': 'Update'})
    >>> file = File()
    >>> view = FileUpload(file, request)
    >>> view.errors()
    ModifiedEvent: ('contentType', 'data')
    'Updated on ${date_time}'
    >>> file.contentType
    'text/foobar'
    >>> file.data == b'some data'
    True

    Now let's guess the content type, but also use a provided file
    name for adding the new content object:

    >>> request = TestRequest(form={'field.data': sio,
    ...                             'field.contentType': '',
    ...                             'add_input_name': 'splat.txt',
    ...                             'UPDATE_SUBMIT': 'Update'})
    >>> file = File()
    >>> view = FileUpload(file, request)
    >>> view.errors()
    ModifiedEvent: ('contentType', 'data')
    'Updated on ${date_time}'
    >>> file.contentType
    'text/plain'

    The ObjectModifiedEvent lists only the contentType if the data
    are omitted:

    >>> request = TestRequest(form={'field.data': None,
    ...                             'field.contentType': '',
    ...                             'add_input_name': 'splat.txt',
    ...                             'UPDATE_SUBMIT': 'Update'})
    >>> file = File()
    >>> view = FileUpload(file, request)
    >>> view.errors()
    ModifiedEvent: ('contentType',)
    'Updated on ${date_time}'


    Cleanup:

    >>> zope.event.subscribers.remove(eventLog)

    """

    def update_object(self, data, contenttype):
        self.context.contentType = contenttype

        descriptor = lifecycleevent.Attributes(IFile, "contentType")

        # Update *only* if a new value is specified
        if data:
            self.context.data = data
            descriptor.attributes += ("data",)

        event = lifecycleevent.ObjectModifiedEvent(self.context, descriptor)
        zope.event.notify(event)

        formatter = self.request.locale.dates.getFormatter(
            'dateTime', 'medium')
        return _("Updated on ${date_time}",
                 mapping={'date_time': formatter.format(datetime.utcnow())})


class IFileEditForm(IFile):
    """Schema for the File edit form.

    Replaces the Bytes `data` field with a Text field.
    """

    data = Text(
        title=_('Data'),
        description=_('The actual content of the object.'),
        default='',
        missing_value='',
        required=False,
    )


class UnknownCharset(Exception):
    """Unknown character set."""


class CharsetTooWeak(Exception):
    """Character set cannot encode all characters in text."""


class FileEdit:
    r"""File edit form mixin.

    Lets the user edit a text file directly via a browser form.

    Converts between Unicode strings used in browser forms and 8-bit strings
    stored internally.

        >>> from zope.publisher.browser import BrowserView, TestRequest
        >>> class FileEditView(FileEdit, BrowserView): pass
        >>> view = FileEditView(File(), TestRequest())
        >>> view.getData()['data']
        ''
        >>> view.getData()['contentType']
        ''

        We install an event logger so we can see the events generated.

        >>> def eventLog(event):
        ...    print(event.__class__.__name__,
        ...          event.descriptions[0].attributes)
        >>> zope.event.subscribers.append(eventLog)

        >>> view.setData({'contentType': 'text/plain; charset=ISO-8859-13',
        ...               'data': 'text \u0105'}) # doctest:+ELLIPSIS
        ObjectModifiedEvent ('data', 'contentType')
        'Updated on ${date_time}'

        >>> view.context.contentType
        'text/plain; charset=ISO-8859-13'
        >>> view.context.data == b'text \xe0'
        True

        >>> view.getData()['data']
        'text \u0105'

        Cleanup eventlog.

        >>> zope.event.subscribers.remove(eventLog)

    You will get an error if you try to specify a charset that cannot encode
    all the characters

        >>> view.setData({'contentType': 'text/xml; charset=ISO-8859-1',
        ...               'data': 'text \u0105'})
        Traceback (most recent call last):
          ...
        zope.app.file.browser.file.CharsetTooWeak: ISO-8859-1

    You will get a different error if you try to specify an invalid charset

        >>> view.setData({'contentType': 'text/xml; charset=UNKNOWN',
        ...               'data': 'text \u0105'})
        Traceback (most recent call last):
          ...
        zope.app.file.browser.file.UnknownCharset: UNKNOWN

    The update method catches those errors and replaces them with error
    messages

        >>> from zope.i18n import translate
        >>> class FakeFormView(BrowserView):
        ...     def update(self):
        ...         raise CharsetTooWeak('ASCII')
        >>> class FileEditView(FileEdit, FakeFormView): pass
        >>> view = FileEditView(File(), TestRequest())
        >>> translate(view.update())
        'The character set you specified (ASCII) cannot encode all characters in text.'
        >>> translate(view.update_status)
        'The character set you specified (ASCII) cannot encode all characters in text.'

        >>> class FakeFormView(BrowserView):
        ...     def update(self):
        ...         raise UnknownCharset('UNKNOWN')
        >>> class FileEditView(FileEdit, FakeFormView): pass
        >>> view = FileEditView(File(), TestRequest())
        >>> translate(view.update())
        'The character set you specified (UNKNOWN) is not supported.'
        >>> translate(view.update_status)
        'The character set you specified (UNKNOWN) is not supported.'

    Speaking about errors, if you trick the system and upload a file with
    incorrect charset designation, you will get a UserError when you visit the
    view:

        >>> view.context.contentType = 'text/plain; charset=UNKNOWN'
        >>> view.context.data = b'\xff'
        >>> view.getData()
        Traceback (most recent call last):
          ...
        zope.exceptions.interfaces.UserError: The character set specified in the content type ($charset) is not supported.

        >>> view.context.contentType = 'text/plain; charset=UTF-8'
        >>> view.context.data = b'\xff'
        >>> view.getData()
        Traceback (most recent call last):
          ...
        zope.exceptions.interfaces.UserError: The character set specified in the content type ($charset) does not match file content.

    """  # noqa: E501 line too long
    context = None
    request = None
    error = None

    def getData(self):
        charset = extractCharset(self.context.contentType)
        try:
            return {'contentType': self.context.contentType,
                    'data': self.context.data.decode(charset)}
        except LookupError:
            msg = _("The character set specified in the content type"
                    " ($charset) is not supported.",
                    mapping={'charset': charset})
            raise UserError(msg)
        except UnicodeDecodeError:
            msg = _("The character set specified in the content type"
                    " ($charset) does not match file content.",
                    mapping={'charset': charset})
            raise UserError(msg)

    def setData(self, data):
        charset = extractCharset(data['contentType'])
        try:
            encodeddata = data['data'].encode(charset)
        except LookupError:
            raise UnknownCharset(charset)
        except UnicodeEncodeError:
            raise CharsetTooWeak(charset)

        modified = []
        if encodeddata != self.context.data:
            self.context.data = encodeddata
            modified.append('data')

        if self.context.contentType != data['contentType']:
            self.context.contentType = data['contentType']
            modified.append('contentType')
        formatter = self.request.locale.dates.getFormatter('dateTime',
                                                           'medium')
        if modified:
            event = lifecycleevent.ObjectModifiedEvent(
                self.context,
                lifecycleevent.Attributes(IFile, *modified))
            zope.event.notify(event)

        return _("Updated on ${date_time}",
                 mapping={'date_time': formatter.format(datetime.utcnow())})

    def update(self):
        try:
            return super().update()
        except CharsetTooWeak as charset:
            self.update_status = _("The character set you specified ($charset)"
                                   " cannot encode all characters in text.",
                                   mapping={'charset': charset})
            return self.update_status
        except UnknownCharset as charset:
            self.update_status = _("The character set you specified ($charset)"
                                   " is not supported.",
                                   mapping={'charset': charset})
            return self.update_status


def extractCharset(content_type):
    """Extract charset information from a MIME type.

        >>> extractCharset('text/plain; charset=US-ASCII')
        'US-ASCII'
        >>> extractCharset('text/html; charset=ISO-8859-1')
        'ISO-8859-1'
        >>> extractCharset('text/plain')
        'UTF-8'

    """
    if content_type and content_type.strip():
        _major, _minor, params = zope.contenttype.parse.parse(content_type)
        return params.get("charset", "UTF-8")

    return "UTF-8"
