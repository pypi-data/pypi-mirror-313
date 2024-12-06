from collections import defaultdict
from itertools import chain
import json

from django.db.models import OuterRef
from django.db.models import Prefetch
from django.db.models import Q
from django.db.models import Subquery
from django.db.models import Value
from django.db.models.fields import TextField
from django.db.models.functions import Cast
from django.db.models.functions import Coalesce

from m3 import plugins

from kinder.core.audit_log_kndg.helpers import get_model
from kinder.core.audit_log_kndg.models import AdditionalEncoder
from kinder.core.children.models import ChildrenDelegate
from kinder.core.declaration.enum import DeclarationSourceEnum
from kinder.core.declaration.enum import DeclarationTypeInteractionEnum as DTIE
from kinder.core.declaration.models import Declaration
from kinder.core.declaration.models import DeclarationPrivilege
from kinder.core.declaration.proxy import get_initial_status
from kinder.core.declaration_status.models import DSS
from kinder.core.declaration_status.models import DeclarationStatus
from kinder.core.helpers import prepare_name
from kinder.core.queue_module.api import get_queue_by_context_service
from kinder.core.queue_module.context import QueueContext
from kinder.core.unit.models import Unit
from kinder.provider import features
from kinder.webservice.helpers import find_existing_child
from kinder.webservice.helpers import find_existing_delegate
from kinder.webservice.spyne_ws.exceptions import SpyneException
from m3.actions import ApplicationLogicException
from yadic.container import Injectable

from concentrator import settings
from concentrator.change import ChangeHelper
from concentrator.change import DeclarationChangeHelper
from concentrator.change import DeclarationDocsChangeHelper
from concentrator.change import StorageHelper
from concentrator.exceptions import DuplicateExternalID
from concentrator.models import ChangeDeclaration
from concentrator.models import ChangeSource
from concentrator.rules import *
from concentrator.webservice.django_objects_proxy import *
from concentrator.webservice.helpers import DocumentWorker
from concentrator.webservice.helpers import _get_document_reference_from_ctx
from concentrator.webservice.helpers import get_delegate
from concentrator.webservice.spyne_objects_proxy import *

from .config import cont


