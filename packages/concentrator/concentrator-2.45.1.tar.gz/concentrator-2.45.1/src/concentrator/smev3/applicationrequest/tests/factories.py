from collections import namedtuple

import factory

from aio_client.base.models import RequestLog
from aio_client.provider.models.provider import GetProviderRequest
from kinder.core.helpers import recursive_getattr
from kinder.test.utils import faker, get_snils

MAPPING = {
    'orderId': 'client_id',
    'ChildInfo.ChildName': 'children.firstname',
    'ChildInfo.ChildSurname': 'children.surname',
    'ChildInfo.ChildMiddleName': 'children.patronymic',
    'ChildInfo.ChildBirthDate': 'children.date_of_birth',
    'ChildInfo.ChildBirthDocRF.ChildBirthDocSeries': 'children.dul_series',
    'ChildInfo.ChildBirthDocRF.ChildBirthDocNumber': 'children.dul_number',
    'ChildInfo.ChildBirthDocRF.ChildBirthDocIssueDate': 'children.dul_date',
    'children_snils': 'children.snils',
}


class RequestLogF(factory.DjangoModelFactory):
    class Meta:
        model = RequestLog


class GetProviderRequestF(factory.DjangoModelFactory):
    class Meta:
        model = GetProviderRequest

    request_id = factory.SubFactory(RequestLogF)
    body = ''
    is_test_message = False


ChildBirthDocRF = namedtuple('ChildBirthDocRF', (
    'ChildBirthDocSeries',
    'ChildBirthDocNumber',
    'ChildBirthDocIssueDate',
))
ChildInfo = namedtuple('ChildInfo', (
    'ChildName',
    'ChildSurname',
    'ChildMiddleName',
    'ChildBirthDate',
    'ChildBirthDocRF',
))
RequestDeclaration = namedtuple('RequestDeclaration', (
    'orderId',
    'ChildInfo',
    'children_snils',
))


class ChildBirthDocRFF(factory.Factory):
    class Meta:
        model = ChildBirthDocRF

    ChildBirthDocSeries = 'I-КБ'
    ChildBirthDocNumber = factory.Sequence(lambda s: u'{0:06d}'.format(s))
    ChildBirthDocIssueDate = faker('date_this_month')


class ChildInfoF(factory.Factory):
    class Meta:
        model = ChildInfo

    ChildName = faker('first_name')
    ChildSurname = faker('last_name')
    ChildMiddleName = faker('first_name')
    ChildBirthDate = faker('date_this_month')
    ChildBirthDocRF = factory.SubFactory(ChildBirthDocRFF)


class RequestDeclarationF(factory.Factory):
    class Meta:
        model = RequestDeclaration

    orderId = '0000000001-17-01-1-6-1'
    ChildInfo = factory.SubFactory(ChildInfoF)

    children_snils = get_snils()

    @classmethod
    def _copy_from(cls, declaration):
        """Создает примерную XML структуру со значениями из заявления."""
        params = {}
        for field, model_field in list(MAPPING.items()):
            params[field.replace('.', '__')] = (
                recursive_getattr(declaration, model_field.replace('.', '__')))
        return cls(**params)
