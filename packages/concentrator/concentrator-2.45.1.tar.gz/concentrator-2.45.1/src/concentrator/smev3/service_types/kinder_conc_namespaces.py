# Схeма ../templates/xsd/concentrator-kindergarten.xsd

GenerateDSNamespaceDefs = {
    'FormDataResponseType':
        'xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.1.1"',
}

GenerateDSNamespaceTypePrefixes = {
    # nsprefix_ для типа FormDataResponseType
    'FormDataResponseType': 'tns',
    'FormDataResponseType_oktmo': 'tns',
    'FormDataResponseType_changeOrderInfo': 'tns',
    'FormDataResponseType_GetApplicationResponse': 'tns',
    'FormDataResponseType_GetApplicationQueueResponse': 'tns',
    'FormDataResponseType_cancelResponse': 'tns',
    'FormDataResponseType_textResponse': 'tns',

    # nsprefix_ для типа changeOrderInfoType
    'changeOrderInfoType': 'tns',
    'changeOrderInfoType_orderId': 'tns',
    'changeOrderInfoType_statusCode': 'tns',
    'changeOrderInfoType_comment': 'tns',
    'changeOrderInfoType_cancelAllowed': 'tns',
    'changeOrderInfoType_sendMessageAllowed': 'tns',

    # nsprefix_ для типа GetApplicationResponseType
    'GetApplicationResponseType': 'tns',
    'GetApplicationResponseType_Application': 'tns',
    'GetApplicationResponseType_ReadOnlyFields': 'tns',
    'GetApplicationResponseType_EduOrganizationNeedChoose': 'tns',

    # nsprefix_ для типа GetApplicationQueueResponseType
    'GetApplicationQueueResponseType': 'tns',
    'GetApplicationQueueResponseType_orderId': 'tns',
    'GetApplicationQueueResponseType_EntryDate': 'tns',
    'GetApplicationQueueResponseType_AdaptationGroup': 'tns',
    'GetApplicationQueueResponseType_AdaptationGroupType': 'tns',
    'GetApplicationQueueResponseType_ScheduleType': 'tns',
    'GetApplicationQueueResponseType_EduOrganizationQueue': 'tns',

    # nsprefix_ для типа cancelResponseType
    'cancelResponseType': 'tns',
    'cancelResponseType_orderId': 'tns',
    'cancelResponseType_result': 'tns',
    'cancelResponseType_comment': 'tns',

    # nsprefix_ для типа textResponseType
    'textResponseType': 'tns',
    'textResponseType_orderId': 'tns',
    'textResponseType_result': 'tns',

    # nsprefix_ для типа ApplicationType
    'ApplicationType': 'tns',
    'ApplicationType_orderId': 'tns',
    'ApplicationType_ServicesType': 'tns',
    'ApplicationType_PersonInfo': 'tns',
    'ApplicationType_ChildInfo': 'tns',
    'ApplicationType_Address': 'tns',
    'ApplicationType_AddressResidence': 'tns',
    'ApplicationType_EduOrganizations': 'tns',
    'ApplicationType_EntryDate': 'tns',
    'ApplicationType_AdaptationProgram': 'tns',
    'ApplicationType_ScheduleType': 'tns',
    'ApplicationType_BenefitsInfo': 'tns',

    # nsprefix_ для типа BenefitsInfoType
    'BenefitsInfoType': 'tns',
    'BenefitsInfoType_BenefitInfo': 'tns',

    # nsprefix_ для типа BenefitInfoType
    'BenefitInfoType': 'tns',
    'BenefitInfoType_BenefitCategory': 'tns',
    'BenefitInfoType_BenefitDocInfo': 'tns',

    # nsprefix_ для типа AdaptationProgramType
    'AdaptationProgramType': 'tns',
    'AdaptationProgramType_AdaptationGroup': 'tns',
    'AdaptationProgramType_AdaptationGroupType': 'tns',
    'AdaptationProgramType_AdaptationDocInfo': 'tns',
    'AdaptationProgramType_AgreementOnGeneralGroup': 'tns',
    'AdaptationProgramType_AgreementOnCareGroup': 'tns',

    # nsprefix_ для типа EduOrganizationsType
    'EduOrganizationsType': 'tns',
    'EduOrganizationsType_EduOrganization': 'tns',
    'EduOrganizationsType_AllowOfferOther': 'tns',

    # nsprefix_ для типа EduOrganizationType
    'EduOrganizationType': 'tns',
    'EduOrganizationType_code': 'tns',
    'EduOrganizationType_priority': 'tns',

    # nsprefix_ для типа ChildInfoType
    'ChildInfoType': 'tns',
    'ChildInfoType_ChildSurname': 'tns',
    'ChildInfoType_ChildName': 'tns',
    'ChildInfoType_ChildMiddleName': 'tns',
    'ChildInfoType_ChildSex': 'tns',
    'ChildInfoType_ChildBirthDate': 'tns',
    'ChildInfoType_ChildSNILS': 'tns',
    'ChildInfoType_ChildBirthDocRF': 'tns',
    'ChildInfoType_ChildBirthDocForeign': 'tns',

    # nsprefix_ для типа ChildBirthDocForeignType
    'ChildBirthDocForeignType': 'tns',
    'ChildBirthDocForeignType_ChildBirthDocName': 'tns',
    'ChildBirthDocForeignType_ChildBirthDocSeries': 'tns',
    'ChildBirthDocForeignType_ChildBirthDocNumber': 'tns',

    # nsprefix_ для типа ChildBirthDocRFType
    'ChildBirthDocRFType': 'tns',
    'ChildBirthDocRFType_ChildBirthDocSeries': 'tns',
    'ChildBirthDocRFType_ChildBirthDocNumber': 'tns',
    'ChildBirthDocRFType_ChildBirthDocActNumber': 'tns',
    'ChildBirthDocRFType_ChildBirthDocIssueDate': 'tns',
    'ChildBirthDocRFType_ChildBirthDocIssued': 'tns',
    'ChildBirthDocRFType_ChildBirthPlace': 'tns',

    # nsprefix_ для типа PersonInfoType
    'PersonInfoType': 'tns',
    'PersonInfoType_PersonSurname': 'tns',
    'PersonInfoType_PersonName': 'tns',
    'PersonInfoType_PersonMiddleName': 'tns',
    'PersonInfoType_PersonBirthDate': 'tns',
    'PersonInfoType_PersonSex': 'tns',
    'PersonInfoType_PersonSNILS': 'tns',
    'PersonInfoType_PersonPhone': 'tns',
    'PersonInfoType_PersonEmail': 'tns',
    'PersonInfoType_PersonIdentityDocInfo': 'tns',
    'PersonInfoType_PersonType': 'tns',
    'PersonInfoType_PersonCredentialsDocInfo': 'tns',

    # nsprefix_ для типа PersonCredentialsDocInfoType
    'PersonCredentialsDocInfoType': 'tns',
    'PersonCredentialsDocInfoType_CredentialsDocName': 'tns',
    'PersonCredentialsDocInfoType_CredentialsDocSeries': 'tns',
    'PersonCredentialsDocInfoType_CredentialsDocNumber': 'tns',
    'PersonCredentialsDocInfoType_CredentialsDocDate': 'tns',
    'PersonCredentialsDocInfoType_CredentialsDocIssued': 'tns',

    # nsprefix_ для типа PersonIdentityDocInfoType
    'PersonIdentityDocInfoType': 'tns',
    'PersonIdentityDocInfoType_IdentityDocName': 'tns',
    'PersonIdentityDocInfoType_IdentityDocSeries': 'tns',
    'PersonIdentityDocInfoType_IdentityDocNumber': 'tns',
    'PersonIdentityDocInfoType_IdentityDocIssueDate': 'tns',
    'PersonIdentityDocInfoType_IdentityDocIssueCode': 'tns',
    'PersonIdentityDocInfoType_IdentityDocIssued': 'tns',
    'PersonIdentityDocInfoType_Citizenship': 'tns',
    'PersonIdentityDocInfoType_BirthCountry': 'tns',
    'PersonIdentityDocInfoType_BirthPlace': 'tns',

    # nsprefix_ для типа DocInfoType
    'DocInfoType': 'tns',
    'DocInfoType_DocName': 'tns',
    'DocInfoType_DocSeries': 'tns',
    'DocInfoType_DocNumber': 'tns',
    'DocInfoType_DocIssueDate': 'tns',
    'DocInfoType_DocIssued': 'tns',

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

    # nsprefix_ для типа DataElementType
    'DataElementType': 'tns',
    'DataElementType_code': 'tns',

    # nsprefix_ для типа ApplicationChooseRequestType
    'ApplicationChooseRequestType': 'tns',
    'ApplicationChooseRequestType_orderId': 'tns',
    'ApplicationChooseRequestType_EduOrganizationCode': 'tns',
    'ApplicationChooseRequestType_EduOrganizationAnswer': 'tns',

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

    # nsprefix_ для типа textRequestType
    'textRequestType': 'tns',
    'textRequestType_orderId': 'tns',
    'textRequestType_text': 'tns',

    # nsprefix_ для типа orderIdType
    'orderIdType': 'tns',
    'orderIdType_pguId': 'tns',

    # nsprefix_ для типа statusCodeType
    'statusCodeType': 'tns',
    'statusCodeType_techCode': 'tns',

    # nsprefix_ для типа FormDataType
    'FormDataType': 'tns',
    'FormDataType_oktmo': 'tns',
    'FormDataType_ApplicationRequest': 'tns',
    'FormDataType_ApplicationChooseRequest': 'tns',
    'FormDataType_GetApplicationRequest': 'tns',
    'FormDataType_GetApplicationQueueRequest': 'tns',
    'FormDataType_cancelRequest': 'tns',
    'FormDataType_textRequest': 'tns',

    # nsprefix_ для типа EduOrganizationQueueType
    'EduOrganizationQueueType': 'tns',
    'EduOrganizationQueueType_Code': 'tns',
    'EduOrganizationQueueType_NumberInQueue': 'tns',
    'EduOrganizationQueueType_AllInQueue': 'tns',
}