class NewApplicationProxy:
    """ Прокси объект для метода NewApplication """

    def __init__(self, request, binary_data, req_code):

        self._request = request
        self._external_id = request.ExternalId
        self._submit_date = request.SubmitDate
        self._entry_date = request.EntryDate
        self._adaptation_program_type = request.AdaptationProgramType
        self._adaptation_program_doc_info = getattr(
            request, "AdaptationProgramDocInfo", None)
        self._delegate_data = request.Applicant
        self._child_data = request.DeclaredPerson
        self._benefits = self._child_data.Benefits
        self._edu_organizations = getattr(request, 'EduOrganizations', None)
        self._schedule = getattr(request, "Schedule", None)
        self._binary_data = binary_data
        self._request_code = req_code
        self._document_references = _get_document_reference_from_ctx(
            request)

        self._ch_helpers = []

    def _build_delegate(self):
        u"""Создает обьект представителя из данных запроса."""
        return DelegateProxy(self._delegate_data).get()

    def _build_child(self):
        u"""Создает обьект ребенка из данных запроса."""
        return ChildrenProxy(
            self._child_data,
            self._adaptation_program_type,
            self._adaptation_program_doc_info).get()

    def _create_benefits(self):
        benefits = getattr(self._benefits, "Benefit", None) or []
        privileges = PrivilegeProxy(
            [(benefit.name, benefit.Type)
                for benefit in benefits]).get()
        return privileges

    def _get_schedule_type(self):
        """Возвращает приоритетное время прибывания, либо None"""

        # В запросе может быть указано несколько режимов,
        # но в системе в заявке можно указать только одно.
        # Приоритет определяется следующим образом:
        # [полн., сокр., крат., продл., кругл.]
        priority = [3, 2, 1, 4, 5]
        schedule = getattr(
            self._schedule, 'ScheduleType', []
        ) if self._schedule else []
        schedule = sorted(schedule, key=lambda x: priority.index(x))

        return WorkTypeRule.get_system(schedule[0]) if schedule else None

    def _build_declaration(self):
        u"""Создает обьект заявления из данных запроса."""

        declaration_source = (
            plugins.ExtensionManager().execute(
                'kinder.plugins.hmao_services.extensions.'
                'get_declaration_source',
                self._external_id)
            or features.get_feature(
                'concentrator.webservice.service.'
                'NewApplicationRequest.get_source')())

        type_interaction = (
            DTIE.SMEV_2
            if declaration_source == DeclarationSourceEnum.CONCENTRATOR
            else None)

        return Declaration(
            date=self._submit_date,
            desired_date=self._entry_date,
            offer_other=self._edu_organizations.AllowOfferOther,
            client_id=self._external_id,
            work_type_id=self._get_schedule_type(),
            source=declaration_source,
            type_interaction=type_interaction,
            portal=1)

    def _attache_documents(self, declaration):

        DocumentWorker(
            declaration, self._binary_data, self._request_code).attach()

    def _save_doc_extra_info(self, declaration):

        DocExtraInfoProxy(declaration, self._document_references).save()

    def _save_privileges(self, privileges, declaration):
        for privilege in privileges:
            DeclarationPrivilege.objects.create(
                declaration=declaration,
                datetime=datetime.datetime.now(),
                privilege=privilege)

    def check_model(self, name_model, conc_data, have_data):
        """собирает все изменения модели
        :type name_model: str
        :param name_model: имя модели из MAP_CHANGES
        :param conc_data: spyne object инстанс модеи воссозданный
         из данных на изменение
        :param have_data: django model инстанс модели из хранилища

        """

        class_model = get_model(name_model)
        ch_help = ChangeHelper(class_model, name_model)
        ch_help.check_diff(conc_data, have_data)
        self._ch_helpers.append(ch_help)

    def _create_or_update_child(self, child):
        u"""Ищет ребенка среди существующих, если такой имеется,
        то добавляются только изменения для принятия

        """

        existing_child = find_existing_child(child)

        if existing_child:
            self.check_model('Children', child, existing_child)
            child = existing_child

        return child

    def _create_or_update_delegate(self, delegate, delegate_extension, child):
        u"""Ищет представителя среди существующих, если такой имеется,
        то добавляются только изменения для принятия

        """

        existing_delegate = find_existing_delegate(delegate, child)

        if existing_delegate:
            self.check_model('Delegate', delegate, existing_delegate)
            delegate = existing_delegate
            if (
                hasattr(delegate, 'concentrator_delegate')
                and delegate.concentrator_delegate
            ):
                delegate_extension = delegate.concentrator_delegate

        return delegate, delegate_extension

    def process(self):
        check_organization_priorities(self._edu_organizations)

        try:
            # Пытаемся найти в системе заявку с таким же ExternalID
            existing_declaration = Declaration.objects.get(
                client_id=self._external_id)
        except Declaration.DoesNotExist:
            # Если заявки с таким статусом нет, то начинаем процесс создания
            # заявки
            pass
        else:
            # Заявка с таким же ExternalID уже существует
            # Если её статус не "Отказано в услуге" или "Архивная"
            # То возвращаем ответ со статусом REJECT
            if existing_declaration.status.code not in [
                    DSS.REFUSED, DSS.ARCHIVE]:
                raise DuplicateExternalID(
                    u"Заявление с таким ExternalID уже существует в системе")

            # Сохраняем то, что пришло во вкладку "Изменения с ЕПГУ"
            update_proxy = cont.get("UpdateProxy", "for_new_application")
            update_proxy.process(
                self._request, existing_declaration,
                binary_data=self._binary_data,
                request_code=self._request_code)

            return existing_declaration.id

        declaration = self._build_declaration()

        child = self._create_or_update_child(self._build_child())

        delegate, delegate_extension = self._build_delegate()
        if child.id:  # ребенок был найден, пробуем обновить представителя
            delegate, delegate_extension = self._create_or_update_delegate(
                delegate, delegate_extension, child
            )

        privileges = self._create_benefits()
        mo = get_mo_from_request(self._edu_organizations, declaration)

        try:
            delegate.save()
        except ApplicationLogicException as err:
            raise SpyneException(message=str(err))

        delegate_extension.delegate = delegate
        delegate_extension.save()

        try:
            child.save()
        except ApplicationLogicException as err:
            raise SpyneException(message=str(err))

        ChildrenDelegate.objects.get_or_create(
            children=child, delegate=delegate)

        declaration.children = child
        declaration.mo = mo
        declaration.status = get_initial_status(child)
        declaration.save()

        # создаются изменения по заявке для принятия
        StorageHelper.create_change(declaration, self._ch_helpers)

        # в declaration в datetime полях на данный момент может хранится
        # offset-aware datetime, но при получении через get может вернуться
        # offset-naive datetime (в зависимости от настроек приложения) и
        # наоборот, это может привести к ошибкам при сравнении поэтому
        # обновляем переменную
        declaration = Declaration.objects.get(pk=declaration.id)

        declaration_units = get_declaration_units_from_request(
            self._edu_organizations, declaration)

        for declaration_unit in declaration_units:
            # bulk create не использую т.к. он не вызывает save
            # метода и не срабатывают сигналы post_save и pre_save
            declaration_unit.declaration = declaration
            declaration_unit.save()

        self._save_privileges(privileges, declaration)
        self._save_doc_extra_info(declaration)
        self._attache_documents(declaration)

        return declaration.id


