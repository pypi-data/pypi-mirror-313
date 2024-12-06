import datetime
import logging
import os
import sys
import traceback

from django.conf import settings as kinder_settings
from django.db.transaction import atomic
from django.db.utils import DataError
from kinder.core.declaration.enum import DeclarationSourceEnum
from kinder.core.declaration.enum import DeclarationTypeInteractionEnum as DTIE
from kinder.core.declaration.enum import (
    ReasonChangingDesiredDateEnumerate as RGDD)
from kinder.core.declaration.models import DeclarationStatusLog
from kinder.core.declaration_status.enum import DSS
from kinder.core.declaration_status.enum import DECL_STATUS_ERR
from kinder.settings import logger
from kinder.webservice.api import declaration as decl_api
from kinder.webservice.api.exceptions import ApiException
from kinder.webservice.signals import Status_send
from kinder.webservice.spyne_ws.exceptions import SpyneException
from lxml import etree as _etree
from spyne.decorator import rpc
from spyne_smev._utils import el_name_with_ns
from spyne_smev.fault import ApiError
from spyne_smev.smev256 import Smev256

from concentrator import settings
from concentrator.dict.constants import OperationEnumerate
from concentrator.exceptions import DuplicateExternalID
from concentrator.rules import AUTO_ARCHIVE
from concentrator.rules import DeclarationStatusCodeRule
from concentrator.rules import DeclarationStatusNameRule
from concentrator.webservice.entities import *
from concentrator.webservice.helpers import get_binary_data
from concentrator.webservice.proxy import FindApplicationsProxy
from concentrator.webservice.proxy import GetApplicationProxy
from concentrator.webservice.proxy import GetApplicationQueueProxy
from concentrator.webservice.proxy import GetApplicationStateProxy
from concentrator.webservice.proxy import new_application_with_duplicate_check

from .client import SmevClient
from .config import cont
from .helpers import reject_request
from .plugins import FixPrefixPluginLoadData
from .plugins import FixPrefixPluginUpdateApplicationState
from .plugins import UpdateStateSpikeNailPlugin
from .spyne_objects_proxy import ApplicantDataProxy
from .spyne_objects_proxy import DeclaredPersonDataProxy
from .spyne_objects_proxy import EduOrganizationsDataProxy


"""
Методы концентратора
- Передача Заявления в региональную систему предоставления услуг
    NewApplication
- Поиск Заявлений по совпадению персональных данных ребенка
    FindApplicationsByDeclaredPersonRequest
- Поиск Заявлений по совпадению персональных данных заявителя
    FindApplicationsByApplicant
- Запрос текущей очереди заявления
    GetApplicationQueue
- Запрос текущего статуса заявления
    GetApplicationStateRequest
- Получение данных Заявления для изменения
    GetApplication
- Изменение данных заявления
    UpdateApplication
"""


def _correct_size(binary_data):

    if settings.MAX_BINARY_DATA_SIZE == 0:
        return True

    if isinstance(binary_data, str):
        try:
            binary_data = str(binary_data)
        except UnicodeEncodeError:
            pass

    return sys.getsizeof(binary_data, default=0) <= (
        settings.MAX_BINARY_DATA_SIZE)


@rpc(
    NewApplicationRequest,
    _returns=NewApplicationResponse,
    _body_style='bare',
    _out_message_name='NewApplicationResponse')
def NewApplicationRequest(self, NewApplicationRequest):
    binary_data, request_code = get_binary_data(self.udc)
    if not _correct_size(binary_data):
        reject_request(self, u'Заявление не принято ведомством. '
                             u'Общий объем файлов превышает максимально '
                             u'допустимый размер 3584 Кб')
    # Создание фильтра на первом этапе

    with atomic():
        try:
            result = new_application_with_duplicate_check(
                self, NewApplicationRequest, binary_data, request_code)
        except DuplicateExternalID as e:
            reject_request(self, ', '.join(e.args))
        except SpyneException as e:
            reject_request(self, e.faultstring)
        except DataError:
            reject_request(
                self, u'Ошибка в заполнении xml-запроса. Заявление не создано'
            )

    return NewApplicationResponse(RegionalId=str(result))


