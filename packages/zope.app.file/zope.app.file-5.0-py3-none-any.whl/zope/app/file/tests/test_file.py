##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
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
"""Test File content component.

"""
import doctest
import unittest
from io import BytesIO

from zope.app.file import file as zfile


class TestFile(unittest.TestCase):

    def test_medium_size_chunk(self):
        # MAXCHUNKSIZE < size <= 2 * MAXCHUNKSIZE
        old_size = zfile.MAXCHUNKSIZE
        try:
            zfile.MAXCHUNKSIZE = 10
            data = BytesIO(b'b' * 15)

            f = zfile.File(data)
            self.assertIsInstance(f._data, zfile.FileChunk)
        finally:
            zfile.MAXCHUNKSIZE = old_size

    def test_large_size_chunk_with_jar(self):
        old_size = zfile.MAXCHUNKSIZE
        try:
            zfile.MAXCHUNKSIZE = 10
            data = BytesIO(b'b' * 30)

            class Jar:
                added = ()

                def add(self, o):
                    self.added += (o,)

                def register(self, o):
                    pass

            f = zfile.File()
            f._p_jar = Jar()

            f.data = data

            self.assertEqual(3, len(f._p_jar.added))

            self.assertEqual(data.getvalue(), f.data)
            self.assertEqual('b' * 30, str(f._data))
        finally:
            zfile.MAXCHUNKSIZE = old_size


class TestFileChunk(unittest.TestCase):

    def test_getitem(self):
        chunk = zfile.FileChunk(b'abc')
        self.assertEqual(chunk[:], b'abc')

    def test_bytes(self):
        chunk = zfile.FileChunk(b'abc')
        self.assertEqual(bytes(chunk), b'abc')
        self.assertEqual('abc', str(chunk))


def test_suite():
    return unittest.TestSuite((
        unittest.defaultTestLoader.loadTestsFromName(__name__),
        doctest.DocTestSuite('zope.app.file.file')
    ))