class GetApplicationQueueProxy:
    """
    Прокси объект для метода GetApplicationQueue
        Запрос текущей очереди заявления
    Возвращает список очередей во все желаемые ДОО заявки,
    каждая очередь содержит все заявки до нашей.

    """

    def __init__(self, declaration, request):
        assert declaration
        assert isinstance(declaration, Declaration)

        self.declaration = declaration
        self.request = request

    @staticmethod
    def _create_application(declaration, i):
        return ApplicationProxy.create_application(declaration, i)

    @staticmethod
    def _create_queue(unit, i, app):
        return Queue(
            EduOrganizationCode=str(unit.id),
            ApplicationsCount=i,
            Application=app)

    def _prepare_query(self, query):
        """Возвращает обработанную выборку.

        Добавляет доп. поля к выборке, отбирает только нужные поля
        и выполняет доп. выгрузку M:M.

        :param query: инстанс выборки
        :return: инстанс выборки
        """

        subquery_status_last_comment = Subquery(
            DeclarationStatusLog.objects.filter(
                declaration=OuterRef('id')
            ).order_by('-id').values('comment')[:1])

        subquery_first_delegate = (
            ChildrenDelegate.objects.filter(
                id=Subquery(
                    ChildrenDelegate.objects.filter(
                        children_id=OuterRef('children_id')
                    ).order_by('id').values('id')[:1])
            ).select_related('delegate').only(
                'delegate__surname', 'delegate__firstname',
                'delegate__patronymic', 'delegate__type',
                'delegate__dul_number', 'children_id'))

        subquery_declaration_privileges = (
            DeclarationPrivilege.objects.select_related(
                'privilege'
            ).only('privilege_id', 'privilege__type_id', 'declaration_id'))

        subquery_privilege_last_comment = Subquery(
            PrivilegeComment.objects.filter(
                declaration_privilege__declaration=OuterRef('id')
            ).order_by(
                '-declaration_privilege__datetime'
            ).values('concentrator_comment')[:1])

        return query.annotate(
                status_last_comment=subquery_status_last_comment,
                privilege_last_comment=subquery_privilege_last_comment,
                health_need_id=Coalesce(
                    'children__health_need_id',
                    Value(HealthNeed.NO_ID))
            ).select_related(
                'children', 'status'
            ).prefetch_related(
                Prefetch('declarationprivilege_set',
                         queryset=subquery_declaration_privileges,
                         to_attr='all_privileges')
            ).prefetch_related(
                Prefetch('children__childrendelegate_set',
                         queryset=subquery_first_delegate,
                         to_attr='first_childrendelegate')
            ).only(
                'client_id', 'date', 'desired_date', 'status__code',
                'children__surname', 'children__firstname',
                'children__patronymic', 'children__snils',
                'children__date_of_birth', 'children__reg_address_full',
                'children__address_full', 'children__gender')

    def _get_declarations(self, queue):
        """Возвращает итератор по заявлениям из инстанса очереди.

        :param queue: инстанс очереди
        :return: итератор по заявлениям
        """

        return chain(*(
            self._prepare_query(query)
            for query, _ in queue._get_queries()))

    def process(self):
        """
        1. Если AllApplications == false, значит это первый запрос и мы должны
        отдать информацию по текущей организации, и вернуть им признак
        разрешено у нас отдавать очередь или нет в тэге SupportAllApplications
        2. Если передано AllApplications == true, но у нас в настроках
        SupportAllApplications = false,
         то отрабатываем как при AllApplications == false
        3. Если передано AllApplications == true и у нас в настроках
        SupportAllApplications = true То отдаем всю очередь перед заявкой
        4. Если передан id организации, то фильтруем желаемые организации
         по нему

        """

        result = []
        declaration_id = self.declaration.id
        all_applications = self.request.AllApplications

        include_all = (
            settings.GET_APPQ_FULL and (
                all_applications or all_applications is None))

        if self.declaration.status.code not in DSS.status_queue():
            return GetApplicationQueueResponse(
                Queue=result, SupportAllApplications=settings.GET_APPQ_FULL)

        declaration_units = (
            self.declaration.declarationunit_set.select_related(
                'unit').only('unit', 'ord').order_by('ord'))

        if self.request.EduOrganizationCode:
            declaration_units = declaration_units.filter(
                unit_id=self.request.EduOrganizationCode)

        # Отбираем только организации с "Не показывать на портале" = False
        showed_declaration_units = declaration_units.filter(
            unit__is_not_show_on_poral=False)
        # Если у всех организаций "Не показывать на портале" = True, то ошибка
        if declaration_units.exists() and not showed_declaration_units.exists():
            raise StatusSpyneException(
                message='Выбранная в заявлении дошкольная образовательная '
                        'организация отсутствует на ЕПГУ',
                status='NOTIFY',
            )
        else:
            declaration_units = showed_declaration_units

        if settings.QUEUE_DOO_LIMIT_COUNT:
            declaration_units = (
                declaration_units[:settings.QUEUE_DOO_LIMIT_COUNT]
            )

        for d_unit in declaration_units:
            unit = d_unit.unit

            queue = get_queue_by_context_service(
                QueueContext.make_base_context(
                    self.declaration.children.date_of_birth, unit))

            app = []
            i = 0

            # Формирует очередь до заявления
            # или отбирает только заявление в зависимости
            # от настройки include_all
            # (Настройка в приложении + данные из тэга запроса).
            # Подсчитывает позицию заявления в очереди.
            for i, decl in enumerate(self._get_declarations(queue), 1):
                if not include_all and declaration_id != decl.id:
                    continue

                app.append(self._create_application(decl, i))

                if declaration_id == decl.id:
                    break

            result.append(self._create_queue(unit, i, app))

        return GetApplicationQueueResponse(
            Queue=result, SupportAllApplications=settings.GET_APPQ_FULL)


