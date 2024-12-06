import base64
import datetime
import io
import zipfile

from django.core.files.base import ContentFile
from django.db import DatabaseError
from lxml import etree

from kinder.core.declaration.helpers import hide
from kinder.core.declaration.models import DeclarationDoc
from kinder.core.declaration.models import DeclarationStatusLog
from kinder.core.declaration.models import DeclarationPrivilege
from kinder.core.dict.models import HealthNeed
from kinder.webservice.spyne_ws.exceptions import SpyneException
from kinder.webservice.spyne_ws.exceptions import StatusSpyneException

from spyne_smev.fault import ApiError

from concentrator.models import PrivilegeComment
from concentrator.rules import DelegateDocTypeRule
from concentrator.webservice.django_objects_proxy import DeclarationUnitProxy


def get_delegate(declaration):
    """Возвращает представителя ребенка из заявления.

    Выбирает среди всех представителей самого первого.
    Если представителей нет у ребенка, то вернет None

    :param declaration: заявка
    :type declaration: Declaration

    :return: инстанс Delegate или None
    :rtype: Optional[Delegate]
    """

    childrendelegate = (
        declaration.children.childrendelegate_set.select_related(
            'delegate').order_by('id').only('delegate').first())

    return childrendelegate.delegate if childrendelegate else None


def get_privilege_comment(declaration):
    """
    Берется последняя добавленная льгота
    :param declaration: заявка
    :rtype: PrivilegeComment
    """
    declaration_privilege = DeclarationPrivilege.objects.filter(
        declaration=declaration).order_by('-datetime').first()
    if not declaration_privilege:
        return ''
    try:
        privilege_comment = PrivilegeComment.objects.get(
            declaration_privilege=declaration_privilege)
    except PrivilegeComment.DoesNotExist:
        privilege_comment = PrivilegeComment(
            declaration_privilege=declaration_privilege)
    return privilege_comment


def get_declaration_units(declaration):
    """
    возвращаем желаемые организации заявки
    в виде списка [('unit_id', 'ord'), ...]

    :param declaration: заявка
    :return:

    """

    return declaration.declarationunit_set.values_list('unit_id', 'ord')


def get_submit_date(declaration):
    """
    возвращаем дату подачи datetime
    :param declaration:
    :return:

    """

    return declaration.date


def get_desire_date(declaration):
    """
    если в заявке Дата желаемого зачисления не заполнена,
    то до календарного 1 сентября текущего года отдаем 1 сентября текущего года,
    после 1 сентября следующего года
    :param declaration:
    :return:

    """

    if declaration.desired_date:
        return declaration.desired_date
    today = datetime.date.today()
    current_first_september = datetime.date(today.year, 9, 1)
    if today > current_first_september:
        return datetime.date(today.year + 1, 9, 1)
    else:
        return current_first_september


def get_doc_type_delegate(delegate):
    """Возвращает тип ДУЛ представителя, пришедший концентратора
    если заявление подавалось с него, иначе по возможной карте сопоставлений
    """
    return DelegateDocTypeRule.get_concetr(delegate)


def get_state_details(declaration):
    """Возвращает комментарий последнего перехода заявки.

    :param declaration: заявление
    :type declaration: Declaration

    :return: последний комментарий при смене статуса заявления
    :rtype: Optional[str]
    """

    return DeclarationStatusLog.objects.filter(
        declaration=declaration
    ).order_by('-id').values_list('comment', flat=True).first()


def get_fio(person):
    """
    возвращавет деперсонализированую фамилию и первые буквы имени и отчества
    :param person: объекта с 3 параметрами surname, firstname, patronymic
    :return:

    """

    def slice(val):
        if isinstance(val, str):
            return val[:1]
        return val

    surname = hide(getattr(person, 'surname'))
    firstname = slice(getattr(person, 'firstname'))
    patronymic = slice(getattr(person, 'patronymic'))
    return '.'.join(
        [x for x in [surname, firstname, patronymic] if x is not None]
    ) or None


