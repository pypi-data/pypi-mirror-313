import datetime

from yadic.container import Injectable

from kinder.core.audit_log_kndg.helpers import get_model
from kinder.core.children.models import ChildrenDelegate
from kinder.core.children.models import Delegate
from kinder.core.declaration.models import Declaration
from kinder.core.declaration.models import DeclarationPrivilege
from kinder.core.declaration.proxy import get_initial_status
from kinder.plugins.privilege_attributes.models import PrivilegeOwnerEnum
from kinder.plugins.privilege_attributes.models import (
    PrivilegeConfirmationAttributes)
from kinder.provider import features
from kinder.webservice.spyne_ws.exceptions import SpyneException

from concentrator.change import StorageHelper
from concentrator.models import ChangeSource
from concentrator.webservice.helpers import check_organization_priorities
from lipetsk_specifics.models import Changes
from lipetsk_specifics.rules import WorkTypeRules

from .django_objects_proxy import DelegatePrivilegeProxy
from .django_objects_proxy import DocExtraInfoProxy
from .django_objects_proxy import LipetskChildrenProxy
from .django_objects_proxy import LipetskDelegateProxy
from .django_objects_proxy import PrivConfirmAttrsProxy
from .django_objects_proxy import PrivilegeProxy
from .entities import GetApplicationResponse
from .entities import UpdateApplicationResponse
from .helpers import DocumentWorker
from .helpers import _get_document_reference_from_ctx
from .helpers import get_decl_priv
from .helpers import get_declaration_units
from .helpers import get_declaration_units_from_request
from .helpers import get_delegate
from .helpers import get_desire_date
from .helpers import get_health_need
from .helpers import get_mo_from_request
from .helpers import get_priv_data
from .spyne_objects_proxy import ApplicationRulesDataProxy
from .spyne_objects_proxy import DocumentReferencesDataProxy


class LipetskNewApplicationProxy:
    u"""Прокси объект для метода NewApplication"""

    def __init__(self, request, binary_data, request_code, **kwargs):
        self._external_id = request.ExternalId
        self._submit_date = request.SubmitDate
        self._entry_date = request.EntryDate
        self._adaptation_program_type = request.AdaptationProgramType
        self._delegate_data = request.Applicant
        self._child_data = request.DeclaredPerson
        self._edu_organizations = getattr(request, 'EduOrganizations', None)
        self._binary_data = binary_data
        self._request_code = request_code
        self._message_id = kwargs.get("message_id", None)
        self._document_references = _get_document_reference_from_ctx(
            request)

    def _create_delegate_for_priv(self, whb, declaration, delegate):
        u"""Возвращаем найденного по <ФИО или данным ДУЛ> родителя
        или нового представителя.

        :param delegate: инстанс "родителя" Application подаваемой заявке.
        :param declaration: инстанс уже созданной заявки
        :param whb: инстанс spyne-модели WhoHaveBenefit,
            описывающий владельца льготы

        """

        if whb.Type == PrivilegeOwnerEnum.DELEGATE:
            owner_delegate = DelegatePrivilegeProxy.get_founded_or_new(
                declaration, DelegatePrivilegeProxy(whb).get())

            # не валидный случай
            if owner_delegate == delegate:
                raise SpyneException(
                    u"В данных об обладателе льгот указаны данные родителя, "
                    u"а не другого законного представителя")
        else:
            # ожидаем родителя и возвращаем его
            owner_delegate = delegate

        return owner_delegate

    def _save_privileges(self, privileges, declaration, doc_number, delegate):
        u"""Согласовано с аналитикаами, что с портала приходит более 1 льготы.
        В методе сохраняются модели Привязки льготы, Атрибуты подтв. льготы,
        [Зак.представителя, Привязка его с ребенком].

        :param privileges: список заявлени. может быть пустым
        :param delegate: инстанс уже созданного представителя

        """

        if len(privileges) > 1:
            raise SpyneException(
                u"Не должно быть более 1 льготы с портала!!!")
        if privileges:
            # если есть льгота, то по условию выше только одна.
            privilege = privileges[0]
            owner_type = self._child_data.Benefits.WhoHaveBenefit.Type

            decl_pr = DeclarationPrivilege.objects.create(
                declaration=declaration,
                datetime=datetime.datetime.now(),
                privilege=privilege,
                doc_number=doc_number)
            data = dict(
                privilege_owner=owner_type,
                declaration_privilege=decl_pr,
                portal=True,
            )

            # если не ребенок, то опредеряем инстанс заявителя:
            # - единственного родителя которого указывали в Applicant,
            # - или нового зак.представителя из WhoHaveBenefit
            if owner_type != PrivilegeOwnerEnum.CHILDREN:
                data['delegate'] = self._create_delegate_for_priv(
                    self._child_data.Benefits.WhoHaveBenefit,
                    declaration, delegate)
            PrivilegeConfirmationAttributes.objects.create(**data)

    def _create_delegate(self):
        return LipetskDelegateProxy(self._delegate_data).get()

    def _create_children(self):
        return LipetskChildrenProxy(
            self._child_data, self._delegate_data,
            self._adaptation_program_type).get()

    def _create_benefits(self):
        result = []
        doc_number = (self._child_data.Benefits.BenefitsDocInfo
                      if self._child_data.Benefits else None)
        if self._child_data.Benefits and self._child_data.Benefits.Benefit:
            result = PrivilegeProxy([
                (benefit.name,
                 benefit.Type)
                for benefit in self._child_data.Benefits.Benefit]).get()
        return result, doc_number

    def _get_work_type(self):
        return WorkTypeRules.get_system(self._child_data.ArrivalTimeType)

    def _create_declaration(self):
        return Declaration(
            date=self._submit_date,
            desired_date=self._entry_date,
            offer_other=self._edu_organizations.AllowOfferOther,
            client_id=self._external_id,
            comment=self._child_data.IssuerState,
            portal=1,
            portal_decl_id=self._message_id,
            work_type_id=self._get_work_type(),
            source=features.get_feature(
                'lipetsk_specifics.webservice.service.'
                'NewApplicationRequest.get_source')())

    def _attache_documents(self, declaration):
        DocumentWorker(
            declaration, self._binary_data, self._request_code).attach()

    def _save_doc_extra_info(self, declaration):
        DocExtraInfoProxy(declaration, self._document_references).save()

    def process(self):
        check_organization_priorities(self._edu_organizations)

        if Declaration.objects.filter(client_id=self._external_id).exists():
            raise SpyneException(
                u'Заявление с ExternalId = %s уже существует' %
                self._external_id)
        declaration = self._create_declaration()
        delegate = self._create_delegate()
        children = self._create_children()
        privileges, doc_number = self._create_benefits()
        mo = get_mo_from_request(self._edu_organizations, declaration)

        delegate.save()
        children.save()
        ChildrenDelegate.objects.create(
            children=children, delegate=delegate)

        declaration.children = children
        declaration.mo = mo
        declaration.status = get_initial_status(children)
        declaration.save()

        declaration_units = get_declaration_units_from_request(
            self._edu_organizations, declaration)

        for declaration_unit in declaration_units:
            # bulk create не использую т.к. он не вызывает save
            # метода и не срабатывают сигналы post_save и pre_save
            declaration_unit.declaration = declaration
            declaration_unit.save()

        self._save_privileges(privileges, declaration, doc_number, delegate)
        self._save_doc_extra_info(declaration)
        self._attache_documents(declaration)

        return declaration.id


