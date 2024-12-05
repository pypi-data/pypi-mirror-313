# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import urban.schedule


class UrbanScheduleLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.

        self.loadZCML(package=urban.schedule)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "urban.schedule:default")


URBAN_SCHEDULE_FIXTURE = UrbanScheduleLayer()


URBAN_SCHEDULE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(URBAN_SCHEDULE_FIXTURE,),
    name="UrbanScheduleLayer:IntegrationTesting",
)


URBAN_SCHEDULE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(URBAN_SCHEDULE_FIXTURE,),
    name="UrbanScheduleLayer:FunctionalTesting",
)


URBAN_SCHEDULE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        URBAN_SCHEDULE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="UrbanScheduleLayer:AcceptanceTesting",
)
