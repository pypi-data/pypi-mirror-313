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
"""Basic File interfaces.

"""
__docformat__ = 'restructuredtext'

from zope.interface import Interface
from zope.schema import Bytes
from zope.schema import NativeStringLine

from zope.app.file.i18n import ZopeMessageFactory as _


class IFile(Interface):

    contentType = NativeStringLine(
        title=_('Content Type'),
        description=_('The content type identifies the type of data.'),
        default='',
        required=False,
        missing_value=''
    )

    data = Bytes(
        title=_('Data'),
        description=_('The actual content of the object.'),
        default=b'',
        missing_value=b'',
        required=False,
    )

    def getSize():
        """Return the byte-size of the data of the object."""


class IImage(IFile):
    """This interface defines an Image that can be displayed.
    """

    def getImageSize():
        """Return a tuple (x, y) that describes the dimensions of
        the object.
        """
