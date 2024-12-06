#!/usr/bin/env python

#
# Generated Fri Sep 27 12:58:39 2024 by generateDS.py version 2.44.1.
# Python 3.9.19 (main, Sep  5 2024, 19:03:10)  [GCC 10.2.1 20210110]
# Command line options:
#   ('-o', '/opt/project/edukndg/py-libs/concentrator/src/concentrator/smev3_v4/service_types/kinder_conc4.py')
#   ('-s', '/opt/project/edukndg/py-libs/concentrator/src/concentrator/smev3_v4/service_types/kinder_conc4_subs.py')
#
# Command line arguments:
#   /opt/project/edukndg/py-libs/concentrator/src/concentrator/smev3_v4/templates/schema/kindergarten401.xsd
#
# Command line:
#   /home/eduser/devel/py-libs/bin/generateDS -o "/opt/project/edukndg/py-libs/concentrator/src/concentrator/smev3_v4/service_types/kinder_conc4.py" -s "/opt/project/edukndg/py-libs/concentrator/src/concentrator/smev3_v4/service_types/kinder_conc4_subs.py" /opt/project/edukndg/py-libs/concentrator/src/concentrator/smev3_v4/templates/schema/kindergarten401.xsd
#
# Current working directory (os.getcwd()):
#   bin
#

import os
import sys
from lxml import etree as etree_

import kinder_conc4 as supermod

