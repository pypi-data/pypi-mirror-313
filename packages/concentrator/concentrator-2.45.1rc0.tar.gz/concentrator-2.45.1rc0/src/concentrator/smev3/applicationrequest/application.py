from django.db.transaction import atomic
from django.core.exceptions import ValidationError

from kinder.core.children.models import Children
from kinder.core.children.models import ChildrenDelegate
from kinder.core.children.models import Delegate
from kinder.core.declaration.enum import DeclPortalEnum
from kinder.core.declaration.models import Declaration
from kinder.core.declaration.models import DeclarationPrivilege
from kinder.core.declaration.models import DeclarationSourceEnum
from kinder.core.declaration.models import DeclarationUnit
from kinder.core.declaration.enum import DeclarationTypeInteractionEnum as DTIE
from kinder.core.declaration_status.models import DSS, DeclarationStatus
from kinder.core.dict.models import DocType
from kinder.core.dict.models import DULDelegateType
from kinder.core.dict.models import GroupType
from kinder.core.dict.models import WorkType
from kinder.core.privilege.models import Privilege
from kinder.core.unit.models import Unit
from kinder.plugins.contingent.models import DelegateContingent

from .rules import ChildGenderRule
from .rules import DelegateTypeRule
from .rules import DulDelegateTypeRule
from .rules import GroupTypeRule
from .rules import WorktypeRule
from .utils import process_attachments


class Application:
    """Сохранение заявления из концентратора."""

    def __init__(self, application, attachments):
        self._application = application
        self._attachments = attachments

    def _create_child(self):
        info = self._application.ChildInfo
        dul = info.ChildBirthDocRF
        addr = self._application.Address

        return Children.objects.create(
            firstname=info.ChildName,
            surname=info.ChildSurname,
            patronymic=info.ChildMiddleName,
            gender=ChildGenderRule.system_value(info.ChildSex),
            date_of_birth=info.ChildBirthDate,

            dul_series=dul.ChildBirthDocSeries,
            dul_number=dul.ChildBirthDocNumber,
            dul_date=dul.ChildBirthDocIssueDate,
            zags_act_number=dul.ChildBirthDocActNumber,
            zags_act_place=dul.ChildBirthDocIssued,
            birthplace=dul.ChildBirthPlace,
            snils=info.ChildSNILS,

            reg_address_place=addr.City.code,
            reg_address_street=addr.Street.code,
            reg_address_full=addr.FullAddress,
            reg_address_house=addr.House.valueOf_,
            reg_address_house_guid=addr.House.code,
            reg_address_flat=addr.Apartment,
        )

    def _create_delegate(self):
        info = self._application.PersonInfo
        dul = info.PersonIdentityDocInfo
        addr = self._application.Address

        delegate = Delegate.objects.create(
            surname=info.PersonSurname,
            firstname=info.PersonName,
            patronymic=info.PersonMiddleName,
            date_of_birth=info.PersonBirthDate,
            snils=info.PersonSNILS,
            phones=info.PersonPhone,
            email=info.PersonEmail,

            dul_type=DULDelegateType.objects.get(
                code=DulDelegateTypeRule.system_value(
                    dul.IdentityDocName.code)),
            dul_series=dul.IdentityDocSeries,
            dul_number=dul.IdentityDocNumber,
            dul_date=dul.IdentityDocIssueDate,
            dul_issued_by=dul.IdentityDocIssued,
            dul_place=dul.IdentityDocIssueCode,

            type=DelegateTypeRule.system_value(info.PersonType.code),

            reg_address_place=addr.City.code,
            reg_address_street=addr.Street.code,
            reg_address_full=addr.FullAddress,
            reg_address_house=addr.House.valueOf_,
            reg_address_house_guid=addr.House.code,
            reg_address_flat=addr.Apartment,
        )
        contingent, _ = DelegateContingent.objects.get_or_create(
            delegate=delegate
        )
        contingent.birthplace = ','.join(
                filter(None, (dul.BirthCountry, dul.BirthPlace))
            )
        contingent.save()

        return delegate

    @staticmethod
    def _add_child_to_delegate(child, delegate):
        ChildrenDelegate.objects.create(
            children=child,
            delegate=delegate,
        )

    def _get_mo(self):
        """Определяем МО."""

        units = self._application.EduOrganizations.EduOrganization
        top_units = [u for u in units if u.priority] or units
        try:
            top_unit = Unit.objects.get(id=top_units[0].code)
        except (Unit.DoesNotExist, IndexError):
            raise ValidationError('Не удалось найти МО')
        return top_unit.get_mo()

    def _create_declaration(self, child):
        info = self._application
        spec = info.AdaptationProgram
        try:
            group_type = GroupType.objects.get(
                code=GroupTypeRule.system_value(spec.AdaptationGroup.code))
        except GroupType.DoesNotExist:
            raise ValidationError('Указано неверное значение AdaptationGroup')

        return Declaration.objects.create(
            client_id=info.orderId,
            source=DeclarationSourceEnum.CONCENTRATOR,
            portal=DeclPortalEnum.PORTAL,
            type_interaction=DTIE.SMEV_3,
            children=child,
            desired_date=info.EntryDate,
            status=DeclarationStatus.objects.get(
                code=DSS.RECEIVED),
            work_type=WorkType.objects.get(
                code=WorktypeRule.system_value(info.ScheduleType.code)),
            offer_other=info.EduOrganizations.AllowOfferOther,
            consent_dev_group=spec.AgreementOnGeneralGroup,
            mo=self._get_mo(),
            desired_group_type=group_type)
    
    def _add_docs(self, declaration):
        """
        Добавляем прикреплённые файлы к заявке
        """
        if self._attachments:
            docs = process_attachments(self._attachments, declaration)

    def _add_declaration_units(self, declaration):
        for i, organization in enumerate(
                self._application.EduOrganizations.EduOrganization, 1):
            DeclarationUnit.objects.create(
                declaration=declaration,
                unit_id=organization.code,
                ord=i)

    def _add_priviledges(self, declaration):
        """Добавляет льготы к заявке."""

        for decl_priviledge in self._application.BenefitsInfo.BenefitInfo:
            try:
                privilege = Privilege.objects.get(
                    id=decl_priviledge.BenefitCategory.code)
            except Privilege.DoesNotExist:
                raise ValidationError('Льгота не найдена')

            # Обработка документа, подтверждающего наличие льготы
            document = decl_priviledge.BenefitDocInfo
            if document:
                try:
                    doc_type = DocType.objects.get(
                        id=document.DocName.code)
                except DocType.DoesNotExist:
                    raise ValidationError(
                        'Документ, подтверждающий наличие льготы, не найден')

                document_dict = dict(
                    doc_type=doc_type,
                    doc_series=document.DocSeries,
                    doc_number=document.DocNumber,
                    doc_date=document.DocIssueDate,
                    doc_issued_by=document.DocIssued,
                )
            else:
                document_dict = {}

            DeclarationPrivilege.objects.create(
                declaration=declaration,
                privilege=privilege,
                **document_dict,
            )

    @atomic
    def create(self):
        """Создает и возвращает заявление."""

        child = self._create_child()
        delegate = self._create_delegate()

        self._add_child_to_delegate(child, delegate)
        declaration = self._create_declaration(child)
        self._add_priviledges(declaration)
        self._add_declaration_units(declaration)
        self._add_docs(declaration)
        return declaration
