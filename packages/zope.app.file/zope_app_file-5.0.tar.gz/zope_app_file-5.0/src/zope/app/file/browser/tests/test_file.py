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
"""Tests for zope.app.file.browser.file.

"""
import doctest

from zope.component.testing import setUp
from zope.component.testing import tearDown


def test_suite():
    return doctest.DocTestSuite(
        "zope.app.file.browser.file",
        setUp=setUp,
        tearDown=tearDown,
        optionflags=(doctest.ELLIPSIS
                     | doctest.NORMALIZE_WHITESPACE))