@rpc(
    FindApplicationsByDeclaredPersonRequest,
    _returns=FindApplicationsByDeclaredPersonResponse,
    _body_style='bare',
    _out_message_name='FindApplicationsByDeclaredPersonResponse')
def FindApplicationsByDeclaredPersonRequest(
        ctx, FindApplicationsByDeclaredPersonRequest):
    return FindApplicationsProxy(
        FindApplicationsByDeclaredPersonRequest,
        mode=FindApplicationsProxy.BY_CHILD
    ).process()


@rpc(
    FindApplicationsByApplicantRequest,
    _returns=FindApplicationsByApplicantResponse,
    _body_style='bare',
    _out_message_name='FindApplicationsByApplicantResponse')
def FindApplicationsByApplicantRequest(
        ctx, FindApplicationsByApplicantRequest):
    return FindApplicationsProxy(
        FindApplicationsByApplicantRequest,
    ).process()


@rpc(
    GetApplicationQueueRequest,
    _returns=GetApplicationQueueResponse,
    _body_style='bare',
    _out_message_name='GetApplicationQueueResponse')
def GetApplicationQueueRequest(ctx, request):

    try:
        declaration = decl_api.get_decl_by_external_id(request.ExternalId)
    except ApiException as e:
        reject_request(ctx, e.message)
    except SpyneException as e:
        reject_request(ctx, e.faultstring)

    return GetApplicationQueueProxy(declaration, request).process()


@rpc(GetApplicationStateRequest,
     _returns=GetApplicationStateResponse,
     _body_style='bare',
     _out_message_name='GetApplicationStateResponse')
def GetApplicationStateRequest(ctx, request):
    ExternalId = request.ExternalId
    try:
        decl = decl_api.get_decl_by_external_id(ExternalId)
    except ApiException as e:
        reject_request(ctx, e.message)
    except SpyneException as e:
        reject_request(ctx, e.faultstring)
    return GetApplicationStateProxy(decl).process()


@rpc(GetApplicationRequest,
     _returns=GetApplicationResponse,
     _body_style='bare',
     _out_message_name='GetApplicationResponse')
def GetApplicationRequest(ctx, request):
    ExternalId = request.ExternalId
    try:
        decl = decl_api.get_decl_by_external_id(ExternalId)
    except ApiException as e:
        reject_request(ctx, e.message)
    except SpyneException as e:
        reject_request(ctx, e.faultstring)
    decl_proxy = DeclaredPersonDataProxy(decl)
    app_proxy = ApplicantDataProxy(decl)
    dou_proxy = EduOrganizationsDataProxy(decl)
    return GetApplicationProxy(
        decl, decl_proxy, app_proxy, dou_proxy).process()


@rpc(UpdateApplicationRequest,
     _returns=UpdateApplicationResponse,
     _body_style='bare',
     _out_message_name='UpdateApplicationResponse')
def UpdateApplicationRequest(ctx, request):

    binary_data, request_code = get_binary_data(ctx.udc)
    if not _correct_size(binary_data):
        reject_request(ctx, u'Заявление не принято ведомством. '
                            u'Общий объем файлов превышает максимально '
                            u'допустимый размер 3584 Кб')

    ExternalId = request.ExternalId
    try:
        decl = decl_api.get_decl_by_external_id(ExternalId)
    except ApiException as e:
        reject_request(ctx, e.message)
    except SpyneException as e:
        reject_request(ctx, e.faultstring)

    if decl.status.code in DSS.update_application_reject_statuses():
        reject_request(ctx, DECL_STATUS_ERR.format(decl.status.name))

    today = datetime.date.today()
    if request.EntryDate < today:
        reject_request(
            ctx, (f'Указанная желаемая дата зачисления раннее, '
                  f'чем {today.strftime(kinder_settings.DATE_FORMAT)}'))

    binary_data, request_code = get_binary_data(ctx.udc)
    proxy_name = "reset" if request.State == "11" else "default"
    update_proxy = cont.get("UpdateProxy", proxy_name)
    return update_proxy.process(
        request, decl, binary_data=binary_data, request_code=request_code)


