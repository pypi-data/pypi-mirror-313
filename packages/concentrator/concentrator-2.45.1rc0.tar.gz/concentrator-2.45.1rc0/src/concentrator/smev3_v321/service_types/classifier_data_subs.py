#!/usr/bin/env python

#
# Generated Thu Jul 16 10:55:08 2020 by generateDS.py version 2.35.24.
# Python 3.6.10 (default, Apr  8 2020, 19:06:55)  [GCC 7.5.0]
#
# Command line options:
#   ('-o', 'classifier_data.py')
#   ('-s', 'classifier_data_subs.py')
#
# Command line arguments:
#   ./schema/data.xsd
#
# Command line:
#   /home/zkksch/.virtualenvs/edukndg/bin/generateDS -o "classifier_data.py" -s "classifier_data_subs.py" ./schema/data.xsd
#
# Current working directory (os.getcwd()):
#   esnsi_smev3
#

import os
import sys

from lxml import etree as etree_

import classifier_data as supermod


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


class ClassifierDataUpdateRequestSub(supermod.ClassifierDataUpdateRequest):
    def __init__(self, record=None, data=None, **kwargs_):
        super(ClassifierDataUpdateRequestSub, self).__init__(record, data,  **kwargs_)
supermod.ClassifierDataUpdateRequest.subclass = ClassifierDataUpdateRequestSub
# end class ClassifierDataUpdateRequestSub


class recordSub(supermod.record):
    def __init__(self, attribute_value=None, **kwargs_):
        super(recordSub, self).__init__(attribute_value,  **kwargs_)
supermod.record.subclass = recordSub
# end class recordSub


class attribute_valueSub(supermod.attribute_value):
    def __init__(self, attribute_name=None, attribute_ref=None, string=None, text=None, bool=None, date=None, integer=None, decimal=None, reference=None, code=None, string_key=None, date_key=None, integer_key=None, decimal_key=None, **kwargs_):
        super(attribute_valueSub, self).__init__(attribute_name, attribute_ref, string, text, bool, date, integer, decimal, reference, code, string_key, date_key, integer_key, decimal_key,  **kwargs_)
supermod.attribute_value.subclass = attribute_valueSub
# end class attribute_valueSub


class classifier_dataSub(supermod.classifier_data):
    def __init__(self, code=None, classifier_ref=None, record=None, **kwargs_):
        super(classifier_dataSub, self).__init__(code, classifier_ref, record,  **kwargs_)
supermod.classifier_data.subclass = classifier_dataSub
# end class classifier_dataSub


class ClassifierDataDeleteRequestSub(supermod.ClassifierDataDeleteRequest):
    def __init__(self, record=None, data=None, **kwargs_):
        super(ClassifierDataDeleteRequestSub, self).__init__(record, data,  **kwargs_)
supermod.ClassifierDataDeleteRequest.subclass = ClassifierDataDeleteRequestSub
# end class ClassifierDataDeleteRequestSub


class recordTypeSub(supermod.recordType):
    def __init__(self, record_key=None, string_key=None, date_key=None, integer_key=None, decimal_key=None, **kwargs_):
        super(recordTypeSub, self).__init__(record_key, string_key, date_key, integer_key, decimal_key,  **kwargs_)
supermod.recordType.subclass = recordTypeSub
# end class recordTypeSub


class dataTypeSub(supermod.dataType):
    def __init__(self, code=None, classifier_ref=None, record=None, **kwargs_):
        super(dataTypeSub, self).__init__(code, classifier_ref, record,  **kwargs_)
supermod.dataType.subclass = dataTypeSub
# end class dataTypeSub


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
        rootTag = 'ClassifierDataUpdateRequest'
        rootClass = supermod.ClassifierDataUpdateRequest
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
            namespacedef_='xmlns:tns="urn://x-artefacts-smev-gov-ru/esnsi/smev-integration/update/2.0.0"',
            pretty_print=True)
    return rootObj


def parseEtree(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'ClassifierDataUpdateRequest'
        rootClass = supermod.ClassifierDataUpdateRequest
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
        rootTag = 'ClassifierDataUpdateRequest'
        rootClass = supermod.ClassifierDataUpdateRequest
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:tns="urn://x-artefacts-smev-gov-ru/esnsi/smev-integration/update/2.0.0"')
    return rootObj


def parseLiteral(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'ClassifierDataUpdateRequest'
        rootClass = supermod.ClassifierDataUpdateRequest
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
