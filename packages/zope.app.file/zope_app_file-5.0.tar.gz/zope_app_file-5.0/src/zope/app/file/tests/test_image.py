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
"""Test Image content component

"""
import unittest

from zope.interface.verify import verifyClass

from zope.app.file.file import File
from zope.app.file.file import FileReadFile
from zope.app.file.file import FileWriteFile
from zope.app.file.image import FileFactory
from zope.app.file.image import Image
from zope.app.file.image import ImageSized
from zope.app.file.interfaces import IImage


zptlogo = (
    b'GIF89a\x10\x00\x10\x00\xd5\x00\x00\xff\xff\xff\xff\xff\xfe\xfc\xfd\xfd'
    b'\xfa\xfb\xfc\xf7\xf9\xfa\xf5\xf8\xf9\xf3\xf6\xf8\xf2\xf5\xf7\xf0\xf4\xf6'
    b'\xeb\xf1\xf3\xe5\xed\xef\xde\xe8\xeb\xdc\xe6\xea\xd9\xe4\xe8\xd7\xe2\xe6'
    b'\xd2\xdf\xe3\xd0\xdd\xe3\xcd\xdc\xe1\xcb\xda\xdf\xc9\xd9\xdf\xc8\xd8\xdd'
    b'\xc6\xd7\xdc\xc4\xd6\xdc\xc3\xd4\xda\xc2\xd3\xd9\xc1\xd3\xd9\xc0\xd2\xd9'
    b'\xbd\xd1\xd8\xbd\xd0\xd7\xbc\xcf\xd7\xbb\xcf\xd6\xbb\xce\xd5\xb9\xcd\xd4'
    b'\xb6\xcc\xd4\xb6\xcb\xd3\xb5\xcb\xd2\xb4\xca\xd1\xb2\xc8\xd0\xb1\xc7\xd0'
    b'\xb0\xc7\xcf\xaf\xc6\xce\xae\xc4\xce\xad\xc4\xcd\xab\xc3\xcc\xa9\xc2\xcb'
    b'\xa8\xc1\xca\xa6\xc0\xc9\xa4\xbe\xc8\xa2\xbd\xc7\xa0\xbb\xc5\x9e\xba\xc4'
    b'\x9b\xbf\xcc\x98\xb6\xc1\x8d\xae\xbaFgs\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00,\x00\x00\x00\x00\x10\x00\x10\x00\x00\x06z@\x80pH,\x12k\xc8$\xd2f'
    b'\x04\xd4\x84\x01\x01\xe1\xf0d\x16\x9f\x80A\x01\x91\xc0ZmL\xb0\xcd\x00V'
    b'\xd4\xc4a\x87z\xed\xb0-\x1a\xb3\xb8\x95\xbdf8\x1e\x11\xca,MoC$\x15\x18{'
    b'\x006}m\x13\x16\x1a\x1f\x83\x85}6\x17\x1b $\x83\x00\x86\x19\x1d!%)\x8c'
    b'\x866#\'+.\x8ca`\x1c`(,/1\x94B5\x19\x1e"&*-024\xacNq\xba\xbb\xb8h\xbeb'
    b'\x00A\x00;'
)


class TestImage(unittest.TestCase):

    def _makeImage(self, *args, **kw):
        return Image(*args, **kw)

    def testEmpty(self):
        file = self._makeImage()
        self.assertEqual(file.contentType, '')
        self.assertEqual(file.data, b'')

    def testConstructor(self):
        file = self._makeImage(b'Data')
        self.assertEqual(file.contentType, '')
        self.assertEqual(file.data, b'Data')

    def testMutators(self):
        image = self._makeImage()

        image.contentType = 'image/jpeg'
        self.assertEqual(image.contentType, 'image/jpeg')

        image._setData(zptlogo)
        self.assertEqual(image.data, zptlogo)
        self.assertEqual(image.contentType, 'image/gif')
        self.assertEqual(image.getImageSize(), (16, 16))

    def testInterface(self):
        self.assertTrue(IImage.implementedBy(Image))
        self.assertTrue(verifyClass(IImage, Image))


class TestFileAdapters(unittest.TestCase):

    def _makeFile(self, *args, **kw):
        return Image(*args, **kw)

    def test_ReadFile(self):
        file = self._makeFile()
        content = b"This is some file\ncontent."
        file.data = content
        file.contentType = 'text/plain'
        self.assertEqual(FileReadFile(file).read(), content)
        self.assertEqual(FileReadFile(file).size(), len(content))

    def test_WriteFile(self):
        file = self._makeFile()
        content = b"This is some file\ncontent."
        FileWriteFile(file).write(content)
        self.assertEqual(file.data, content)


class DummyImage:

    def __init__(self, width, height, bytes):
        self.width = width
        self.height = height
        self.bytes = bytes

    def getSize(self):
        return self.bytes

    def getImageSize(self):
        return self.width, self.height