def get_doc_number(person):
    """
    возвращвет деперсонализированные цифры номера документа
    :param person: объекта с параметром dul_number
    :return:

    """

    dul_number = getattr(person, 'dul_number') or ''
    return hide(dul_number, 4) if len(dul_number) > 3 else None


def get_snils_number(person):
    """
    возвращвет деперсонализированные цифры снилса
    :param person: объекта с параметром snils
    :return:

    """

    snils = getattr(person, 'snils') or ''
    return hide(snils, 4) if len(snils) > 3 else None


def get_child_address(child):
    """
    возвращает адрес регистрации и фактический ребенка
    :return:

    """

    reg_address = child.reg_address_full
    fact_address = child.address_full
    return reg_address, fact_address


def get_delegate_address(child):
    """
    возвращает адрес регистрации и фактический родителя
    :return:

    """

    # Берем первого родителя ребенка, созданного раньше
    delegates = child.childrendelegate_set.all().order_by('id')
    if delegates:
        delegate = delegates[0].delegate
        reg_address = delegate.reg_address_full
        fact_address = delegate.address_full
    else:
        reg_address = fact_address = u''

    return reg_address, fact_address


def get_sex(child):
    """
    возвращает числовое представление поля Пол ребенка
    либо пустую строку
    :param child:
    :return:

    """

    return str(child.gender) if child.gender else None


def get_health_need(decl):
    """
    возвращает текстовое представление
    :param decl:
    :return:

    """

    if decl.children.health_need:
        return str(decl.children.health_need.id)
    return str(HealthNeed.objects.get(code=HealthNeed.NO).id)


def get_declaration_units_from_request(edu_organizations, declaration):
    """Возвращается список желаемых организаций DeclarationUnit-ов.

    :param edu_organizations: данные об ДОО из запроса.
                              spyne EduOrganizationsData
    :param declaration: Django model instance

    """

    return DeclarationUnitProxy(
        units=edu_organizations.EduOrganization,
        declaration=declaration).get()


def get_mo_from_request(edu_organizations, declaration):
    """Возвращается инстанс МО, к которому должны
    принадлежать все организации, указанные в запросе.

    :param edu_organizations: данные об ДОО из запроса.
                              spyne EduOrganizationsData
    :param declaration: заявление

    """

    return DeclarationUnitProxy(
        units=edu_organizations.EduOrganization,
        declaration=declaration).get_mo()


def get_binary_data(ctx):
    """
    Получаем из контекста запроса бинарные данные

    """

    binary_data = None
    request_code = None
    # TODO: Нужно ли динамически подтягивать namespace
    if ctx.in_smev_appdoc_document:
        binary_data_node = ctx.in_smev_appdoc_document.find(
            '{http://smev.gosuslugi.ru/rev120315}BinaryData')
        binary_data = None
        if binary_data_node is not None:
            binary_data = (
                binary_data_node.text.encode()
                if isinstance(binary_data_node.text, str)
                else binary_data_node.text)

        request_code_node = ctx.in_smev_appdoc_document.find(
            '{http://smev.gosuslugi.ru/rev120315}RequestCode')
        if request_code_node is not None:
            request_code = (
                request_code_node.text.encode()
                if isinstance(request_code_node.text, str)
                else request_code_node.text)

    return binary_data, request_code


def _get_document_reference_from_ctx(ctx):
    if not ctx.DocumentReferences:
        return []
    elif not ctx.DocumentReferences.DocumentReference:
        return []
    else:
        return ctx.DocumentReferences.DocumentReference


def get_dul_date(dul_date=None):
    """Возвращаем дату если есть входное значение,
    иначе дефолтное значение,поскольку в системе данных
    может не быть,а сервис отправить их должен

    """

    if dul_date is None:
        dul_date = datetime.date(1900, 0o1, 0o1)
    return dul_date


