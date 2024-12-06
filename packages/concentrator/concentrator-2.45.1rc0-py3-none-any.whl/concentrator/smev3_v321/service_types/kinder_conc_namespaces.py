# Схeма ../templates/schema/concentrator-kindergarten.xsd

GenerateDSNamespaceDefs = {
    'FormDataResponseType':
        'xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"',
}

GenerateDSNamespaceTypePrefixes = {
    # nsprefix_ для типа FormDataResponseType
    'FormDataResponseType': 'tns',
    'FormDataResponseType_changeOrderInfo': 'tns',
    'FormDataResponseType_GetApplicationQueueResponse': 'tns',
    'FormDataResponseType_GetApplicationQueueReasonResponse': 'tns',
    'FormDataResponseType_GetApplicationResponse': 'tns',
    'FormDataResponseType_GetApplicationAdmissionResponse': 'tns',
    'FormDataResponseType_cancelResponse': 'tns',

    # nsprefix_ для типа changeOrderInfoType
    'changeOrderInfoType': 'tns',
    'changeOrderInfoType_orderId': 'tns',
    'changeOrderInfoType_statusCode': 'tns',
    'changeOrderInfoType_comment': 'tns',
    'changeOrderInfoType_cancelAllowed': 'tns',

    # nsprefix_ для типа ApplicationQueueResponseType
    # (GetApplicationQueueResponse)
    'ApplicationQueueResponseType': 'tns',
    'ApplicationQueueResponseType_orderId': 'tns',
    'ApplicationQueueResponseType_Position': 'tns',
    'ApplicationQueueResponseType_Total': 'tns',
    'ApplicationQueueResponseType_WithoutQueue': 'tns',
    'ApplicationQueueResponseType_FirstQueue': 'tns',
    'ApplicationQueueResponseType_AdvantageQueue': 'tns',
    'ApplicationQueueResponseType_RelevantDT': 'tns',

    # nsprefix_ для типа GetApplicationQueueReasonResponseType
    'GetApplicationQueueReasonResponseType': 'tns',
    'GetApplicationQueueReasonResponseType_orderId': 'tns',
    'GetApplicationQueueReasonResponseType_IncreaseQueue': 'tns',
    'GetApplicationQueueReasonResponseType_GotAPlace': 'tns',
    'GetApplicationQueueReasonResponseType_IncreaseBenefits': 'tns',

    # nsprefix_ для типа GetApplicationResponseType
    'GetApplicationResponseType': 'tns',
    'GetApplicationResponseType_orderId': 'tns',
    'GetApplicationResponseType_PersonInfo': 'tns',
    'GetApplicationResponseType_PersonIdentityDocInfo': 'tns',
    'GetApplicationResponseType_ChildInfo': 'tns',
    'GetApplicationResponseType_Address': 'tns',
    'GetApplicationResponseType_EntryParams': 'tns',
    'GetApplicationResponseType_AdaptationProgram': 'tns',
    'GetApplicationResponseType_MedicalReport': 'tns',
    'GetApplicationResponseType_EduOrganizations': 'tns',
    'GetApplicationResponseType_BrotherSisterInfo': 'tns',
    'GetApplicationResponseType_BenefitInfo': 'tns',

    # nsprefix_ для типа GetApplicationAdmissionResponseType
    'GetApplicationAdmissionResponseType': 'tns',
    'GetApplicationAdmissionResponseType_orderId': 'tns',
    'GetApplicationAdmissionResponseType_PersonInfo': 'tns',
    'GetApplicationAdmissionResponseType_PersonIdentityDocInfo': 'tns',
    'GetApplicationAdmissionResponseType_ChildInfo': 'tns',
    'GetApplicationAdmissionResponseType_Address': 'tns',
    'GetApplicationAdmissionResponseType_EntryParams': 'tns',
    'GetApplicationAdmissionResponseType_AdaptationProgram': 'tns',
    'GetApplicationAdmissionResponseType_MedicalReport': 'tns',
    'GetApplicationAdmissionResponseType_EduOrganizationCode': 'tns',

    # nsprefix_ для типа cancelResponseType
    'cancelResponseType': 'tns',
    'cancelResponseType_orderId': 'tns',
    'cancelResponseType_result': 'tns',
    'cancelResponseType_comment': 'tns',

    # nsprefix_ для типа ApplicationType
    'ApplicationType': 'tns',
    'ApplicationType_orderId': 'tns',
    'ApplicationType_ServicesType': 'tns',
    'ApplicationType_FilingDate': 'tns',
    'ApplicationType_PersonInfo': 'tns',
    'ApplicationType_PersonIdentityDocInfo': 'tns',
    'ApplicationType_ChildInfo': 'tns',
    'ApplicationType_Address': 'tns',
    'ApplicationType_EntryParams': 'tns',
    'ApplicationType_AdaptationProgram': 'tns',
    'ApplicationType_MedicalReport': 'tns',
    'ApplicationType_EduOrganizations': 'tns',
    'ApplicationType_BrotherSisterInfo': 'tns',
    'ApplicationType_BenefitInfo': 'tns',

    # nsprefix_ для типа BenefitInfoType
    'BenefitInfoType': 'tns',
    'BenefitInfoType_BenefitCategory': 'tns',
    'BenefitInfoType_BenefitDocInfo': 'tns',
    'BenefitInfoType_BenefitFile': 'tns',

    # nsprefix_ для типа AdaptationProgramType
    'AdaptationProgramType': 'tns',
    'AdaptationProgramType_AdaptationGroup': 'tns',
    'AdaptationProgramType_AdaptationGroupType': 'tns',
    'AdaptationProgramType_AgreementOnGeneralGroup': 'tns',
    'AdaptationProgramType_AgreementOnCareGroup': 'tns',
    'AdaptationProgramType_NeedSpecialCareConditions': 'tns',

    # nsprefix_ для типа MedicalReportWithoutFilesType
    'MedicalReportWithoutFilesType': 'tns',
    'MedicalReportWithoutFilesType_DocName': 'tns',
    'MedicalReportWithoutFilesType_DocSeries': 'tns',
    'MedicalReportWithoutFilesType_DocNumber': 'tns',
    'MedicalReportWithoutFilesType_DocIssueDate': 'tns',
    'MedicalReportWithoutFilesType_DocIssued': 'tns',
    'MedicalReportWithoutFilesType_DocExpirationDate': 'tns',

    # nsprefix_ для типа EduOrganizationsType
    'EduOrganizationsType': 'tns',
    'EduOrganizationsType_EduOrganization': 'tns',
    'EduOrganizationsType_AllowOfferOther': 'tns',

    # nsprefix_ для типа EduOrganizationType
    'EduOrganizationType': 'tns',
    'EduOrganizationType_code': 'tns',
    'EduOrganizationType_PriorityNumber': 'tns',

    # nsprefix_ для типа BrotherSisterInfoType
    'BrotherSisterInfoType': 'tns',
    'BrotherSisterInfoType_ChildSurname': 'tns',
    'BrotherSisterInfoType_ChildName': 'tns',
    'BrotherSisterInfoType_ChildMiddleName': 'tns',
    'BrotherSisterInfoType_EduOrganization': 'tns',

    # nsprefix_ для типа ChildInfoType
    'ChildInfoType': 'tns',
    'ChildInfoType_ChildSurname': 'tns',
    'ChildInfoType_ChildName': 'tns',
    'ChildInfoType_ChildMiddleName': 'tns',
    'ChildInfoType_ChildBirthDate': 'tns',
    'ChildInfoType_ChildBirthDocRF': 'tns',
    'ChildInfoType_ChildBirthDocForeign': 'tns',

    # nsprefix_ для типа ChildBirthDocForeignType
    'ChildBirthDocForeignType': 'tns',
    'ChildBirthDocForeignType_ChildBirthDocName': 'tns',
    'ChildBirthDocForeignType_ChildBirthDocSeries': 'tns',
    'ChildBirthDocForeignType_ChildBirthDocNumber': 'tns',
    'ChildBirthDocForeignType_ChildBirthDocIssueDate': 'tns',
    'ChildBirthDocForeignType_ChildBirthDocIssued': 'tns',

    # nsprefix_ для типа ChildBirthDocRFType
    'ChildBirthDocRFType': 'tns',
    'ChildBirthDocRFType_ChildBirthDocSeries': 'tns',
    'ChildBirthDocRFType_ChildBirthDocNumber': 'tns',
    'ChildBirthDocRFType_ChildBirthDocIssueDate': 'tns',
    'ChildBirthDocRFType_ChildBirthDocActNumber': 'tns',
    'ChildBirthDocRFType_ChildBirthDocActDate': 'tns',
    'ChildBirthDocRFType_ChildBirthDocIssued': 'tns',

    # nsprefix_ для типа BenefitInfoWithoutFilesType
    'BenefitInfoWithoutFilesType': 'tns',
    'BenefitInfoWithoutFilesType_BenefitCategory': 'tns',
    'BenefitInfoWithoutFilesType_BenefitDocInfo': 'tns',

    # nsprefix_ для типа PersonInfoType
    'PersonInfoType': 'tns',
    'PersonInfoType_PersonSurname': 'tns',
    'PersonInfoType_PersonName': 'tns',
    'PersonInfoType_PersonMiddleName': 'tns',
    'PersonInfoType_PersonPhone': 'tns',
    'PersonInfoType_PersonEmail': 'tns',
    'PersonInfoType_Parents': 'tns',
    'PersonInfoType_OtherRepresentative': 'tns',

    # nsprefix_ для типа OtherRepresentativeType
    'OtherRepresentativeType': 'tns',
    'OtherRepresentativeType_OtherRepresentativeDocName': 'tns',
    'OtherRepresentativeType_OtherRepresentativeDocSeries': 'tns',
    'OtherRepresentativeType_OtherRepresentativeDocNumber': 'tns',
    'OtherRepresentativeType_OtherRepresentativeDocDate': 'tns',
    'OtherRepresentativeType_OtherRepresentativeDocIssued': 'tns',

    # nsprefix_ для типа PersonIdentityDocInfoType
    'PersonIdentityDocInfoType': 'tns',
    'PersonIdentityDocInfoType_IdentityDocName': 'tns',
    'PersonIdentityDocInfoType_IdentityDocSeries': 'tns',
    'PersonIdentityDocInfoType_IdentityDocNumber': 'tns',
    'PersonIdentityDocInfoType_IdentityDocIssueDate': 'tns',
    'PersonIdentityDocInfoType_IdentityDocIssueCode': 'tns',
    'PersonIdentityDocInfoType_IdentityDocIssued': 'tns',

    # nsprefix_ для типа DocInfoType
    'DocInfoType': 'tns',
    'DocInfoType_DocIssueDate': 'tns',
    'DocInfoType_DocIssued': 'tns',
    'DocInfoType_DocExpirationDate': 'tns',

    # nsprefix_ для типа AddressType
    'AddressType': 'tns',
    'AddressType_FullAddress': 'tns',
    'AddressType_Index': 'tns',
    'AddressType_Region': 'tns',
    'AddressType_Area': 'tns',
    'AddressType_City': 'tns',
    'AddressType_CityArea': 'tns',
    'AddressType_Place': 'tns',
    'AddressType_Street': 'tns',
    'AddressType_AdditionalArea': 'tns',
    'AddressType_AdditionalStreet': 'tns',
    'AddressType_House': 'tns',
    'AddressType_Building1': 'tns',
    'AddressType_Building2': 'tns',
    'AddressType_Apartment': 'tns',

    # nsprefix_ для типа EntryParamsType
    'EntryParamsType': 'tns',
    'EntryParamsType_EntryDate': 'tns',
    'EntryParamsType_Language': 'tns',
    'EntryParamsType_Schedule': 'tns',
    'EntryParamsType_AgreementOnFullDayGroup': 'tns',

    # nsprefix_ для типа DataElementType
    'DataElementType': 'tns',
    'DataElementType_code': 'tns',

    # nsprefix_ для типа GetApplicationRequestType
    'GetApplicationRequestType': 'tns',
    'GetApplicationRequestType_orderId': 'tns',

    # nsprefix_ для типа GetApplicationQueueRequestType
    'GetApplicationQueueRequestType': 'tns',
    'GetApplicationQueueRequestType_orderId': 'tns',

    # nsprefix_ для типа cancelRequestType
    'cancelRequestType': 'tns',
    'cancelRequestType_orderId': 'tns',
    'cancelRequestType_reason': 'tns',

    # nsprefix_ для типа orderIdType
    'orderIdType': 'tns',
    'orderIdType_pguId': 'tns',

    # nsprefix_ для типа statusCodeType
    'statusCodeType': 'tns',
    'statusCodeType_orgCode': 'tns',
    'statusCodeType_techCode': 'tns',

    # nsprefix_ для типа FormDataType
    'FormDataType': 'tns',
    'FormDataType_oktmo': 'tns',
    'FormDataType_ApplicationRequest': 'tns',
    'FormDataType_ApplicationOrderInfoRequest': 'tns',
    'FormDataType_ApplicationAdmissionRequest': 'tns',
    'FormDataType_GetApplicationQueueRequest': 'tns',
    'FormDataType_GetApplicationQueueReasonRequest': 'tns',
    'FormDataType_GetApplicationRequest': 'tns',
    'FormDataType_GetApplicationAdmissionRequest': 'tns',
    'FormDataType_ApplicationRejectionRequest': 'tns',
    'FormDataType_cancelRequest': 'tns',

    # nsprefix_ для типа AppliedDocumentType
    'AppliedDocumentType': 'tns',
    'AppliedDocumentType_CodeDocument': 'tns',
    'AppliedDocumentType_NameDocument': 'tns',
    'AppliedDocumentType_TypeDocument': 'tns',

    # nsprefix_ для типа ApplicationAdmissionRequestType
    'ApplicationAdmissionRequestType': 'tns',
    'ApplicationAdmissionRequestType_orderId': 'tns',
    'ApplicationAdmissionRequestType_ServicesType': 'tns',
    'ApplicationAdmissionRequestType_PersonInfo': 'tns',
    'ApplicationAdmissionRequestType_PersonIdentityDocInfo': 'tns',
    'ApplicationAdmissionRequestType_Person2Info': 'tns',
    'ApplicationAdmissionRequestType_ChildInfo': 'tns',
    'ApplicationAdmissionRequestType_Address': 'tns',
    'ApplicationAdmissionRequestType_EntryParams': 'tns',
    'ApplicationAdmissionRequestType_AdaptationProgram': 'tns',
    'ApplicationAdmissionRequestType_MedicalReport': 'tns',
    'ApplicationAdmissionRequestType_EduOrganizationCode': 'tns',
    'ApplicationAdmissionRequestType_DocListReview': 'tns',
    'ApplicationAdmissionRequestType_LicenseCharter': 'tns',

    # nsprefix_ для типа Person2InfoType
    'Person2InfoType': 'tns',
    'Person2InfoType_Person2Surname': 'tns',
    'Person2InfoType_Person2Name': 'tns',
    'Person2InfoType_Person2MiddleName': 'tns',
    'Person2InfoType_Person2Phone': 'tns',
    'Person2InfoType_Person2Email': 'tns',

    # nsprefix_ для типа GetApplicationQueueReasonRequestType
    'GetApplicationQueueReasonRequestType': 'tns',
    'GetApplicationQueueReasonRequestType_orderId': 'tns',
    'GetApplicationQueueReasonRequestType_PeriodStart': 'tns',
    'GetApplicationQueueReasonRequestType_PeriodEnd': 'tns',

    # nsprefix_ для типа GetApplicationAdmissionRequestType
    'GetApplicationAdmissionRequestType': 'tns',
    'GetApplicationAdmissionRequestType_orderId': 'tns',

    # nsprefix_ для типа ApplicationRejectionRequestType
    'ApplicationRejectionRequestType': 'tns',
    'ApplicationRejectionRequestType_orderId': 'tns',
    'ApplicationRejectionRequestType_comment': 'tns',
}
