from abc import ABC
from abc import abstractmethod

from kinder.core.declaration.models import DeclarationPrivilege

from concentrator.change import map_changes
from concentrator.models import DocExtraInfo
from concentrator.models import PrivilegeComment
from concentrator.rules import *
from concentrator.webservice.entities import *
from concentrator.webservice.helpers import *


class ProxyData:
    """
    Прокси для расширения извне
    """
    DEFAULT_CLASS = None

    def __init__(self, decl, out_class=None):
        assert self.DEFAULT_CLASS
        self.declaration = decl
        self.out_class = out_class or self.DEFAULT_CLASS

    def get_extra_data(self):
        """
        Метод для возможости расширения данных
        :return:

        """

        return {}

    def create_data(self):
        """
        Метод нужно перекрыть
        :return:

        """

        pass

    def create_spyne_obj(self):
        data = self.create_data()
        data.update(self.get_extra_data())
        return self.DEFAULT_CLASS(**data)


class BaseApplicantSearchResultProxy(ABC):
    """Формирует ответ с данными представителя."""

    @staticmethod
    @abstractmethod
    def create_applicant(declaration):
        pass


class GetApplicationQueueApplicantSearchResultProxy(
        BaseApplicantSearchResultProxy
):
    """Формирует ответ с данными представителя для сервиса GetApplicationQueue.
    """

    @staticmethod
    def create_applicant(declaration):
        first_childrendelegate = declaration.children.first_childrendelegate
        childrendelegate = (first_childrendelegate[0]
                            if first_childrendelegate else None)

        if childrendelegate:
            delegate_type = None

            if childrendelegate.delegate.type:
                delegate_type = str(
                    DelegateTypeRule.get_concetr(
                        childrendelegate.delegate.type))

            return ApplicantSearchResult(
                FIO=get_fio(childrendelegate.delegate),
                ApplicantType=delegate_type,
                DocNumber=get_doc_number(childrendelegate.delegate))

        return ApplicantSearchResult()


class ApplicantSearchResultProxy(BaseApplicantSearchResultProxy):
    """Формирует ответ с данными представителя."""

    @staticmethod
    def create_applicant(declaration):
        delegate = get_delegate(declaration)
        if delegate:
            delegate_type = None
            if delegate.type:
                delegate_type = str(
                    DelegateTypeRule.get_concetr(delegate.type))
            return ApplicantSearchResult(**{
                'FIO': get_fio(delegate),
                'ApplicantType': delegate_type,
                'DocNumber': get_doc_number(delegate)})
        else:
            return ApplicantSearchResult()


class BaseDeclaredProxy(ABC):
    """Формирует ответ с данными ребенка."""

    @staticmethod
    @abstractmethod
    def create_declared_person(declaration):
        pass


class GetApplicationQueueDeclaredProxy(BaseDeclaredProxy):
    """Формирует ответ с данными ребенка используется
    в сервисе GetApplicationQueue.
    """

    @staticmethod
    def create_declared_person(declaration):
        children = declaration.children
        reg_address, fact_address = get_child_address(children)

        return DeclaredPersonSearchResult(**{
            'FIO': get_fio(children),
            'DocNumber': get_snils_number(children),
            'DateOfBirth': children.date_of_birth,
            'Sex': get_sex(children),
            'AddressRegistration': reg_address,
            'AddressResidence': fact_address,
            'Benefits':
                GetApplicationQueueBenefitsProxy.create_benefits(declaration),
            'AgeGroupType': get_age_group_type(children.date_of_birth),
        })


class DeclaredProxy(BaseDeclaredProxy):
    """Формирует ответ с данными ребенка."""

    @staticmethod
    def create_declared_person(declaration):

        children = declaration.children
        reg_address, fact_address = get_child_address(children)
        return DeclaredPersonSearchResult(**{
            'FIO': get_fio(children),
            'DocNumber': get_snils_number(children),
            'DateOfBirth': children.date_of_birth,
            'Sex': get_sex(children),
            'AddressRegistration': reg_address,
            'AddressResidence': fact_address,
            'Benefits': BenefitsProxy.create_benefits(declaration),
            'AgeGroupType': get_age_group_type(children.date_of_birth),
        })


