from spyne.decorator import rpc
from spyne.model.complex import Array
from spyne.model.primitive import Unicode

from kinder.core.declaration_status.enum import DSS
from kinder.core.declaration_status.enum import DECL_STATUS_ERR
from kinder.webservice.api import declaration as decl_api
from kinder.webservice.api.exceptions import ApiException
from kinder.webservice.spyne_ws.declaration_info import helpers
from kinder.webservice.spyne_ws.declaration_info.errors import DeclCheckErrors
from kinder.webservice.spyne_ws.declaration_info.errors import (
    DeclCheckException)
from kinder.webservice.spyne_ws.declaration_info.types import ChildPersonal
from kinder.webservice.spyne_ws.declaration_info.types import DeclarantPersonal
from kinder.webservice.spyne_ws.exceptions import SpyneException

from lipetsk_specifics.webservice.entities import DeclarationStatus
from lipetsk_specifics.webservice.entities import GetApplicationResponse
from lipetsk_specifics.webservice.entities import NewApplicationRequest
from lipetsk_specifics.webservice.entities import UpdateApplicationRequest
from lipetsk_specifics.webservice.entities import UpdateApplicationResponse
from lipetsk_specifics.webservice.proxy import LipetskNewApplicationProxy

from .config import cont
from .entities import GetApplicationRequest
from .entities import NewApplicationResponse
from .helpers import RegionalCheckDeclarationProcess
from .helpers import get_binary_data
from .proxy import GetApplicationProxy
from .spyne_objects_proxy import LipetskApplicantDataProxy
from .spyne_objects_proxy import LipetskDeclaredPersonDataProxy
from .spyne_objects_proxy import LipetskEduOrganizationsDataProxy


# Методы концентратора
# - Передача Заявления в региональную систему предоставления услуг
#   NewApplication
@rpc(
    NewApplicationRequest,
    _returns=NewApplicationResponse,
    _body_style='bare',
    _out_message_name='NewApplicationResponse')
def NewApplicationRequest(self, NewApplicationRequest):
    binary_data, request_code = get_binary_data(self.udc)
    message_id = self.udc.in_smev_header.MessageId
    result = LipetskNewApplicationProxy(
        NewApplicationRequest,
        binary_data,
        request_code,
        message_id=message_id).process()

    return NewApplicationResponse(RegionalId=str(result))


# Получение данных Заявления для изменения
# GetApplication
@rpc(GetApplicationRequest,
     _returns=GetApplicationResponse,
     _body_style='bare',
     _out_message_name='GetApplicationResponse')
def GetApplicationRequest(ctx, request):

    ExternalId = request.ExternalId
    try:
        decl = decl_api.get_decl_by_external_id(ExternalId)
    except ApiException as exc:
        raise SpyneException(exc.code, exc.message)

    decl_proxy = LipetskDeclaredPersonDataProxy(decl)
    app_proxy = LipetskApplicantDataProxy(decl)
    dou_proxy = LipetskEduOrganizationsDataProxy(decl)
    return GetApplicationProxy(
        decl, decl_proxy, app_proxy, dou_proxy).process()


# - Изменение Заявления в региональной системе предоставления услуг
@rpc(
    UpdateApplicationRequest,
    _returns=UpdateApplicationResponse,
    _body_style='bare',
    _out_message_name='UpdateApplicationResponse')
def UpdateApplicationRequest(
        ctx, request):
    ExternalId = request.ExternalId
    try:
        decl = decl_api.get_decl_by_external_id(ExternalId)
    except ApiException as exc:
        raise SpyneException(exc.code, exc.message)

    if decl.status.code in DSS.update_application_reject_statuses():
        ctx.udc.is_reject = "REJECT"
        raise SpyneException(DECL_STATUS_ERR.format(decl.status.name))

    binary_data, request_code = get_binary_data(ctx.udc)

    case_number_tag = ctx.udc.in_smev_message_document.find(
        "{http://smev.gosuslugi.ru/rev120315}CaseNumber")
    if case_number_tag is None or not case_number_tag.text:
        raise SpyneException(
            message=u"Тэг CaseNumber отсутствует или не заполнен")

    proxy_name = "reset" if request.State == "11" else "lipetsk_proxy"
    update_proxy = cont.get("UpdateProxy", proxy_name)
    return update_proxy.process(
        request, decl, binary_data=binary_data, request_code=request_code,
        case_number=case_number_tag.text)


@rpc(Unicode(nillable=False, min_occurs=1),
     DeclarantPersonal,
     ChildPersonal.customize(nillable=False, min_occurs=1),
     _in_variable_names={
         "okato": "OKATO",
         "declarant_personal": "DeclarantPersonal",
         "child_personal": "ChildPersonal"},
     _in_message_name="CheckDeclarationDOURequest",
     _returns=Array(DeclarationStatus))
def CheckDeclarationDOU(ctx, okato, declarant_personal, child_personal):

    results = []

    try:
        declarations = helpers.find_declarations(
            child_personal, True, okato
        )
    except DeclCheckException as e:
        err_code = e.message
        err = DeclCheckErrors.ERR_CODES.get(err_code)
        raise SpyneException(
            code=err_code,
            message=err[1] if err else u'Неизвестная ошибка. Код %s' % err_code
        )

    for declaration in declarations:

        results.extend(
            RegionalCheckDeclarationProcess(
                declaration).process())

    return results
