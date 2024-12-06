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
"""Image content type implementation

"""
__docformat__ = 'restructuredtext'

import struct
from io import BytesIO

from zope.contenttype import guess_content_type
from zope.interface import implementer
from zope.size import byteDisplay
from zope.size.interfaces import ISized

from zope.app.file.file import File
from zope.app.file.i18n import ZopeMessageFactory as _
from zope.app.file.interfaces import IImage


@implementer(IImage)
class Image(File):

    def __init__(self, data=b''):
        '''See interface `IFile`'''
        contentType, self._width, self._height = getImageInfo(data)
        super().__init__(data, contentType)

    def _setData(self, data):
        super()._setData(data)

        contentType, self._width, self._height = getImageInfo(self._data)
        if contentType:
            self.contentType = contentType

    def getImageSize(self):
        '''See interface `IImage`'''
        return (self._width, self._height)

    data = property(File._getData, _setData)


@implementer(ISized)
class ImageSized:

    def __init__(self, image):
        self._image = image

    def sizeForSorting(self):
        '''See `ISized`'''
        return ('byte', self._image.getSize())

    def sizeForDisplay(self):
        '''See `ISized`'''
        w, h = self._image.getImageSize()
        if w < 0:
            w = '?'
        if h < 0:
            h = '?'
        bytes = self._image.getSize()
        byte_size = byteDisplay(bytes)
        mapping = byte_size.mapping
        if mapping is None:
            mapping = {}
        mapping.update({'width': str(w), 'height': str(h)})
        # TODO the way this message id is defined, it won't be picked up by
        # i18nextract and never show up in message catalogs
        return _(byte_size + ' ${width}x${height}', mapping=mapping)


class FileFactory:

    def __init__(self, context):
        self.context = context

    def __call__(self, name, content_type, data):
        if not content_type and data:
            content_type, _width, _height = getImageInfo(data)
        if not content_type:
            content_type, _encoding = guess_content_type(name, data, '')

        if content_type.startswith('image/'):
            return Image(data)

        return File(data, content_type)


def getImageInfo(data):
    data = bytes(data)
    size = len(data)
    height = -1
    width = -1
    content_type = ''

    # handle GIFs
    if (size >= 10) and data[:6] in (b'GIF87a', b'GIF89a'):
        # Check to see if content_type is correct
        content_type = 'image/gif'
        w, h = struct.unpack(b"<HH", data[6:10])
        width = int(w)
        height = int(h)

    # See PNG 2. Edition spec (http://www.w3.org/TR/PNG/)
    # Bytes 0-7 are below, 4-byte chunk length, then 'IHDR'
    # and finally the 4-byte width, height
    elif ((size >= 24) and data.startswith(b'\211PNG\r\n\032\n')
          and (data[12:16] == b'IHDR')):
        content_type = 'image/png'
        w, h = struct.unpack(b">LL", data[16:24])
        width = int(w)
        height = int(h)

    # Maybe this is for an older PNG version.
    elif ((size >= 16)
          and data.startswith(b'\211PNG\r\n\032\n')):  # pragma: no cover
        # Check to see if we have the right content type
        content_type = 'image/png'
        w, h = struct.unpack(">LL", data[8:16])
        width = int(w)
        height = int(h)

    # handle JPEGs
    elif (size >= 2) and data.startswith(b'\xff\xd8'):
        content_type = 'image/jpeg'
        jpeg = BytesIO(data)
        jpeg.read(2)
        b = jpeg.read(1)
        try:
            w = -1
            h = -1
            while b and ord(b) != 0xDA:
                while ord(b) != 0xFF:
                    b = jpeg.read(1)
                while ord(b) == 0xFF:
                    b = jpeg.read(1)
                if 0xC0 <= ord(b) <= 0xC3:
                    jpeg.read(3)
                    h, w = struct.unpack(b">HH", jpeg.read(4))
                    break
                else:
                    jpeg.read(int(struct.unpack(b">H", jpeg.read(2))[0]) - 2)
                b = jpeg.read(1)
            width = int(w)
            height = int(h)
        except (struct.error, ValueError):  # pragma: no cover
            pass

    # handle BMPs
    elif (size >= 30) and data.startswith(b'BM'):
        kind = struct.unpack(b"<H", data[14:16])[0]
        if kind == 40:  # Windows 3.x bitmap
            content_type = 'image/x-ms-bmp'
            width, height = struct.unpack(b"<LL", data[18:26])

    return content_type, width, height
