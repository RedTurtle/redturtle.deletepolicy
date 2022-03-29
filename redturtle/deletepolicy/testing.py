from zope.configuration import xmlconfig

from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile


class DeletePolicyLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import redturtle.deletepolicy
        xmlconfig.file('configure.zcml',
                       redturtle.deletepolicy,
                       context=configurationContext)

FIXTURE = DeletePolicyLayer()

INTEGRATION_TESTING = \
    IntegrationTesting(bases=(FIXTURE, ),
                       name="DeletePolicy:Integration")

FUNCTIONAL_TESTING = \
    FunctionalTesting(bases=(FIXTURE, ),
                       name="DeletePolicy:Functional")