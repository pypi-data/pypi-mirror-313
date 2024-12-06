import factory

from kinder.core.children.tests.factory_child import DelegateF

from concentrator.constants import ConcentratorDelegateDocType
from concentrator.models import DelegatePerson


class DelegatePersonF(factory.DjangoModelFactory):
    class Meta:
        model = DelegatePerson

    doc_type = ConcentratorDelegateDocType.IDENTITY_CARD
    delegate = factory.SubFactory(DelegateF)
