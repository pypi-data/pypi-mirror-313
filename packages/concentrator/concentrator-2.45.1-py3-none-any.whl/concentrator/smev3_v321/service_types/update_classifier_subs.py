#!/usr/bin/env python

#
# Generated Fri Jun 19 10:49:47 2020 by generateDS.py version 2.35.24.
# Python 3.6.10 (default, Apr  8 2020, 19:06:55)  [GCC 7.5.0]
#
# Command line options:
#   ('-o', 'update_classifier.py')
#   ('-s', 'update_classifier_subs.py')
#
# Command line arguments:
#   ./schema/update.xsd
#
# Command line:
#   /home/zkksch/.virtualenvs/edukndg/bin/generateDS -o "update_classifier.py" -s "update_classifier_subs.py" ./schema/update.xsd
#
# Current working directory (os.getcwd()):
#   esnsi_smev3
#

import os
import sys

from lxml import etree as etree_

import update_classifier as supermod


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


class CnsiRequestSub(supermod.CnsiRequest):
    def __init__(self, UpdateClassifierData=None, DeleteClassifierData=None, **kwargs_):
        super(CnsiRequestSub, self).__init__(UpdateClassifierData, DeleteClassifierData,  **kwargs_)
supermod.CnsiRequest.subclass = CnsiRequestSub
# end class CnsiRequestSub


class CnsiResponseSub(supermod.CnsiResponse):
    def __init__(self, UpdateClassifierData=None, DeleteClassifierData=None, **kwargs_):
        super(CnsiResponseSub, self).__init__(UpdateClassifierData, DeleteClassifierData,  **kwargs_)
supermod.CnsiResponse.subclass = CnsiResponseSub
# end class CnsiResponseSub


class UpdateClassifierDataRequestTypeSub(supermod.UpdateClassifierDataRequestType):
    def __init__(self, authorizationString=None, code=None, uid=None, removeMissing=None, **kwargs_):
        super(UpdateClassifierDataRequestTypeSub, self).__init__(authorizationString, code, uid, removeMissing,  **kwargs_)
supermod.UpdateClassifierDataRequestType.subclass = UpdateClassifierDataRequestTypeSub
# end class UpdateClassifierDataRequestTypeSub


class UpdateClassifierDataResponseTypeSub(supermod.UpdateClassifierDataResponseType):
    def __init__(self, ClassifierUpdateSuccessful=None, **kwargs_):
        super(UpdateClassifierDataResponseTypeSub, self).__init__(ClassifierUpdateSuccessful,  **kwargs_)
supermod.UpdateClassifierDataResponseType.subclass = UpdateClassifierDataResponseTypeSub
# end class UpdateClassifierDataResponseTypeSub


class DeleteClassifierDataRequestTypeSub(supermod.DeleteClassifierDataRequestType):
    def __init__(self, authorizationString=None, code=None, uid=None, **kwargs_):
        super(DeleteClassifierDataRequestTypeSub, self).__init__(authorizationString, code, uid,  **kwargs_)
supermod.DeleteClassifierDataRequestType.subclass = DeleteClassifierDataRequestTypeSub
# end class DeleteClassifierDataRequestTypeSub


class DeleteClassifierDataResponseTypeSub(supermod.DeleteClassifierDataResponseType):
    def __init__(self, ClassifierDeleteSuccessful=None, **kwargs_):
        super(DeleteClassifierDataResponseTypeSub, self).__init__(ClassifierDeleteSuccessful,  **kwargs_)
supermod.DeleteClassifierDataResponseType.subclass = DeleteClassifierDataResponseTypeSub
# end class DeleteClassifierDataResponseTypeSub


class ClassifierDetailsRequestTypeSub(supermod.ClassifierDetailsRequestType):
    def __init__(self, code=None, uid=None, **kwargs_):
        super(ClassifierDetailsRequestTypeSub, self).__init__(code, uid,  **kwargs_)
supermod.ClassifierDetailsRequestType.subclass = ClassifierDetailsRequestTypeSub
# end class ClassifierDetailsRequestTypeSub


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
        rootTag = 'CnsiRequest'
        rootClass = supermod.CnsiRequest
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
        rootTag = 'CnsiRequest'
        rootClass = supermod.CnsiRequest
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
        rootTag = 'CnsiRequest'
        rootClass = supermod.CnsiRequest
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
        rootTag = 'CnsiRequest'
        rootClass = supermod.CnsiRequest
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
