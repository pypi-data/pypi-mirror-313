##############################################################################
#
# Copyright (c) 2003, 2004 Zope Corporation and Contributors.
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
"""Functional tests for File and Image.

"""
import doctest
import unittest
from io import BytesIO
from xml.sax.saxutils import escape

from webtest import TestApp
from zope.app.wsgi.testlayer import encodeMultipartFormdata
from zope.interface.interfaces import ComponentLookupError

from zope.app.file.file import File
from zope.app.file.image import Image
from zope.app.file.testing import AppFileLayer
from zope.app.file.tests import http
from zope.app.file.tests.test_image import zptlogo


class StringIO(BytesIO):

    def __init__(self, contents):
        if not isinstance(contents, bytes):
            contents = contents.encode("ascii")
        super().__init__(contents)


class BrowserTestCase(unittest.TestCase):

    layer = AppFileLayer

    def setUp(self):
        super().setUp()
        self._testapp = TestApp(self.layer.make_wsgi_app())

    def getRootFolder(self):
        return self.layer.getRootFolder()

    def commit(self):
        pass

    def checkForBrokenLinks(self, orig_response, path, basic=None):
        response = self.publish(path, basic=basic)
        try:
            links = response.html.find_all('a')
        except (AttributeError, TypeError):
            # Not html
            return

        for link in links:
            href = link.attrs['href']
            if href.endswith('@@SelectedManagementView.html'):
                # We don't install this at test time
                continue

            if not href.startswith('/'):
                href = path.rsplit('/', 1)[0] + '/' + href
            try:
                self.publish(href, basic=basic)
            except ComponentLookupError:
                # PrincipalSource, not installed at testing
                pass

    def publish(self, path, basic=None, form=None, headers=None):
        assert basic
        self._testapp.authorization = ('Basic', tuple(basic.split(':')))
        env = {'wsgi.handleErrors': False}
        if form:
            upload_files = []
            for k, v in list(form.items()):
                if isinstance(v, StringIO):
                    upload_files.append((k,
                                         getattr(v, 'filename', 'a file'),
                                         v.getvalue()))
                    del form[k]
            response = self._testapp.post(path, params=form,
                                          upload_files=upload_files,
                                          extra_environ=env, headers=headers)
        else:
            response = self._testapp.get(
                path, extra_environ=env, headers=headers)

        response.getBody = lambda: response.unicode_normal_body
        response.getStatus = lambda: response.status_int
        response.getHeader = lambda n: response.headers[n]
        return response


