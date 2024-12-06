import base64
import datetime
import io
import zipfile

from django.core.files.base import ContentFile
from lxml import etree

from kinder.core.declaration.helpers import hide
from kinder.core.declaration.models import DeclarationDoc
from kinder.core.declaration.models import DeclarationStatusLog
from kinder.core.declaration.models import DeclarationUnit
from kinder.core.declaration_status.models import DSS
from kinder.core.direct.models import Direct
from kinder.core.group.models import Pupil
from kinder.plugins.privilege_attributes.models import (
    PrivilegeConfirmationAttributes)
from kinder.webservice.spyne_ws.declaration_info.helpers import filter_by_unit
from kinder.webservice.spyne_ws.declaration_info.logics import (
    CheckDeclarationProcess)
from kinder.webservice.spyne_ws.exceptions import SpyneException

from lipetsk_specifics.rules import DelegateDocTypeRule

from .descriptors import SummaryWithOutAgePosition


def get_delegate(declaration):
    """
    Пока логикатакая что берем первого родителя ребенка,
    созданного раньше
    :param declaration: заявка
    :return: инстанс Delegate

    """

    delegates = declaration.children.childrendelegate_set.all().order_by('id')
    if delegates:
        delegate = delegates[0].delegate
        return delegate
    return None


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
    то до календарного 1 сентября текущего года отдаем
    1 сентября текущего года, после 1 сентября следующего года

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
    """Возвращает значение тип ДУЛ представителя для липецкого ЕПГУ"""
    return DelegateDocTypeRule.get_concetr(delegate.dul_type_id)


def get_state_details(declaration):
    """
    отдаем комментарий последнего перехода заявки
    :param declaration:
    :return:

    """

    log = DeclarationStatusLog.objects.filter(
        declaration=declaration).order_by('-id')
    if log:
        return log[0].comment
    else:
        return None


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
    return None


def get_declaration_units_from_request(edu_organizations, declaration):
    """Возвращается список желаемых организаций DeclarationUnit-ов.

    :param edu_organizations: данные об ДОО из запроса.
                              spyne EduOrganizationsData
    :param declaration: Django model instance

    """

    from .django_objects_proxy import DeclarationUnitProxy
    return DeclarationUnitProxy(
        units=edu_organizations.EduOrganization,
        declaration=declaration).get()


def get_mo_from_request(edu_organizations, declaration):
    """
    Возвращается инстанс МО, к которому должны
    принадлежать все организации, указанные в запросе.

    :param edu_organizations: данные об ДОО из запроса.
                              spyne EduOrganizationsData

    """

    from .django_objects_proxy import DeclarationUnitProxy
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


class SmevAppliedDocuments(object):

    ns = "{http://smev.gosuslugi.ru/request/rev111111}"

    def __init__(self, unzipped, req_code):

        str_req_code = (
            req_code if isinstance(req_code, str) else req_code.decode()
        )
        description_xml_name = f'{str_req_code}.xml'
        if description_xml_name not in unzipped.namelist():
            raise SpyneException(
                u"Отсутствует xml описание приложенных файлов с именем "
                u"{name}".format(name=description_xml_name))
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

    def _save(self, file_info, unzipped):

        file_code, file_name, url = file_info
        try:
            _file = unzipped.open(url)
        except KeyError:
            try:
                _file = unzipped.open(file_code)
            except KeyError:
                raise SpyneException(
                    u"В архиве отсутствует файл с кодом {code}, "
                    u"что описан в xml".format(code=file_code))

        content_file = ContentFile(_file.read(), name=file_name)
        _file.close()

        DeclarationDoc.objects.create(
            file=content_file,
            name=file_name,
            declaration=self._declaration)

    def attach(self):

        # Если есть BinaryData но нет RequestCode выбрасываем исключение
        if (self._binary_data
            and self._binary_data.strip()
                and not self._request_code):
            raise SpyneException(u"Тег RequestCode не задан")

        if self._binary_data and self._binary_data.strip():
            decode_file_data = base64.decodebytes(self._binary_data)
            decode_file_data_io = io.BytesIO(decode_file_data)
            unzipped = zipfile.ZipFile(decode_file_data_io)

            smev_applied_files = SmevAppliedDocuments(
                unzipped, self._request_code)

            for file_info in smev_applied_files:
                self._save(file_info, unzipped)


