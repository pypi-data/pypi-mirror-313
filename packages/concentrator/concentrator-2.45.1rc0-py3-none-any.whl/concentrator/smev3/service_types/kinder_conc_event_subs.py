#!/usr/bin/env python

#
# Generated Fri Oct  9 11:58:49 2020 by generateDS.py version 2.36.2.
# Python 3.8.1 (default, Oct  9 2020, 11:20:41)  [GCC 9.3.0]
#
# Command line options:
#   ('-o', '/home/mark/PycharmProjects/concentrator/src/concentrator/smev3/service_types/kinder_conc_event.py')
#   ('-s', '/home/mark/PycharmProjects/concentrator/src/concentrator/smev3/service_types/kinder_conc_event_subs.py')
#
# Command line arguments:
#   ./event.xsd
#
# Command line:
#   /home/mark/PycharmProjects/concentrator/venv3.8/bin/generateDS -o "/home/mark/PycharmProjects/concentrator/src/concentrator/smev3/service_types/kinder_conc_event.py" -s "/home/mark/PycharmProjects/concentrator/src/concentrator/smev3/service_types/kinder_conc_event_subs.py" ./event.xsd
#
# Current working directory (os.getcwd()):
#   xsd
#

import os
import sys
from lxml import etree as etree_

from . import kinder_conc_event as supermod

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


class statusCodeTypeSub(supermod.statusCodeType):
    def __init__(self, orgCode=None, techCode=None, **kwargs_):
        super(statusCodeTypeSub, self).__init__(orgCode, techCode,  **kwargs_)
supermod.statusCodeType.subclass = statusCodeTypeSub
# end class statusCodeTypeSub


class OrderStatusEventTypeSub(supermod.OrderStatusEventType):
    def __init__(self, statusCode=None, cancelAllowed=None, sendMessageAllowed=None, **kwargs_):
        super(OrderStatusEventTypeSub, self).__init__(statusCode, cancelAllowed, sendMessageAllowed,  **kwargs_)
supermod.OrderStatusEventType.subclass = OrderStatusEventTypeSub
# end class OrderStatusEventTypeSub


class PaymentTypeSub(supermod.PaymentType):
    def __init__(self, source=None, uin=None, description=None, **kwargs_):
        super(PaymentTypeSub, self).__init__(source, uin, description,  **kwargs_)
supermod.PaymentType.subclass = PaymentTypeSub
# end class PaymentTypeSub


class PaymentStatusEventTypeSub(supermod.PaymentStatusEventType):
    def __init__(self, status=None, payment=None, **kwargs_):
        super(PaymentStatusEventTypeSub, self).__init__(status, payment,  **kwargs_)
supermod.PaymentStatusEventType.subclass = PaymentStatusEventTypeSub
# end class PaymentStatusEventTypeSub


class InfoEventTypeSub(supermod.InfoEventType):
    def __init__(self, code=None, **kwargs_):
        super(InfoEventTypeSub, self).__init__(code,  **kwargs_)
supermod.InfoEventType.subclass = InfoEventTypeSub
# end class InfoEventTypeSub


class TextMessageEventTypeSub(supermod.TextMessageEventType):
    def __init__(self, **kwargs_):
        super(TextMessageEventTypeSub, self).__init__( **kwargs_)
supermod.TextMessageEventType.subclass = TextMessageEventTypeSub
# end class TextMessageEventTypeSub


class organizationDataTypeSub(supermod.organizationDataType):
    def __init__(self, organizationId=None, areaId=None, **kwargs_):
        super(organizationDataTypeSub, self).__init__(organizationId, areaId,  **kwargs_)
supermod.organizationDataType.subclass = organizationDataTypeSub
# end class organizationDataTypeSub


class equeueInvitationTypeSub(supermod.equeueInvitationType):
    def __init__(self, organizationData=None, startDate=None, endDate=None, **kwargs_):
        super(equeueInvitationTypeSub, self).__init__(organizationData, startDate, endDate,  **kwargs_)
supermod.equeueInvitationType.subclass = equeueInvitationTypeSub
# end class equeueInvitationTypeSub


class equeueClosedTypeSub(supermod.equeueClosedType):
    def __init__(self, **kwargs_):
        super(equeueClosedTypeSub, self).__init__( **kwargs_)
supermod.equeueClosedType.subclass = equeueClosedTypeSub
# end class equeueClosedTypeSub


class EqueueEventTypeSub(supermod.EqueueEventType):
    def __init__(self, equeueInvitation=None, equeueClosed=None, **kwargs_):
        super(EqueueEventTypeSub, self).__init__(equeueInvitation, equeueClosed,  **kwargs_)
supermod.EqueueEventType.subclass = EqueueEventTypeSub
# end class EqueueEventTypeSub


class EventTypeSub(supermod.EventType):
    def __init__(self, orderStatusEvent=None, paymentStatusEvent=None, infoEvent=None, textMessageEvent=None, equeueEvent=None, **kwargs_):
        super(EventTypeSub, self).__init__(orderStatusEvent, paymentStatusEvent, infoEvent, textMessageEvent, equeueEvent,  **kwargs_)
supermod.EventType.subclass = EventTypeSub
# end class EventTypeSub


class EventServiceRequestTypeSub(supermod.EventServiceRequestType):
    def __init__(self, env=None, orderId=None, eventDate=None, eventComment=None, eventAuthor=None, event=None, **kwargs_):
        super(EventServiceRequestTypeSub, self).__init__(env, orderId, eventDate, eventComment, eventAuthor, event,  **kwargs_)
supermod.EventServiceRequestType.subclass = EventServiceRequestTypeSub
# end class EventServiceRequestTypeSub


class EventServiceResponseTypeSub(supermod.EventServiceResponseType):
    def __init__(self, code=None, message=None, **kwargs_):
        super(EventServiceResponseTypeSub, self).__init__(code, message,  **kwargs_)
supermod.EventServiceResponseType.subclass = EventServiceResponseTypeSub
# end class EventServiceResponseTypeSub


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
        rootTag = 'statusCodeType'
        rootClass = supermod.statusCodeType
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
            namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"',
            pretty_print=True)
    return rootObj


def parseEtree(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'statusCodeType'
        rootClass = supermod.statusCodeType
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
        rootTag = 'statusCodeType'
        rootClass = supermod.statusCodeType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"')
    return rootObj


def parseLiteral(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'statusCodeType'
        rootClass = supermod.statusCodeType
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