class FileTest(BrowserTestCase):

    content = b'File <Data>'

    def addFile(self):
        file = File(self.content)
        root = self.getRootFolder()
        root['file'] = file
        self.commit()

    def testAddForm(self):
        response = self.publish(
            '/+/zope.app.file.File=',
            basic='mgr:mgrpw')
        self.assertEqual(response.getStatus(), 200)
        body = response.getBody()
        self.assertIn('Add a File', body)
        self.assertIn('Content Type', body)
        self.assertIn('Data', body)
        self.assertIn('Object Name', body)
        self.assertIn('"Add"', body)
        self.checkForBrokenLinks(response, '/+/zope.app.file.File=',
                                 'mgr:mgrpw')

    def testAdd(self):
        response = self.publish(
            '/+/zope.app.file.File=',
            form={'type_name': 'zope.app.file.File',
                  'field.data': StringIO('A file'),
                  'field.data.used': '',
                  'add_input_name': 'file',
                  'UPDATE_SUBMIT': 'Add'},
            basic='mgr:mgrpw')
        self.assertEqual(response.getStatus(), 302)
        self.assertEqual(response.getHeader('Location'),
                         'http://localhost/@@contents.html')
        root = self.getRootFolder()
        self.assertIn('file', root)
        file = root['file']
        self.assertEqual(file.data, b'A file')

    def testAddWithoutName(self):
        data = StringIO('File Contents')
        data.filename = "test.txt"
        response = self.publish(
            '/+/zope.app.file.File=',
            form={'type_name': 'zope.app.file.File',
                  'field.data': data,
                  'field.data.used': '',
                  'UPDATE_SUBMIT': 'Add'},
            basic='mgr:mgrpw')
        self.assertEqual(response.getStatus(), 302)
        self.assertEqual(response.getHeader('Location'),
                         'http://localhost/@@contents.html')
        root = self.getRootFolder()
        self.assertIn('test.txt', root, list(root))
        file = root['test.txt']
        self.assertEqual(file.data, b'File Contents')

    def testEditForm(self):
        self.addFile()
        response = self.publish(
            '/file/@@edit.html',
            basic='mgr:mgrpw')
        self.assertEqual(response.getStatus(), 200)
        body = response.getBody()
        self.assertIn('Change a file', body)
        self.assertIn('Content Type', body)
        self.assertIn('Data', body)
        self.assertIn(escape(self.content.decode('ascii')), body)
        self.checkForBrokenLinks(response, '/file/@@edit.html', 'mgr:mgrpw')

    def testEdit(self):
        self.addFile()
        response = self.publish(
            '/file/@@edit.html',
            form={'field.data': '<h1>A File</h1>',
                  'field.data.used': '',
                  'field.contentType': 'text/plain',
                  'UPDATE_SUBMIT': 'Edit'},
            basic='mgr:mgrpw')
        self.assertEqual(response.getStatus(), 200)
        body = response.getBody()
        self.assertIn('Change a file', body)
        self.assertIn('Content Type', body)
        self.assertIn('Data', body)
        self.assertIn(escape('<h1>A File</h1>'), body)
        root = self.getRootFolder()
        file = root['file']
        self.assertEqual(file.data, b'<h1>A File</h1>')
        self.assertEqual(file.contentType, 'text/plain')

    def testUploadForm(self):
        self.addFile()
        response = self.publish(
            '/file/@@upload.html',
            basic='mgr:mgrpw')
        self.assertEqual(response.getStatus(), 200)
        body = response.getBody()
        self.assertIn('Upload a file', body)
        self.assertIn('Content Type', body)
        self.assertIn('Data', body)
        self.assertNotIn(escape(self.content.decode('ascii')), body)
        self.checkForBrokenLinks(response, '/file/@@upload.html', 'mgr:mgrpw')

    def testUpload(self):
        self.addFile()
        response = self.publish(
            '/file/@@upload.html',
            form={'field.data': StringIO('<h1>A file</h1>'),
                  'field.data.used': '',
                  'field.contentType': 'text/plain',
                  'UPDATE_SUBMIT': 'Change'},
            basic='mgr:mgrpw')
        self.assertEqual(response.getStatus(), 200)
        body = response.getBody()
        self.assertIn('Upload a file', body)
        self.assertIn('Content Type', body)
        self.assertIn('Data', body)
        self.assertNotIn(escape('<h1>A File</h1>'), body)
        root = self.getRootFolder()
        file = root['file']
        self.assertEqual(file.data, b'<h1>A file</h1>')
        self.assertEqual(file.contentType, 'text/plain')

    def testIndex(self):
        self.addFile()
        response = self.publish(
            '/file/@@index.html',
            basic='mgr:mgrpw')
        self.assertEqual(response.getStatus(), 200)
        body = response.body
        self.assertEqual(body, self.content)
        self.checkForBrokenLinks(response, '/file/@@index.html', 'mgr:mgrpw')

    def testPreview(self):
        self.addFile()
        response = self.publish(
            '/file/@@preview.html',
            basic='mgr:mgrpw')
        self.assertEqual(response.getStatus(), 200)
        body = response.getBody()
        self.assertIn('<iframe src="."', body)
        self.checkForBrokenLinks(response, '/file/@@preview.html', 'mgr:mgrpw')