class GetApplicationStateProxy:
    """
    Прокси объект для метода GetApplicationQueue
    Запрос текущего статуса заявления

    """

    def __init__(self, declaration):
        assert declaration
        assert isinstance(declaration, Declaration)
        self.declaration = declaration

    def process(self):
        status_code = DeclarationStatusCodeRule.get_concetr(
            self.declaration.status.code)
        return GetApplicationStateResponse(**{
            'Code': str(status_code) if status_code else None,
            'Name': DeclarationStatusNameRule.get_concetr(
                self.declaration.status.code),
            'Details': self.declaration.status.description
        })


class FindApplicationsProxy:

    BY_DELEGATE = 1
    BY_CHILD = 2

    DOC_TYPE_RULE = {
        BY_DELEGATE: DelegateDocTypeRule,
        BY_CHILD: ChildrenDocTypeRule
    }

    def __init__(self, person_info, mode=BY_DELEGATE):

        self._person = person_info
        self._search_dict = {}
        self._mode = mode

        delegate_doc_type_rule = plugins.ExtensionManager().execute(
            'kinder.plugins.hmao_services.extensions.'
            'get_delegate_doc_type_rule')

        if delegate_doc_type_rule:
            self.DOC_TYPE_RULE[self.BY_DELEGATE] = delegate_doc_type_rule

        children_doc_type_rule = plugins.ExtensionManager().execute(
            'kinder.plugins.hmao_services.extensions.'
            'get_children_doc_type_rule')

        if children_doc_type_rule:
            self.DOC_TYPE_RULE[self.BY_CHILD] = children_doc_type_rule

    def _fill_attribute(
            self, spyne_attribute, django_field):

        value = getattr(self._person, spyne_attribute, None)
        if value:
            self._search_dict[django_field] = value

    def _convert_doc_type(self):

        value = getattr(self._person, 'DocType', None)
        if value:
            self._person.DocType = self.DOC_TYPE_RULE[
                self._mode].get_system(
                    self._person.DocType)

    def _convert_data(self):

        self._convert_doc_type()

    def _find_declarations(self, prefix):

        self._convert_data()

        self._fill_attribute('FirstName', '%s__firstname' % prefix)
        self._fill_attribute('LastName', '%s__surname' % prefix)
        self._fill_attribute('MiddleName', '%s__patronymic' % prefix)
        self._fill_attribute('Snils', '%s__snils' % prefix)
        self._fill_attribute('DateOfBirth', '%s__date_of_birth' % prefix)
        self._fill_attribute('DocType', '%s__dul_type' % prefix)
        self._fill_attribute('DocNumber', '%s__dul_number' % prefix)
        self._fill_attribute('DocIssueDate', '%s__dul_date' % prefix)

        declarations = Declaration.objects.filter(
            **self._search_dict).distinct('id')
        return declarations

    def process(self):
        if self._mode == self.BY_CHILD:
            type_response = FindApplicationsByDeclaredPersonResponse
            declarations = self._find_declarations('children')
        else:
            type_response = FindApplicationsByApplicantResponse
            declarations = self._find_declarations(
                'children__childrendelegate__delegate')

        applicants = []
        for declaration in declarations:

            applicants.append(
                ApplicationSearchResultProxy.create_application(
                    declaration))

        return type_response(Application=applicants)


