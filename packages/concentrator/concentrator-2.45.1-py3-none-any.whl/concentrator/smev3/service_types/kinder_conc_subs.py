#!/usr/bin/env python

#
# Generated Fri Oct  9 11:46:55 2020 by generateDS.py version 2.36.2.
# Python 3.8.1 (default, Oct  9 2020, 11:20:41)  [GCC 9.3.0]
#
# Command line options:
#   ('-o', '/home/mark/PycharmProjects/concentrator/src/concentrator/smev3/service_types/kinder_conc.py')
#   ('-s', '/home/mark/PycharmProjects/concentrator/src/concentrator/smev3/service_types/kinder_conc_subs.py')
#
# Command line arguments:
#   ./concentrator-kindergarten.xsd
#
# Command line:
#   /home/mark/PycharmProjects/concentrator/venv3.8/bin/generateDS -o "/home/mark/PycharmProjects/concentrator/src/concentrator/smev3/service_types/kinder_conc.py" -s "/home/mark/PycharmProjects/concentrator/src/concentrator/smev3/service_types/kinder_conc_subs.py" ./concentrator-kindergarten.xsd
#
# Current working directory (os.getcwd()):
#   xsd
#

import os
import sys
from lxml import etree as etree_

from . import kinder_conc as supermod

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


class DataElementTypeSub(supermod.DataElementType):
    def __init__(self, code=None, valueOf_=None, **kwargs_):
        super(DataElementTypeSub, self).__init__(code, valueOf_,  **kwargs_)
supermod.DataElementType.subclass = DataElementTypeSub
# end class DataElementTypeSub


class AddressTypeSub(supermod.AddressType):
    def __init__(self, FullAddress=None, Index=None, Region=None, Area=None, City=None, CityArea=None, Place=None, Street=None, AdditionalArea=None, AdditionalStreet=None, House=None, Building1=None, Building2=None, Apartment=None, **kwargs_):
        super(AddressTypeSub, self).__init__(FullAddress, Index, Region, Area, City, CityArea, Place, Street, AdditionalArea, AdditionalStreet, House, Building1, Building2, Apartment,  **kwargs_)
supermod.AddressType.subclass = AddressTypeSub
# end class AddressTypeSub


class DocInfoTypeSub(supermod.DocInfoType):
    def __init__(self, DocName=None, DocSeries=None, DocNumber=None, DocIssueDate=None, DocIssued=None, **kwargs_):
        super(DocInfoTypeSub, self).__init__(DocName, DocSeries, DocNumber, DocIssueDate, DocIssued,  **kwargs_)
supermod.DocInfoType.subclass = DocInfoTypeSub
# end class DocInfoTypeSub


class PersonIdentityDocInfoTypeSub(supermod.PersonIdentityDocInfoType):
    def __init__(self, IdentityDocName=None, IdentityDocSeries=None, IdentityDocNumber=None, IdentityDocIssueDate=None, IdentityDocIssueCode=None, IdentityDocIssued=None, Citizenship=None, BirthCountry=None, BirthPlace=None, **kwargs_):
        super(PersonIdentityDocInfoTypeSub, self).__init__(IdentityDocName, IdentityDocSeries, IdentityDocNumber, IdentityDocIssueDate, IdentityDocIssueCode, IdentityDocIssued, Citizenship, BirthCountry, BirthPlace,  **kwargs_)
supermod.PersonIdentityDocInfoType.subclass = PersonIdentityDocInfoTypeSub
# end class PersonIdentityDocInfoTypeSub


class PersonCredentialsDocInfoTypeSub(supermod.PersonCredentialsDocInfoType):
    def __init__(self, CredentialsDocName=None, CredentialsDocSeries=None, CredentialsDocNumber=None, CredentialsDocDate=None, CredentialsDocIssued=None, **kwargs_):
        super(PersonCredentialsDocInfoTypeSub, self).__init__(CredentialsDocName, CredentialsDocSeries, CredentialsDocNumber, CredentialsDocDate, CredentialsDocIssued,  **kwargs_)
supermod.PersonCredentialsDocInfoType.subclass = PersonCredentialsDocInfoTypeSub
# end class PersonCredentialsDocInfoTypeSub