class AppProxy:
    """
    Общие поля для всех типов заявления
    """
    @staticmethod
    def create_app(declaration):
        conf = {
            'ExternalId': declaration.client_id,
            'RegionalId': str(declaration.id),
            'EducationProgramType': '',
            'AdaptationProgramType': get_health_need(declaration),
            'SubmitDate': get_submit_date(declaration),
            'EntryDate': get_desire_date(declaration),
            'State': str(DeclarationStatusCodeRule.get_concetr(
                declaration.status.code)),
            'StateDetails': get_state_details(declaration),
            'Applicant': ApplicantSearchResultProxy.create_applicant(
                declaration),
            'DeclaredPerson': DeclaredProxy.create_declared_person(
                declaration)
        }
        return conf


class ApplicationProxy:
    """
    Используется в сервисе GetApplicationQueue
    """

    @staticmethod
    def create_application(declaration, order=None):
        conf = {
            'ExternalId': declaration.client_id,
            'RegionalId': str(declaration.id),
            'EducationProgramType': '',
            'AdaptationProgramType': str(declaration.health_need_id),
            'SubmitDate': get_submit_date(declaration),
            'EntryDate': get_desire_date(declaration),
            'State':
                str(DeclarationStatusCodeRule.get_concetr(
                    declaration.status.code)),
            'StateDetails': declaration.status_last_comment or '',
            'Applicant':
                GetApplicationQueueApplicantSearchResultProxy.create_applicant(
                    declaration),
            'DeclaredPerson':
                GetApplicationQueueDeclaredProxy.create_declared_person(
                    declaration),
            'Order': order
        }

        return Application(**conf)


class ApplicationSearchResultProxy(object):
    """
    изпользуется в 2-ух сервисах FindApplications
    """
    @staticmethod
    def create_application(declaration):
        conf = AppProxy.create_app(declaration)
        return ApplicationSearchResult(**conf)


class ScheduleDataProxy(ProxyData):
    """ Используется в методе GetApplicationResponse """
    DEFAULT_CLASS = ScheduleData

    def create_data(self, ):
        conf = {
            'ScheduleType': [WorkTypeRule.get_concetr(
                self.declaration.work_type_id)]
        }
        return conf


class EduOrganizationsDataProxy(ProxyData):
    """
    В концентраторе есть только приоритет 1 и 2
    """
    DEFAULT_CLASS = EduOrganizationsData

    def _create_edu_organizations(self):
        result = []
        for du in self.declaration.declarationunit_set.all():
            result.append(EduOrganization(**{
                'Code': str(du.unit.id),
                'Priority': du.ord if du.ord in [1, 2] else 2,
            }))
        return result

    def create_data(self):
        conf = {
            'AllowOfferOther': self.declaration.offer_other,
            'EduOrganization': self._create_edu_organizations()
        }
        return conf


class BaseBenefitsProxy(ABC):
    """Формирует ответ с данными привилегий."""

    @staticmethod
    @abstractmethod
    def create_benefits(declaration):
        pass


class GetApplicationQueueBenefitsProxy(BaseBenefitsProxy):
    """Формирует ответ с данными привилегий для сервиса GetApplicationQueue."""

    @staticmethod
    def create_benefits(declaration):
        return Benefits(
            Benefit=(BenefitItem(
                name=str(d_privilege.privilege_id),
                Type=str(
                    PrivilegeTypeRule.get_concetr(
                        d_privilege.privilege.type_id)))
                    for d_privilege in declaration.all_privileges or ()),
            BenefitsDocInfo=(declaration.privilege_last_comment or ''))


class BenefitsProxy(BaseBenefitsProxy):
    """Формирует ответ с данными привилегий."""

    @staticmethod
    def _get_privileges(declaration):

        return DeclarationPrivilege.objects.filter(
            declaration=declaration).values_list(
                'privilege__id', 'privilege__type',
                'doc_series', 'doc_number')

    @staticmethod
    def create_benefits(declaration):
        privileges = BenefitsProxy._get_privileges(declaration)
        benefits = []
        for code, privilege_type, doc_series, doc_number in privileges:
            benefits.append(
                BenefitItem(
                    name=str(code),
                    Type=str(
                        PrivilegeTypeRule.get_concetr(privilege_type)))
            )

        privilege_comment = PrivilegeComment.objects.filter(
                declaration_privilege__declaration=declaration).order_by(
                                'declaration_privilege__datetime').last()
        privilege_comment = (privilege_comment.concentrator_comment
                              if privilege_comment else "")

        return Benefits(Benefit=benefits,
                        BenefitsDocInfo=privilege_comment)