class Protocol(Smev256):
    """
    xsd концентратра не совпадает с найше, поэтому приходится хакать
    у них пустой тип appData
    """
    def __init__(self, *args, **kwargs):
        super(Protocol, self).__init__(*args, **kwargs)

        def rebuild_error(ctx):
            """Ошибки должны быть в виде
            <MessageText> Заявление по заданным.... </MessageText>"""
            app_data = ctx.out_document.find('.//{{{smev}}}AppData'.format(
                **self._ns))
            if app_data is not None:
                result = app_data.getchildren()
                # проверяем что сообщение об ошибке и меняем его
                if result and 'Error' in result[0].tag:
                    error_message = ''
                    error_message_tag = app_data.find(
                        './/{{{tns}}}Error/{{{tns}}}errorMessage'.format(
                            **app_data.nsmap))
                    if error_message_tag is not None:
                        error_message = error_message_tag.text
                    app_data.clear()
                    result = _etree.SubElement(app_data, 'MessageText')
                    result.text = error_message

        self.smev_params.update(
            dict(SenderCode=kinder_settings.SMEV_SYS_MNEMONICS,
                 SenderName=kinder_settings.SMEV_SYS_NAME)
        )
        # Разрешаем парсить большие XML
        self.parser_kwargs['huge_tree'] = True
        self.event_manager.add_listener(
            'after_serialize_smev', rebuild_error)

    def _validate_smev_element(self, element):
        if settings.ADDXSITYPE:
            attr = "{http://www.w3.org/2001/XMLSchema-instance}type"
            xsi_typed = element.findall('./*[@%s]' % attr)
            for el in xsi_typed:
                el.attrib.pop(attr)
        super(Protocol, self)._validate_smev_element(element)

    def serialize(self, ctx, message):
        super(Protocol, self).serialize(ctx, message)
        if settings.ADDXSITYPE:
            list_paths = []
            if ctx.method_name in ['GetApplicationQueueRequest']:
                list_paths = [
                    './/tns:Applicant', './/tns:Applicant//',
                    './/tns:DeclaredPerson', './/tns:DeclaredPerson//'
                ]
            if ctx.method_name in [
                    'FindApplicationsByApplicantRequest',
                    'FindApplicationsByDeclaredPersonRequest',
                ]:
                list_paths = ['.//tns:Application']
            namespaces = {
                'tns':
                    "http://concentrator.gosuslugi.ru/regservicedelivery/smev"
            }
            elem_list = []
            for path in list_paths:
                elem_list.extend(ctx.out_document.findall(
                    path, namespaces=namespaces))
            for elem in elem_list:
                i = elem.tag.find('}')
                elem.tag = elem.tag[i + 1:]

        if settings.ADDXSITYPE:
            app_data = ctx.out_document.find(
                './/{{{smev}}}AppData'.format(**self._ns))
            if app_data is not None:
                app_data.attrib[
                    "{http://www.w3.org/2001/XMLSchema-instance}type"] = (
                    "tns:%s" % ctx.method_name.replace('Request', 'Response'))


class ConcentratorProtocol(Protocol):
    """Наследуемся от Protocol
    Разница в работе заключается в том, что родитель
    при ошибке в тег Status запишет строку INVALID,
    а наследник строку FAILURE.
    <smev:Status>INVALID</smev:Status> --> <smev:Status>FAILURE</smev:Status>

    """

    def _create_message_element(self, ctx):
        root_element = super(
            ConcentratorProtocol, self)._create_message_element(ctx)

        if ctx.out_error and isinstance(ctx.out_error, ApiError):
            SMEV = el_name_with_ns(self._ns["smev"])
            status_element = root_element.find(
                ".//{0}".format(SMEV("Status")))
            if status_element is not None:
                status_element.text = getattr(
                    ctx.udc, "is_reject", False) or "FAILURE"

        return root_element


