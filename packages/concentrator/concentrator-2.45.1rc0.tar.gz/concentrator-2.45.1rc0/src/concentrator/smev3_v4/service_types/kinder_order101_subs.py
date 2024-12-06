#!/usr/bin/env python

#
# Generated Mon Sep 30 16:38:23 2024 by generateDS.py version 2.44.1.
# Python 3.9.19 (main, Sep  5 2024, 19:03:10)  [GCC 10.2.1 20210110]
#
# Command line options:
#   ('-o', '/opt/project/edukndg/py-libs/concentrator/src/concentrator/smev3_v4/service_types/kinder_order101.py')
#   ('-s', '/opt/project/edukndg/py-libs/concentrator/src/concentrator/smev3_v4/service_types/kinder_order101_subs.py')
#
# Command line arguments:
#   /opt/project/edukndg/py-libs/concentrator/src/concentrator/smev3_v4/templates/schema/kinderorder101.xsd
#
# Command line:
#   /home/eduser/devel/py-libs/bin/generateDS -o "/opt/project/edukndg/py-libs/concentrator/src/concentrator/smev3_v4/service_types/kinder_order101.py" -s "/opt/project/edukndg/py-libs/concentrator/src/concentrator/smev3_v4/service_types/kinder_order101_subs.py" /opt/project/edukndg/py-libs/concentrator/src/concentrator/smev3_v4/templates/schema/kinderorder101.xsd
#
# Current working directory (os.getcwd()):
#   bin
#

import os
import sys
from lxml import etree as etree_

import kinder_order101 as supermod

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


class ChildBirthDocForeignTypeSub(supermod.ChildBirthDocForeignType):
    def __init__(self, ChildBirthDocName=None, ChildBirthDocSeries=None, ChildBirthDocNumber=None, ChildBirthDocIssueDate=None, ChildBirthDocIssued=None, **kwargs_):
        super(ChildBirthDocForeignTypeSub, self).__init__(ChildBirthDocName, ChildBirthDocSeries, ChildBirthDocNumber, ChildBirthDocIssueDate, ChildBirthDocIssued,  **kwargs_)
supermod.ChildBirthDocForeignType.subclass = ChildBirthDocForeignTypeSub
# end class ChildBirthDocForeignTypeSub


class AddressTypeSub(supermod.AddressType):
    def __init__(self, FullAddress=None, Index=None, Region=None, Area=None, City=None, CityArea=None, Place=None, Street=None, AdditionalArea=None, AdditionalStreet=None, House=None, Building1=None, Building2=None, Apartment=None, **kwargs_):
        super(AddressTypeSub, self).__init__(FullAddress, Index, Region, Area, City, CityArea, Place, Street, AdditionalArea, AdditionalStreet, House, Building1, Building2, Apartment,  **kwargs_)
supermod.AddressType.subclass = AddressTypeSub
# end class AddressTypeSub


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


class BenefitInfoWithoutFilesTypeSub(supermod.BenefitInfoWithoutFilesType):
    def __init__(self, BenefitCategory=None, BenefitDocInfo=None, **kwargs_):
        super(BenefitInfoWithoutFilesTypeSub, self).__init__(BenefitCategory, BenefitDocInfo,  **kwargs_)
supermod.BenefitInfoWithoutFilesType.subclass = BenefitInfoWithoutFilesTypeSub
# end class BenefitInfoWithoutFilesTypeSub


class ChildBirthActTypeSub(supermod.ChildBirthActType):
    def __init__(self, ChildBirthDocActNumber=None, ChildBirthDocActDate=None, ChildActBirthDocIssued=None, **kwargs_):
        super(ChildBirthActTypeSub, self).__init__(ChildBirthDocActNumber, ChildBirthDocActDate, ChildActBirthDocIssued,  **kwargs_)
supermod.ChildBirthActType.subclass = ChildBirthActTypeSub
# end class ChildBirthActTypeSub


