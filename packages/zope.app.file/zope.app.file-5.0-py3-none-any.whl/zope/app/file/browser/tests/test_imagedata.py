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
"""Test Image Data handling

"""
import unittest

from zope.component import adapter
from zope.component import provideAdapter
from zope.component.testing import PlacelessSetup
from zope.interface import implementer
from zope.traversing.browser.interfaces import IAbsoluteURL

from zope.app.file.browser.image import ImageAdd
from zope.app.file.browser.image import ImageData
from zope.app.file.image import Image


class FakeRequest:
    pass


@adapter(Image, FakeRequest)
@implementer(IAbsoluteURL)
class StubAbsoluteURL:

    def __init__(self, *objects):
        pass

    def __str__(self):
        return '/img'

    __call__ = __str__


class ImageDataTest(PlacelessSetup, unittest.TestCase):

    def testData(self):
        image = Image(b'Data')
        data = ImageData()
        data.context = image
        data.request = None
        self.assertEqual(data(), b'Data')

    def testTag(self):
        provideAdapter(StubAbsoluteURL)
        image = Image()
        fe = ImageData()
        fe.context = image
        fe.request = FakeRequest()

        self.assertEqual(
            fe.tag(),
            '<img src="/img" alt="" height="-1" width="-1" border="0" />')
        self.assertEqual(
            fe.tag(scale=.9, width=10, height=10),
            '<img src="/img" alt="" height="9" width="9" border="0" />')
        self.assertEqual(
            fe.tag(alt="Test Image"),
            '<img src="/img" alt="Test Image"'
            ' height="-1" width="-1" border="0" />')
        self.assertEqual(
            fe.tag(height=100, width=100),
            '<img src="/img" alt="" height="100" width="100" border="0" />')
        self.assertEqual(
            fe.tag(border=1),
            '<img src="/img" alt="" height="-1" width="-1" border="1" />')
        self.assertEqual(
            fe.tag(css_class="Image"),
            '<img src="/img" alt=""'
            ' height="-1" width="-1" border="0" class="Image" />')
        self.assertEqual(
            fe.tag(height=100, width="100", border=1, css_class="Image"),
            '<img src="/img" alt=""'
            ' height="100" width="100" class="Image" border="1" />')


class TestImageAdd(unittest.TestCase):

    def test_update_idempotent(self):
        add = ImageAdd()
        add.update_status = "Hi"
        self.assertEqual(add.update(), "Hi")


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)


if __name__ == '__main__':
    unittest.main()