class LoadData(object):
    """
    Загрузка справочников в концентратор
    """
    # TODO: Вынести в параметры
    REQUST_PARAMS = dict(
        EpguName='',
        IscName='',
        ServiceName='ISC',
        TypeCode='GSRV',
        Status='REQUEST',
        ExchangeType='2',
    )

    OPERATIONS = (OperationEnumerate.ADD,
                  OperationEnumerate.UPDATE,
                  OperationEnumerate.DELETE)

    def __init__(self, params):
        if not settings.SMEV_CONCENTRATOR_WSDL_URL:
            raise Exception('not found SMEV_CONCENTRATOR_WSDL_URL')
        if settings.SMEV_CONCENTRATOR_WSDL_FILE.startswith('file://'):
            path = settings.SMEV_CONCENTRATOR_WSDL_FILE.split('file://')[1]
            if not os.path.exists(path):
                raise Exception(
                    'WSDL file not found.'
                    'Check SMEV_CONCENTRATOR_WSDL_FILE. ({})'.format(path)
                )

        # Запрос на синхронизацию справочников
        logging.basicConfig(level=logging.INFO)
        logging.getLogger('suds.client').setLevel(logging.DEBUG)
        logging.getLogger('suds.transport').setLevel(logging.DEBUG)
        self.url = settings.SMEV_CONCENTRATOR_WSDL_URL

        client_params = dict(
            url=settings.SMEV_CONCENTRATOR_WSDL_FILE,
            private_key_path=kinder_settings.SMEV_CERT_AND_KEY,
            private_key_pass=kinder_settings.SMEV_PRIVKEY_PASS,
            certificate_path=kinder_settings.SMEV_CERT_AND_KEY,
            in_certificate_path=kinder_settings.SMEV_CERT_AND_KEY,
            digest_method=kinder_settings.DIGEST_METHOD,
            autoblend=True,
            plugins=self._get_plugins(),
            location=self.url,
            timeout=settings.LOAD_DATA_TIMEOUT
        )
        if kinder_settings.USE_PROXY and kinder_settings.PROXY_PARAMS:
            client_params.update(
                proxy=dict(http=kinder_settings.PROXY_PARAMS,
                           https=kinder_settings.PROXY_PARAMS)
            )
        self.client = SmevClient(**client_params)
        self.msg = self.create_message(params)
        self.params = params

    def _get_plugins(self):

        return [FixPrefixPluginLoadData(), ]

    def _find_tns(self, list_types, name_type):
        """
        Получаем на вход список Имя типа, его ns,
        ищем нужный нам ns и возвращаем его
        :param list_types:
        :param name_type:
        :return:

        """

        prefix = ''
        for name, tns in list_types:
            if name == name_type:
                prefix = tns
                break
        return prefix

    def create_elem(self, name,  pref=None, params=None):
        params = {} if params is None else params
        element = self.client.factory.create(
            '{%s}%s' % (pref, name) if pref else name)
        for key, value in params.items():
            setattr(element, key, value)
        return element

    def create_message(self, params):
        prefix = self._find_tns(list(self.client.wsdl.schema.elements.keys()),
                                'LoadDataRequest')
        msg = self.create_elem('LoadDataRequest', prefix)
        msg.Message = self.create_message_message()
        msg.MessageData = self.create_message_data(params)
        return msg

    def create_message_message(self):
        # Заголовок
        prefix = self._find_tns(list(self.client.wsdl.schema.types.keys()),
                                'MessageType')
        message = self.create_elem('MessageType', prefix)

        message.Sender = self.create_elem(
            'Sender', prefix, dict(Code=kinder_settings.SMEV_SYS_MNEMONICS,
                                   Name=kinder_settings.SMEV_SYS_NAME))

        message.Recipient = self.create_elem(
            'Recipient', prefix, dict(Code=kinder_settings.SMEV_EPGU_MNEMONIC,
                                      Name=kinder_settings.SMEV_EPGU_NAME))
        message.ServiceName = self.REQUST_PARAMS['ServiceName']
        message.TypeCode = self.REQUST_PARAMS['TypeCode']
        message.Status = self.REQUST_PARAMS['Status']

        message.Date = datetime.datetime.now()
        message.ExchangeType = self.REQUST_PARAMS['ExchangeType']

        return message

    def create_values_list(self, params):
        params = [] if params is None else params
        values_list = []
        prefix = self._find_tns(list(self.client.wsdl.schema.types.keys()),
                                'CatalogProperty')
        for name, value in params:
            val = self.create_elem('CatalogProperty', prefix)
            val.value = value
            val._Name = name
            values_list.append(val)
        return values_list

    def create_elements_list(self, root_elem, params_list=None, pref=None):
        if not pref:
            pref = OperationEnumerate.DELETE
        prefix = self._find_tns(list(self.client.wsdl.schema.types.keys()),
                                'AddCatalogDataItem')
        factory_class_names = {
            OperationEnumerate.ADD: '{%s}AddCatalogDataItem' % prefix,
            OperationEnumerate.UPDATE: '{%s}UpdateCatalogDataItem' % prefix,
            OperationEnumerate.DELETE: '{%s}DeleteCatalogDataItem' % prefix
        }
        elements_list = []
        for item in params_list:
            code, params = item
            elem = self.client.factory.create(factory_class_names[pref])
            elem.Code = code
            if pref != OperationEnumerate.DELETE:
                elem.Value = self.create_values_list(params)
            elements_list.append(elem)
        setattr(root_elem, pref, elements_list)

    def create_message_data(self, params):
        # Сообщение
        prefix = self._find_tns(list(self.client.wsdl.schema.types.keys()),
                                'MessageDataType')
        message_data = self.create_elem('MessageDataType', prefix)
        prefix = self._find_tns(list(self.client.wsdl.schema.elements.keys()),
                                'AppData')
        app_data = self.create_elem('AppData', prefix)
        app_data.Code = params['code']
        app_data.RegCode = (
            settings.SMEV_CONCENTRATOR_REG_CODE)
        for operation in self.OPERATIONS:
            params_list = params.get(operation)
            if params_list:
                self.create_elements_list(
                    app_data, params_list, operation)
        message_data.AppData = app_data
        return message_data

    def log_request(self, method_name=None, error=None):
        return self.client.log_request(
            smev_method=method_name or self.__class__.__name__,
            error=error)

    def load_data(self):
        """
        Отправка данных на синхронизацию.
        Логирование неудачных отправок.
        :return:

        """

        error = None
        try:
            result = self.client.service.LoadData(
                self.msg.Message, self.msg.MessageData)
        except Exception:
            error = traceback.format_exc()

        self.log_request(error=error)