class PersonInfoTypeSub(supermod.PersonInfoType):
    def __init__(self, PersonSurname=None, PersonName=None, PersonMiddleName=None, PersonBirthDate=None, PersonSex=None, PersonSNILS=None, PersonPhone=None, PersonEmail=None, PersonIdentityDocInfo=None, PersonType=None, PersonCredentialsDocInfo=None, **kwargs_):
        super(PersonInfoTypeSub, self).__init__(PersonSurname, PersonName, PersonMiddleName, PersonBirthDate, PersonSex, PersonSNILS, PersonPhone, PersonEmail, PersonIdentityDocInfo, PersonType, PersonCredentialsDocInfo,  **kwargs_)
supermod.PersonInfoType.subclass = PersonInfoTypeSub
# end class PersonInfoTypeSub


class ChildBirthDocRFTypeSub(supermod.ChildBirthDocRFType):
    def __init__(self, ChildBirthDocSeries=None, ChildBirthDocNumber=None, ChildBirthDocActNumber=None, ChildBirthDocIssueDate=None, ChildBirthDocIssued=None, ChildBirthPlace=None, **kwargs_):
        super(ChildBirthDocRFTypeSub, self).__init__(ChildBirthDocSeries, ChildBirthDocNumber, ChildBirthDocActNumber, ChildBirthDocIssueDate, ChildBirthDocIssued, ChildBirthPlace,  **kwargs_)
supermod.ChildBirthDocRFType.subclass = ChildBirthDocRFTypeSub
# end class ChildBirthDocRFTypeSub


class ChildBirthDocForeignTypeSub(supermod.ChildBirthDocForeignType):
    def __init__(self, ChildBirthDocName=None, ChildBirthDocSeries=None, ChildBirthDocNumber=None, **kwargs_):
        super(ChildBirthDocForeignTypeSub, self).__init__(ChildBirthDocName, ChildBirthDocSeries, ChildBirthDocNumber,  **kwargs_)
supermod.ChildBirthDocForeignType.subclass = ChildBirthDocForeignTypeSub
# end class ChildBirthDocForeignTypeSub


class ChildInfoTypeSub(supermod.ChildInfoType):
    def __init__(self, ChildSurname=None, ChildName=None, ChildMiddleName=None, ChildSex=None, ChildBirthDate=None, ChildSNILS=None, ChildBirthDocRF=None, ChildBirthDocForeign=None, **kwargs_):
        super(ChildInfoTypeSub, self).__init__(ChildSurname, ChildName, ChildMiddleName, ChildSex, ChildBirthDate, ChildSNILS, ChildBirthDocRF, ChildBirthDocForeign,  **kwargs_)
supermod.ChildInfoType.subclass = ChildInfoTypeSub
# end class ChildInfoTypeSub


class EduOrganizationTypeSub(supermod.EduOrganizationType):
    def __init__(self, code=None, priority=None, valueOf_=None, **kwargs_):
        super(EduOrganizationTypeSub, self).__init__(code, priority, valueOf_,  **kwargs_)
supermod.EduOrganizationType.subclass = EduOrganizationTypeSub
# end class EduOrganizationTypeSub


class EduOrganizationsTypeSub(supermod.EduOrganizationsType):
    def __init__(self, EduOrganization=None, AllowOfferOther=None, **kwargs_):
        super(EduOrganizationsTypeSub, self).__init__(EduOrganization, AllowOfferOther,  **kwargs_)
supermod.EduOrganizationsType.subclass = EduOrganizationsTypeSub
# end class EduOrganizationsTypeSub


class AdaptationProgramTypeSub(supermod.AdaptationProgramType):
    def __init__(self, AdaptationGroup=None, AdaptationGroupType=None, AdaptationDocInfo=None, AgreementOnGeneralGroup=None, AgreementOnCareGroup=None, **kwargs_):
        super(AdaptationProgramTypeSub, self).__init__(AdaptationGroup, AdaptationGroupType, AdaptationDocInfo, AgreementOnGeneralGroup, AgreementOnCareGroup,  **kwargs_)
supermod.AdaptationProgramType.subclass = AdaptationProgramTypeSub
# end class AdaptationProgramTypeSub


class BenefitInfoTypeSub(supermod.BenefitInfoType):
    def __init__(self, BenefitCategory=None, BenefitDocInfo=None, **kwargs_):
        super(BenefitInfoTypeSub, self).__init__(BenefitCategory, BenefitDocInfo,  **kwargs_)
supermod.BenefitInfoType.subclass = BenefitInfoTypeSub
# end class BenefitInfoTypeSub


