#!/usr/bin/env python

#
# Generated Sun Apr  4 14:57:24 2021 by generateDS.py version 2.38.5.
# Python 3.6.12 (default, Dec 15 2020, 16:33:02)  [GCC 5.5.0]
#
# Command line options:
#   ('-o', './src/concentrator/smev3_v321/service_types/lists_children_received_place.py')
#   ('-s', './src/concentrator/smev3_v321/service_types/lists_children_received_place_subs.py')
#
# Command line arguments:
#   /home/zkksch/Загрузки/lists_children_received_place.xsd
#
# Command line:
#   /home/zkksch/.virtualenvs/edukndg/bin/generateDS -o "./src/concentrator/smev3_v321/service_types/lists_children_received_place.py" -s "./src/concentrator/smev3_v321/service_types/lists_children_received_place_subs.py" /home/zkksch/Загрузки/lists_children_received_place.xsd
#
# Current working directory (os.getcwd()):
#   concentrator
#

import os
import sys
from lxml import etree as etree_

from . import lists_children_received_place as supermod

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


class AttachmentRequestTypeSub(supermod.AttachmentRequestType):
    def __init__(self, env=None, EduOrganizationCode=None, **kwargs_):
        super(AttachmentRequestTypeSub, self).__init__(env, EduOrganizationCode,  **kwargs_)
supermod.AttachmentRequestType.subclass = AttachmentRequestTypeSub
# end class AttachmentRequestTypeSub


class AttachmentResponseTypeSub(supermod.AttachmentResponseType):
    def __init__(self, code=None, message=None, **kwargs_):
        super(AttachmentResponseTypeSub, self).__init__(code, message,  **kwargs_)
supermod.AttachmentResponseType.subclass = AttachmentResponseTypeSub
# end class AttachmentResponseTypeSub


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
        rootTag = 'AttachmentRequestType'
        rootClass = supermod.AttachmentRequestType
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
            namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/lists_children_received_place/1.0.0"',
            pretty_print=True)
    return rootObj


def parseEtree(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'AttachmentRequestType'
        rootClass = supermod.AttachmentRequestType
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
        rootTag = 'AttachmentRequestType'
        rootClass = supermod.AttachmentRequestType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/lists_children_received_place/1.0.0"')
    return rootObj


def parseLiteral(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'AttachmentRequestType'
        rootClass = supermod.AttachmentRequestType
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