class UpdateApplicationState(LoadData):
    def log_request(self, method_name=None, error=None):
        log = super(UpdateApplicationState, self).log_request(
            method_name, error
        )
        Status_send.send(
            sender=self.__class__,
            declaration_id=self.params['regional_id'],
            smev_log_id=log.id
        )
        return log

    def create_message(self, params):
        msg = self.client.factory.create('UpdateApplicationStateRequest')
        msg.Message = self.create_message_message()
        msg.MessageData = self.create_message_data(params)
        return msg

    def create_message_data(self, params):
        # Сообщение
        prefix = self._find_tns(list(self.client.wsdl.schema.types.keys()),
                                'MessageDataType')
        message_data = self.create_elem('MessageDataType', prefix)
        prefix = self._find_tns(list(self.client.wsdl.schema.elements.keys()),
                                'AppData')
        app_data = self.create_elem('AppData', prefix)
        if params.get('external_id'):
            app_data.ExternalId = params['external_id']
        app_data.RegionalId = params['regional_id']
        app_data.State = params['state']
        app_data.Details = params['details']
        app_data.RegCode = (
            settings.SMEV_CONCENTRATOR_REG_CODE)
        message_data.AppData = app_data
        return message_data

    def _get_plugins(self):
        return [FixPrefixPluginUpdateApplicationState()]

    def load_data(self):
        """
        Отправка данных на синхронизацию.
        Логирование неудачных отправок.
        :return:

        """

        error = None
        try:
            self.client.service.UpdateApplicationState(
                self.msg.Message, self.msg.MessageData)
        except Exception as e:
            error = traceback.format_exc()
        finally:
            return self.log_request(
                error=error, method_name='UpdateApplicationState'
            )