class GetApplicationProxy:
    """
    Прокси объект для метода GetApplication
    Получение данных Заявления для изменения

    """

    def __init__(self, declaration, decl_proxy, app_proxy, dou_proxy):
        assert declaration
        assert isinstance(declaration, Declaration)
        self.declaration = declaration
        self.decl_proxy = decl_proxy
        self.app_proxy = app_proxy
        self.dou_proxy = dou_proxy
        self.schedule_proxy = ScheduleDataProxy(declaration)

    def process(self):

        conf = {
            'SubmitDate': self.declaration.date,
            'EntryDate': get_desire_date(self.declaration),
            'EducationProgramType': '',
            'AdaptationProgramType': get_health_need(self.declaration),
            'Applicant': self.app_proxy.create_spyne_obj(),
            'DeclaredPerson': self.decl_proxy.create_spyne_obj(),
            'Schedule': self.schedule_proxy.create_spyne_obj(),
            'EduOrganizationsData': self.dou_proxy.create_spyne_obj(),
            'ApplicationRules': ApplicationRulesDataProxy.create_rules_data(
                self.declaration),
            'DocumentReferences': DocumentReferencesDataProxy.get_data(
                self.declaration)
        }

        if self.declaration.children.health_need_confirmation:
            conf['AdaptationProgramDocInfo'] = (
                self.declaration.children.health_need_confirmation.name)

        return GetApplicationResponse(**conf)


