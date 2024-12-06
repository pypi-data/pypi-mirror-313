from django.db.models import OuterRef
from django.db.models import Prefetch
from django.db.models import Subquery

from aio_client.base import const as aio_base_const
from aio_client.provider.api import PostProviderRequest
from aio_client.provider.api import push_request
from kinder.core.children.models import ChildrenDelegate
from kinder.core.declaration.models import Declaration
from kinder.core.declaration.models import DeclarationPrivilege
from kinder.core.declaration.models import DeclarationUnit
from kinder.core.utils.address import name_from_guid
from kinder.webservice.api.declaration import get_declaration_by_client_id
from kinder.webservice.api.exceptions import ApiException

from concentrator.smev3.base import constants as base_enums
from concentrator.smev3.base.exceptions import ContentFailure
from concentrator.smev3.base.utils import BaseExecutor
from concentrator.smev3.base.utils import SMEV3Response
from concentrator.smev3.base.utils import gender_mapping
from concentrator.smev3.base.utils import get_contingent_param_delegate
from concentrator.smev3.base.utils import get_dul_delegate_type
from concentrator.smev3.base.utils import get_oktmo_region
from concentrator.smev3.base.utils import render_type2xml
from concentrator.smev3.service_types import kinder_conc


class GetApplicationRequestExecutor(BaseExecutor):
    """Исполнитель сервиса GetApplicationRequest."""

    name_service = 'GetApplicationRequest'
    type_service = kinder_conc.GetApplicationRequestType

    @classmethod
    def prepare_query(cls):
        """Выполняет подготовку запроса."""

        subquery_first_delegate = (
            ChildrenDelegate.objects.filter(
                id=Subquery(
                    ChildrenDelegate.objects.filter(
                        children_id=OuterRef('children_id')
                    ).order_by('id').values('id')[:1])
            ).select_related('delegate'))

        subquery_declaration_units = (
            DeclarationUnit.objects.select_related('unit').only(
                'unit__name', 'unit_id', 'ord', 'declaration_id'))

        subquery_declaration_privileges = (
            DeclarationPrivilege.objects.select_related(
                'privilege', 'doc_type'
            ).only(
                'privilege_id', 'privilege__name', 'doc_type_id',
                'doc_type__name', 'doc_series', 'doc_number',
                'declaration_id'))

        query = (
            Declaration.objects.select_related(
                'children'
            ).prefetch_related(
                Prefetch('declarationunit_set',
                         queryset=subquery_declaration_units,
                         to_attr='declaration_units')
            ).prefetch_related(
                Prefetch('children__childrendelegate_set',
                         queryset=subquery_first_delegate,
                         to_attr='first_childrendelegate')
            ).prefetch_related(
                Prefetch('declarationprivilege_set',
                         queryset=subquery_declaration_privileges,
                         to_attr='all_privileges')))

        return query

    @classmethod
    def process(cls, message, request_body):

        try:
            declaration = get_declaration_by_client_id(
                cls.prepare_query(),
                request_body.GetApplicationRequest.orderId)
        except ApiException:
            declaration = None

        try:
            response_body = render_type2xml(
                cls.get_response(declaration), name_type='FormDataResponse')
            content_failure_code = None
            content_failure_comment = None
        except ContentFailure as exc:
            response_body = 'null'
            content_failure_code = exc.content_failure_code
            content_failure_comment = exc.content_failure_comment

        response = push_request(PostProviderRequest(
            origin_message_id=message['origin_message_id'],
            body=response_body,
            message_type=message['message_type'],
            attachments=None,
            content_failure_code=content_failure_code,
            content_failure_comment=content_failure_comment or '',
            replay_to=message['replay_to'],
            is_test_message=message['is_test_message']
        ))

        return SMEV3Response(
            response,
            {
                'method_name': cls.name_service,
                'response': response_body,
                'result': content_failure_comment or base_enums.SUCCESS_MESSAGE
            })

    @classmethod
    def get_response(cls, declaration):
        """Формирует ответ на GetApplicationRequest.

        :param declaration: Заявление
        :type declaration: Declaration
        :return: ответ
        :rtype: FormDataResponseType
        :raise: ContentFailure
        """

        if not declaration:
            raise ContentFailure(
                aio_base_const.FAILURE,
                'Заявление по указанным параметрам не найдено')

        child = declaration.children
        children_delegate, *_ = (
            declaration.children.first_childrendelegate or (None, ))
        if not children_delegate:
            raise ContentFailure(
                aio_base_const.FAILURE, 'Не найден представитель')

        delegate = children_delegate.delegate
        citizenship, citizenship_country, birthplace = (
            get_contingent_param_delegate(delegate))

        delegate_doc = kinder_conc.PersonIdentityDocInfoType(
            IdentityDocName=kinder_conc.DataElementType(
                code=delegate.dul_type_id,
                valueOf_=get_dul_delegate_type(delegate)),
            IdentityDocSeries=delegate.dul_series,
            IdentityDocNumber=delegate.dul_number,
            IdentityDocIssueDate=delegate.dul_date,
            IdentityDocIssueCode=delegate.dul_place,
            IdentityDocIssued=delegate.dul_issued_by,
            Citizenship=citizenship,
            BirthPlace=birthplace
        )
        type_code, type_name = base_enums.DELEGATE_TYPE_CONC[delegate.type]

        delegate_info = kinder_conc.PersonInfoType(
            PersonSurname=delegate.surname,
            PersonName=delegate.firstname,
            PersonMiddleName=delegate.patronymic,
            PersonBirthDate=delegate.date_of_birth,
            PersonSex=gender_mapping(delegate),
            PersonSNILS=delegate.snils,
            PersonPhone=delegate.phones,
            PersonEmail=delegate.email,
            PersonIdentityDocInfo=delegate_doc,
            PersonType=kinder_conc.DataElementType(
                code=type_code,
                valueOf_=type_name
            )
        )

        child_doc = kinder_conc.ChildBirthDocRFType(
            ChildBirthDocSeries=child.dul_series,
            ChildBirthDocNumber=child.dul_number,
            ChildBirthDocActNumber=child.zags_act_number,
            ChildBirthDocIssueDate=child.dul_date,
            ChildBirthDocIssued=child.zags_act_place,
            ChildBirthPlace=child.birthplace,
        )

        child_info = kinder_conc.ChildInfoType(
            ChildSurname=child.surname,
            ChildName=child.firstname,
            ChildMiddleName=child.patronymic,
            ChildSex=(
                base_enums.CHILD_GENDER_ENUM.get(child.gender)),
            ChildBirthDate=child.date_of_birth,
            ChildSNILS=child.snils,
            ChildBirthDocRF=child_doc
        )

        address_info = kinder_conc.AddressType(
            FullAddress=child.reg_address_full,
            Region=kinder_conc.DataElementType(
                code=child.reg_address_place,
                valueOf_=name_from_guid(child.reg_address_place)),
            Street=kinder_conc.DataElementType(
                code=child.reg_address_street,
                valueOf_=name_from_guid(child.reg_address_street)),
            House=kinder_conc.DataElementType(
                code=child.reg_address_house_guid,
                valueOf_=child.reg_address_house),
            Building1=child.reg_address_corps,
            Apartment=child.reg_address_flat,
        )

        edu_org_info = kinder_conc.EduOrganizationsType(
            AllowOfferOther=declaration.offer_other)
        all_declaration_units = declaration.declaration_units or ()
        for declaration_unit in all_declaration_units:
            edu_org_info.add_EduOrganization(kinder_conc.EduOrganizationType(
                code=declaration_unit.unit_id,
                priority=declaration_unit.ord == '1',
                valueOf_=declaration_unit.unit.name
            ))

        benefits_info = kinder_conc.BenefitsInfoType()
        all_privileges = declaration.all_privileges or ()
        for declaration_privilege in all_privileges:
            doc_info = {}

            if declaration_privilege.doc_type:
                doc_info['DocName'] = kinder_conc.DataElementType(
                    code=declaration_privilege.doc_type_id,
                    valueOf_=declaration_privilege.doc_type.name
                )
            
            if declaration_privilege.doc_series:
                doc_info['DocSeries'] = declaration_privilege.doc_series
            
            if declaration_privilege.doc_number:
                doc_info['DocNumber'] = declaration_privilege.doc_number
            
            doc_info_content = {}

            if doc_info:
                doc_info_content['BenefitDocInfo'] = kinder_conc.DocInfoType(
                    **doc_info
                )

            benefits_info.add_BenefitInfo(
                kinder_conc.BenefitInfoType(
                    BenefitCategory=kinder_conc.DataElementType(
                        code=declaration_privilege.privilege_id,
                        valueOf_=declaration_privilege.privilege.name,
                    ),
                    **doc_info_content
                )
            )
        
        schedule_type = None

        if declaration.work_type:
            schedule_type = kinder_conc.DataElementType(
                code=getattr(declaration.work_type, 'id', None),
                valueOf_=getattr(declaration.work_type, 'name', None)
            )
        
        adaptation_program_params = {}

        if declaration.desired_group_type:
            adaptation_program_params['AdaptationGroup'] = (
                kinder_conc.DataElementType(
                    code=declaration.desired_group_type.code,
                    valueOf_=declaration.desired_group_type.name
                )
            )
        
        adaptation_doc_info_params = {}
        if child.health_need_confirmation:
            adaptation_doc_info_params['DocName'] = (
                kinder_conc.DataElementType(
                    valueOf_=child.health_need_confirmation
                )
            )

        if child.health_series:
            adaptation_doc_info_params['DocSeries'] = child.health_series
        
        if child.health_number:
            adaptation_doc_info_params['DocNumber'] = child.health_number
        
        if child.health_need_start_date:
            adaptation_doc_info_params['DocIssueDate'] = (
                child.health_need_start_date)
            
        if child.health_issued_by:
            adaptation_doc_info_params['DocIssued'] = child.health_issued_by
        
        adaptation_doc_info = None
        if adaptation_doc_info_params:
            adaptation_doc_info = kinder_conc.DocInfoType(
                **adaptation_doc_info_params)

        adaptation_program = kinder_conc.AdaptationProgramType(
            AdaptationDocInfo=adaptation_doc_info,
            AgreementOnCareGroup=declaration.consent_care_group,
            AgreementOnGeneralGroup=declaration.consent_dev_group,
            **adaptation_program_params,
        )

        app_type = kinder_conc.ApplicationType(
            orderId=int(declaration.client_id),
            ServicesType=base_enums.GETAPP_SERVICE_TYPE,
            PersonInfo=delegate_info,
            ChildInfo=child_info,
            Address=address_info,
            EduOrganizations=edu_org_info,
            EntryDate=declaration.desired_date,
            AdaptationProgram=adaptation_program,
            ScheduleType=schedule_type,
            BenefitsInfo=benefits_info
        )
        response = kinder_conc.FormDataResponseType(
            oktmo=get_oktmo_region(),
            GetApplicationResponse=kinder_conc.GetApplicationResponseType(
                Application=app_type))

        return response
