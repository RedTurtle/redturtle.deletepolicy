"""
import unittest

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
ptc.setupPloneSite()

import redturtle.deletepolicy

class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml',
                             redturtle.deletepolicy)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass


def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='redturtle.deletepolicy',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='redturtle.deletepolicy.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        #ztc.ZopeDocFileSuite(
        #    'README.txt', package='redturtle.deletepolicy',
        #    test_class=TestCase),

        #ztc.FunctionalDocFileSuite(
        #    'browser.txt', package='redturtle.deletepolicy',
        #    test_class=TestCase),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
"""

# -*- coding: utf-8 -*-

import unittest
import transaction

from zope.interface import implementer
from zope.interface import Interface
from zope.component import getAdapter

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import login

from redturtle.deletepolicy.testing import INTEGRATION_TESTING
from redturtle.deletepolicy.testing import FUNCTIONAL_TESTING

from plone import api

from plone.testing import zope
from plone.app.testing.interfaces import SITE_OWNER_NAME
from plone.app.testing.interfaces import PLONE_SITE_ID
from plone.app.testing.interfaces import TEST_USER_PASSWORD

from AccessControl.unauthorized import Unauthorized

from plone.testing.z2 import Browser


class TestDeletePolicy(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        """ """      
        self.app = self.layer['app']
        self.portal = self.layer['portal']

        #zope.login(app['acl_users'], SITE_OWNER_NAME)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        api.user.create('user-1@example.com', 'user-1', password=TEST_USER_PASSWORD, roles=('Member',))
        self.contributor = api.user.get('user-1')
        setRoles(self.portal, 'user-1', ['Contributor',])

        self.parent = api.content.create(self.portal, 'Folder', id='parent')
        self.child = api.content.create(self.parent, 'Document', id='child-1')


    def test_delete_possible_with_all_permissions(self):
        """ """
        self.parent.manage_permission('Delete objects',
                                 roles=['Contributor'], acquire=False)
        self.child.manage_permission('Delete objects',
                                roles=['Contributor'], acquire=False)
        self.child.manage_permission('Modify portal content',
                                roles=['Contributor'], acquire=False)

        login(self.portal, self.contributor.id)

        self.assertIn(self.child.getId(), self.parent.objectIds())
        self.parent.manage_delObjects([self.child.getId()])
        self.assertNotIn(self.child.getId(), self.parent.objectIds())

    def test_delete_unauthorized_when_no_delete_permission_on_child(self):
        """ """
        self.parent.manage_permission('Delete objects',
                                      roles=['Contributor'], acquire=False)
        self.child.manage_permission('Delete objects',
                                     roles=[], acquire=False)
        self.child.manage_permission('Modify portal content',
                                roles=['Contributor'], acquire=False)

        login(self.portal, self.contributor.id)
        with self.assertRaises(Unauthorized):
            self.parent.manage_delObjects([self.child.getId()])


    def test_delete_unauthorized_when_no_modify_permission_on_child(self):
        """ """
        self.parent.manage_permission('Delete objects',
                                      roles=['Contributor'], acquire=False)
        self.child.manage_permission('Delete objects',
                                roles=['Contributor'], acquire=False)
        self.child.manage_permission('Modify portal content',
                                roles=[], acquire=False)

        login(self.portal, self.contributor.id)
        with self.assertRaises(Unauthorized):
            self.parent.manage_delObjects([self.child.getId()])


    def test_delete_unauthorized_when_no_permission_on_parent(self):
        """ """
        login(self.portal, self.contributor.id)

        self.portal.manage_permission('Delete objects',
                                 roles=['Contributor'], acquire=False)
        self.assertTrue(api.user.get_permissions(self.contributor.id, obj=self.parent)['Delete objects'])

        # remove permission on parent, add to child
        self.parent.manage_permission('Delete objects',
                                      roles=[], acquire=False)
        self.child.manage_permission('Delete objects',
                                      roles=['Contributor'], acquire=False)

        # verify permissions
        self.assertFalse(api.user.get_permissions(self.contributor.id, obj=self.parent)['Delete objects'])
        self.assertTrue(api.user.get_permissions(self.contributor.id, obj=self.child)['Delete objects'])

        with self.assertRaises(Unauthorized):
            self.parent.manage_delObjects([self.child.getId()])


class TestFunctionalDeletePolicy(unittest.TestCase):
    # https://github.com/4teamwork/collective.deletepermission/blob/master/collective/deletepermission/tests/test_actions.py

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        """ """      
        self.app = self.layer['app']
        self.portal = self.layer['portal']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        api.user.create('user-1@example.com', 'user-0', password=TEST_USER_PASSWORD, roles=('Manager',))
        api.user.create('user-1@example.com', 'user-1', password=TEST_USER_PASSWORD, roles=('Member','Contributor',))

        self.portal.manage_permission('Delete objects',
                                 roles=['Contributor'], acquire=False)

        login(self.portal, 'user-1')
        self.parent = api.content.create(self.portal, 'Folder', id='parent')
        self.child = api.content.create(self.parent, 'Document', id='child-1')

        transaction.commit()

    def test_check_contributor_actions(self):
        """ """
        login(self.portal, 'user-0')

        # verify user-2 permissions
        self.assertTrue(api.user.has_permission('Delete objects', username='user-1',obj=self.parent))
        self.assertTrue(api.user.has_permission('Delete objects', username='user-1',obj=self.child))
        self.assertTrue(api.user.has_permission('Modify portal content', username='user-1',obj=self.child))

        #login(self.portal, 'user-1')
        browser = Browser(self.app)
        browser.addHeader('Authorization', 'Basic %s:%s' % ('user-1', TEST_USER_PASSWORD,))

        url = self.child.absolute_url()
        browser.open(url)

        # verify actions
        self.assertTrue(u"Copy" in browser.contents)
        self.assertTrue(u"Cut" in browser.contents)
        self.assertTrue(u"Delete" in browser.contents)