def reject_request(ctx, message):
    ctx.udc.is_reject = u"REJECT"

    raise SpyneException(message)


def get_decl_priv(declaration, for_change=False):
    """
    Возвращает наиболее приоритетную льготу из заявки
    Для метода изменения пришедший список сравниваем совсем списком льгот
    :param declaration: заявление
    :return: list of DeclsrationPrivilege или []

    """

    benefits = []
    if for_change:
        benefits = list(declaration.declarationprivilege_set.all())
        return benefits
    else:
        confir_attr = get_priv_data(declaration)
        if confir_attr:
            benefits = [confir_attr.declaration_privilege, ]
    return benefits


def get_priv_data(declaration):
    """
    возвращает информацию о подтверждении приоритетной льготы, если она есть
    :param declaration: Заявление
    :return: DeclarationPrivilege или None

    """

    priv_conf_attr = None
    best_privilege = declaration.best_privilege
    if best_privilege:
        # Выбираем доп информацию среди подтвержденных данных
        # по данной льготе для данного заявления.
        # Если в заявке нет "лучшей" льготы, то и других льгот тоже нет
        priv_conf_attr = PrivilegeConfirmationAttributes.objects.filter(
            declaration_privilege__privilege_id=best_privilege.id,
            declaration_privilege__declaration_id=declaration.id
        ).first()
    return priv_conf_attr


class RegionalCheckDeclarationProcess(CheckDeclarationProcess):
    """Расширяем базовый класс

    Включаем несколько новых тегов в ответ. Изменяем формат даты.
    Фильтруем список учреждений на выходе, если заявление в статусах
    направлен и зачислен

    """

    summary_with_out_age = SummaryWithOutAgePosition()

    def process(self):

        result = []

        decl_units = DeclarationUnit.objects.filter(
            declaration=self.declaration
        ).order_by("ord").select_related("unit")
        if self.declaration.status.code == DSS.DIRECTED:
            decl_units = decl_units.filter(
                unit_id__in=Direct.objects.for_declaration(
                    self.declaration).values_list('group__unit'))
        elif self.declaration.status.code == DSS.ACCEPTED:
            decl_units = decl_units.filter(
                unit_id__in=Pupil.objects.for_declaration(
                    self.declaration).values_list('grup__unit'))

        for declaration_unit in decl_units:

            unit_queue = self._get_base_unit_queue_dict(declaration_unit)

            if self.summary_position:
                positions = self._get_indexes(declaration_unit)

                for attribute, positions in list(positions.items()):
                    position = (
                        positions[0].get("position", u"-")
                        if positions else None)
                    if position is None:
                        continue

                    unit_queue.update({attribute: str(position)})
            result.append(unit_queue)
        return result

    def _get_base_unit_queue_dict(self, declaration_unit):

        unit_queue = super(
            RegionalCheckDeclarationProcess, self
        )._get_base_unit_queue_dict(
            declaration_unit)

        unit_queue.update(DeclID=self.declaration.client_id)

        # Заменяем значения дат строковыми представлениями
        unit_queue['Date'] = unit_queue['Date'].strftime(
            '%d.%m.%Y %H:%m:%S')
        unit_queue['DesiredDate'] = unit_queue['DesiredDate'].strftime(
            '%d.%m.%Y') if unit_queue['DesiredDate'] else ''

        return unit_queue

    def _get_indexes(self, declaration_unit):

        result_dict = super(
            RegionalCheckDeclarationProcess, self
        )._get_indexes(declaration_unit)

        result_dict.update(
            AllCategoryPosition=filter_by_unit(
                self.summary_with_out_age, declaration_unit.unit_id)
        )

        return result_dict
