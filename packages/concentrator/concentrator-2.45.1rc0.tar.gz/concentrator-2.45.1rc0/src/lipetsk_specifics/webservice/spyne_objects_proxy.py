from concentrator.models import DocExtraInfo
from lipetsk_specifics.change import map_changes
from lipetsk_specifics.rules import DelegateTypeRule
from lipetsk_specifics.rules import PrivilegeTypeRule
from lipetsk_specifics.rules import WorkTypeRules
from lipetsk_specifics.rules import get_age_group_type

from . import helpers
from .entities import ApplicationRulesData
from .entities import BenefitItem
from .entities import DocumentReference
from .entities import DocumentReferencesData
from .entities import LipetskApplicantData
from .entities import LipetskBenefits
from .entities import LipetskDeclaredPersonData
from .entities import LipetskEduOrganization
from .entities import LipetskEduOrganizationsData
from .entities import WhoHaveBenefit


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
        @return:
        """
        return {}

    def create_data(self):
        """
        Метод нужно перекрыть
        @return:
        """
        pass

    def create_spyne_obj(self):
        data = self.create_data()
        data.update(self.get_extra_data())
        return self.DEFAULT_CLASS(**data)


class WhoHaveBenefitProxy:
    """
    Заполняем данные о владельце льготы
    """
    @staticmethod
    def create_delegate(declaration):
        conf = dict()
        priv_conf_data = helpers.get_priv_data(declaration)
        if priv_conf_data:
            conf = dict(
                Type=priv_conf_data.privilege_owner,
            )
            if priv_conf_data.delegate:
                conf.update(dict(
                    FirstName=priv_conf_data.delegate.firstname,
                    LastName=priv_conf_data.delegate.surname,
                    MiddleName=priv_conf_data.delegate.patronymic,
                    DocType=str(
                        helpers.get_doc_type_delegate(priv_conf_data.delegate)
                    ),
                    DocSeria=priv_conf_data.delegate.dul_series,
                    DocNumber=priv_conf_data.delegate.dul_number,
                    DocIssueDate=priv_conf_data.delegate.dul_date,
                    DocIssuerName=priv_conf_data.delegate.dul_issued_by,
                    Snils=priv_conf_data.delegate.snils,
                ))

        return WhoHaveBenefit(**conf)


class LipetskBenefitsProxy:
    """
    Отдаем только льготу пришедшую с портала,
    она должна быть одна!
    """

    @staticmethod
    def _get_privileges(declaration):
        return [
            (
                declaration_privilege.privilege.id,
                declaration_privilege.privilege.type_id,
                declaration_privilege.doc_series,
                declaration_privilege.doc_number
            ) for declaration_privilege in helpers.get_decl_priv(declaration)
        ]

    @staticmethod
    def create_benefits(declaration):
        result = None
        privileges = LipetskBenefitsProxy._get_privileges(declaration)
        doc_info = []
        benefits = []
        for code, privilege_type, doc_series, doc_number in privileges:
            benefits.append(
                BenefitItem(
                    name=str(code),
                    Type=str(
                        PrivilegeTypeRule.get_concetr(privilege_type)))
            )
            list(
                map(
                    lambda x: doc_info.append(x)
                    if x else None, [doc_series, doc_number]
                )
            )
        who_have_benefit = WhoHaveBenefitProxy.create_delegate(declaration)
        if benefits:
            result = LipetskBenefits(
                Benefit=benefits, BenefitsDocInfo=','.join(doc_info),
                WhoHaveBenefit=who_have_benefit)
        return result


class LipetskDeclaredPersonDataProxy(ProxyData):
    """
    Пробрасываем поле дата создания актовой записи и время пребывания в блок
    "DeclaredPerson"

    """

    DEFAULT_CLASS = LipetskDeclaredPersonData

    def create_data(self):
        child = self.declaration.children
        reg_address, fact_address = helpers.get_child_address(child)
        conf = {
            "FirstName": child.firstname,
            "LastName": child.surname,
            "MiddleName": child.patronymic,
            "Snils": child.snils,
            "BirthPlace": child.birthplace,
            "BirthDocSeria": child.dul_series,
            "BirthDocNumber": child.dul_number,
            "BirthDocActNumber": child.zags_act_number,
            "BirthDocIssueDate": child.dul_date,
            "BirthDocIssuer": child.zags_act_place,
            # TODO: нет данных в БД
            "BirthDocForeign": "",
            "BirthDocForeignNumber": "",
            "AgeGroupType": get_age_group_type(child.date_of_birth),
            "DateOfBirth": child.date_of_birth,
            "Sex": helpers.get_sex(child),
            "AddressRegistration": reg_address,
            "AddressResidence": fact_address,
        }
        conf.update(self._get_benefits())
        return conf

    def _get_benefits(self):
        """
        Возвращаем данные по льготам только в том случае,
        если они присутствуют в заявке
        """
        data = dict()
        benefits = LipetskBenefitsProxy.create_benefits(self.declaration)
        if benefits:
            data['Benefits'] = LipetskBenefitsProxy.create_benefits(
                self.declaration)
        return data

    def get_extra_data(self):
        child = self.declaration.children
        work_type = WorkTypeRules.get_concetr(self.declaration.work_type_id)
        if work_type:
            work_type = str(work_type)
        data = {
            'DateOfActNumber': child.zags_act_date,
            'ArrivalTimeType': work_type,
        }
        return data


class LipetskApplicantDataProxy(ProxyData):
    DEFAULT_CLASS = LipetskApplicantData

    def create_data(self):
        conf = {}
        delegate = helpers.get_delegate(self.declaration)
        if delegate:
            delegate_type = None
            if delegate.type:
                delegate_type = str(
                    DelegateTypeRule.get_concetr(delegate.type)
                )
            conf = {
                "FirstName": delegate.firstname,
                "LastName": delegate.surname,
                "MiddleName": delegate.patronymic,
                "DocType": str(helpers.get_doc_type_delegate(delegate)),
                "DocSeria": delegate.dul_series,
                "DocNumber": delegate.dul_number,
                "DocIssueDate": delegate.dul_date,
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

    def get_extra_data(self):
        child = self.declaration.children
        reg_address, fact_address = helpers.get_delegate_address(child)
        return {
            'AddressRegistration': reg_address,
            'AddressResidence': fact_address
        }


class LipetskEduOrganizationsDataProxy(ProxyData):
    DEFAULT_CLASS = LipetskEduOrganizationsData

    def _create_edu_organizations(self):
        result = []
        for du in self.declaration.declarationunit_set.all():
            mo = du.unit.get_mo()
            result.append(LipetskEduOrganization(**{
                'Code': str(du.unit.id),
                'Priority': du.ord if du.ord in [1, 2] else 2,
                'CodeMO': mo.id,
                'OkatoMO': mo.ocato,
            }))
        return result

    def create_data(self):
        conf = {
            'AllowOfferOther': self.declaration.offer_other,
            'EduOrganization': self._create_edu_organizations()
        }
        return conf


class ApplicationRulesDataProxy:

    @staticmethod
    def _get_ReadOnlyFields():
        return [map_changes.get_read_only_fields()]

    @staticmethod
    def create_rules_data(declaration):
        conf = {
            "ReadOnlyFields": ApplicationRulesDataProxy._get_ReadOnlyFields()
        }
        return ApplicationRulesData(**conf)


class DocumentReferencesDataProxy:

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