class ApplicationTypeSub(supermod.ApplicationType):
    def __init__(self, PersonInfo=None, PersonIdentityDocInfo=None, ChildInfo=None, Address=None, EntryParams=None, AdaptationProgram=None, MedicalReport=None, EduOrganizations=None, BrotherSisterInfo=None, BenefitInfo=None, **kwargs_):
        super(ApplicationTypeSub, self).__init__(PersonInfo, PersonIdentityDocInfo, ChildInfo, Address, EntryParams, AdaptationProgram, MedicalReport, EduOrganizations, BrotherSisterInfo, BenefitInfo,  **kwargs_)
supermod.ApplicationType.subclass = ApplicationTypeSub
# end class ApplicationTypeSub


class statusCodeTypeSub(supermod.statusCodeType):
    def __init__(self, orgCode=None, techCode=None, **kwargs_):
        super(statusCodeTypeSub, self).__init__(orgCode, techCode,  **kwargs_)
supermod.statusCodeType.subclass = statusCodeTypeSub
# end class statusCodeTypeSub


class statusHistoryTypeSub(supermod.statusHistoryType):
    def __init__(self, statusCode=None, statusDate=None, statusComment=None, cancelAllowed=None, **kwargs_):
        super(statusHistoryTypeSub, self).__init__(statusCode, statusDate, statusComment, cancelAllowed,  **kwargs_)
supermod.statusHistoryType.subclass = statusHistoryTypeSub
# end class statusHistoryTypeSub


class statusHistoryListTypeSub(supermod.statusHistoryListType):
    def __init__(self, statusHistory=None, **kwargs_):
        super(statusHistoryListTypeSub, self).__init__(statusHistory,  **kwargs_)
supermod.statusHistoryListType.subclass = statusHistoryListTypeSub
# end class statusHistoryListTypeSub


class CreateOrderRequestTypeSub(supermod.CreateOrderRequestType):
    def __init__(self, orderId_InfoRequest=None, requestDate=None, statusHistoryList=None, application=None, **kwargs_):
        super(CreateOrderRequestTypeSub, self).__init__(orderId_InfoRequest, requestDate, statusHistoryList, application,  **kwargs_)
supermod.CreateOrderRequestType.subclass = CreateOrderRequestTypeSub
# end class CreateOrderRequestTypeSub


class UpdateOrderRequestTypeSub(supermod.UpdateOrderRequestType):
    def __init__(self, orderId=None, statusHistoryList=None, application=None, **kwargs_):
        super(UpdateOrderRequestTypeSub, self).__init__(orderId, statusHistoryList, application,  **kwargs_)
supermod.UpdateOrderRequestType.subclass = UpdateOrderRequestTypeSub
# end class UpdateOrderRequestTypeSub


class OrderRequestTypeSub(supermod.OrderRequestType):
    def __init__(self, env=None, CreateOrderRequest=None, UpdateOrderRequest=None, **kwargs_):
        super(OrderRequestTypeSub, self).__init__(env, CreateOrderRequest, UpdateOrderRequest,  **kwargs_)
supermod.OrderRequestType.subclass = OrderRequestTypeSub
# end class OrderRequestTypeSub


class CreateOrderResponseTypeSub(supermod.CreateOrderResponseType):
    def __init__(self, code=None, message=None, orderId_InfoRequest=None, orderId=None, **kwargs_):
        super(CreateOrderResponseTypeSub, self).__init__(code, message, orderId_InfoRequest, orderId,  **kwargs_)
supermod.CreateOrderResponseType.subclass = CreateOrderResponseTypeSub
# end class CreateOrderResponseTypeSub


class UpdateOrderResponseTypeSub(supermod.UpdateOrderResponseType):
    def __init__(self, code=None, message=None, **kwargs_):
        super(UpdateOrderResponseTypeSub, self).__init__(code, message,  **kwargs_)
supermod.UpdateOrderResponseType.subclass = UpdateOrderResponseTypeSub
# end class UpdateOrderResponseTypeSub


class OrderResponseTypeSub(supermod.OrderResponseType):
    def __init__(self, CreateOrderResponse=None, UpdateOrderResponse=None, **kwargs_):
        super(OrderResponseTypeSub, self).__init__(CreateOrderResponse, UpdateOrderResponse,  **kwargs_)
supermod.OrderResponseType.subclass = OrderResponseTypeSub
# end class OrderResponseTypeSub


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
            namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.1"',
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
            namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.1"')
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