def parsexml_(infile, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        parser = etree_.ETCompatXMLParser()
    try:
        if isinstance(infile, os.PathLike):
            infile = os.path.join(infile)
    except AttributeError:
        pass
    doc = etree_.parse(infile, parser=parser, **kwargs)
    return doc

def parsexmlstring_(instring, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        try:
            parser = etree_.ETCompatXMLParser()
        except AttributeError:
            # fallback to xml.etree
            parser = etree_.XMLParser()
    element = etree_.fromstring(instring, parser=parser, **kwargs)
    return element

#
# Globals
#

ExternalEncoding = ''
SaveElementTreeNode = True

#
# Data representation classes
#


class AddressTypeSub(supermod.AddressType):
    def __init__(self, FullAddress=None, Index=None, Region=None, Area=None, City=None, CityArea=None, Place=None, Street=None, AdditionalArea=None, AdditionalStreet=None, House=None, Building1=None, Building2=None, Apartment=None, **kwargs_):
        super(AddressTypeSub, self).__init__(FullAddress, Index, Region, Area, City, CityArea, Place, Street, AdditionalArea, AdditionalStreet, House, Building1, Building2, Apartment,  **kwargs_)
supermod.AddressType.subclass = AddressTypeSub
# end class AddressTypeSub


class EduOrganizationDataTypeSub(supermod.EduOrganizationDataType):
    def __init__(self, EduOrganizationCode=None, EduOrganizationName=None, **kwargs_):
        super(EduOrganizationDataTypeSub, self).__init__(EduOrganizationCode, EduOrganizationName,  **kwargs_)
supermod.EduOrganizationDataType.subclass = EduOrganizationDataTypeSub
# end class EduOrganizationDataTypeSub


class DataElementTypeSub(supermod.DataElementType):
    def __init__(self, code=None, valueOf_=None, **kwargs_):
        super(DataElementTypeSub, self).__init__(code, valueOf_,  **kwargs_)
supermod.DataElementType.subclass = DataElementTypeSub
# end class DataElementTypeSub


class AppliedDocumentTypeSub(supermod.AppliedDocumentType):
    def __init__(self, CodeDocument=None, NameDocument=None, TypeDocument=None, **kwargs_):
        super(AppliedDocumentTypeSub, self).__init__(CodeDocument, NameDocument, TypeDocument,  **kwargs_)
supermod.AppliedDocumentType.subclass = AppliedDocumentTypeSub
# end class AppliedDocumentTypeSub


class DocInfoTypeSub(supermod.DocInfoType):
    def __init__(self, DocIssueDate=None, DocIssued=None, DocExpirationDate=None, **kwargs_):
        super(DocInfoTypeSub, self).__init__(DocIssueDate, DocIssued, DocExpirationDate,  **kwargs_)
supermod.DocInfoType.subclass = DocInfoTypeSub
# end class DocInfoTypeSub


class PersonInfoTypeSub(supermod.PersonInfoType):
    def __init__(self, PersonSurname=None, PersonName=None, PersonMiddleName=None, PersonPhone=None, PersonEmail=None, Parents=None, OtherRepresentative=None, **kwargs_):
        super(PersonInfoTypeSub, self).__init__(PersonSurname, PersonName, PersonMiddleName, PersonPhone, PersonEmail, Parents, OtherRepresentative,  **kwargs_)
supermod.PersonInfoType.subclass = PersonInfoTypeSub
# end class PersonInfoTypeSub


class OtherRepresentativeTypeSub(supermod.OtherRepresentativeType):
    def __init__(self, OtherRepresentativeDocName=None, OtherRepresentativeDocSeries=None, OtherRepresentativeDocNumber=None, OtherRepresentativeDocDate=None, OtherRepresentativeDocIssued=None, **kwargs_):
        super(OtherRepresentativeTypeSub, self).__init__(OtherRepresentativeDocName, OtherRepresentativeDocSeries, OtherRepresentativeDocNumber, OtherRepresentativeDocDate, OtherRepresentativeDocIssued,  **kwargs_)
supermod.OtherRepresentativeType.subclass = OtherRepresentativeTypeSub
# end class OtherRepresentativeTypeSub


class PersonIdentityDocInfoTypeSub(supermod.PersonIdentityDocInfoType):
    def __init__(self, IdentityDocName=None, IdentityDocSeries=None, IdentityDocNumber=None, IdentityDocIssueDate=None, IdentityDocIssueCode=None, IdentityDocIssued=None, **kwargs_):
        super(PersonIdentityDocInfoTypeSub, self).__init__(IdentityDocName, IdentityDocSeries, IdentityDocNumber, IdentityDocIssueDate, IdentityDocIssueCode, IdentityDocIssued,  **kwargs_)
supermod.PersonIdentityDocInfoType.subclass = PersonIdentityDocInfoTypeSub
# end class PersonIdentityDocInfoTypeSub


class ChildInfoTypeSub(supermod.ChildInfoType):
    def __init__(self, ChildSurname=None, ChildName=None, ChildMiddleName=None, ChildBirthDate=None, ChildBirthDocRF=None, ChildBirthDocForeign=None, ChildBirthAct=None, **kwargs_):
        super(ChildInfoTypeSub, self).__init__(ChildSurname, ChildName, ChildMiddleName, ChildBirthDate, ChildBirthDocRF, ChildBirthDocForeign, ChildBirthAct,  **kwargs_)
supermod.ChildInfoType.subclass = ChildInfoTypeSub
# end class ChildInfoTypeSub


class ChildBirthDocRFTypeSub(supermod.ChildBirthDocRFType):
    def __init__(self, ChildBirthDocSeries=None, ChildBirthDocNumber=None, ChildBirthDocIssueDate=None, ChildBirthDocActNumber=None, ChildBirthDocActDate=None, ChildBirthDocIssued=None, **kwargs_):
        super(ChildBirthDocRFTypeSub, self).__init__(ChildBirthDocSeries, ChildBirthDocNumber, ChildBirthDocIssueDate, ChildBirthDocActNumber, ChildBirthDocActDate, ChildBirthDocIssued,  **kwargs_)
supermod.ChildBirthDocRFType.subclass = ChildBirthDocRFTypeSub
# end class ChildBirthDocRFTypeSub


class ChildBirthActTypeSub(supermod.ChildBirthActType):
    def __init__(self, ChildBirthDocActNumber=None, ChildBirthDocActDate=None, ChildActBirthDocIssued=None, **kwargs_):
        super(ChildBirthActTypeSub, self).__init__(ChildBirthDocActNumber, ChildBirthDocActDate, ChildActBirthDocIssued,  **kwargs_)
supermod.ChildBirthActType.subclass = ChildBirthActTypeSub
# end class ChildBirthActTypeSub


class ChildBirthDocForeignTypeSub(supermod.ChildBirthDocForeignType):
    def __init__(self, ChildBirthDocName=None, ChildBirthDocSeries=None, ChildBirthDocNumber=None, ChildBirthDocIssueDate=None, ChildBirthDocIssued=None, **kwargs_):
        super(ChildBirthDocForeignTypeSub, self).__init__(ChildBirthDocName, ChildBirthDocSeries, ChildBirthDocNumber, ChildBirthDocIssueDate, ChildBirthDocIssued,  **kwargs_)
supermod.ChildBirthDocForeignType.subclass = ChildBirthDocForeignTypeSub
# end class ChildBirthDocForeignTypeSub


class EntryParamsTypeSub(supermod.EntryParamsType):
    def __init__(self, EntryDate=None, Language=None, Schedule=None, AgreementOnFullDayGroup=None, AgreementOnOtherDayGroup=None, **kwargs_):
        super(EntryParamsTypeSub, self).__init__(EntryDate, Language, Schedule, AgreementOnFullDayGroup, AgreementOnOtherDayGroup,  **kwargs_)
supermod.EntryParamsType.subclass = EntryParamsTypeSub
# end class EntryParamsTypeSub


class AdaptationProgramTypeSub(supermod.AdaptationProgramType):
    def __init__(self, AdaptationGroup=None, AdaptationGroupType=None, AgreementAdaptationEducationGroup=None, AgreementOnGeneralGroup=None, AgreementOnCareGroup=None, NeedSpecialCareConditions=None, **kwargs_):
        super(AdaptationProgramTypeSub, self).__init__(AdaptationGroup, AdaptationGroupType, AgreementAdaptationEducationGroup, AgreementOnGeneralGroup, AgreementOnCareGroup, NeedSpecialCareConditions,  **kwargs_)
supermod.AdaptationProgramType.subclass = AdaptationProgramTypeSub
# end class AdaptationProgramTypeSub


class MedicalReportTypeSub(supermod.MedicalReportType):
    def __init__(self, DocName=None, DocSeries=None, DocNumber=None, DocIssueDate=None, DocIssued=None, DocExpirationDate=None, DocFile=None, **kwargs_):
        super(MedicalReportTypeSub, self).__init__(DocName, DocSeries, DocNumber, DocIssueDate, DocIssued, DocExpirationDate, DocFile,  **kwargs_)
supermod.MedicalReportType.subclass = MedicalReportTypeSub
# end class MedicalReportTypeSub


class MedicalReportWithoutFilesTypeSub(supermod.MedicalReportWithoutFilesType):
    def __init__(self, DocName=None, DocSeries=None, DocNumber=None, DocIssueDate=None, DocIssued=None, DocExpirationDate=None, **kwargs_):
        super(MedicalReportWithoutFilesTypeSub, self).__init__(DocName, DocSeries, DocNumber, DocIssueDate, DocIssued, DocExpirationDate,  **kwargs_)
supermod.MedicalReportWithoutFilesType.subclass = MedicalReportWithoutFilesTypeSub
# end class MedicalReportWithoutFilesTypeSub


class EduOrganizationTypeSub(supermod.EduOrganizationType):
    def __init__(self, code=None, PriorityNumber=None, valueOf_=None, **kwargs_):
        super(EduOrganizationTypeSub, self).__init__(code, PriorityNumber, valueOf_,  **kwargs_)
supermod.EduOrganizationType.subclass = EduOrganizationTypeSub
# end class EduOrganizationTypeSub


class EduOrganizationsTypeSub(supermod.EduOrganizationsType):
    def __init__(self, EduOrganization=None, AllowOfferOther=None, **kwargs_):
        super(EduOrganizationsTypeSub, self).__init__(EduOrganization, AllowOfferOther,  **kwargs_)
supermod.EduOrganizationsType.subclass = EduOrganizationsTypeSub
# end class EduOrganizationsTypeSub


class BrotherSisterInfoTypeSub(supermod.BrotherSisterInfoType):
    def __init__(self, ChildSurname=None, ChildName=None, ChildMiddleName=None, EduOrganization=None, **kwargs_):
        super(BrotherSisterInfoTypeSub, self).__init__(ChildSurname, ChildName, ChildMiddleName, EduOrganization,  **kwargs_)
supermod.BrotherSisterInfoType.subclass = BrotherSisterInfoTypeSub
# end class BrotherSisterInfoTypeSub


class BenefitInfoTypeSub(supermod.BenefitInfoType):
    def __init__(self, BenefitCategory=None, BenefitDocInfo=None, BenefitFile=None, **kwargs_):
        super(BenefitInfoTypeSub, self).__init__(BenefitCategory, BenefitDocInfo, BenefitFile,  **kwargs_)
supermod.BenefitInfoType.subclass = BenefitInfoTypeSub
# end class BenefitInfoTypeSub


class BenefitInfoWithoutFilesTypeSub(supermod.BenefitInfoWithoutFilesType):
    def __init__(self, BenefitCategory=None, BenefitDocInfo=None, **kwargs_):
        super(BenefitInfoWithoutFilesTypeSub, self).__init__(BenefitCategory, BenefitDocInfo,  **kwargs_)
supermod.BenefitInfoWithoutFilesType.subclass = BenefitInfoWithoutFilesTypeSub
# end class BenefitInfoWithoutFilesTypeSub


class ApplicationTypeSub(supermod.ApplicationType):
    def __init__(self, orderId=None, ServicesType=None, FilingDate=None, PersonInfo=None, PersonIdentityDocInfo=None, ChildInfo=None, Address=None, EntryParams=None, AdaptationProgram=None, MedicalReport=None, EduOrganizations=None, BrotherSisterInfo=None, BenefitInfo=None, ConfirmingRightIsLocatedRF=None, attribute=None, refInfo=None, **kwargs_):
        super(ApplicationTypeSub, self).__init__(orderId, ServicesType, FilingDate, PersonInfo, PersonIdentityDocInfo, ChildInfo, Address, EntryParams, AdaptationProgram, MedicalReport, EduOrganizations, BrotherSisterInfo, BenefitInfo, ConfirmingRightIsLocatedRF, attribute, refInfo,  **kwargs_)
supermod.ApplicationType.subclass = ApplicationTypeSub
# end class ApplicationTypeSub


class ApplicationOrderInfoRequestTypeSub(supermod.ApplicationOrderInfoRequestType):
    def __init__(self, orderId=None, ServicesType=None, PersonInfo=None, PersonIdentityDocInfo=None, ChildInfo=None, attribute=None, refInfo=None, **kwargs_):
        super(ApplicationOrderInfoRequestTypeSub, self).__init__(orderId, ServicesType, PersonInfo, PersonIdentityDocInfo, ChildInfo, attribute, refInfo,  **kwargs_)
supermod.ApplicationOrderInfoRequestType.subclass = ApplicationOrderInfoRequestTypeSub
# end class ApplicationOrderInfoRequestTypeSub


class Person2InfoTypeSub(supermod.Person2InfoType):
    def __init__(self, Person2Surname=None, Person2Name=None, Person2MiddleName=None, Person2Phone=None, Person2Email=None, **kwargs_):
        super(Person2InfoTypeSub, self).__init__(Person2Surname, Person2Name, Person2MiddleName, Person2Phone, Person2Email,  **kwargs_)
supermod.Person2InfoType.subclass = Person2InfoTypeSub
# end class Person2InfoTypeSub


class ApplicationAdmissionRequestTypeSub(supermod.ApplicationAdmissionRequestType):
    def __init__(self, orderId=None, ServicesType=None, PersonInfo=None, PersonIdentityDocInfo=None, Person2Info=None, ChildInfo=None, Address=None, EntryParams=None, AdaptationProgram=None, MedicalReport=None, EduOrganizationCode=None, DocListReview=None, LicenseCharter=None, attribute=None, refInfo=None, **kwargs_):
        super(ApplicationAdmissionRequestTypeSub, self).__init__(orderId, ServicesType, PersonInfo, PersonIdentityDocInfo, Person2Info, ChildInfo, Address, EntryParams, AdaptationProgram, MedicalReport, EduOrganizationCode, DocListReview, LicenseCharter, attribute, refInfo,  **kwargs_)
supermod.ApplicationAdmissionRequestType.subclass = ApplicationAdmissionRequestTypeSub
# end class ApplicationAdmissionRequestTypeSub


class GetApplicationQueueRequestTypeSub(supermod.GetApplicationQueueRequestType):
    def __init__(self, orderId=None, attribute=None, refInfo=None, **kwargs_):
        super(GetApplicationQueueRequestTypeSub, self).__init__(orderId, attribute, refInfo,  **kwargs_)
supermod.GetApplicationQueueRequestType.subclass = GetApplicationQueueRequestTypeSub
# end class GetApplicationQueueRequestTypeSub


class GetApplicationQueueReasonRequestTypeSub(supermod.GetApplicationQueueReasonRequestType):
    def __init__(self, orderId=None, PeriodStart=None, PeriodEnd=None, attribute=None, refInfo=None, **kwargs_):
        super(GetApplicationQueueReasonRequestTypeSub, self).__init__(orderId, PeriodStart, PeriodEnd, attribute, refInfo,  **kwargs_)
supermod.GetApplicationQueueReasonRequestType.subclass = GetApplicationQueueReasonRequestTypeSub
# end class GetApplicationQueueReasonRequestTypeSub


class GetApplicationRequestTypeSub(supermod.GetApplicationRequestType):
    def __init__(self, orderId=None, attribute=None, refInfo=None, **kwargs_):
        super(GetApplicationRequestTypeSub, self).__init__(orderId, attribute, refInfo,  **kwargs_)
supermod.GetApplicationRequestType.subclass = GetApplicationRequestTypeSub
# end class GetApplicationRequestTypeSub


class GetApplicationAdmissionRequestTypeSub(supermod.GetApplicationAdmissionRequestType):
    def __init__(self, orderId=None, attribute=None, refInfo=None, **kwargs_):
        super(GetApplicationAdmissionRequestTypeSub, self).__init__(orderId, attribute, refInfo,  **kwargs_)
supermod.GetApplicationAdmissionRequestType.subclass = GetApplicationAdmissionRequestTypeSub
# end class GetApplicationAdmissionRequestTypeSub


class ApplicationRejectionRequestTypeSub(supermod.ApplicationRejectionRequestType):
    def __init__(self, orderId=None, eduOrganizationCode=None, comment=None, attribute=None, refInfo=None, **kwargs_):
        super(ApplicationRejectionRequestTypeSub, self).__init__(orderId, eduOrganizationCode, comment, attribute, refInfo,  **kwargs_)
supermod.ApplicationRejectionRequestType.subclass = ApplicationRejectionRequestTypeSub
# end class ApplicationRejectionRequestTypeSub


class cancelRequestTypeSub(supermod.cancelRequestType):
    def __init__(self, orderId=None, reason=None, attribute=None, refInfo=None, **kwargs_):
        super(cancelRequestTypeSub, self).__init__(orderId, reason, attribute, refInfo,  **kwargs_)
supermod.cancelRequestType.subclass = cancelRequestTypeSub
# end class cancelRequestTypeSub


class orderIdTypeSub(supermod.orderIdType):
    def __init__(self, pguId=None, **kwargs_):
        super(orderIdTypeSub, self).__init__(pguId,  **kwargs_)
supermod.orderIdType.subclass = orderIdTypeSub
# end class orderIdTypeSub


class statusCodeTypeSub(supermod.statusCodeType):
    def __init__(self, orgCode=None, techCode=None, **kwargs_):
        super(statusCodeTypeSub, self).__init__(orgCode, techCode,  **kwargs_)
supermod.statusCodeType.subclass = statusCodeTypeSub
# end class statusCodeTypeSub


class changeOrderInfoTypeSub(supermod.changeOrderInfoType):
    def __init__(self, orderId=None, statusCode=None, comment=None, cancelAllowed=None, refInfo=None, attribute=None, **kwargs_):
        super(changeOrderInfoTypeSub, self).__init__(orderId, statusCode, comment, cancelAllowed, refInfo, attribute,  **kwargs_)
supermod.changeOrderInfoType.subclass = changeOrderInfoTypeSub
# end class changeOrderInfoTypeSub


class ApplicationQueueResponseTypeSub(supermod.ApplicationQueueResponseType):
    def __init__(self, orderId=None, Position=None, Total=None, WithoutQueue=None, FirstQueue=None, AdvantageQueue=None, RelevantDT=None, refInfo=None, attribute=None, **kwargs_):
        super(ApplicationQueueResponseTypeSub, self).__init__(orderId, Position, Total, WithoutQueue, FirstQueue, AdvantageQueue, RelevantDT, refInfo, attribute,  **kwargs_)
supermod.ApplicationQueueResponseType.subclass = ApplicationQueueResponseTypeSub
# end class ApplicationQueueResponseTypeSub


class GetApplicationQueueReasonResponseTypeSub(supermod.GetApplicationQueueReasonResponseType):
    def __init__(self, orderId=None, IncreaseQueue=None, GotAPlace=None, IncreaseBenefits=None, refInfo=None, attribute=None, **kwargs_):
        super(GetApplicationQueueReasonResponseTypeSub, self).__init__(orderId, IncreaseQueue, GotAPlace, IncreaseBenefits, refInfo, attribute,  **kwargs_)
supermod.GetApplicationQueueReasonResponseType.subclass = GetApplicationQueueReasonResponseTypeSub
# end class GetApplicationQueueReasonResponseTypeSub


class GetApplicationResponseTypeSub(supermod.GetApplicationResponseType):
    def __init__(self, orderId=None, PersonInfo=None, PersonIdentityDocInfo=None, ChildInfo=None, Address=None, EntryParams=None, AdaptationProgram=None, MedicalReport=None, EduOrganizations=None, BrotherSisterInfo=None, BenefitInfo=None, refInfo=None, attribute=None, **kwargs_):
        super(GetApplicationResponseTypeSub, self).__init__(orderId, PersonInfo, PersonIdentityDocInfo, ChildInfo, Address, EntryParams, AdaptationProgram, MedicalReport, EduOrganizations, BrotherSisterInfo, BenefitInfo, refInfo, attribute,  **kwargs_)
supermod.GetApplicationResponseType.subclass = GetApplicationResponseTypeSub
# end class GetApplicationResponseTypeSub


class GetApplicationAdmissionResponseTypeSub(supermod.GetApplicationAdmissionResponseType):
    def __init__(self, orderId=None, PersonInfo=None, PersonIdentityDocInfo=None, ChildInfo=None, Address=None, EntryParams=None, AdaptationProgram=None, MedicalReport=None, EduOrganizationData=None, refInfo=None, attribute=None, **kwargs_):
        super(GetApplicationAdmissionResponseTypeSub, self).__init__(orderId, PersonInfo, PersonIdentityDocInfo, ChildInfo, Address, EntryParams, AdaptationProgram, MedicalReport, EduOrganizationData, refInfo, attribute,  **kwargs_)
supermod.GetApplicationAdmissionResponseType.subclass = GetApplicationAdmissionResponseTypeSub
# end class GetApplicationAdmissionResponseTypeSub


class attributeTypeSub(supermod.attributeType):
    def __init__(self, attributeName=None, attributeValue=None, **kwargs_):
        super(attributeTypeSub, self).__init__(attributeName, attributeValue,  **kwargs_)
supermod.attributeType.subclass = attributeTypeSub
# end class attributeTypeSub


class referenceInfoTypeSub(supermod.referenceInfoType):
    def __init__(self, Attribute=None, DirectoryValue=None, **kwargs_):
        super(referenceInfoTypeSub, self).__init__(Attribute, DirectoryValue,  **kwargs_)
supermod.referenceInfoType.subclass = referenceInfoTypeSub
# end class referenceInfoTypeSub


class directoryValueTypeSub(supermod.directoryValueType):
    def __init__(self, Code=None, Value=None, **kwargs_):
        super(directoryValueTypeSub, self).__init__(Code, Value,  **kwargs_)
supermod.directoryValueType.subclass = directoryValueTypeSub
# end class directoryValueTypeSub


class cancelResponseTypeSub(supermod.cancelResponseType):
    def __init__(self, orderId=None, result=None, comment=None, refInfo=None, attribute=None, **kwargs_):
        super(cancelResponseTypeSub, self).__init__(orderId, result, comment, refInfo, attribute,  **kwargs_)
supermod.cancelResponseType.subclass = cancelResponseTypeSub
# end class cancelResponseTypeSub


class FormDataTypeSub(supermod.FormDataType):
    def __init__(self, oktmo=None, ApplicationRequest=None, ApplicationOrderInfoRequest=None, ApplicationAdmissionRequest=None, GetApplicationQueueRequest=None, GetApplicationQueueReasonRequest=None, GetApplicationRequest=None, GetApplicationAdmissionRequest=None, ApplicationRejectionRequest=None, cancelRequest=None, **kwargs_):
        super(FormDataTypeSub, self).__init__(oktmo, ApplicationRequest, ApplicationOrderInfoRequest, ApplicationAdmissionRequest, GetApplicationQueueRequest, GetApplicationQueueReasonRequest, GetApplicationRequest, GetApplicationAdmissionRequest, ApplicationRejectionRequest, cancelRequest,  **kwargs_)
supermod.FormDataType.subclass = FormDataTypeSub
# end class FormDataTypeSub


class FormDataResponseTypeSub(supermod.FormDataResponseType):
    def __init__(self, changeOrderInfo=None, GetApplicationQueueResponse=None, GetApplicationQueueReasonResponse=None, GetApplicationResponse=None, GetApplicationAdmissionResponse=None, cancelResponse=None, **kwargs_):
        super(FormDataResponseTypeSub, self).__init__(changeOrderInfo, GetApplicationQueueResponse, GetApplicationQueueReasonResponse, GetApplicationResponse, GetApplicationAdmissionResponse, cancelResponse,  **kwargs_)
supermod.FormDataResponseType.subclass = FormDataResponseTypeSub
# end class FormDataResponseTypeSub


def get_root_tag(node):
    tag = supermod.Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = None
    rootClass = supermod.GDSClassesMapping.get(tag)
    if rootClass is None and hasattr(supermod, tag):
        rootClass = getattr(supermod, tag)
    return tag, rootClass


def parse(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'AddressType'
        rootClass = supermod.AddressType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/4.0.1"',
            pretty_print=True)
    return rootObj


def parseEtree(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'AddressType'
        rootClass = supermod.AddressType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    mapping = {}
    rootElement = rootObj.to_etree(None, name_=rootTag, mapping_=mapping)
    reverse_mapping = rootObj.gds_reverse_node_mapping(mapping)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        content = etree_.tostring(
            rootElement, pretty_print=True,
            xml_declaration=True, encoding="utf-8")
        sys.stdout.write(content)
        sys.stdout.write('\n')
    return rootObj, rootElement, mapping, reverse_mapping


def parseString(inString, silence=False):
    if sys.version_info.major == 2:
        from StringIO import StringIO
    else:
        from io import BytesIO as StringIO
    parser = None
    rootNode= parsexmlstring_(inString, parser)
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'AddressType'
        rootClass = supermod.AddressType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/4.0.1"')
    return rootObj


def parseLiteral(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'AddressType'
        rootClass = supermod.AddressType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from ??? import *\n\n')
        sys.stdout.write('import ??? as model_\n\n')
        sys.stdout.write('rootObj = model_.rootClass(\n')
        rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
        sys.stdout.write(')\n')
    return rootObj


USAGE_TEXT = """
Usage: python ???.py <infilename>
"""


def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    infilename = args[0]
    parse(infilename)


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()