class BenefitsInfoTypeSub(supermod.BenefitsInfoType):
    def __init__(self, BenefitInfo=None, **kwargs_):
        super(BenefitsInfoTypeSub, self).__init__(BenefitInfo,  **kwargs_)
supermod.BenefitsInfoType.subclass = BenefitsInfoTypeSub
# end class BenefitsInfoTypeSub


class ApplicationTypeSub(supermod.ApplicationType):
    def __init__(self, orderId=None, ServicesType=None, PersonInfo=None, ChildInfo=None, Address=None, AddressResidence=None, EduOrganizations=None, EntryDate=None, AdaptationProgram=None, ScheduleType=None, BenefitsInfo=None, **kwargs_):
        super(ApplicationTypeSub, self).__init__(orderId, ServicesType, PersonInfo, ChildInfo, Address, AddressResidence, EduOrganizations, EntryDate, AdaptationProgram, ScheduleType, BenefitsInfo,  **kwargs_)
supermod.ApplicationType.subclass = ApplicationTypeSub
# end class ApplicationTypeSub


class ApplicationChooseRequestTypeSub(supermod.ApplicationChooseRequestType):
    def __init__(self, orderId=None, EduOrganizationCode=None, EduOrganizationAnswer=None, **kwargs_):
        super(ApplicationChooseRequestTypeSub, self).__init__(orderId, EduOrganizationCode, EduOrganizationAnswer,  **kwargs_)
supermod.ApplicationChooseRequestType.subclass = ApplicationChooseRequestTypeSub
# end class ApplicationChooseRequestTypeSub


class GetApplicationRequestTypeSub(supermod.GetApplicationRequestType):
    def __init__(self, orderId=None, **kwargs_):
        super(GetApplicationRequestTypeSub, self).__init__(orderId,  **kwargs_)
supermod.GetApplicationRequestType.subclass = GetApplicationRequestTypeSub
# end class GetApplicationRequestTypeSub


class GetApplicationQueueRequestTypeSub(supermod.GetApplicationQueueRequestType):
    def __init__(self, orderId=None, **kwargs_):
        super(GetApplicationQueueRequestTypeSub, self).__init__(orderId,  **kwargs_)
supermod.GetApplicationQueueRequestType.subclass = GetApplicationQueueRequestTypeSub
# end class GetApplicationQueueRequestTypeSub


class cancelRequestTypeSub(supermod.cancelRequestType):
    def __init__(self, orderId=None, reason=None, **kwargs_):
        super(cancelRequestTypeSub, self).__init__(orderId, reason,  **kwargs_)
supermod.cancelRequestType.subclass = cancelRequestTypeSub
# end class cancelRequestTypeSub


class textRequestTypeSub(supermod.textRequestType):
    def __init__(self, orderId=None, text=None, **kwargs_):
        super(textRequestTypeSub, self).__init__(orderId, text,  **kwargs_)
supermod.textRequestType.subclass = textRequestTypeSub
# end class textRequestTypeSub


class FormDataTypeSub(supermod.FormDataType):
    def __init__(self, oktmo=None, ApplicationRequest=None, ApplicationChooseRequest=None, GetApplicationRequest=None, GetApplicationQueueRequest=None, cancelRequest=None, textRequest=None, **kwargs_):
        super(FormDataTypeSub, self).__init__(oktmo, ApplicationRequest, ApplicationChooseRequest, GetApplicationRequest, GetApplicationQueueRequest, cancelRequest, textRequest,  **kwargs_)
supermod.FormDataType.subclass = FormDataTypeSub
# end class FormDataTypeSub


class orderIdTypeSub(supermod.orderIdType):
    def __init__(self, pguId=None, **kwargs_):
        super(orderIdTypeSub, self).__init__(pguId,  **kwargs_)
supermod.orderIdType.subclass = orderIdTypeSub
# end class orderIdTypeSub


class statusCodeTypeSub(supermod.statusCodeType):
    def __init__(self, techCode=None, **kwargs_):
        super(statusCodeTypeSub, self).__init__(techCode,  **kwargs_)
supermod.statusCodeType.subclass = statusCodeTypeSub
# end class statusCodeTypeSub


class changeOrderInfoTypeSub(supermod.changeOrderInfoType):
    def __init__(self, orderId=None, statusCode=None, comment=None, cancelAllowed=None, sendMessageAllowed=None, **kwargs_):
        super(changeOrderInfoTypeSub, self).__init__(orderId, statusCode, comment, cancelAllowed, sendMessageAllowed,  **kwargs_)