class UpdateProxy(NewApplicationProxy, metaclass=Injectable):
    """
    Прокси объект отвечает за сохранение запроса
    об изменении заявки UpdateApplication

    """

    def __init__(
            self, request, declaration, binary_data, request_code, **kwargs):
        super(UpdateProxy, self).__init__(request, binary_data, request_code)
        if hasattr(request, "EduOrganizationsData"):
            self._edu_organizations = request.EduOrganizationsData
        self.declaration = declaration
        self.result = []
        # Переменная для передачи пар ключ/значение в
        # concentrator_changedeclaration_data минуя этапы сборки и валидации
        self.path_to_change_data = {}

    def chek_model(self, name_model, conc_data, have_data, **kwargs):
        """собирает в список все ссылки на наследников класса
        :param name_model: str имя модели из MAP_CHANGES
        :param conc_data: spyne object инстанс модеи воссозданный
         из данных на изменение
        :param have_data: django model инстанс моделииз хранилища

        """

        class_model = get_model(name_model)
        class_helper = self.storage.get_change_helper(name_model)
        ch_help = class_helper(class_model, name_model)
        ch_help.check_diff(conc_data, have_data, **kwargs)
        self.result.append(ch_help)

    def _get_declaration_units_list(self):
        """Возвращает список (unit_id, ord) по данным из запроса,
        прошедших всю валидацию

        """

        decl_units = get_declaration_units_from_request(
            self._edu_organizations, self.declaration)
        return [(x.unit_id, x.ord) for x in decl_units]

    def _create_benefits(self):
        result = super(UpdateProxy, self)._create_benefits()
        return [x.id for x in result]

    def _check_benefits(self):
        conc_benefits = self._create_benefits()
        benefits = DeclarationPrivilege.objects.filter(
            declaration=self.declaration
        ).values_list('privilege_id', flat=True)
        self.chek_model('DeclarationPrivilege', conc_benefits, benefits)
        if conc_benefits and self._benefits.BenefitsDocInfo:
            self.path_to_change_data.update(
                {
                    'ConcentratorPrivilegeComment':
                        self._benefits.BenefitsDocInfo
                }
            )

    def _check_docs(self):
        """
        - сохраняем бинарники к нам в базу с признаком не принято
        - помещаем данные о новых файлах в параметр класса
        DeclarationDocsChangeHelper
        :return:

        """

        if self._document_references:
            helper = DeclarationDocsChangeHelper(DocExtraInfo)
            helper.check_diff(
                self._document_references,
                self.declaration,
                self._binary_data,
                self._request_code)
            self.result.append(helper)

    def process(self):
        check_organization_priorities(self._edu_organizations)

        msg = u'OK'
        # проверем поля заявки
        self.chek_model('Declaration', self._build_declaration(),
                        self.declaration)
        # проверяем поля ребенка
        self.chek_model('Children', self._build_child(),
                        self.declaration.children)
        # проверяем поля представителя
        conc_delegate, _ = self._build_delegate()
        # тут также надеемся что родитль один и его же мы и редактируем!
        delegate = get_delegate(self.declaration)
        self.chek_model('Delegate', conc_delegate, delegate)

        # проверяем поля ЖУ и текущее МО заявления
        conc_decl_units = self._get_declaration_units_list()
        sys_decl_units = get_declaration_units(self.declaration)
        declaration_mo = self.declaration.mo
        requested_mo = None
        if self._edu_organizations.EduOrganization:
            requested_mo = get_mo_from_request(self._edu_organizations,
                                               self.declaration)
        self.chek_model('DeclarationUnit', conc_decl_units, sys_decl_units,
                        declaration_mo=declaration_mo,
                        requested_mo=requested_mo)

        self._check_benefits()
        self._check_docs()

        result = self.storage.create_change(
            # Какая-то магия творится с yadicoм
            self.declaration, self.result, raw_data=self.path_to_change_data,
            source=self.storage.source)
        if not result:
            msg = 'Изменений не найдено'

        return UpdateApplicationResponse(**{
            'Status': msg
        })