class TestFileFactory(unittest.TestCase):

    def test_image(self):
        factory = FileFactory(None)
        f = factory("spam.txt", "image/foo", b"hello world")
        self.assertIsInstance(f, Image)
        f = factory("spam.txt", "", zptlogo)
        self.assertIsInstance(f, Image)

    def test_text(self):
        factory = FileFactory(None)
        f = factory("spam.txt", "", b"hello world")
        self.assertIsInstance(f, File)
        self.assertNotIsInstance(f, Image)
        f = factory("spam.txt", "", b"\0\1\2\3\4")
        self.assertIsInstance(f, File)
        self.assertNotIsInstance(f, Image)
        f = factory("spam.txt", "text/splat", zptlogo)
        self.assertIsInstance(f, File)
        self.assertNotIsInstance(f, Image)
        f = factory("spam.txt", "application/splat", zptlogo)
        self.assertIsInstance(f, File)
        self.assertNotIsInstance(f, Image)


class TestSized(unittest.TestCase):

    def testInterface(self):
        from zope.size.interfaces import ISized
        self.assertTrue(ISized.implementedBy(ImageSized))
        self.assertTrue(verifyClass(ISized, ImageSized))

    def test_zeroSized(self):
        s = ImageSized(DummyImage(0, 0, 0))
        self.assertEqual(s.sizeForSorting(), ('byte', 0))
        self.assertEqual(s.sizeForDisplay(), '0 KB ${width}x${height}')
        self.assertEqual(s.sizeForDisplay().mapping['width'], '0')
        self.assertEqual(s.sizeForDisplay().mapping['height'], '0')

    def test_arbitrarySize(self):
        s = ImageSized(DummyImage(34, 56, 78))
        self.assertEqual(s.sizeForSorting(), ('byte', 78))
        self.assertEqual(s.sizeForDisplay(), '1 KB ${width}x${height}')
        self.assertEqual(s.sizeForDisplay().mapping['width'], '34')
        self.assertEqual(s.sizeForDisplay().mapping['height'], '56')

    def test_unknownSize(self):
        s = ImageSized(DummyImage(-1, -1, 23))
        self.assertEqual(s.sizeForSorting(), ('byte', 23))
        self.assertEqual(s.sizeForDisplay(), '1 KB ${width}x${height}')
        self.assertEqual(s.sizeForDisplay().mapping['width'], '?')
        self.assertEqual(s.sizeForDisplay().mapping['height'], '?')


class TestGetImageInfo(unittest.TestCase):

    def _info(self, data):
        from zope.app.file.image import getImageInfo
        return getImageInfo(data)

    def test_getImageInfo(self):
        t, w, h = self._info(
            b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00"
            b"\x00\xff\xdb\x00C")
        self.assertEqual(t, "image/jpeg")
        self.assertEqual(w, -1)
        self.assertEqual(h, -1)

    def test_getImageInfo_jpeg(self):
        data = (
            b'\xff\xd8\x00\xff\xe0\x00\x10JFIF\x00\x01\x02\x00\x00\x01\x00\x01'
            b'\x00\x00\xff\xdb\x00C\x00\t\x06\x07\x08\x07\x06\t\x08\x08\x08\n'
            b'\n\t\x0b\x0e\x17\x0f\x0e\r\r\x0e\x1c\x14\x15\x11\x17"\x1e##!\x1e'
            b'  %*5-%\'2(  .?/279<<<$-BFA:F5;<9\xff\xdb\x00C\x01\n\n\n\x0e'
            b'\x0c\x0e\x1b\x0f\x0f\x1b9& &999999999999999999999999999999999999'
            b'99999999999999\xff\xc0\x00\x11\x08\x04\x80\x08\x00')

        t, w, h = self._info(data)
        self.assertEqual(t, "image/jpeg")
        self.assertEqual(w, 2048)
        self.assertEqual(h, 1152)

    def test_getImageInfo_bmp(self):
        t, w, h = self._info(b'BMl\x05\x00\x00\x00\x00\x00\x006\x04\x00\x00('
                             b'\x00\x00\x00\x10\x00\x00\x00\x10\x00\x00\x00'
                             b'\x01\x00\x08\x00\x01\x00\x00\x006\x01\x00\x00'
                             b'\x12\x0b\x00\x00\x12\x0b\x00\x00\x00\x01\x00'
                             b'... and so on ...')
        self.assertEqual(t, "image/x-ms-bmp")
        self.assertEqual(w, 16)
        self.assertEqual(h, 16)

    def test_getImageInfo_png(self):
        data = (
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x05\x1c\x00\x00\x01'
            b'p\x08\x06\x00\x00\x00\xda\x1b\xb7')
        t, w, h = self._info(data)
        self.assertEqual(t, "image/png")
        self.assertEqual(w, 1308)
        self.assertEqual(h, 368)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
