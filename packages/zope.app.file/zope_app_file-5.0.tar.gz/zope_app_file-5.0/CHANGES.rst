Changes
=======

5.0 (2024-12-04)
----------------

- Add support for Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13.

- Drop support for Python 2.7, 3.4, 3.5, 3.6.

- Fix tests to support ``multipart >= 1.1``.

4.0.0 (2017-05-16)
------------------

- Add support for Python 3.4, 3.5, 3.6 and PyPy.

- Remove test dependency on ``zope.app.testing`` and ``zope.app.zcmlfiles``,
  among others.

- Change dependency from ZODB3 to persistent and add missing
  dependencies on ``zope.app.content``.


3.6.1 (2010-09-17)
------------------

- Removed ZPKG slugs and ZCML ones.

- Moved a functional test here from `zope.app.http`.

- Using Python's ``doctest`` instead of deprecated ``zope.testing.doctest``.


3.6.0 (2010-08-19)
------------------

- Updated ``ftesting.zcml`` to use the new permission names exported by
  ``zope.dublincore`` 3.7.

- Using python's `doctest` instead of deprecated `zope.testing.doctest`.


3.5.1 (2010-01-08)
------------------

- Fix ftesting.zcml due to zope.securitypolicy update.

- Added missing dependency on transaction.

- Import content-type parser from zope.contenttype, reducing zope.publisher to
  a test dependency.

- Fix tests using a newer zope.publisher that requires zope.login.

3.5.0 (2009-01-31)
------------------

- Replace ``zope.app.folder`` use by ``zope.site``. Add missing
  dependency in ``setup.py``.

3.4.6 (2009-01-27)
------------------

- Remove zope.app.zapi dependency again. Previous release
  was wrong. We removed the zope.app.zapi uses before, so
  we don't need it anymore.

3.4.5 (2009-01-27)
------------------

- added missing dependency: zope.app.zapi

3.4.4 (2008-09-05)
------------------

- Bug: Get actual filename instead of full filesystem path when adding
  file/image using Internet Explorer.

3.4.3 (2008-06-18)
------------------

- Using IDCTimes interface instead of IZopeDublinCore to determine the
  modification date of a file.

3.4.2 (2007-11-09)
------------------

- Include information about which attributes changed in the
  ``IObjectModifiedEvent`` after upload.

  This fixes https://bugs.launchpad.net/zope3/+bug/98483.

3.4.1 (2007-10-31)
------------------

- Resolve ``ZopeSecurityPolicy`` deprecation warning.


3.4.0 (2007-10-24)
------------------

- Initial release independent of the main Zope tree.
