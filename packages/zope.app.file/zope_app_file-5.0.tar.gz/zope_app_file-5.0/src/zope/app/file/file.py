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
"""File content component
"""
__docformat__ = 'restructuredtext'

import transaction
import zope.app.publication.interfaces
from persistent import Persistent
from zope.interface import implementer

from zope.app.file import interfaces


# set the size of the chunks
MAXCHUNKSIZE = 1 << 16

try:
    text_type = unicode
except NameError:
    text_type = str


@implementer(zope.app.publication.interfaces.IFileContent,
             interfaces.IFile)
class File(Persistent):
    """A persistent content component storing binary file data

    Let's test the constructor:

    >>> file = File()
    >>> file.contentType
    ''
    >>> file.data == b''
    True

    >>> file = File(b'Foobar')
    >>> file.contentType
    ''
    >>> file.data == b'Foobar'
    True

    >>> file = File(b'Foobar', 'text/plain')
    >>> file.contentType
    'text/plain'
    >>> file.data == b'Foobar'
    True

    >>> file = File(data=b'Foobar', contentType='text/plain')
    >>> file.contentType
    'text/plain'
    >>> file.data == b'Foobar'
    True


    Let's test the mutators:

    >>> file = File()
    >>> file.contentType = 'text/plain'
    >>> file.contentType
    'text/plain'

    >>> file.data = b'Foobar'
    >>> file.data == b'Foobar'
    True

    >>> file.data = None
    Traceback (most recent call last):
    ...
    TypeError: Cannot set None data on a file.


    Let's test large data input:

    >>> file = File()

    Insert as string:

    >>> file.data = b'Foobar'*60000
    >>> file.getSize()
    360000
    >>> file.data == b'Foobar'*60000
    True

    Insert data as FileChunk:

    >>> fc = FileChunk(b'Foobar'*4000)
    >>> file.data = fc
    >>> file.getSize()
    24000
    >>> file.data == b'Foobar'*4000
    True

    Insert data from file object:

    >>> from io import BytesIO
    >>> sio = BytesIO()
    >>> _ = sio.write(b'Foobar'*100000)
    >>> _ = sio.seek(0)
    >>> file.data = sio
    >>> file.getSize() == 600000
    True
    >>> file.data == b'Foobar'*100000
    True


    Last, but not least, verify the interface:

    >>> from zope.interface.verify import verifyClass
    >>> interfaces.IFile.implementedBy(File)
    True
    >>> verifyClass(interfaces.IFile, File)
    True
    """

    _data = None
    _size = 0

    def __init__(self, data=b'', contentType=''):
        self.data = data
        self.contentType = contentType

    def _getData(self):
        if isinstance(self._data, FileChunk):
            return bytes(self._data)
        return self._data

    def _setData(self, data):

        # Handle case when data is a string
        if isinstance(data, text_type):
            data = data.encode('UTF-8')

        if isinstance(data, bytes):
            self._data, self._size = FileChunk(data), len(data)
            return

        # Handle case when data is None
        if data is None:
            raise TypeError('Cannot set None data on a file.')

        # Handle case when data is already a FileChunk
        if isinstance(data, FileChunk):
            size = len(data)
            self._data, self._size = data, size
            return

        # Handle case when data is a file object
        seek = data.seek
        read = data.read

        seek(0, 2)
        size = end = data.tell()

        if size <= 2 * MAXCHUNKSIZE:
            seek(0)
            if size < MAXCHUNKSIZE:
                self._data, self._size = read(size), size
                return
            self._data, self._size = FileChunk(read(size)), size
            return

        # Make sure we have an _p_jar, even if we are a new object, by
        # doing a sub-transaction commit.
        transaction.savepoint(optimistic=True)

        jar = self._p_jar

        if jar is None:
            # Ugh
            seek(0)
            self._data, self._size = FileChunk(read(size)), size
            return

        # Now we're going to build a linked list from back
        # to front to minimize the number of database updates
        # and to allow us to get things out of memory as soon as
        # possible.
        next = None
        while end > 0:
            pos = end - MAXCHUNKSIZE
            if pos < MAXCHUNKSIZE:
                pos = 0  # we always want at least MAXCHUNKSIZE bytes
            seek(pos)
            data = FileChunk(read(end - pos))

            # Woooop Woooop Woooop! This is a trick.
            # We stuff the data directly into our jar to reduce the
            # number of updates necessary.
            jar.add(data)

            # This is needed and has side benefit of getting
            # the thing registered:
            data.next = next

            # Now make it get saved in a sub-transaction!
            transaction.savepoint(optimistic=True)

            # Now make it a ghost to free the memory.  We
            # don't need it anymore!
            data._p_changed = None

            next = data
            end = pos

        self._data, self._size = next, size
        return

    def getSize(self):
        '''See `IFile`'''
        return self._size

    # See IFile.
    data = property(_getData, _setData)


class FileChunk(Persistent):
    """Wrapper for possibly large data"""

    next = None

    def __init__(self, data):
        self._data = data

    def __getitem__(self, i):
        return self._data[i]

    def __len__(self):
        data = bytes(self)
        return len(data)

    def __bytes__(self):
        next = self.next
        if next is None:
            return self._data

        result = [self._data]
        while next is not None:
            self = next
            result.append(self._data)
            next = self.next

        return b''.join(result)

    if str is bytes:
        __str__ = __bytes__
    else:
        def __str__(self):
            return self.__bytes__().decode("iso-8859-1", errors='ignore')


class FileReadFile:
    '''Adapter for file-system style read access.

    >>> file = File()
    >>> content = b"This is some file\\ncontent."
    >>> file.data = content
    >>> file.contentType = "text/plain"
    >>> FileReadFile(file).read() == content
    True
    >>> FileReadFile(file).size() == len(content)
    True
    '''

    def __init__(self, context):
        self.context = context

    def read(self):
        return self.context.data

    def size(self):
        return len(self.context.data)


class FileWriteFile:
    """Adapter for file-system style write access.

    >>> file = File()
    >>> content = b"This is some file\\ncontent."
    >>> FileWriteFile(file).write(content)
    >>> file.data == content
    True
    """

    def __init__(self, context):
        self.context = context

    def write(self, data):
        self.context.data = data