class ImageTest(BrowserTestCase):

    content = zptlogo

    def addImage(self):
        image = Image(self.content)
        root = self.getRootFolder()
        root['image'] = image
        self.commit()

    def testAddForm(self):
        response = self.publish(
            '/+/zope.app.file.Image=',
            basic='mgr:mgrpw')
        self.assertEqual(response.getStatus(), 200)
        body = response.getBody()
        self.assertIn('Add an Image', body)
        self.assertIn('Content Type', body)
        self.assertIn('Data', body)
        self.assertIn('Object Name', body)
        self.assertIn('"Add"', body)
        self.checkForBrokenLinks(response, '/+/zope.app.file.Image=',
                                 'mgr:mgrpw')

    def testAdd(self):
        response = self.publish(
            '/+/zope.app.file.Image=',
            form={'type_name': 'zope.app.image.Image',
                  'field.data': StringIO(self.content),
                  'field.data.used': '',
                  'add_input_name': 'image',
                  'UPDATE_SUBMIT': 'Add'},
            basic='mgr:mgrpw')
        self.assertEqual(response.getStatus(), 302)
        self.assertEqual(response.getHeader('Location'),
                         'http://localhost/@@contents.html')
        root = self.getRootFolder()
        self.assertIn('image', root)
        image = root['image']
        self.assertEqual(image.data, self.content)

    def testAddWithoutName(self):
        data = StringIO(self.content)
        data.filename = "test.gif"
        response = self.publish(
            '/+/zope.app.file.Image=',
            form={'type_name': 'zope.app.image.Image',
                  'field.data': data,
                  'field.data.used': '',
                  'UPDATE_SUBMIT': 'Add'},
            basic='mgr:mgrpw')
        self.assertEqual(response.getStatus(), 302)
        self.assertEqual(response.getHeader('Location'),
                         'http://localhost/@@contents.html')
        root = self.getRootFolder()
        self.assertIn('test.gif', root, list(root))
        image = root['test.gif']
        self.assertEqual(image.data, self.content)

    def testUploadForm(self):
        self.addImage()
        response = self.publish(
            '/image/@@upload.html',
            basic='mgr:mgrpw')
        self.assertEqual(response.getStatus(), 200)
        body = response.getBody()
        self.assertIn('Upload an image', body)
        self.assertIn('Content Type', body)
        self.assertIn('Data', body)
        self.assertIn('1 KB 16x16', body)
        self.checkForBrokenLinks(response, '/image/@@upload.html', 'mgr:mgrpw')

    def testUpload(self):
        self.addImage()
        response = self.publish(
            '/image/@@upload.html',
            form={'field.data': StringIO(''),
                  'field.data.used': '',
                  'UPDATE_SUBMIT': 'Change'},
            basic='mgr:mgrpw')
        self.assertEqual(response.getStatus(), 200)
        body = response.getBody()
        self.assertIn('Upload an image', body)
        self.assertIn('Content Type', body)
        self.assertIn('Data', body)
        self.assertIn('0 KB ?x?', body)
        root = self.getRootFolder()
        image = root['image']
        self.assertEqual(image.data, b'')
        self.assertEqual(image.contentType, 'image/gif')

    def testUpload_only_change_content_type(self):
        self.addImage()
        response = self.publish(
            '/image/@@upload.html',
            form={'field.contentType': 'image/png',
                  'UPDATE_SUBMIT': 'Change'},
            basic='mgr:mgrpw')
        self.assertEqual(response.getStatus(), 200)
        body = response.getBody()
        self.assertIn('Upload an image', body)
        self.assertIn('Content Type', body)
        self.assertIn('Data', body)
        self.assertIn('1 KB 16x16', body)
        root = self.getRootFolder()
        image = root['image']
        self.assertEqual(image.data, self.content)
        self.assertEqual(image.contentType, 'image/png')

    def testIndex(self):
        self.addImage()
        response = self.publish(
            '/image/@@index.html',
            basic='mgr:mgrpw')
        self.assertEqual(response.getStatus(), 200)
        body = response.body
        self.assertEqual(body, self.content)
        self.checkForBrokenLinks(response, '/image/@@index.html', 'mgr:mgrpw')

    def testPreview(self):
        self.addImage()
        response = self.publish(
            '/image/@@preview.html',
            basic='mgr:mgrpw')
        self.assertEqual(response.getStatus(), 200)
        body = response.getBody()
        self.assertIn('<iframe src="."', body)
        self.checkForBrokenLinks(
            response, '/image/@@preview.html', 'mgr:mgrpw')


def test_suite():
    def _make_doctest(fname):
        test = doctest.DocFileSuite(
            fname,
            globs={'http': http,
                   'encodeMultipartFormdata': encodeMultipartFormdata},
            optionflags=(doctest.ELLIPSIS
                         | doctest.NORMALIZE_WHITESPACE
                         | doctest.IGNORE_EXCEPTION_DETAIL))
        test.layer = AppFileLayer
        return test

    url = _make_doctest('../url.rst')
    file = _make_doctest('../file.rst')
    return unittest.TestSuite((
        unittest.defaultTestLoader.loadTestsFromName(__name__),
        url,
        file,
    ))