class ResetDeclarationProxy(metaclass=Injectable):

    STATUS_TRANSFER_COMMENT = u"""
        Авто-смена статуса в связи с поступившей заявкой
        на отказ от участия в очереди поступила с ЕПГУ.
        Необходимо уточнить актуальность запроса у законных
        представителей.
        """

    def __init__(self, request, declaration, **kwargs):
        self._request = request
        self.declaration = declaration
        self.result = defaultdict(list)
        self.case_number = kwargs.get("case_number", None)

    def process(self):
        ch_help = DeclarationChangeHelper(Declaration, 'Declaration')
        self.result['Declaration'].extend(
            ch_help.get_status_change(self.declaration))

        ChangeDeclaration(
            declaration=self.declaration,
            data=json.dumps(
                self.result, cls=AdditionalEncoder),
            source=ChangeSource.UPDATE_APPLICATION,
            case_number=self.case_number).save()

        return UpdateApplicationResponse(**{
            'Status': u'Успех'
        })


class IUpdateApplicationProxy(metaclass=Injectable):

    depends_on = ('behavior', 'storage', )

    def process(
            self, request, declaration, binary_data,
            request_code, case_number=None):
        behavior = self.behavior(
            request, declaration,
            binary_data=binary_data, request_code=request_code,
            case_number=case_number)

        behavior.storage = self.storage

        return behavior.process()


def new_application_with_duplicate_check(
        ctx, request, binary_data, request_code
):
    """Проверяет наличие дубликатов заявки в системе.
    При их отсутствии запускает процесс создания заявки

    :param ctx: Spyne контекст запроса
    :param request: Данные в запросе
    :param binary_data: Бинарники
    :param request_code: код запроса
    :return: Результат работы

    """

    # Формирует фильтр:
    # Точное совпадение Фамилии ребенка (не чуствительный к регистру);
    # И Точное совпадение Имени ребенка (не чувствительный к регистру);
    # И Равенство Даты рождения ребенка
    # И Исключаются заявления с неактивными статусами
    # (Зачислен, Архивная, Отказано в услуге, Не явился)
    # И (Равенство СНИЛС ИЛИ Равество ДУЛ (Серия И Номер и Дата))
    base_filter = (
        Q(children__surname__iexact=prepare_name(
            request.DeclaredPerson.LastName))
        & Q(children__firstname__iexact=prepare_name(
            request.DeclaredPerson.FirstName))
        & Q(children__date_of_birth=request.DeclaredPerson.DateOfBirth)
        & ~Q(status__code__in=DSS.no_active_statuses())
        & (Q(children__snils=request.DeclaredPerson.Snils)
           | Q(children__dul_series=request.DeclaredPerson.BirthDocSeria,
               children__dul_number=request.DeclaredPerson.BirthDocNumber,
               children__dul_date=request.DeclaredPerson.BirthDocIssueDate)))

    if Declaration.objects.filter(base_filter).exists():
        # Формирует ответ с сообщением о существовании дубля в системе
        reject_request(ctx, 'Заявление по заданным параметрам уже существует')

    else:
        # Если записи не найдены, то создает заявку
        result = NewApplicationProxy(
            request, binary_data, request_code).process()

    return result