class ApplicantDataProxy(ProxyData):
    DEFAULT_CLASS = ApplicantData

    def create_data(self):
        conf = {}
        delegate = get_delegate(self.declaration)
        if delegate:
            delegate_type = None
            if delegate.type:
                delegate_type = str(
                    DelegateTypeRule.get_concetr(delegate.type))
            conf = {
                "FirstName": delegate.firstname,
                "LastName": delegate.surname,
                "MiddleName": delegate.patronymic,
                "DocType": str(get_doc_type_delegate(delegate)),
                "DocSeria": delegate.dul_series,
                "DocNumber": delegate.dul_number,
                "DocIssueDate": get_dul_date(delegate.dul_date),
                "DocIssuerName": delegate.dul_issued_by,
                "DocIssuerDepartmentCode": delegate.dul_place,
                "Snils": delegate.snils,
                "ApplicantType": delegate_type,
                "ApplicantTypeOtherName": "",
                "ApplicantTypeOtherDocNumber": "",
                "Email": delegate.email,
                "PhoneNumber": delegate.phones,
            }
        return conf


class DeclaredPersonDataProxy(ProxyData):
    DEFAULT_CLASS = DeclaredPersonData

    def create_data(self):
        child = self.declaration.children
        reg_address, fact_address = get_child_address(child)
        conf = {
            "FirstName": child.firstname,
            "LastName": child.surname,
            "MiddleName": child.patronymic,
            "Snils": child.snils,
            "BirthPlace": child.birthplace,
            "AgeGroupType": get_age_group_type(child.date_of_birth),
            "DateOfBirth": child.date_of_birth,
            "Sex": get_sex(child),
            "AddressRegistration": reg_address,
            "AddressResidence": fact_address,
        }
        conf.update(self._get_benefits())
        conf.update(self._get_dul_data())
        return conf

    def _get_dul_data(self):
        """Возвращаем данные по ДУЛ, которые зависят от Типа документа.
        Примерно такая же логика на портале, которую уже нельзя поменять.
        """
        child = self.declaration.children

        if child.dul_type == DULTypeEnumerate.SVID:
            data = {
                "BirthDocSeria": child.dul_series,
                "BirthDocNumber": child.dul_number,
                "BirthDocActNumber": child.zags_act_number,
                "BirthDocIssueDate": child.dul_date,
                "BirthDocIssuer": child.zags_act_place,
            }
        else:
            # в BirthDocForeign всегда отдаем текстовое значение типа OTHER
            data = {
                "BirthDocForeign": DULTypeEnumerate.values[
                    DULTypeEnumerate.OTHER],
                "BirthDocForeignNumber": child.dul_number,
            }
        return data

    def _get_benefits(self):
        """Возвращает словарь данных по льготам"""
        return dict(Benefits=BenefitsProxy.create_benefits(self.declaration))


class ApplicationRulesDataProxy(object):

    @staticmethod
    def _get_ReadOnlyFields():
        return [map_changes.get_read_only_fields()]

    @staticmethod
    def create_rules_data(declaration):
        conf = {
            "ReadOnlyFields": ApplicationRulesDataProxy._get_ReadOnlyFields()
        }
        return ApplicationRulesData(**conf)


class DocumentReferencesDataProxy(object):

    @staticmethod
    def _document_reference_create(doc_extra_info):

        document_reference_params = {'Code': doc_extra_info.code}
        if doc_extra_info.name:
            document_reference_params.update({'Name': doc_extra_info.name})
        if doc_extra_info.description:
            document_reference_params.update(
                {'Description': doc_extra_info.description})

        return DocumentReference(**document_reference_params)

    @staticmethod
    def get_data(declaration):

        result = list(map(
            DocumentReferencesDataProxy._document_reference_create,
            DocExtraInfo.objects.filter(declaration=declaration)))

        return DocumentReferencesData(
            **{'DocumentReference': result})
