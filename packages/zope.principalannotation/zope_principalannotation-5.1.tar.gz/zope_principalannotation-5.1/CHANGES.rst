=========
 Changes
=========

5.1 (2024-12-06)
================

- Add support for Python 3.12, 3.13.

- Drop support for Python 3.7.

- Update to ``persistent`` 6.0 API usage.


5.0 (2023-06-29)
================

- Drop support for Python 2.7, 3.5, 3.6.

- Drop support for deprecated ``python setup.py test``.

- Add support for Python 3.11.


4.4 (2022-03-17)
================

- Add support for Python 3.8, 3.9 and 3.10.

- Drop support for Python 3.4.


4.3.0 (2018-10-19)
==================

- Add support for Python 3.7.


4.2.0 (2017-08-18)
==================

- Add support for Python 3.5 and 3.6.

- Drop support for Python 2.6 and 3.3.


4.1.1 (2015-06-02)
==================

- Replace use of long-deprecated ``zope.testing.doctest`` with stdlib's
  ``doctest``.


4.1.0 (2015-01-09)
==================

- Accomodate new methods added to ``zope.annotation.interfaces.IAnnotations``
  in upcoming zope.annotation 4.4.0 release.


4.0.0 (2014-12-24)
==================

- Add support for PyPy.

- Add support for Python 3.4.

- Add support for testing on Travis.


4.0.0a2 (2013-02-25)
====================

- Correct Trove classifiers.


4.0.0a1 (2013-02-24)
====================

- Add support for Python 3.3.

- Replace deprecated ``zope.interface.implements`` usage with equivalent
  ``zope.interface.implementer`` decorator.

- Drop support for Python 2.4 and 2.5.

3.6.1 (2010-05-05)
==================

- Fix a test failure in nested local site manager setup.

- Remove dependency on zope.container.

3.6.0 (2009-03-09)
==================

Initial release. This package was splitted off zope.app.principalannotation
to remove its dependencies on "zope 3 application server" components.

In addition, the following changes were made after split off:

 - The IAnnotations implementation was fixed to look in the higher-level
   utility not only on ``__getitem__``, but also on ``get`` and ``__nonzero``.

 - Tests was reworked into the README.txt doctest.

 - Added a buildout part that generates Sphinx documentation from the
   README.txt