class GetApplicationProxy:
    """
    Прокси объект для метода GetApplication
    Получение данных Заявления для изменения.

    """

    def __init__(self, declaration, decl_proxy, app_proxy, dou_proxy):
        assert declaration
        assert isinstance(declaration, Declaration)
        self.declaration = declaration
        self.decl_proxy = decl_proxy
        self.app_proxy = app_proxy
        self.dou_proxy = dou_proxy

    def process(self):
        conf = {
            'SubmitDate': self.declaration.date,
            'EntryDate': get_desire_date(self.declaration),
            'EducationProgramType': '',
            'AdaptationProgramType': get_health_need(self.declaration),
            'Applicant': self.app_proxy.create_spyne_obj(),
            'DeclaredPerson': self.decl_proxy.create_spyne_obj(),
            'EduOrganizationsData': self.dou_proxy.create_spyne_obj(),
            'ApplicationRules': ApplicationRulesDataProxy.create_rules_data(
                self.declaration),
            'DocumentReferences': DocumentReferencesDataProxy.get_data(
                self.declaration)
        }

        return GetApplicationResponse(**conf)


class LipetskUpdateProxy(LipetskNewApplicationProxy, metaclass=Injectable):
    u"""Сравниваем только с льготами с портала"""

    def __init__(self, request, declaration,
                 binary_data, request_code, **kwargs):
        super(
            LipetskUpdateProxy, self
        ).__init__(request, binary_data, request_code)

        self._edu_organizations = request.EduOrganizationsData
        self.declaration = declaration
        self.result = []
        self.case_number = kwargs.get("case_number", None)
        # Переменная для передачи пар ключ/значение в
        # concentrator_changedeclaration_data минуя этапы сборки и валидации
        self.path_to_change_data = {}

    def chek_model(self, name_model, conc_data, have_data, **kwargs):
        """
        :param name_model: str имя модели из MAP_CHANGES
        :param conc_data: spyne object инстанс модеи воссозданный
         из данных на изменение
        :param have_data: django model инстанс моделииз хранилища

        """

        class_model = get_model(name_model)
        class_helper = StorageHelper.get_change_helper(name_model)
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

    def _save_documents(self):
        u"""Сохранение документов"""
        DocumentWorker(
            self.declaration, self._binary_data, self._request_code).attach()
        DocExtraInfoProxy(self.declaration, self._document_references).save()

    def _create_delegate(self):
        return LipetskDelegateProxy(self._delegate_data).get()

    def _create_children(self):
        return LipetskChildrenProxy(
            self._child_data, self._delegate_data,
            self._adaptation_program_type).get()

    def _create_benefits(self):
        result, doc_number = super(LipetskUpdateProxy, self)._create_benefits()
        return [x.id for x in result]

    def _create_privilegeconfattributes(self):
        u"""Получение прокси класса по доп.аттрибутам льгот."""
        # В липецке на портале нельзя указать больше 1 льготы
        declaration_privilege_set = get_decl_priv(self.declaration)
        if self._child_data.Benefits.Benefit:
            # льгота указана в запросе,
            # проверяем есть ли привязка ко льготе в БД...
            if declaration_privilege_set:
                priv_conf_attr = PrivConfirmAttrsProxy(
                    self._child_data,
                    self.declaration,
                    declaration_privilege_set[0]
                ).get()
            else:
                # создается новая льгота и к ней подтверждение
                privilege_id = self._child_data.Benefits.Benefit[0].name
                priv_conf_attr = PrivConfirmAttrsProxy(
                    self._child_data,
                    self.declaration,
                    DeclarationPrivilege(
                        declaration=self.declaration,
                        privilege_id=privilege_id)
                ).get()
        else:
            # нет тега Benefit, значит привязка ко льготе
            # и ее подтверждение будут удалены.
            priv_conf_attr = PrivilegeConfirmationAttributes()

        return priv_conf_attr

    def _check_privilegeconfattributes(self):
        """Применения изменений по подтверждению льготы.
        В общей сложности 16 кейсов смены обладателя льгот!
        Т.к. 4 варианта: Нет льготы, Родитель, Ребенок, Представитель.

        """

        new_priv_conf_attrs = self._create_privilegeconfattributes()
        priv_conf_attrs = get_priv_data(self.declaration)

        if new_priv_conf_attrs:
            # киллерфича. Если просходит смена с/на Ребенка,
            # то подменяем инстанс delegate на фейковый с данными ребенка
            new_owner = getattr(new_priv_conf_attrs, 'privilege_owner', None)
            old_owner = getattr(priv_conf_attrs, 'privilege_owner', None)

            # была ли смена обладателя
            if old_owner != new_owner:
                fake_delegate = DelegatePrivilegeProxy.get_fake_delegate(
                    self.declaration.children)

                if old_owner == PrivilegeOwnerEnum.CHILDREN:
                    # Ребенок -> Родитель/Заявитель
                    if new_owner != PrivilegeOwnerEnum.CHILDREN:
                        priv_conf_attrs.delegate = fake_delegate
                else:
                    if new_owner == PrivilegeOwnerEnum.CHILDREN:
                        # Родитель/Заявитель -> Ребенок
                        new_priv_conf_attrs.delegate = fake_delegate
                    elif new_owner == PrivilegeOwnerEnum.DELEGATE:
                        # Родитель -> Заявитель, приходится сравнивать с пустым
                        # инстансом, т.к. фамилии у заявителей могут совпасть и
                        # диффка по фамилии не создастся.
                        if not priv_conf_attrs:
                            # льготы и ее подтверждения нет
                            # при добавлении новой,
                            # потэтому создаем пустой инстанс для диффки
                            priv_conf_attrs = PrivilegeConfirmationAttributes()
                        priv_conf_attrs.delegate = Delegate()

            # диффку создаем только для изменения данных Представителя
            # или при смене обладателя льготы.
            if (new_owner == PrivilegeOwnerEnum.DELEGATE
                    or old_owner != new_owner):
                self.chek_model(
                    'PrivilegeConfirmationAttributes',
                    new_priv_conf_attrs, priv_conf_attrs)

    def _check_benefits(self):
        conc_benefits = self._create_benefits()
        declarationprivilege_set = get_decl_priv(self.declaration, True)
        benefits = [x.privilege.id for x in declarationprivilege_set]

        # 1. Основная модель привелегий
        self.chek_model('DeclarationPrivilege', conc_benefits, benefits)

        # 2. Модель доп.аттрибут о льготах (липецкая, внутри плагина)
        if self._child_data.Benefits:
            self._check_privilegeconfattributes()

        if conc_benefits and self._child_data.Benefits.BenefitsDocInfo:
            self.path_to_change_data.update(
                {
                    'ConcentratorPrivilegeComment':
                        self._child_data.Benefits.BenefitsDocInfo
                }
            )

    def process(self):
        check_organization_priorities(self._edu_organizations)

        msg = u'OK'
        # проверем поля заявки
        self.chek_model('Declaration', self._create_declaration(),
                        self.declaration)
        # проверяем поля ребенка
        self.chek_model('Children', self._create_children(),
                        self.declaration.children)
        # проверяем поля представителя
        conc_delegate = self._create_delegate()
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

        result = StorageHelper.create_change(
            self.declaration, self.result, raw_data=self.path_to_change_data,
            source=ChangeSource.UPDATE_APPLICATION,
            case_number=self.case_number)
        if result is None:
            msg = 'Изменений не найдено'
        else:
            lipetsk_change = Changes(change_declaration=result)
            lipetsk_change.save()

        # Сохранение документов без подтверждения
        self._save_documents()

        return UpdateApplicationResponse(**{'Status': msg})