class SmevAppliedDocuments(object):
    ns = "{http://smev.gosuslugi.ru/request/rev111111}"

    def __init__(self, unzipped, req_code):

        str_req_code = (
            req_code if isinstance(req_code, str) else req_code.decode()
        )
        description_xml_name = f'{str_req_code}.xml'
        if description_xml_name not in unzipped.namelist():
            raise SpyneException(
                message=u"Отсутствует xml описание приложенных файлов "
                        u"с именем {name}".format(name=description_xml_name))
        _file = unzipped.open(description_xml_name)
        self.content = etree.fromstring(_file.read())
        _file.close()

    def __iter__(self):

        for applied_file in self.content.iterfind(
                "./{ns}AppliedDocuments/{ns}AppliedDocument".format(
                    ns=self.ns)):
            code_document = applied_file.find(
                "./{ns}CodeDocument".format(ns=self.ns))
            url = applied_file.find(
                "./{ns}URL".format(ns=self.ns))
            if url is not None:
                url = url.text
            name = applied_file.find("./{ns}Name".format(ns=self.ns))

            if code_document is not None and name is not None:
                yield (code_document.text, name.text, url)


class DocumentWorker(object):
    """
    Класс для работы с документами
    """

    def __init__(self, declaration, binary_data=None, req_code=None):

        self._declaration = declaration
        self._binary_data = binary_data
        self._request_code = req_code

    def _save(self, file_info, unzipped, approve):

        file_code, file_name, url = file_info
        try:
            _file = unzipped.open(url)
        except KeyError:
            try:
                _file = unzipped.open(file_code)
            except KeyError:
                raise SpyneException(
                    message=u"В архиве отсутствует файл с кодом {code}, "
                            u"что описан в xml".format(code=file_code))

        content_file = ContentFile(_file.read(), name=file_name)
        _file.close()

        try:
            doc = DeclarationDoc.objects.create(
                file=content_file,
                name=file_name,
                declaration=self._declaration,
                approve=approve
            )
        except DatabaseError:
            raise SpyneException(
                message=u"Невозможно сохранить файл '{name}'. "
                        u"Длина имени не должна превышать 300 "
                        u"символов.".format(name=file_name)
            )
        return doc

    def attach(self, approve=True):
        list_of_docs = []
        # Если есть BinaryData но нет RequestCode выбрасываем исключение
        if (self._binary_data and self._binary_data.strip() and
                not self._request_code):
            raise SpyneException(message=u"Тег RequestCode не задан")

        if self._binary_data and self._binary_data.strip():
            decode_file_data = base64.decodebytes(self._binary_data)
            decode_file_data_io = io.BytesIO(decode_file_data)
            unzipped = zipfile.ZipFile(decode_file_data_io)

            smev_applied_files = SmevAppliedDocuments(
                unzipped, self._request_code)

            for file_info in smev_applied_files:
                list_of_docs.append(self._save(file_info, unzipped, approve))
        return list_of_docs


def reject_request(ctx, message: str):
    """
    Формирует и поднимает исключение ApiError.

    :param ctx:
    :param message: сообщение исключения
    :type message: str
    :return: None
    :raise: ApiError

    """

    ctx.udc.is_reject = 'REJECT'
    response_name = ctx.method_name.replace('Request', 'Response')

    raise ApiError(ApiError.faultactor, message, response_name, 'REJECT')


def check_organization_priorities(organizations_data):
    u"""Проверка данных приоритетов переданных организаций.

    Если в заявлении выбрано несколько раз одно и то же ДОО с разными
    приоритетами нужно отправить ошибку.

    """

    if not organizations_data:
        return

    organizations = organizations_data.EduOrganization
    if not organizations:
        return

    organization_priorities = {}
    for code, priority in organizations:
        if code in organization_priorities:
            if priority != organization_priorities[code]:
                raise StatusSpyneException(
                    message=u'В желаемых организациях есть одинаковые '
                            u'организации с разными приоритетами',
                    status='REJECT'
                )

        else:
            organization_priorities[code] = priority
