##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
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
"""Principal Annotation Tests
"""
import doctest
import unittest

from zope.configuration import xmlconfig
from zope.site.testing import siteSetUp
from zope.site.testing import siteTearDown

import zope.principalannotation


def setUp(test):
    site = siteSetUp(site=True)
    test.globs['root'] = site
    xmlconfig.file('configure.zcml', zope.principalannotation)


def tearDown(test):
    siteTearDown()


def test_suite():
    return unittest.TestSuite(
        doctest.DocFileSuite(
            'README.rst',
            setUp=setUp, tearDown=tearDown,
            optionflags=doctest.ELLIPSIS)
    )
