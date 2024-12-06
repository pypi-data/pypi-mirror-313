from spyne.model.complex import XmlAttribute
from spyne.model.complex import XmlData
from spyne.model.primitive import Boolean
from spyne.model.primitive import Date
from spyne.model.primitive import DateTime
from spyne.model.primitive import Integer
from spyne.model.primitive import Long
from spyne.model.primitive import Unicode
from spyne.model.primitive import UnsignedInteger

from kinder.plugins.privilege_attributes.models import PrivilegeOwnerEnum
from kinder.webservice.spyne_ws.declaration_info.types import (
    CustomComplexModel)

from concentrator.webservice.entities import ComplexModelWithNamespace
from concentrator.webservice.entities import NotBlankDate
from concentrator.webservice.entities import NotBlankDateTime
from concentrator.webservice.entities import NotBlankUnicode


# -----------------------------------------------------------------------------
# Типы заявления
# -----------------------------------------------------------------------------
class ExternalId(NotBlankUnicode):
    class Attributes(Unicode.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(Unicode.Annotations):
        doc = u'Идентификатор заявления в подсистеме "Концентратор Услуг"'


class Status(NotBlankUnicode):
    class Attributes(Unicode.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(Unicode.Annotations):
        doc = u'Статус запроса'


class RegionalId(NotBlankUnicode):
    class Attributes(Unicode.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(Unicode.Annotations):
        doc = u'Идентификатор заявления в региональной системе'


class SubmitDate(NotBlankDateTime):
    class Attributes(DateTime.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(DateTime.Annotations):
        doc = u'Дата создания заявление'


class EntryDate(NotBlankDate):
    class Attributes(NotBlankDate.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(DateTime.Annotations):
        doc = u'Дата желаемого зачисления'


class StateName(NotBlankUnicode):
    class Annotations(Unicode.Annotations):
        doc = u'Статус заявления'


class StateDetails(NotBlankUnicode):
    class Annotations(Unicode.Annotations):
        doc = u'Детализация статуса'


class StateCode(NotBlankUnicode):
    class Annotations(Unicode.Annotations):
        doc = u'Код статуса'


# -----------------------------------------------------------------------------
# Типы фил лица
# -----------------------------------------------------------------------------
class FIO(NotBlankUnicode):
    class Attributes(Unicode.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(Unicode.Annotations):
        doc = u'Первые буквы фамилии, имени и отчества'


class FirstName(NotBlankUnicode):
    class Annotations(Unicode.Annotations):
        doc = u'Имя'


class LastName(NotBlankUnicode):
    class Annotations(Unicode.Annotations):
        doc = u'Фамилия'


class MiddleName(NotBlankUnicode):
    class Annotations(Unicode.Annotations):
        doc = u'Отчество ребенка'


# TODO: Регулярочка не помешала бы
class Snils(NotBlankUnicode):
    class Annotations(Unicode.Annotations):
        doc = u'СНИЛС'


class FourDocNumber(NotBlankUnicode):
    class Annotations(Unicode.Annotations):
        doc = u'4 цифры номера документа'


class DocNumber(NotBlankUnicode):
    class Annotations(Unicode.Annotations):
        doc = u'Серия и номер документа удостоверяющего личность'


class DocSeria(NotBlankUnicode):
    class Annotations(Unicode.Annotations):
        doc = u'Серия документа удостоверяющего личность'


class DocType(NotBlankUnicode):
    class Annotations(Unicode.Annotations):
        doc = u'Идентификатор типа документа удостоверяющего личность'


class DocIssueDate(NotBlankDate):
    class Annotations(Date.Annotations):
        doc = u'Дата выдачи документа удостоверяющего личность'


class DocIssuerName(NotBlankUnicode):
    class Attributes(Unicode.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(Unicode.Annotations):
        doc = u'Место выдачи документа удостоверяющего личность'


class DocIssuerDepartmentCode(NotBlankUnicode):
    class Attributes(Unicode.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(Unicode.Annotations):
        doc = u'Код подзразделения выдавший документ удостоверяющей личность'


class DateOfBirth(NotBlankDate):
    class Annotations(Date.Annotations):
        doc = u'День рождения'


# -----------------------------------------------------------------------------
# Типы групп
# -----------------------------------------------------------------------------
class AgeGroupType(NotBlankUnicode):
    class Attributes(Unicode.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(Unicode.Annotations):
        doc = u'Возрастная группа в ДОО. Справочника'


# -----------------------------------------------------------------------------
# Типы ребенка
# -----------------------------------------------------------------------------
# Потребность по здоровью
class AdaptationProgramType(NotBlankUnicode):
    class Annotations(NotBlankUnicode.Annotations):
        doc = u'Адаптационная программа'


class Sex(NotBlankUnicode):
    class Attributes(Unicode.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(NotBlankUnicode.Annotations):
        doc = u'Пол заявлемого'


class AddressRegistration(NotBlankUnicode):
    class Attributes(Unicode.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(NotBlankUnicode.Annotations):
        doc = u'Адрес регистрации'


class AddressResidence(NotBlankUnicode):
    class Attributes(Unicode.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(NotBlankUnicode.Annotations):
        doc = u'Адрес проживания'


class BenefitItem(ComplexModelWithNamespace):
    """
    Информация о льготе
    """

    name = XmlData(Unicode)
    Type = XmlAttribute(Integer)

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = u'Информация о льготе'


class Benefits(ComplexModelWithNamespace):

    Benefit = BenefitItem.customize(min_occurs=0, max_occurs="unbounded",
                                    nillable=False)
    BenefitsDocInfo = NotBlankUnicode
    Other = NotBlankUnicode


class DeclaredPersonSearchResult(ComplexModelWithNamespace):
    FIO = FIO
    DocNumber = DocNumber(min_occurs=1)
    DateOfBirth = DateOfBirth(min_occurs=1)
    Sex = Sex
    AddressRegistration = AddressRegistration
    AddressResidence = AddressResidence
    AgeGroupType = AgeGroupType
    Benefits = Benefits.customize(min_occurs=0, nillable=False)

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = u'Данные о ребенке'


# -----------------------------------------------------------------------------
# Типы организации
# -----------------------------------------------------------------------------
class EduOrganizationCode(NotBlankUnicode):
    class Attributes(Unicode.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(Unicode.Annotations):
        doc = u'Код ОО в регионе'


class EducationProgramType(NotBlankUnicode):
    class Annotations(Unicode.Annotations):
        doc = u'Образовательная программа'


class Other(NotBlankUnicode):
    class Annotations(Unicode.Annotations):
        doc = u'Другие льготы'


class EduOrganization(ComplexModelWithNamespace):
    """
    Информация об организации
    """

    Code = Unicode
    Priority = Integer

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = u'Контейнер, содержит информацию об ОО'


class EduOrganizationsData(ComplexModelWithNamespace):
    """
    Информация о ОО
    """

    _type_info = [
        ('EduOrganization', EduOrganization.customize(
            max_occurs='unbounded')),
        ('AllowOfferOther', Boolean)
    ]

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = u'Информация об ОО'


# -----------------------------------------------------------------------------
# Типы представителя
# -----------------------------------------------------------------------------
class ApplicantType(NotBlankUnicode):
    class Attributes(Unicode.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(Unicode.Annotations):
        doc = u'Категоря заявителя'


class ApplicantSearchResult(ComplexModelWithNamespace):
    FIO = FIO
    ApplicantType = ApplicantType
    DocNumber = DocNumber(min_occurs=1)

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = u'Данные о заявителе'


class ApplicationSearchResult(ComplexModelWithNamespace):
    ExternalId = ExternalId
    RegionalId = RegionalId
    EducationProgramType = EducationProgramType
    AdaptationProgramType = AdaptationProgramType
    SubmitDate = SubmitDate
    EntryDate = EntryDate
    State = StateName
    StateDetails = StateDetails
    Applicant = ApplicantSearchResult
    DeclaredPerson = DeclaredPersonSearchResult


# -----------------------------------------------------------------------------
# Типы очереди
# -----------------------------------------------------------------------------
class Order(Long):
    class Attributes(Long.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(Unicode.Annotations):
        doc = u'Порядок заявления в очереди'


class Application(ComplexModelWithNamespace):
    Order = Order
    ExternalId = ExternalId
    RegionalId = RegionalId
    EducationProgramType = EducationProgramType
    AdaptationProgramType = AdaptationProgramType
    SubmitDate = SubmitDate
    EntryDate = EntryDate
    State = StateName(min_occurs=1)
    StateDetails = StateDetails
    Applicant = ApplicantSearchResult.customize(nillable=False, min_occurs=1)
    DeclaredPerson = DeclaredPersonSearchResult.customize(nillable=False,
                                                          min_occurs=1)

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = u'Данные о заявке'


class Queue(ComplexModelWithNamespace):
    EduOrganizationCode = EduOrganizationCode
    ApplicationsCount = Long(nillable=False, min_occurs=1)
    Application = Application.customize(min_occurs=1, max_occurs="unbounded",
                                        nillable=False)

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = u'Контейнер, содержит информацию об Очереди'


# -----------------------------------------------------------------------------
# Типы очереди
# -----------------------------------------------------------------------------

class ApplicantData(ComplexModelWithNamespace):
    """
    Информация о заявителе
    """
    FirstName = FirstName(min_occurs=1)
    LastName = LastName(min_occurs=1)
    MiddleName = MiddleName
    DocType = DocType(min_occurs=1)
    DocSeria = DocSeria(min_occurs=1)
    DocNumber = DocNumber(min_occurs=1)
    DocIssueDate = DocIssueDate(min_occurs=1)
    DocIssuerName = DocIssuerName
    DocIssuerDepartmentCode = DocIssuerDepartmentCode
    Snils = Snils(min_occurs=1)
    ApplicantType = ApplicantType
    ApplicantTypeOtherName = NotBlankUnicode
    ApplicantTypeOtherDocNumber = NotBlankUnicode
    Email = NotBlankUnicode(min_occurs=1)
    PhoneNumber = NotBlankUnicode

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = u'Контейнер, содержит информацию о заявителе'


class DeclaredPersonData(ComplexModelWithNamespace):
    """
    Информация о ребенке
    """
    FirstName = FirstName(min_occurs=1)
    LastName = LastName(min_occurs=1)
    MiddleName = MiddleName
    Snils = Snils(min_occurs=1)
    BirthPlace = Unicode
    BirthDocSeria = DocSeria
    BirthDocNumber = DocNumber
    BirthDocActNumber = Unicode.customize(min_occurs=0)
    BirthDocIssueDate = DocIssueDate
    BirthDocIssuer = Unicode.customize(min_occurs=0)
    BirthDocForeign = Unicode.customize(min_occurs=0)
    BirthDocForeignNumber = Unicode.customize(min_occurs=0)
    AgeGroupType = AgeGroupType
    DateOfBirth = Date
    # В большом городе
    Sex = Sex
    AddressRegistration = AddressRegistration
    AddressResidence = AddressResidence
    Benefits = Benefits.customize(min_occurs=0, nillable=False)

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = u'Контейнер, содержит информацию о ребенке'


# -----------------------------------------------------------------------------
# Типы сервиса "Запрос текущей очереди заявления"
# -----------------------------------------------------------------------------
class GetApplicationQueueRequest(ComplexModelWithNamespace):
    ExternalId = ExternalId(min_occurs=1)
    AllApplications = Boolean(min_occurs=0, nillable=False)
    EduOrganizationCode = EduOrganizationCode(min_occurs=0)

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = u'Идентификатор заявления в подсистеме “Концентратор Услуг”.'


class GetApplicationQueueResponse(ComplexModelWithNamespace):
    Queue = Queue.customize(max_occurs='unbounded', nillable=False)
    SupportAllApplications = Boolean(min_occurs=0, nillable=False)


# -----------------------------------------------------------------------------
# Типы сервиса “Запрос текущего статуса заявления”
# -----------------------------------------------------------------------------
class GetApplicationStateResponse(ComplexModelWithNamespace):
    Code = StateCode(min_occurs=1)
    Name = StateName(min_occurs=1)
    Details = StateDetails


class GetApplicationStateRequest(ComplexModelWithNamespace):

    _type_info = [
        ('ExternalId',
         ExternalId(min_occurs=1))
    ]

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = (
            u'Идентификатор заявления в подсистеме “Концентратор Услуг”.')


# -----------------------------------------------------------------------------
# типы сервиса Поиск Заявлений по совпадению персональных данных ребенка и
# представителя
# -----------------------------------------------------------------------------
class FindApplicationsByDeclaredPersonRequest(ComplexModelWithNamespace):
    FirstName = FirstName
    LastName = LastName
    MiddleName = MiddleName
    Snils = Snils
    DateOfBirth = DateOfBirth
    DocType = DocType
    DocNumber = DocNumber
    DocIssueDate = Date

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = (u'Контейнер, содержит '
               u'информацию о персональных данных')


class FindApplicationsByApplicantRequest(ComplexModelWithNamespace):
    FirstName = FirstName
    LastName = LastName
    MiddleName = MiddleName
    Snils = Snils
    DateOfBirth = DateOfBirth
    DocType = DocType
    DocSeria = DocSeria
    DocNumber = DocNumber
    DocIssueDate = Date


class FindApplicationsByDeclaredPersonResponse(ComplexModelWithNamespace):
    Application = ApplicationSearchResult.customize(max_occurs='unbounded',
                                                    nillable=False)


class FindApplicationsByApplicantResponse(ComplexModelWithNamespace):
    Application = ApplicationSearchResult.customize(max_occurs='unbounded',
                                                    nillable=False)


# -----------------------------------------------------------------------------
# типы сервиса Создания заявления
# -----------------------------------------------------------------------------
class DocumentReference(ComplexModelWithNamespace):

    Code = Unicode.customize(nillable=False, min_occurs=1, max_occurs=1)
    Name = NotBlankUnicode
    Description = NotBlankUnicode

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = u'Контейнер, содержит информацию о документах'


class DocumentReferencesData(ComplexModelWithNamespace):

    _type_info = [
        ('DocumentReference', DocumentReference.customize(
            max_occurs='unbounded', min_occurs=0))
    ]

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = u'Контейнер, содержит информацию о документах'


class NewApplicationResponse(ComplexModelWithNamespace):

    _type_info = [
        ('RegionalId', RegionalId)
    ]

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = u'Контейнер, содержит информацию о результатах работы метода'


# -----------------------------------------------------------------------------
# типы сервиса Получение данных Заявления для изменения
# -----------------------------------------------------------------------------
class ReadOnlyFields(ComplexModelWithNamespace):
    Field = Unicode.customize(
        max_occurs='unbounded', min_occurs=0, nillable=False)


class ApplicationRulesData(ComplexModelWithNamespace):
    ReadOnlyFields = ReadOnlyFields.customize(min_occurs=0, nillable=False)


class GetApplicationRequest(ComplexModelWithNamespace):
    ExternalId = ExternalId
    ApplicantFirstName = FirstName(min_occurs=1)
    ApplicantLastName = LastName(min_occurs=1)
    ApplicantMiddleName = MiddleName


class LipetskEduOrganization(EduOrganization):
    """
    Информация об организации
    """
    CodeMO = Integer
    OkatoMO = Unicode


class LipetskEduOrganizationsData(ComplexModelWithNamespace):
    """
    Информация о ОО
    """
    EduOrganization = LipetskEduOrganization.customize(max_occurs='unbounded')
    AllowOfferOther = Boolean

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = u'Информация об ОО'


class WhoHaveBenefit(ComplexModelWithNamespace):
    Type = UnsignedInteger(values=list(PrivilegeOwnerEnum.values.keys()),
                           min_occurs=1, nillable=False)
    FirstName = FirstName
    LastName = LastName
    MiddleName = MiddleName
    DocType = DocType
    DocSeria = DocSeria
    DocNumber = DocNumber
    DocIssueDate = DocIssueDate
    DocIssuerName = DocIssuerName
    DocIssuerDepartmentCode = DocIssuerDepartmentCode
    Snils = Snils

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = u'Информация об ОО'


class LipetskBenefits(ComplexModelWithNamespace):
    Benefit = BenefitItem.customize(min_occurs=0, max_occurs="unbounded",
                                    nillable=False)
    WhoHaveBenefit = WhoHaveBenefit.customize(min_occurs=1, nillable=False)

    BenefitsDocInfo = NotBlankUnicode
    Other = NotBlankUnicode


# -----------------------------------------------------------------------------
# типы сервиса Создания заявления
# -----------------------------------------------------------------------------
class LipetskApplicantData(ApplicantData):
    u"""Информация о заявителе
    добавили AddressResidence AddressRegistration
    """
    AddressRegistration = AddressRegistration
    AddressResidence = AddressResidence

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = u'Контейнер, содержит информацию о заявителе'


class LipetskDeclaredPersonData(ComplexModelWithNamespace):
    u"""Информация о ребенке
    добавили DateOfActNumber
    """
    FirstName = FirstName(min_occurs=1)
    LastName = LastName(min_occurs=1)
    MiddleName = MiddleName
    Snils = Snils(min_occurs=1)
    BirthPlace = Unicode
    BirthDocSeria = DocSeria
    BirthDocNumber = DocNumber
    BirthDocActNumber = Unicode.customize(min_occurs=0)
    BirthDocIssueDate = DocIssueDate
    BirthDocIssuer = Unicode.customize(min_occurs=0)
    BirthDocForeign = Unicode.customize(min_occurs=0)
    BirthDocForeignNumber = Unicode.customize(min_occurs=0)
    AgeGroupType = AgeGroupType
    DateOfBirth = Date
    # В большом городе
    Sex = Sex
    AddressRegistration = AddressRegistration
    AddressResidence = AddressResidence
    Benefits = LipetskBenefits.customize(min_occurs=0, nillable=False)
    DateOfActNumber = Date
    ArrivalTimeType = Unicode
    IssuerState = Unicode

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = u'Контейнер, содержит информацию о ребенке'


class NewApplicationRequest(ComplexModelWithNamespace):
    _type_info = [
        ('ExternalId', ExternalId),
        ('SubmitDate', SubmitDate),
        ('EntryDate', EntryDate),
        ('EducationProgramType', EducationProgramType),
        ('AdaptationProgramType', AdaptationProgramType),
        ('Applicant', LipetskApplicantData),
        ('DeclaredPerson', LipetskDeclaredPersonData),
        ('EduOrganizations', EduOrganizationsData),
        ('DocumentReferences', DocumentReferencesData.customize(
            min_occurs=0))
    ]

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = u'Контейнер, содержит информацию о заявлении'


# -----------------------------------------------------------------------------
# типы сервиса Изменения данных заявки
# -----------------------------------------------------------------------------
class UpdateApplicationRequest(ComplexModelWithNamespace):

    ExternalId = ExternalId
    State = StateCode
    SubmitDate = SubmitDate
    EntryDate = EntryDate
    EducationProgramType = EducationProgramType
    AdaptationProgramType = AdaptationProgramType
    Applicant = LipetskApplicantData.customize(nillable=False, min_occurs=1)
    DeclaredPerson = LipetskDeclaredPersonData.customize(
        nillable=False, min_occurs=1)
    EduOrganizationsData = EduOrganizationsData.customize(nillable=False,
                                                          min_occurs=1)
    DocumentReferences = DocumentReferencesData.customize(
        min_occurs=0)


class UpdateApplicationResponse(ComplexModelWithNamespace):
    Status = Status


# -----------------------------------------------------------------------------
# типы сервиса Получение данных Заявления для изменения
# -----------------------------------------------------------------------------
class GetApplicationResponse(ComplexModelWithNamespace):
    SubmitDate = SubmitDate
    EntryDate = EntryDate
    EducationProgramType = EducationProgramType
    AdaptationProgramType = AdaptationProgramType
    Applicant = LipetskApplicantData.customize(nillable=False, min_occurs=1)
    DeclaredPerson = LipetskDeclaredPersonData.customize(
        nillable=False, min_occurs=1)
    EduOrganizationsData = LipetskEduOrganizationsData.customize(
        nillable=False, min_occurs=1)
    ApplicationRules = ApplicationRulesData.customize(nillable=False,
                                                      min_occurs=1)
    DocumentReferences = DocumentReferencesData.customize(min_occurs=0)


class DeclarationStatus(CustomComplexModel):

    DeclID = Unicode
    AllCategoryPosition = Unicode
    StatusName = Unicode(nillable=False, min_occurs=1)
    Position = Unicode(nillable=False, min_occurs=1)
    CommonPosition = Unicode
    CommonRayonPosition = Unicode
    SummaryRayonPosition = Unicode
    CommonMoPosition = Unicode
    SummaryMoPosition = Unicode
    UnitName = Unicode(nillable=False, min_occurs=1)
    Date = Unicode(nillable=False, min_occurs=1)
    DesiredDate = Unicode(nillable=False, min_occurs=1)
    StatusDescription = Unicode(nillable=False, min_occurs=1)
    Raion = Unicode()

    class Annotations(CustomComplexModel.Annotations):
        doc = u'Информация о статусе заявления и позиции в очереди'