def send_update_application_state(
        declaration,
        is_auto=False,
        auto_archive=True,
        commentary=None,
        log_id=None,
        desired_date_changed=False):
    """
    Хелпер отправки информации о смене статуса заявления из концентратора
    Статус берем не текущий, а из лога смены статуса,
    т.к. отправка мб отложенной, и текущий статус мб уже другой.

    :param declaration: заявление
    :type declaration: Declaration
    :param is_auto: авто-смена статуса при применении изменений из ЕПГУ
    :param commentary: комментарий пользователя при применение,
    либо отмене изменений
    :param log_id: идентификатор записи в логе о смене статуса заявления
    :param desired_date_changed: Признак изменения желаемой даты
    :type desired_date_changed: bool
    :param auto_archive: Присваивать ли архивный статус при авто-смене
    :type auto_archive: bool

    :return: СМЕВ лог запроса
    :rtype: Optional[SmevLog]

    """

    def _get_state(state, auto, commentary, auto_archive):

        # Статус по которому ищется соответствие в
        # DeclarationStatusCodeRule и DeclarationStatusNameRule
        search_state = state

        if auto and auto_archive:
            search_state = AUTO_ARCHIVE

        if kinder_settings.PARTNER_QUIRKS == 'NSO':
            details = commentary
        elif settings.SEND_STATE_WITH_USER_COMMENTARY:
            if commentary:
                details = commentary
            else:
                details = u'Комментарий отсутствует'
        else:
            details = DeclarationStatusNameRule.get_concetr(search_state)

        return DeclarationStatusCodeRule.get_concetr(search_state), details

    if settings.DISABLE_UPDATE_APPLICATION_STATE:
        return

    # UpdateState выполняется только для заявок пришедших из концентратора.
    # https://conf.bars-open.ru/pages/viewpage.action?pageId=3080736
    if (
        declaration.source != DeclarationSourceEnum.CONCENTRATOR
        or declaration.type_interaction is None
        or declaration.type_interaction != DTIE.SMEV_2
    ):
        return
    if log_id:
        log = DeclarationStatusLog.objects.get(id=log_id)
        status = log.status.code
    else:
        status = declaration.status.code
    state, details = _get_state(status, is_auto, commentary, auto_archive)

    # В случае изменения статуса заявки на статус учавствующий в очереди
    # и изменения желаемой даты зачисления дополняется текст сообщения.
    if desired_date_changed and status in DSS.status_queue_full():
        details = (
            f'{details}. Изменена дата желаемого зачисления. '
            f'Причина: {RGDD.values[declaration.reason_change]}')

    params = {
        'state': state,
        'details': details,
        'regional_id': declaration.id,
    }

    if declaration.client_id:
        params.update({'external_id': declaration.client_id})

    try:
        # не логируется, если client не доступен, за это отвечает LoadData.
        smev_log = UpdateApplicationState(params).load_data()
        return smev_log
    except Exception:
        logger.error(traceback.format_exc())
        # Ошибки запроса отлавливаются и логгируются внутри load_data.
        # Сюда попадёт, если ошибка произошла до load_data.
        # (например если WSDL файл не существует)
        raise
