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
"""Implementation of IPrincipalAnnotationUtility
"""
__docformat__ = 'restructuredtext'
from BTrees.OOBTree import OOBTree
from persistent import Persistent
from persistent.mapping import PersistentMapping
from zope.annotation.interfaces import IAnnotations
from zope.component import queryNextUtility
from zope.location import Location
from zope.location.interfaces import IContained
from zope.security.interfaces import IPrincipal

from zope import component
from zope import interface
from zope.principalannotation.interfaces import IPrincipalAnnotationUtility


# TODO: register utility as adapter for IAnnotations on utility activation.


@interface.implementer(IPrincipalAnnotationUtility, IContained)
class PrincipalAnnotationUtility(Persistent):
    """
    Stores :class:`zope.annotation.interfaces.IAnnotations` for
    :class:`zope.security.interfaces.IPrinicipals`.
    """

    __parent__ = None
    __name__ = None

    def __init__(self):
        self.annotations = OOBTree()

    def getAnnotations(self, principal):
        """
        See :meth:`.IPrincipalAnnotationUtility.getAnnotations`.
        """
        return self.getAnnotationsById(principal.id)

    def getAnnotationsById(self, principalId):
        """
        See :meth:`.IPrincipalAnnotationUtility.getAnnotationsById`.
        """
        annotations = self.annotations.get(principalId)
        if annotations is None:
            annotations = Annotations(principalId, store=self.annotations)
            annotations.__parent__ = self
            annotations.__name__ = principalId
        return annotations

    def hasAnnotations(self, principal):
        """
        See :meth:`.IPrincipalAnnotationUtility.hasAnnotations`.
        """
        return principal.id in self.annotations


@interface.implementer(IAnnotations)
class Annotations(Persistent, Location):
    """
    Stores annotations for a single principal in a :class:`~.PersistentDict`.

    Implements the dict-like API of
    :class:`zope.annotation.interfaces.IAnnotations`.

    Cooperates with the site hierarchy to find annotations in parent sites.
    """

    def __init__(self, principalId, store=None):
        self.principalId = principalId
        self.data = PersistentMapping()  # We don't really expect that many

        # _v_store is used to remember a mapping object that we should
        # be saved in if we ever change
        self._v_store = store

    def __bool__(self):
        nz = bool(self.data)
        if not nz:
            # maybe higher-level utility's annotations will be non-zero
            next = queryNextUtility(self, IPrincipalAnnotationUtility)
            if next is not None:
                annotations = next.getAnnotationsById(self.principalId)
                return bool(annotations)
        return nz

    __nonzero__ = __bool__

    def __getitem__(self, key):
        try:
            return self.data[key]
        except KeyError:
            # We failed locally: delegate to a higher-level utility.
            next = queryNextUtility(self, IPrincipalAnnotationUtility)
            if next is not None:
                annotations = next.getAnnotationsById(self.principalId)
                return annotations[key]
            raise

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __setitem__(self, key, value):
        if getattr(self, '_v_store', None) is not None:
            # _v_store is used to remember a mapping object that we should
            # be saved in if we ever change
            self._v_store[self.principalId] = self
            del self._v_store

        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        return iter(self.data)

    def __contains__(self, key):
        return key in self.data

    def items(self):
        return self.data.items()


@component.adapter(IPrincipal)
@interface.implementer(IAnnotations)
def annotations(principal, context=None):
    utility = component.getUtility(
        IPrincipalAnnotationUtility,
        context=context)
    return utility.getAnnotations(principal)
