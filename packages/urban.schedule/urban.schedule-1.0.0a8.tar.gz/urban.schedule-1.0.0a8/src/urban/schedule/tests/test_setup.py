# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from urban.schedule import testing  # noqa: E501

import unittest


class TestSetup(unittest.TestCase):
    """Test that urban.schedule is properly installed."""

    layer = testing.URBAN_SCHEDULE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if urban.schedule is installed."""
        self.assertTrue(self.installer.is_product_installed("urban.schedule"))

    def test_browserlayer(self):
        """Test that IUrbanScheduleLayer is registered."""
        from urban.schedule.interfaces import IUrbanScheduleLayer
        from plone.browserlayer import utils

        self.assertIn(IUrbanScheduleLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = testing.URBAN_SCHEDULE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("urban.schedule")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if urban.schedule is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("urban.schedule"))

    def test_browserlayer_removed(self):
        """Test that IUrbanScheduleLayer is removed."""
        from urban.schedule.interfaces import IUrbanScheduleLayer
        from plone.browserlayer import utils

        self.assertNotIn(IUrbanScheduleLayer, utils.registered_layers())