supermod.changeOrderInfoType.subclass = changeOrderInfoTypeSub
# end class changeOrderInfoTypeSub


class EduOrganizationNeedChooseTypeSub(supermod.EduOrganizationNeedChooseType):
    def __init__(self, orderId=None, EduOrganizationCode=None, EduOrganizationOtherCode=None, **kwargs_):
        super(EduOrganizationNeedChooseTypeSub, self).__init__(orderId, EduOrganizationCode, EduOrganizationOtherCode,  **kwargs_)
supermod.EduOrganizationNeedChooseType.subclass = EduOrganizationNeedChooseTypeSub
# end class EduOrganizationNeedChooseTypeSub


class ReadOnlyFieldsTypeSub(supermod.ReadOnlyFieldsType):
    def __init__(self, Field=None, **kwargs_):
        super(ReadOnlyFieldsTypeSub, self).__init__(Field,  **kwargs_)
supermod.ReadOnlyFieldsType.subclass = ReadOnlyFieldsTypeSub
# end class ReadOnlyFieldsTypeSub


class GetApplicationResponseTypeSub(supermod.GetApplicationResponseType):
    def __init__(self, Application=None, ReadOnlyFields=None, EduOrganizationNeedChoose=None, **kwargs_):
        super(GetApplicationResponseTypeSub, self).__init__(Application, ReadOnlyFields, EduOrganizationNeedChoose,  **kwargs_)
supermod.GetApplicationResponseType.subclass = GetApplicationResponseTypeSub
# end class GetApplicationResponseTypeSub


class EduOrganizationQueueTypeSub(supermod.EduOrganizationQueueType):
    def __init__(self, Code=None, NumberInQueue=None, AllInQueue=None, **kwargs_):
        super(EduOrganizationQueueTypeSub, self).__init__(Code, NumberInQueue, AllInQueue,  **kwargs_)
supermod.EduOrganizationQueueType.subclass = EduOrganizationQueueTypeSub
# end class EduOrganizationQueueTypeSub


class GetApplicationQueueResponseTypeSub(supermod.GetApplicationQueueResponseType):
    def __init__(self, orderId=None, EntryDate=None, AdaptationGroup=None, AdaptationGroupType=None, ScheduleType=None, EduOrganizationQueue=None, **kwargs_):
        super(GetApplicationQueueResponseTypeSub, self).__init__(orderId, EntryDate, AdaptationGroup, AdaptationGroupType, ScheduleType, EduOrganizationQueue,  **kwargs_)
supermod.GetApplicationQueueResponseType.subclass = GetApplicationQueueResponseTypeSub
# end class GetApplicationQueueResponseTypeSub


class cancelResponseTypeSub(supermod.cancelResponseType):
    def __init__(self, orderId=None, result=None, comment=None, **kwargs_):
        super(cancelResponseTypeSub, self).__init__(orderId, result, comment,  **kwargs_)
supermod.cancelResponseType.subclass = cancelResponseTypeSub
# end class cancelResponseTypeSub


class textResponseTypeSub(supermod.textResponseType):
    def __init__(self, orderId=None, result=None, **kwargs_):
        super(textResponseTypeSub, self).__init__(orderId, result,  **kwargs_)
supermod.textResponseType.subclass = textResponseTypeSub
# end class textResponseTypeSub


class FormDataResponseTypeSub(supermod.FormDataResponseType):
    def __init__(self, oktmo=None, changeOrderInfo=None, GetApplicationResponse=None, GetApplicationQueueResponse=None, cancelResponse=None, textResponse=None, **kwargs_):
        super(FormDataResponseTypeSub, self).__init__(oktmo, changeOrderInfo, GetApplicationResponse, GetApplicationQueueResponse, cancelResponse, textResponse,  **kwargs_)
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
        rootTag = 'DataElementType'
        rootClass = supermod.DataElementType
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
            namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.1.1"',
            pretty_print=True)
    return rootObj


def parseEtree(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DataElementType'
        rootClass = supermod.DataElementType
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
        rootTag = 'DataElementType'
        rootClass = supermod.DataElementType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.1.1"')
    return rootObj


def parseLiteral(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DataElementType'
        rootClass = supermod.DataElementType
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
