#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Tue Mar 16 14:26:53 2021 by generateDS.py version 2.36.2.
# Python 3.6.10 (default, Feb 25 2020, 11:09:54)  [GCC 7.4.0]
#
# Command line options:
#   ('-o', '/home/mark/PycharmProjects/concentrator/src/concentrator/smev3_v321/service_types/kinder_conc.py')
#   ('-s', '/home/mark/PycharmProjects/concentrator/src/concentrator/smev3_v321/service_types/kinder_conc_subs.py')
#
# Command line arguments:
#   concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd
#
# Command line:
#   /home/mark/PycharmProjects/concentrator/venv3.8/bin/generateDS -o "/home/mark/PycharmProjects/concentrator/src/concentrator/smev3_v321/service_types/kinder_conc.py" -s "/home/mark/PycharmProjects/concentrator/src/concentrator/smev3_v321/service_types/kinder_conc_subs.py" concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd
#
# Current working directory (os.getcwd()):
#   src
#

from six.moves import zip_longest
import os
import sys
import re as re_
import base64
import datetime as datetime_
import decimal as decimal_
try:
    from lxml import etree as etree_
except ImportError:
    from xml.etree import ElementTree as etree_


Validate_simpletypes_ = True
SaveElementTreeNode = True
if sys.version_info.major == 2:
    BaseStrType_ = basestring
else:
    BaseStrType_ = str


def parsexml_(infile, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        try:
            parser = etree_.ETCompatXMLParser()
        except AttributeError:
            # fallback to xml.etree
            parser = etree_.XMLParser()
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
# Namespace prefix definition table (and other attributes, too)
#
# The module generatedsnamespaces, if it is importable, must contain
# a dictionary named GeneratedsNamespaceDefs.  This Python dictionary
# should map element type names (strings) to XML schema namespace prefix
# definitions.  The export method for any class for which there is
# a namespace prefix definition, will export that definition in the
# XML representation of that element.  See the export method of
# any generated element type class for an example of the use of this
# table.
# A sample table is:
#
#     # File: generatedsnamespaces.py
#
#     GenerateDSNamespaceDefs = {
#         "ElementtypeA": "http://www.xxx.com/namespaceA",
#         "ElementtypeB": "http://www.xxx.com/namespaceB",
#     }
#
# Additionally, the generatedsnamespaces module can contain a python
# dictionary named GenerateDSNamespaceTypePrefixes that associates element
# types with the namespace prefixes that are to be added to the
# "xsi:type" attribute value.  See the exportAttributes method of
# any generated element type and the generation of "xsi:type" for an
# example of the use of this table.
# An example table:
#
#     # File: generatedsnamespaces.py
#
#     GenerateDSNamespaceTypePrefixes = {
#         "ElementtypeC": "aaa:",
#         "ElementtypeD": "bbb:",
#     }
#

try:
    from .kinder_conc_namespaces import GenerateDSNamespaceDefs as GenerateDSNamespaceDefs_
except ImportError:
    GenerateDSNamespaceDefs_ = {}
try:
    from .kinder_conc_namespaces import GenerateDSNamespaceTypePrefixes as GenerateDSNamespaceTypePrefixes_
except ImportError:
    GenerateDSNamespaceTypePrefixes_ = {}

#
# You can replace the following class definition by defining an
# importable module named "generatedscollector" containing a class
# named "GdsCollector".  See the default class definition below for
# clues about the possible content of that class.
#
try:
    from generatedscollector import GdsCollector as GdsCollector_
except ImportError:

    class GdsCollector_(object):

        def __init__(self, messages=None):
            if messages is None:
                self.messages = []
            else:
                self.messages = messages

        def add_message(self, msg):
            self.messages.append(msg)

        def get_messages(self):
            return self.messages

        def clear_messages(self):
            self.messages = []

        def print_messages(self):
            for msg in self.messages:
                print("Warning: {}".format(msg))

        def write_messages(self, outstream):
            for msg in self.messages:
                outstream.write("Warning: {}\n".format(msg))


#
# The super-class for enum types
#

try:
    from enum import Enum
except ImportError:
    Enum = object

#
# The root super-class for element type classes
#
# Calls to the methods in these classes are generated by generateDS.py.
# You can replace these methods by re-implementing the following class
#   in a module named generatedssuper.py.

try:
    from generatedssuper import GeneratedsSuper
except ImportError as exp:
    
    class GeneratedsSuper(object):
        __hash__ = object.__hash__
        tzoff_pattern = re_.compile(r'(\+|-)((0\d|1[0-3]):[0-5]\d|14:00)$')
        class _FixedOffsetTZ(datetime_.tzinfo):
            def __init__(self, offset, name):
                self.__offset = datetime_.timedelta(minutes=offset)
                self.__name = name
            def utcoffset(self, dt):
                return self.__offset
            def tzname(self, dt):
                return self.__name
            def dst(self, dt):
                return None
        def gds_format_string(self, input_data, input_name=''):
            return input_data
        def gds_parse_string(self, input_data, node=None, input_name=''):
            return input_data
        def gds_validate_string(self, input_data, node=None, input_name=''):
            if not input_data:
                return ''
            else:
                return input_data
        def gds_format_base64(self, input_data, input_name=''):
            return base64.b64encode(input_data)
        def gds_validate_base64(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_integer(self, input_data, input_name=''):
            return '%d' % input_data
        def gds_parse_integer(self, input_data, node=None, input_name=''):
            try:
                ival = int(input_data)
            except (TypeError, ValueError) as exp:
                raise_parse_error(node, 'Requires integer value: %s' % exp)
            return ival
        def gds_validate_integer(self, input_data, node=None, input_name=''):
            try:
                value = int(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires integer value')
            return value
        def gds_format_integer_list(self, input_data, input_name=''):
            return '%s' % ' '.join(input_data)
        def gds_validate_integer_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    int(value)
                except (TypeError, ValueError):
                    raise_parse_error(node, 'Requires sequence of integer valuess')
            return values
        def gds_format_float(self, input_data, input_name=''):
            return ('%.15f' % input_data).rstrip('0')
        def gds_parse_float(self, input_data, node=None, input_name=''):
            try:
                fval_ = float(input_data)
            except (TypeError, ValueError) as exp:
                raise_parse_error(node, 'Requires float or double value: %s' % exp)
            return fval_
        def gds_validate_float(self, input_data, node=None, input_name=''):
            try:
                value = float(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires float value')
            return value
        def gds_format_float_list(self, input_data, input_name=''):
            return '%s' % ' '.join(input_data)
        def gds_validate_float_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    float(value)
                except (TypeError, ValueError):
                    raise_parse_error(node, 'Requires sequence of float values')
            return values
        def gds_format_decimal(self, input_data, input_name=''):
            return_value = '%s' % input_data
            if '.' in return_value:
                return_value = return_value.rstrip('0')
                if return_value.endswith('.'):
                    return_value = return_value.rstrip('.')
            return return_value
        def gds_parse_decimal(self, input_data, node=None, input_name=''):
            try:
                decimal_value = decimal_.Decimal(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires decimal value')
            return decimal_value
        def gds_validate_decimal(self, input_data, node=None, input_name=''):
            try:
                value = decimal_.Decimal(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires decimal value')
            return value
        def gds_format_decimal_list(self, input_data, input_name=''):
            return ' '.join([self.gds_format_decimal(item) for item in input_data])
        def gds_validate_decimal_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    decimal_.Decimal(value)
                except (TypeError, ValueError):
                    raise_parse_error(node, 'Requires sequence of decimal values')
            return values
        def gds_format_double(self, input_data, input_name=''):
            return '%e' % input_data
        def gds_parse_double(self, input_data, node=None, input_name=''):
            try:
                fval_ = float(input_data)
            except (TypeError, ValueError) as exp:
                raise_parse_error(node, 'Requires double or float value: %s' % exp)
            return fval_
        def gds_validate_double(self, input_data, node=None, input_name=''):
            try:
                value = float(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires double or float value')
            return value
        def gds_format_double_list(self, input_data, input_name=''):
            return '%s' % ' '.join(input_data)
        def gds_validate_double_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    float(value)
                except (TypeError, ValueError):
                    raise_parse_error(
                        node, 'Requires sequence of double or float values')
            return values
        def gds_format_boolean(self, input_data, input_name=''):
            return ('%s' % input_data).lower()
        def gds_parse_boolean(self, input_data, node=None, input_name=''):
            if input_data in ('true', '1'):
                bval = True
            elif input_data in ('false', '0'):
                bval = False
            else:
                raise_parse_error(node, 'Requires boolean value')
            return bval
        def gds_validate_boolean(self, input_data, node=None, input_name=''):
            if input_data not in (True, 1, False, 0, ):
                raise_parse_error(
                    node,
                    'Requires boolean value '
                    '(one of True, 1, False, 0)')
            return input_data
        def gds_format_boolean_list(self, input_data, input_name=''):
            return '%s' % ' '.join(input_data)
        def gds_validate_boolean_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                if value not in (True, 1, False, 0, ):
                    raise_parse_error(
                        node,
                        'Requires sequence of boolean values '
                        '(one of True, 1, False, 0)')
            return values
        def gds_validate_datetime(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_datetime(self, input_data, input_name=''):
            if input_data.microsecond == 0:
                _svalue = '%04d-%02d-%02dT%02d:%02d:%02d' % (
                    input_data.year,
                    input_data.month,
                    input_data.day,
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                )
            else:
                _svalue = '%04d-%02d-%02dT%02d:%02d:%02d.%s' % (
                    input_data.year,
                    input_data.month,
                    input_data.day,
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                    ('%f' % (float(input_data.microsecond) / 1000000))[2:],
                )
            if input_data.tzinfo is not None:
                tzoff = input_data.tzinfo.utcoffset(input_data)
                if tzoff is not None:
                    total_seconds = tzoff.seconds + (86400 * tzoff.days)
                    if total_seconds == 0:
                        _svalue += 'Z'
                    else:
                        if total_seconds < 0:
                            _svalue += '-'
                            total_seconds *= -1
                        else:
                            _svalue += '+'
                        hours = total_seconds // 3600
                        minutes = (total_seconds - (hours * 3600)) // 60
                        _svalue += '{0:02d}:{1:02d}'.format(hours, minutes)
            return _svalue
        @classmethod
        def gds_parse_datetime(cls, input_data):
            tz = None
            if input_data[-1] == 'Z':
                tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
                input_data = input_data[:-1]
            else:
                results = GeneratedsSuper.tzoff_pattern.search(input_data)
                if results is not None:
                    tzoff_parts = results.group(2).split(':')
                    tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                    if results.group(1) == '-':
                        tzoff *= -1
                    tz = GeneratedsSuper._FixedOffsetTZ(
                        tzoff, results.group(0))
                    input_data = input_data[:-6]
            time_parts = input_data.split('.')
            if len(time_parts) > 1:
                micro_seconds = int(float('0.' + time_parts[1]) * 1000000)
                input_data = '%s.%s' % (
                    time_parts[0], "{}".format(micro_seconds).rjust(6, "0"), )
                dt = datetime_.datetime.strptime(
                    input_data, '%Y-%m-%dT%H:%M:%S.%f')
            else:
                dt = datetime_.datetime.strptime(
                    input_data, '%Y-%m-%dT%H:%M:%S')
            dt = dt.replace(tzinfo=tz)
            return dt
        def gds_validate_date(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_date(self, input_data, input_name=''):
            _svalue = '%04d-%02d-%02d' % (
                input_data.year,
                input_data.month,
                input_data.day,
            )
            try:
                if input_data.tzinfo is not None:
                    tzoff = input_data.tzinfo.utcoffset(input_data)
                    if tzoff is not None:
                        total_seconds = tzoff.seconds + (86400 * tzoff.days)
                        if total_seconds == 0:
                            _svalue += 'Z'
                        else:
                            if total_seconds < 0:
                                _svalue += '-'
                                total_seconds *= -1
                            else:
                                _svalue += '+'
                            hours = total_seconds // 3600
                            minutes = (total_seconds - (hours * 3600)) // 60
                            _svalue += '{0:02d}:{1:02d}'.format(
                                hours, minutes)
            except AttributeError:
                pass
            return _svalue
        @classmethod
        def gds_parse_date(cls, input_data):
            tz = None
            if input_data[-1] == 'Z':
                tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
                input_data = input_data[:-1]
            else:
                results = GeneratedsSuper.tzoff_pattern.search(input_data)
                if results is not None:
                    tzoff_parts = results.group(2).split(':')
                    tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                    if results.group(1) == '-':
                        tzoff *= -1
                    tz = GeneratedsSuper._FixedOffsetTZ(
                        tzoff, results.group(0))
                    input_data = input_data[:-6]
            dt = datetime_.datetime.strptime(input_data, '%Y-%m-%d')
            dt = dt.replace(tzinfo=tz)
            return dt.date()
        def gds_validate_time(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_time(self, input_data, input_name=''):
            if input_data.microsecond == 0:
                _svalue = '%02d:%02d:%02d' % (
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                )
            else:
                _svalue = '%02d:%02d:%02d.%s' % (
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                    ('%f' % (float(input_data.microsecond) / 1000000))[2:],
                )
            if input_data.tzinfo is not None:
                tzoff = input_data.tzinfo.utcoffset(input_data)
                if tzoff is not None:
                    total_seconds = tzoff.seconds + (86400 * tzoff.days)
                    if total_seconds == 0:
                        _svalue += 'Z'
                    else:
                        if total_seconds < 0:
                            _svalue += '-'
                            total_seconds *= -1
                        else:
                            _svalue += '+'
                        hours = total_seconds // 3600
                        minutes = (total_seconds - (hours * 3600)) // 60
                        _svalue += '{0:02d}:{1:02d}'.format(hours, minutes)
            return _svalue
        def gds_validate_simple_patterns(self, patterns, target):
            # pat is a list of lists of strings/patterns.
            # The target value must match at least one of the patterns
            # in order for the test to succeed.
            found1 = True
            for patterns1 in patterns:
                found2 = False
                for patterns2 in patterns1:
                    mo = re_.search(patterns2, target)
                    if mo is not None and len(mo.group(0)) == len(target):
                        found2 = True
                        break
                if not found2:
                    found1 = False
                    break
            return found1
        @classmethod
        def gds_parse_time(cls, input_data):
            tz = None
            if input_data[-1] == 'Z':
                tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
                input_data = input_data[:-1]
            else:
                results = GeneratedsSuper.tzoff_pattern.search(input_data)
                if results is not None:
                    tzoff_parts = results.group(2).split(':')
                    tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                    if results.group(1) == '-':
                        tzoff *= -1
                    tz = GeneratedsSuper._FixedOffsetTZ(
                        tzoff, results.group(0))
                    input_data = input_data[:-6]
            if len(input_data.split('.')) > 1:
                dt = datetime_.datetime.strptime(input_data, '%H:%M:%S.%f')
            else:
                dt = datetime_.datetime.strptime(input_data, '%H:%M:%S')
            dt = dt.replace(tzinfo=tz)
            return dt.time()
        def gds_check_cardinality_(
                self, value, input_name,
                min_occurs=0, max_occurs=1, required=None):
            if value is None:
                length = 0
            elif isinstance(value, list):
                length = len(value)
            else:
                length = 1
            if required is not None :
                if required and length < 1:
                    self.gds_collector_.add_message(
                        "Required value {}{} is missing".format(
                            input_name, self.gds_get_node_lineno_()))
            if length < min_occurs:
                self.gds_collector_.add_message(
                    "Number of values for {}{} is below "
                    "the minimum allowed, "
                    "expected at least {}, found {}".format(
                        input_name, self.gds_get_node_lineno_(),
                        min_occurs, length))
            elif length > max_occurs:
                self.gds_collector_.add_message(
                    "Number of values for {}{} is above "
                    "the maximum allowed, "
                    "expected at most {}, found {}".format(
                        input_name, self.gds_get_node_lineno_(),
                        max_occurs, length))
        def gds_validate_builtin_ST_(
                self, validator, value, input_name,
                min_occurs=None, max_occurs=None, required=None):
            if value is not None:
                try:
                    validator(value, input_name=input_name)
                except GDSParseError as parse_error:
                    self.gds_collector_.add_message(str(parse_error))
        def gds_validate_defined_ST_(
                self, validator, value, input_name,
                min_occurs=None, max_occurs=None, required=None):
            if value is not None:
                try:
                    validator(value)
                except GDSParseError as parse_error:
                    self.gds_collector_.add_message(str(parse_error))
        def gds_str_lower(self, instring):
            return instring.lower()
        def get_path_(self, node):
            path_list = []
            self.get_path_list_(node, path_list)
            path_list.reverse()
            path = '/'.join(path_list)
            return path
        Tag_strip_pattern_ = re_.compile(r'\{.*\}')
        def get_path_list_(self, node, path_list):
            if node is None:
                return
            tag = GeneratedsSuper.Tag_strip_pattern_.sub('', node.tag)
            if tag:
                path_list.append(tag)
            self.get_path_list_(node.getparent(), path_list)
        def get_class_obj_(self, node, default_class=None):
            class_obj1 = default_class
            if 'xsi' in node.nsmap:
                classname = node.get('{%s}type' % node.nsmap['xsi'])
                if classname is not None:
                    names = classname.split(':')
                    if len(names) == 2:
                        classname = names[1]
                    class_obj2 = globals().get(classname)
                    if class_obj2 is not None:
                        class_obj1 = class_obj2
            return class_obj1
        def gds_build_any(self, node, type_name=None):
            # provide default value in case option --disable-xml is used.
            content = ""
            content = etree_.tostring(node, encoding="unicode")
            return content
        @classmethod
        def gds_reverse_node_mapping(cls, mapping):
            return dict(((v, k) for k, v in mapping.items()))
        @staticmethod
        def gds_encode(instring):
            if sys.version_info.major == 2:
                if ExternalEncoding:
                    encoding = ExternalEncoding
                else:
                    encoding = 'utf-8'
                return instring.encode(encoding)
            else:
                return instring
        @staticmethod
        def convert_unicode(instring):
            if isinstance(instring, str):
                result = quote_xml(instring)
            elif sys.version_info.major == 2 and isinstance(instring, unicode):
                result = quote_xml(instring).encode('utf8')
            else:
                result = GeneratedsSuper.gds_encode(str(instring))
            return result
        def __eq__(self, other):
            def excl_select_objs_(obj):
                return (obj[0] != 'parent_object_' and
                        obj[0] != 'gds_collector_')
            if type(self) != type(other):
                return False
            return all(x == y for x, y in zip_longest(
                filter(excl_select_objs_, self.__dict__.items()),
                filter(excl_select_objs_, other.__dict__.items())))
        def __ne__(self, other):
            return not self.__eq__(other)
        # Django ETL transform hooks.
        def gds_djo_etl_transform(self):
            pass
        def gds_djo_etl_transform_db_obj(self, dbobj):
            pass
        # SQLAlchemy ETL transform hooks.
        def gds_sqa_etl_transform(self):
            return 0, None
        def gds_sqa_etl_transform_db_obj(self, dbobj):
            pass
        def gds_get_node_lineno_(self):
            if (hasattr(self, "gds_elementtree_node_") and
                    self.gds_elementtree_node_ is not None):
                return ' near line {}'.format(
                    self.gds_elementtree_node_.sourceline)
            else:
                return ""
    
    
    def getSubclassFromModule_(module, class_):
        '''Get the subclass of a class from a specific module.'''
        name = class_.__name__ + 'Sub'
        if hasattr(module, name):
            return getattr(module, name)
        else:
            return None


#
# If you have installed IPython you can uncomment and use the following.
# IPython is available from http://ipython.scipy.org/.
#

## from IPython.Shell import IPShellEmbed
## args = ''
## ipshell = IPShellEmbed(args,
##     banner = 'Dropping into IPython',
##     exit_msg = 'Leaving Interpreter, back to program.')

# Then use the following line where and when you want to drop into the
# IPython shell:
#    ipshell('<some message> -- Entering ipshell.\nHit Ctrl-D to exit')

#
# Globals
#

ExternalEncoding = ''
# Set this to false in order to deactivate during export, the use of
# name space prefixes captured from the input document.
UseCapturedNS_ = True
CapturedNsmap_ = {}
Tag_pattern_ = re_.compile(r'({.*})?(.*)')
String_cleanup_pat_ = re_.compile(r"[\n\r\s]+")
Namespace_extract_pat_ = re_.compile(r'{(.*)}(.*)')
CDATA_pattern_ = re_.compile(r"<!\[CDATA\[.*?\]\]>", re_.DOTALL)

# Change this to redirect the generated superclass module to use a
# specific subclass module.
CurrentSubclassModule_ = None

#
# Support/utility functions.
#


def showIndent(outfile, level, pretty_print=True):
    if pretty_print:
        for idx in range(level):
            outfile.write('    ')


def quote_xml(inStr):
    "Escape markup chars, but do not modify CDATA sections."
    if not inStr:
        return ''
    s1 = (isinstance(inStr, BaseStrType_) and inStr or '%s' % inStr)
    s2 = ''
    pos = 0
    matchobjects = CDATA_pattern_.finditer(s1)
    for mo in matchobjects:
        s3 = s1[pos:mo.start()]
        s2 += quote_xml_aux(s3)
        s2 += s1[mo.start():mo.end()]
        pos = mo.end()
    s3 = s1[pos:]
    s2 += quote_xml_aux(s3)
    return s2


def quote_xml_aux(inStr):
    s1 = inStr.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    return s1


def quote_attrib(inStr):
    s1 = (isinstance(inStr, BaseStrType_) and inStr or '%s' % inStr)
    s1 = s1.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    if '"' in s1:
        if "'" in s1:
            s1 = '"%s"' % s1.replace('"', "&quot;")
        else:
            s1 = "'%s'" % s1
    else:
        s1 = '"%s"' % s1
    return s1


def quote_python(inStr):
    s1 = inStr
    if s1.find("'") == -1:
        if s1.find('\n') == -1:
            return "'%s'" % s1
        else:
            return "'''%s'''" % s1
    else:
        if s1.find('"') != -1:
            s1 = s1.replace('"', '\\"')
        if s1.find('\n') == -1:
            return '"%s"' % s1
        else:
            return '"""%s"""' % s1


def get_all_text_(node):
    if node.text is not None:
        text = node.text
    else:
        text = ''
    for child in node:
        if child.tail is not None:
            text += child.tail
    return text


def find_attr_value_(attr_name, node):
    attrs = node.attrib
    attr_parts = attr_name.split(':')
    value = None
    if len(attr_parts) == 1:
        value = attrs.get(attr_name)
    elif len(attr_parts) == 2:
        prefix, name = attr_parts
        namespace = node.nsmap.get(prefix)
        if namespace is not None:
            value = attrs.get('{%s}%s' % (namespace, name, ))
    return value


def encode_str_2_3(instr):
    return instr


class GDSParseError(Exception):
    pass


def raise_parse_error(node, msg):
    if node is not None:
        msg = '%s (element %s/line %d)' % (msg, node.tag, node.sourceline, )
    raise GDSParseError(msg)


class MixedContainer:
    # Constants for category:
    CategoryNone = 0
    CategoryText = 1
    CategorySimple = 2
    CategoryComplex = 3
    # Constants for content_type:
    TypeNone = 0
    TypeText = 1
    TypeString = 2
    TypeInteger = 3
    TypeFloat = 4
    TypeDecimal = 5
    TypeDouble = 6
    TypeBoolean = 7
    TypeBase64 = 8
    def __init__(self, category, content_type, name, value):
        self.category = category
        self.content_type = content_type
        self.name = name
        self.value = value
    def getCategory(self):
        return self.category
    def getContenttype(self, content_type):
        return self.content_type
    def getValue(self):
        return self.value
    def getName(self):
        return self.name
    def export(self, outfile, level, name, namespace,
               pretty_print=True):
        if self.category == MixedContainer.CategoryText:
            # Prevent exporting empty content as empty lines.
            if self.value.strip():
                outfile.write(self.value)
        elif self.category == MixedContainer.CategorySimple:
            self.exportSimple(outfile, level, name)
        else:    # category == MixedContainer.CategoryComplex
            self.value.export(
                outfile, level, namespace, name_=name,
                pretty_print=pretty_print)
    def exportSimple(self, outfile, level, name):
        if self.content_type == MixedContainer.TypeString:
            outfile.write('<%s>%s</%s>' % (
                self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeInteger or \
                self.content_type == MixedContainer.TypeBoolean:
            outfile.write('<%s>%d</%s>' % (
                self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeFloat or \
                self.content_type == MixedContainer.TypeDecimal:
            outfile.write('<%s>%f</%s>' % (
                self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeDouble:
            outfile.write('<%s>%g</%s>' % (
                self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeBase64:
            outfile.write('<%s>%s</%s>' % (
                self.name,
                base64.b64encode(self.value),
                self.name))
    def to_etree(self, element, mapping_=None, nsmap_=None):
        if self.category == MixedContainer.CategoryText:
            # Prevent exporting empty content as empty lines.
            if self.value.strip():
                if len(element) > 0:
                    if element[-1].tail is None:
                        element[-1].tail = self.value
                    else:
                        element[-1].tail += self.value
                else:
                    if element.text is None:
                        element.text = self.value
                    else:
                        element.text += self.value
        elif self.category == MixedContainer.CategorySimple:
            subelement = etree_.SubElement(
                element, '%s' % self.name)
            subelement.text = self.to_etree_simple()
        else:    # category == MixedContainer.CategoryComplex
            self.value.to_etree(element)
    def to_etree_simple(self, mapping_=None, nsmap_=None):
        if self.content_type == MixedContainer.TypeString:
            text = self.value
        elif (self.content_type == MixedContainer.TypeInteger or
                self.content_type == MixedContainer.TypeBoolean):
            text = '%d' % self.value
        elif (self.content_type == MixedContainer.TypeFloat or
                self.content_type == MixedContainer.TypeDecimal):
            text = '%f' % self.value
        elif self.content_type == MixedContainer.TypeDouble:
            text = '%g' % self.value
        elif self.content_type == MixedContainer.TypeBase64:
            text = '%s' % base64.b64encode(self.value)
        return text
    def exportLiteral(self, outfile, level, name):
        if self.category == MixedContainer.CategoryText:
            showIndent(outfile, level)
            outfile.write(
                'model_.MixedContainer(%d, %d, "%s", "%s"),\n' % (
                    self.category, self.content_type,
                    self.name, self.value))
        elif self.category == MixedContainer.CategorySimple:
            showIndent(outfile, level)
            outfile.write(
                'model_.MixedContainer(%d, %d, "%s", "%s"),\n' % (
                    self.category, self.content_type,
                    self.name, self.value))
        else:    # category == MixedContainer.CategoryComplex
            showIndent(outfile, level)
            outfile.write(
                'model_.MixedContainer(%d, %d, "%s",\n' % (
                    self.category, self.content_type, self.name,))
            self.value.exportLiteral(outfile, level + 1)
            showIndent(outfile, level)
            outfile.write(')\n')


class MemberSpec_(object):
    def __init__(self, name='', data_type='', container=0,
            optional=0, child_attrs=None, choice=None):
        self.name = name
        self.data_type = data_type
        self.container = container
        self.child_attrs = child_attrs
        self.choice = choice
        self.optional = optional
    def set_name(self, name): self.name = name
    def get_name(self): return self.name
    def set_data_type(self, data_type): self.data_type = data_type
    def get_data_type_chain(self): return self.data_type
    def get_data_type(self):
        if isinstance(self.data_type, list):
            if len(self.data_type) > 0:
                return self.data_type[-1]
            else:
                return 'xs:string'
        else:
            return self.data_type
    def set_container(self, container): self.container = container
    def get_container(self): return self.container
    def set_child_attrs(self, child_attrs): self.child_attrs = child_attrs
    def get_child_attrs(self): return self.child_attrs
    def set_choice(self, choice): self.choice = choice
    def get_choice(self): return self.choice
    def set_optional(self, optional): self.optional = optional
    def get_optional(self): return self.optional


def _cast(typ, value):
    if typ is None or value is None:
        return value
    return typ(value)

#
# Data representation classes.
#


class CancelResultType(str, Enum):
    """Результат передачи запроса на отмену заявления"""
    CANCELLED='CANCELLED'
    IN_PROGRESS='IN_PROGRESS'
    REJECTED='REJECTED'


class DataElementType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, code=None, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.code = _cast(None, code)
        self.code_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_code')
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DataElementType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DataElementType.subclass:
            return DataElementType.subclass(*args_, **kwargs_)
        else:
            return DataElementType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_code(self):
        return self.code
    def set_code(self, code):
        self.code = code
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def validate_string_50(self, value):
        # Validate type tns:string-50, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-50' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
    def hasContent_(self):
        if (
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_)
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='DataElementType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DataElementType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DataElementType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DataElementType')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.convert_unicode(self.valueOf_))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DataElementType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DataElementType'):
        if self.code is not None and 'code' not in already_processed:
            already_processed.add('code')
            outfile.write(' code=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.code), input_name='code')), ))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='DataElementType', fromsubclass_=False, pretty_print=True):
        pass
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('code', node)
        if value is not None and 'code' not in already_processed:
            already_processed.add('code')
            self.code = value
            self.validate_string_50(self.code)    # validate type string-50
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class DataElementType


class AddressType(GeneratedsSuper):
    """Адрес"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, FullAddress=None, Index=None, Region=None, Area=None, City=None, CityArea=None, Place=None, Street=None, AdditionalArea=None, AdditionalStreet=None, House=None, Building1=None, Building2=None, Apartment=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.FullAddress = FullAddress
        self.validate_string_1024(self.FullAddress)
        self.FullAddress_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_FullAddress')
        self.Index = Index
        self.validate_string_6(self.Index)
        self.Index_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_Index')
        self.Region = Region
        self.Region_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_Region')
        self.Area = Area
        self.Area_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_Area')
        self.City = City
        self.City_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_City')
        self.CityArea = CityArea
        self.CityArea_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_CityArea')
        self.Place = Place
        self.Place_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_Place')
        self.Street = Street
        self.Street_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_Street')
        self.AdditionalArea = AdditionalArea
        self.AdditionalArea_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_AdditionalArea')
        self.AdditionalStreet = AdditionalStreet
        self.AdditionalStreet_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_AdditionalStreet')
        self.House = House
        self.House_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_House')
        self.Building1 = Building1
        self.validate_string_50(self.Building1)
        self.Building1_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_Building1')
        self.Building2 = Building2
        self.validate_string_50(self.Building2)
        self.Building2_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_Building2')
        self.Apartment = Apartment
        self.validate_string_50(self.Apartment)
        self.Apartment_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_Apartment')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AddressType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AddressType.subclass:
            return AddressType.subclass(*args_, **kwargs_)
        else:
            return AddressType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_FullAddress(self):
        return self.FullAddress
    def set_FullAddress(self, FullAddress):
        self.FullAddress = FullAddress
    def get_Index(self):
        return self.Index
    def set_Index(self, Index):
        self.Index = Index
    def get_Region(self):
        return self.Region
    def set_Region(self, Region):
        self.Region = Region
    def get_Area(self):
        return self.Area
    def set_Area(self, Area):
        self.Area = Area
    def get_City(self):
        return self.City
    def set_City(self, City):
        self.City = City
    def get_CityArea(self):
        return self.CityArea
    def set_CityArea(self, CityArea):
        self.CityArea = CityArea
    def get_Place(self):
        return self.Place
    def set_Place(self, Place):
        self.Place = Place
    def get_Street(self):
        return self.Street
    def set_Street(self, Street):
        self.Street = Street
    def get_AdditionalArea(self):
        return self.AdditionalArea
    def set_AdditionalArea(self, AdditionalArea):
        self.AdditionalArea = AdditionalArea
    def get_AdditionalStreet(self):
        return self.AdditionalStreet
    def set_AdditionalStreet(self, AdditionalStreet):
        self.AdditionalStreet = AdditionalStreet
    def get_House(self):
        return self.House
    def set_House(self, House):
        self.House = House
    def get_Building1(self):
        return self.Building1
    def set_Building1(self, Building1):
        self.Building1 = Building1
    def get_Building2(self):
        return self.Building2
    def set_Building2(self, Building2):
        self.Building2 = Building2
    def get_Apartment(self):
        return self.Apartment
    def set_Apartment(self, Apartment):
        self.Apartment = Apartment
    def validate_string_1024(self, value):
        result = True
        # Validate type string-1024, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 1024:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-1024' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_string_6(self, value):
        result = True
        # Validate type string-6, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 6:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-6' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_string_50(self, value):
        result = True
        # Validate type string-50, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-50' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.FullAddress is not None or
            self.Index is not None or
            self.Region is not None or
            self.Area is not None or
            self.City is not None or
            self.CityArea is not None or
            self.Place is not None or
            self.Street is not None or
            self.AdditionalArea is not None or
            self.AdditionalStreet is not None or
            self.House is not None or
            self.Building1 is not None or
            self.Building2 is not None or
            self.Apartment is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='AddressType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AddressType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AddressType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AddressType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AddressType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AddressType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='AddressType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.FullAddress is not None:
            namespaceprefix_ = self.FullAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.FullAddress_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFullAddress>%s</%sFullAddress>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FullAddress), input_name='FullAddress')), namespaceprefix_ , eol_))
        if self.Index is not None:
            namespaceprefix_ = self.Index_nsprefix_ + ':' if (UseCapturedNS_ and self.Index_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIndex>%s</%sIndex>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Index), input_name='Index')), namespaceprefix_ , eol_))
        if self.Region is not None:
            namespaceprefix_ = self.Region_nsprefix_ + ':' if (UseCapturedNS_ and self.Region_nsprefix_) else ''
            self.Region.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Region', pretty_print=pretty_print)
        if self.Area is not None:
            namespaceprefix_ = self.Area_nsprefix_ + ':' if (UseCapturedNS_ and self.Area_nsprefix_) else ''
            self.Area.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Area', pretty_print=pretty_print)
        if self.City is not None:
            namespaceprefix_ = self.City_nsprefix_ + ':' if (UseCapturedNS_ and self.City_nsprefix_) else ''
            self.City.export(outfile, level, namespaceprefix_, namespacedef_='', name_='City', pretty_print=pretty_print)
        if self.CityArea is not None:
            namespaceprefix_ = self.CityArea_nsprefix_ + ':' if (UseCapturedNS_ and self.CityArea_nsprefix_) else ''
            self.CityArea.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CityArea', pretty_print=pretty_print)
        if self.Place is not None:
            namespaceprefix_ = self.Place_nsprefix_ + ':' if (UseCapturedNS_ and self.Place_nsprefix_) else ''
            self.Place.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Place', pretty_print=pretty_print)
        if self.Street is not None:
            namespaceprefix_ = self.Street_nsprefix_ + ':' if (UseCapturedNS_ and self.Street_nsprefix_) else ''
            self.Street.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Street', pretty_print=pretty_print)
        if self.AdditionalArea is not None:
            namespaceprefix_ = self.AdditionalArea_nsprefix_ + ':' if (UseCapturedNS_ and self.AdditionalArea_nsprefix_) else ''
            self.AdditionalArea.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AdditionalArea', pretty_print=pretty_print)
        if self.AdditionalStreet is not None:
            namespaceprefix_ = self.AdditionalStreet_nsprefix_ + ':' if (UseCapturedNS_ and self.AdditionalStreet_nsprefix_) else ''
            self.AdditionalStreet.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AdditionalStreet', pretty_print=pretty_print)
        if self.House is not None:
            namespaceprefix_ = self.House_nsprefix_ + ':' if (UseCapturedNS_ and self.House_nsprefix_) else ''
            self.House.export(outfile, level, namespaceprefix_, namespacedef_='', name_='House', pretty_print=pretty_print)
        if self.Building1 is not None:
            namespaceprefix_ = self.Building1_nsprefix_ + ':' if (UseCapturedNS_ and self.Building1_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBuilding1>%s</%sBuilding1>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Building1), input_name='Building1')), namespaceprefix_ , eol_))
        if self.Building2 is not None:
            namespaceprefix_ = self.Building2_nsprefix_ + ':' if (UseCapturedNS_ and self.Building2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBuilding2>%s</%sBuilding2>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Building2), input_name='Building2')), namespaceprefix_ , eol_))
        if self.Apartment is not None:
            namespaceprefix_ = self.Apartment_nsprefix_ + ':' if (UseCapturedNS_ and self.Apartment_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sApartment>%s</%sApartment>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Apartment), input_name='Apartment')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'FullAddress':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FullAddress')
            value_ = self.gds_validate_string(value_, node, 'FullAddress')
            self.FullAddress = value_
            self.FullAddress_nsprefix_ = child_.prefix
            # validate type string-1024
            self.validate_string_1024(self.FullAddress)
        elif nodeName_ == 'Index':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Index')
            value_ = self.gds_validate_string(value_, node, 'Index')
            self.Index = value_
            self.Index_nsprefix_ = child_.prefix
            # validate type string-6
            self.validate_string_6(self.Index)
        elif nodeName_ == 'Region':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Region = obj_
            obj_.original_tagname_ = 'Region'
        elif nodeName_ == 'Area':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Area = obj_
            obj_.original_tagname_ = 'Area'
        elif nodeName_ == 'City':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.City = obj_
            obj_.original_tagname_ = 'City'
        elif nodeName_ == 'CityArea':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CityArea = obj_
            obj_.original_tagname_ = 'CityArea'
        elif nodeName_ == 'Place':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Place = obj_
            obj_.original_tagname_ = 'Place'
        elif nodeName_ == 'Street':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Street = obj_
            obj_.original_tagname_ = 'Street'
        elif nodeName_ == 'AdditionalArea':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AdditionalArea = obj_
            obj_.original_tagname_ = 'AdditionalArea'
        elif nodeName_ == 'AdditionalStreet':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AdditionalStreet = obj_
            obj_.original_tagname_ = 'AdditionalStreet'
        elif nodeName_ == 'House':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.House = obj_
            obj_.original_tagname_ = 'House'
        elif nodeName_ == 'Building1':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Building1')
            value_ = self.gds_validate_string(value_, node, 'Building1')
            self.Building1 = value_
            self.Building1_nsprefix_ = child_.prefix
            # validate type string-50
            self.validate_string_50(self.Building1)
        elif nodeName_ == 'Building2':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Building2')
            value_ = self.gds_validate_string(value_, node, 'Building2')
            self.Building2 = value_
            self.Building2_nsprefix_ = child_.prefix
            # validate type string-50
            self.validate_string_50(self.Building2)
        elif nodeName_ == 'Apartment':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Apartment')
            value_ = self.gds_validate_string(value_, node, 'Apartment')
            self.Apartment = value_
            self.Apartment_nsprefix_ = child_.prefix
            # validate type string-50
            self.validate_string_50(self.Apartment)
# end class AddressType


class AppliedDocumentType(GeneratedsSuper):
    """Описание прилагаемого документа"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CodeDocument=None, NameDocument=None, TypeDocument=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.CodeDocument = CodeDocument
        self.validate_string_50(self.CodeDocument)
        self.CodeDocument_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_CodeDocument')
        self.NameDocument = NameDocument
        self.validate_string_50(self.NameDocument)
        self.NameDocument_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_NameDocument')
        self.TypeDocument = TypeDocument
        self.validate_string_50(self.TypeDocument)
        self.TypeDocument_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_TypeDocument')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AppliedDocumentType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AppliedDocumentType.subclass:
            return AppliedDocumentType.subclass(*args_, **kwargs_)
        else:
            return AppliedDocumentType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CodeDocument(self):
        return self.CodeDocument
    def set_CodeDocument(self, CodeDocument):
        self.CodeDocument = CodeDocument
    def get_NameDocument(self):
        return self.NameDocument
    def set_NameDocument(self, NameDocument):
        self.NameDocument = NameDocument
    def get_TypeDocument(self):
        return self.TypeDocument
    def set_TypeDocument(self, TypeDocument):
        self.TypeDocument = TypeDocument
    def validate_string_50(self, value):
        result = True
        # Validate type string-50, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-50' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.CodeDocument is not None or
            self.NameDocument is not None or
            self.TypeDocument is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='AppliedDocumentType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AppliedDocumentType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AppliedDocumentType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AppliedDocumentType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AppliedDocumentType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AppliedDocumentType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='AppliedDocumentType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CodeDocument is not None:
            namespaceprefix_ = self.CodeDocument_nsprefix_ + ':' if (UseCapturedNS_ and self.CodeDocument_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCodeDocument>%s</%sCodeDocument>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CodeDocument), input_name='CodeDocument')), namespaceprefix_ , eol_))
        if self.NameDocument is not None:
            namespaceprefix_ = self.NameDocument_nsprefix_ + ':' if (UseCapturedNS_ and self.NameDocument_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNameDocument>%s</%sNameDocument>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.NameDocument), input_name='NameDocument')), namespaceprefix_ , eol_))
        if self.TypeDocument is not None:
            namespaceprefix_ = self.TypeDocument_nsprefix_ + ':' if (UseCapturedNS_ and self.TypeDocument_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTypeDocument>%s</%sTypeDocument>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TypeDocument), input_name='TypeDocument')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'CodeDocument':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CodeDocument')
            value_ = self.gds_validate_string(value_, node, 'CodeDocument')
            self.CodeDocument = value_
            self.CodeDocument_nsprefix_ = child_.prefix
            # validate type string-50
            self.validate_string_50(self.CodeDocument)
        elif nodeName_ == 'NameDocument':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'NameDocument')
            value_ = self.gds_validate_string(value_, node, 'NameDocument')
            self.NameDocument = value_
            self.NameDocument_nsprefix_ = child_.prefix
            # validate type string-50
            self.validate_string_50(self.NameDocument)
        elif nodeName_ == 'TypeDocument':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TypeDocument')
            value_ = self.gds_validate_string(value_, node, 'TypeDocument')
            self.TypeDocument = value_
            self.TypeDocument_nsprefix_ = child_.prefix
            # validate type string-50
            self.validate_string_50(self.TypeDocument)
# end class AppliedDocumentType


class DocInfoType(GeneratedsSuper):
    """Описание документа"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DocIssueDate=None, DocIssued=None, DocExpirationDate=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        if isinstance(DocIssueDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(DocIssueDate, '%Y-%m-%d').date()
        else:
            initvalue_ = DocIssueDate
        self.DocIssueDate = initvalue_
        self.DocIssueDate_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_DocIssueDate')
        self.DocIssued = DocIssued
        self.validate_string_256(self.DocIssued)
        self.DocIssued_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_DocIssued')
        if isinstance(DocExpirationDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(DocExpirationDate, '%Y-%m-%d').date()
        else:
            initvalue_ = DocExpirationDate
        self.DocExpirationDate = initvalue_
        self.DocExpirationDate_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_DocExpirationDate')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DocInfoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DocInfoType.subclass:
            return DocInfoType.subclass(*args_, **kwargs_)
        else:
            return DocInfoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DocIssueDate(self):
        return self.DocIssueDate
    def set_DocIssueDate(self, DocIssueDate):
        self.DocIssueDate = DocIssueDate
    def get_DocIssued(self):
        return self.DocIssued
    def set_DocIssued(self, DocIssued):
        self.DocIssued = DocIssued
    def get_DocExpirationDate(self):
        return self.DocExpirationDate
    def set_DocExpirationDate(self, DocExpirationDate):
        self.DocExpirationDate = DocExpirationDate
    def validate_string_256(self, value):
        result = True
        # Validate type string-256, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 256:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-256' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.DocIssueDate is not None or
            self.DocIssued is not None or
            self.DocExpirationDate is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='DocInfoType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DocInfoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DocInfoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DocInfoType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DocInfoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DocInfoType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='DocInfoType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.DocIssueDate is not None:
            namespaceprefix_ = self.DocIssueDate_nsprefix_ + ':' if (UseCapturedNS_ and self.DocIssueDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDocIssueDate>%s</%sDocIssueDate>%s' % (namespaceprefix_ , self.gds_format_date(self.DocIssueDate, input_name='DocIssueDate'), namespaceprefix_ , eol_))
        if self.DocIssued is not None:
            namespaceprefix_ = self.DocIssued_nsprefix_ + ':' if (UseCapturedNS_ and self.DocIssued_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDocIssued>%s</%sDocIssued>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DocIssued), input_name='DocIssued')), namespaceprefix_ , eol_))
        if self.DocExpirationDate is not None:
            namespaceprefix_ = self.DocExpirationDate_nsprefix_ + ':' if (UseCapturedNS_ and self.DocExpirationDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDocExpirationDate>%s</%sDocExpirationDate>%s' % (namespaceprefix_ , self.gds_format_date(self.DocExpirationDate, input_name='DocExpirationDate'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'DocIssueDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.DocIssueDate = dval_
            self.DocIssueDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'DocIssued':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DocIssued')
            value_ = self.gds_validate_string(value_, node, 'DocIssued')
            self.DocIssued = value_
            self.DocIssued_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.DocIssued)
        elif nodeName_ == 'DocExpirationDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.DocExpirationDate = dval_
            self.DocExpirationDate_nsprefix_ = child_.prefix
# end class DocInfoType


class PersonInfoType(GeneratedsSuper):
    """Сведения о заявителе"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, PersonSurname=None, PersonName=None, PersonMiddleName=None, PersonPhone=None, PersonEmail=None, Parents=None, OtherRepresentative=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.PersonSurname = PersonSurname
        self.validate_string_256(self.PersonSurname)
        self.PersonSurname_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_PersonSurname')
        self.PersonName = PersonName
        self.validate_string_256(self.PersonName)
        self.PersonName_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_PersonName')
        self.PersonMiddleName = PersonMiddleName
        self.validate_string_256(self.PersonMiddleName)
        self.PersonMiddleName_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_PersonMiddleName')
        self.PersonPhone = PersonPhone
        self.validate_string_14(self.PersonPhone)
        self.PersonPhone_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_PersonPhone')
        self.PersonEmail = PersonEmail
        self.validate_string_256(self.PersonEmail)
        self.PersonEmail_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_PersonEmail')
        self.Parents = Parents
        self.Parents_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_Parents')
        self.OtherRepresentative = OtherRepresentative
        self.OtherRepresentative_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_OtherRepresentative')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PersonInfoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PersonInfoType.subclass:
            return PersonInfoType.subclass(*args_, **kwargs_)
        else:
            return PersonInfoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_PersonSurname(self):
        return self.PersonSurname
    def set_PersonSurname(self, PersonSurname):
        self.PersonSurname = PersonSurname
    def get_PersonName(self):
        return self.PersonName
    def set_PersonName(self, PersonName):
        self.PersonName = PersonName
    def get_PersonMiddleName(self):
        return self.PersonMiddleName
    def set_PersonMiddleName(self, PersonMiddleName):
        self.PersonMiddleName = PersonMiddleName
    def get_PersonPhone(self):
        return self.PersonPhone
    def set_PersonPhone(self, PersonPhone):
        self.PersonPhone = PersonPhone
    def get_PersonEmail(self):
        return self.PersonEmail
    def set_PersonEmail(self, PersonEmail):
        self.PersonEmail = PersonEmail
    def get_Parents(self):
        return self.Parents
    def set_Parents(self, Parents):
        self.Parents = Parents
    def get_OtherRepresentative(self):
        return self.OtherRepresentative
    def set_OtherRepresentative(self, OtherRepresentative):
        self.OtherRepresentative = OtherRepresentative
    def validate_string_256(self, value):
        result = True
        # Validate type string-256, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 256:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-256' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_string_14(self, value):
        result = True
        # Validate type string-14, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 14:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-14' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.PersonSurname is not None or
            self.PersonName is not None or
            self.PersonMiddleName is not None or
            self.PersonPhone is not None or
            self.PersonEmail is not None or
            self.Parents is not None or
            self.OtherRepresentative is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='PersonInfoType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PersonInfoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PersonInfoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PersonInfoType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PersonInfoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PersonInfoType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='PersonInfoType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.PersonSurname is not None:
            namespaceprefix_ = self.PersonSurname_nsprefix_ + ':' if (UseCapturedNS_ and self.PersonSurname_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPersonSurname>%s</%sPersonSurname>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PersonSurname), input_name='PersonSurname')), namespaceprefix_ , eol_))
        if self.PersonName is not None:
            namespaceprefix_ = self.PersonName_nsprefix_ + ':' if (UseCapturedNS_ and self.PersonName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPersonName>%s</%sPersonName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PersonName), input_name='PersonName')), namespaceprefix_ , eol_))
        if self.PersonMiddleName is not None:
            namespaceprefix_ = self.PersonMiddleName_nsprefix_ + ':' if (UseCapturedNS_ and self.PersonMiddleName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPersonMiddleName>%s</%sPersonMiddleName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PersonMiddleName), input_name='PersonMiddleName')), namespaceprefix_ , eol_))
        if self.PersonPhone is not None:
            namespaceprefix_ = self.PersonPhone_nsprefix_ + ':' if (UseCapturedNS_ and self.PersonPhone_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPersonPhone>%s</%sPersonPhone>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PersonPhone), input_name='PersonPhone')), namespaceprefix_ , eol_))
        if self.PersonEmail is not None:
            namespaceprefix_ = self.PersonEmail_nsprefix_ + ':' if (UseCapturedNS_ and self.PersonEmail_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPersonEmail>%s</%sPersonEmail>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PersonEmail), input_name='PersonEmail')), namespaceprefix_ , eol_))
        if self.Parents is not None:
            namespaceprefix_ = self.Parents_nsprefix_ + ':' if (UseCapturedNS_ and self.Parents_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sParents>%s</%sParents>%s' % (namespaceprefix_ , self.gds_format_boolean(self.Parents, input_name='Parents'), namespaceprefix_ , eol_))
        if self.OtherRepresentative is not None:
            namespaceprefix_ = self.OtherRepresentative_nsprefix_ + ':' if (UseCapturedNS_ and self.OtherRepresentative_nsprefix_) else ''
            self.OtherRepresentative.export(outfile, level, namespaceprefix_, namespacedef_='', name_='OtherRepresentative', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'PersonSurname':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PersonSurname')
            value_ = self.gds_validate_string(value_, node, 'PersonSurname')
            self.PersonSurname = value_
            self.PersonSurname_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.PersonSurname)
        elif nodeName_ == 'PersonName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PersonName')
            value_ = self.gds_validate_string(value_, node, 'PersonName')
            self.PersonName = value_
            self.PersonName_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.PersonName)
        elif nodeName_ == 'PersonMiddleName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PersonMiddleName')
            value_ = self.gds_validate_string(value_, node, 'PersonMiddleName')
            self.PersonMiddleName = value_
            self.PersonMiddleName_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.PersonMiddleName)
        elif nodeName_ == 'PersonPhone':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PersonPhone')
            value_ = self.gds_validate_string(value_, node, 'PersonPhone')
            self.PersonPhone = value_
            self.PersonPhone_nsprefix_ = child_.prefix
            # validate type string-14
            self.validate_string_14(self.PersonPhone)
        elif nodeName_ == 'PersonEmail':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PersonEmail')
            value_ = self.gds_validate_string(value_, node, 'PersonEmail')
            self.PersonEmail = value_
            self.PersonEmail_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.PersonEmail)
        elif nodeName_ == 'Parents':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'Parents')
            ival_ = self.gds_validate_boolean(ival_, node, 'Parents')
            self.Parents = ival_
            self.Parents_nsprefix_ = child_.prefix
        elif nodeName_ == 'OtherRepresentative':
            obj_ = OtherRepresentativeType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.OtherRepresentative = obj_
            obj_.original_tagname_ = 'OtherRepresentative'
# end class PersonInfoType


class OtherRepresentativeType(GeneratedsSuper):
    """Сведения о документе, подтверждающем полномочия заявителя"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, OtherRepresentativeDocName=None, OtherRepresentativeDocSeries=None, OtherRepresentativeDocNumber=None, OtherRepresentativeDocDate=None, OtherRepresentativeDocIssued=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.OtherRepresentativeDocName = OtherRepresentativeDocName
        self.validate_string_256(self.OtherRepresentativeDocName)
        self.OtherRepresentativeDocName_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_OtherRepresentativeDocName')
        self.OtherRepresentativeDocSeries = OtherRepresentativeDocSeries
        self.validate_string_10(self.OtherRepresentativeDocSeries)
        self.OtherRepresentativeDocSeries_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_OtherRepresentativeDocSeries')
        self.OtherRepresentativeDocNumber = OtherRepresentativeDocNumber
        self.validate_string_10(self.OtherRepresentativeDocNumber)
        self.OtherRepresentativeDocNumber_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_OtherRepresentativeDocNumber')
        if isinstance(OtherRepresentativeDocDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(OtherRepresentativeDocDate, '%Y-%m-%d').date()
        else:
            initvalue_ = OtherRepresentativeDocDate
        self.OtherRepresentativeDocDate = initvalue_
        self.OtherRepresentativeDocDate_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_OtherRepresentativeDocDate')
        self.OtherRepresentativeDocIssued = OtherRepresentativeDocIssued
        self.validate_string_256(self.OtherRepresentativeDocIssued)
        self.OtherRepresentativeDocIssued_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_OtherRepresentativeDocIssued')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, OtherRepresentativeType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if OtherRepresentativeType.subclass:
            return OtherRepresentativeType.subclass(*args_, **kwargs_)
        else:
            return OtherRepresentativeType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_OtherRepresentativeDocName(self):
        return self.OtherRepresentativeDocName
    def set_OtherRepresentativeDocName(self, OtherRepresentativeDocName):
        self.OtherRepresentativeDocName = OtherRepresentativeDocName
    def get_OtherRepresentativeDocSeries(self):
        return self.OtherRepresentativeDocSeries
    def set_OtherRepresentativeDocSeries(self, OtherRepresentativeDocSeries):
        self.OtherRepresentativeDocSeries = OtherRepresentativeDocSeries
    def get_OtherRepresentativeDocNumber(self):
        return self.OtherRepresentativeDocNumber
    def set_OtherRepresentativeDocNumber(self, OtherRepresentativeDocNumber):
        self.OtherRepresentativeDocNumber = OtherRepresentativeDocNumber
    def get_OtherRepresentativeDocDate(self):
        return self.OtherRepresentativeDocDate
    def set_OtherRepresentativeDocDate(self, OtherRepresentativeDocDate):
        self.OtherRepresentativeDocDate = OtherRepresentativeDocDate
    def get_OtherRepresentativeDocIssued(self):
        return self.OtherRepresentativeDocIssued
    def set_OtherRepresentativeDocIssued(self, OtherRepresentativeDocIssued):
        self.OtherRepresentativeDocIssued = OtherRepresentativeDocIssued
    def validate_string_256(self, value):
        result = True
        # Validate type string-256, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 256:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-256' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_string_10(self, value):
        result = True
        # Validate type string-10, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-10' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.OtherRepresentativeDocName is not None or
            self.OtherRepresentativeDocSeries is not None or
            self.OtherRepresentativeDocNumber is not None or
            self.OtherRepresentativeDocDate is not None or
            self.OtherRepresentativeDocIssued is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='OtherRepresentativeType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('OtherRepresentativeType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'OtherRepresentativeType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='OtherRepresentativeType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='OtherRepresentativeType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='OtherRepresentativeType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='OtherRepresentativeType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.OtherRepresentativeDocName is not None:
            namespaceprefix_ = self.OtherRepresentativeDocName_nsprefix_ + ':' if (UseCapturedNS_ and self.OtherRepresentativeDocName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOtherRepresentativeDocName>%s</%sOtherRepresentativeDocName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.OtherRepresentativeDocName), input_name='OtherRepresentativeDocName')), namespaceprefix_ , eol_))
        if self.OtherRepresentativeDocSeries is not None:
            namespaceprefix_ = self.OtherRepresentativeDocSeries_nsprefix_ + ':' if (UseCapturedNS_ and self.OtherRepresentativeDocSeries_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOtherRepresentativeDocSeries>%s</%sOtherRepresentativeDocSeries>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.OtherRepresentativeDocSeries), input_name='OtherRepresentativeDocSeries')), namespaceprefix_ , eol_))
        if self.OtherRepresentativeDocNumber is not None:
            namespaceprefix_ = self.OtherRepresentativeDocNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.OtherRepresentativeDocNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOtherRepresentativeDocNumber>%s</%sOtherRepresentativeDocNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.OtherRepresentativeDocNumber), input_name='OtherRepresentativeDocNumber')), namespaceprefix_ , eol_))
        if self.OtherRepresentativeDocDate is not None:
            namespaceprefix_ = self.OtherRepresentativeDocDate_nsprefix_ + ':' if (UseCapturedNS_ and self.OtherRepresentativeDocDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOtherRepresentativeDocDate>%s</%sOtherRepresentativeDocDate>%s' % (namespaceprefix_ , self.gds_format_date(self.OtherRepresentativeDocDate, input_name='OtherRepresentativeDocDate'), namespaceprefix_ , eol_))
        if self.OtherRepresentativeDocIssued is not None:
            namespaceprefix_ = self.OtherRepresentativeDocIssued_nsprefix_ + ':' if (UseCapturedNS_ and self.OtherRepresentativeDocIssued_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOtherRepresentativeDocIssued>%s</%sOtherRepresentativeDocIssued>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.OtherRepresentativeDocIssued), input_name='OtherRepresentativeDocIssued')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'OtherRepresentativeDocName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OtherRepresentativeDocName')
            value_ = self.gds_validate_string(value_, node, 'OtherRepresentativeDocName')
            self.OtherRepresentativeDocName = value_
            self.OtherRepresentativeDocName_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.OtherRepresentativeDocName)
        elif nodeName_ == 'OtherRepresentativeDocSeries':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OtherRepresentativeDocSeries')
            value_ = self.gds_validate_string(value_, node, 'OtherRepresentativeDocSeries')
            self.OtherRepresentativeDocSeries = value_
            self.OtherRepresentativeDocSeries_nsprefix_ = child_.prefix
            # validate type string-10
            self.validate_string_10(self.OtherRepresentativeDocSeries)
        elif nodeName_ == 'OtherRepresentativeDocNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OtherRepresentativeDocNumber')
            value_ = self.gds_validate_string(value_, node, 'OtherRepresentativeDocNumber')
            self.OtherRepresentativeDocNumber = value_
            self.OtherRepresentativeDocNumber_nsprefix_ = child_.prefix
            # validate type string-10
            self.validate_string_10(self.OtherRepresentativeDocNumber)
        elif nodeName_ == 'OtherRepresentativeDocDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.OtherRepresentativeDocDate = dval_
            self.OtherRepresentativeDocDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'OtherRepresentativeDocIssued':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OtherRepresentativeDocIssued')
            value_ = self.gds_validate_string(value_, node, 'OtherRepresentativeDocIssued')
            self.OtherRepresentativeDocIssued = value_
            self.OtherRepresentativeDocIssued_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.OtherRepresentativeDocIssued)
# end class OtherRepresentativeType


class PersonIdentityDocInfoType(GeneratedsSuper):
    """Паспортные данные заявителя"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, IdentityDocName=None, IdentityDocSeries=None, IdentityDocNumber=None, IdentityDocIssueDate=None, IdentityDocIssueCode=None, IdentityDocIssued=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.IdentityDocName = IdentityDocName
        self.IdentityDocName_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_IdentityDocName')
        self.IdentityDocSeries = IdentityDocSeries
        self.validate_string_10(self.IdentityDocSeries)
        self.IdentityDocSeries_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_IdentityDocSeries')
        self.IdentityDocNumber = IdentityDocNumber
        self.validate_string_10(self.IdentityDocNumber)
        self.IdentityDocNumber_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_IdentityDocNumber')
        if isinstance(IdentityDocIssueDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(IdentityDocIssueDate, '%Y-%m-%d').date()
        else:
            initvalue_ = IdentityDocIssueDate
        self.IdentityDocIssueDate = initvalue_
        self.IdentityDocIssueDate_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_IdentityDocIssueDate')
        self.IdentityDocIssueCode = IdentityDocIssueCode
        self.validate_string_6(self.IdentityDocIssueCode)
        self.IdentityDocIssueCode_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_IdentityDocIssueCode')
        self.IdentityDocIssued = IdentityDocIssued
        self.validate_string_256(self.IdentityDocIssued)
        self.IdentityDocIssued_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_IdentityDocIssued')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PersonIdentityDocInfoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PersonIdentityDocInfoType.subclass:
            return PersonIdentityDocInfoType.subclass(*args_, **kwargs_)
        else:
            return PersonIdentityDocInfoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_IdentityDocName(self):
        return self.IdentityDocName
    def set_IdentityDocName(self, IdentityDocName):
        self.IdentityDocName = IdentityDocName
    def get_IdentityDocSeries(self):
        return self.IdentityDocSeries
    def set_IdentityDocSeries(self, IdentityDocSeries):
        self.IdentityDocSeries = IdentityDocSeries
    def get_IdentityDocNumber(self):
        return self.IdentityDocNumber
    def set_IdentityDocNumber(self, IdentityDocNumber):
        self.IdentityDocNumber = IdentityDocNumber
    def get_IdentityDocIssueDate(self):
        return self.IdentityDocIssueDate
    def set_IdentityDocIssueDate(self, IdentityDocIssueDate):
        self.IdentityDocIssueDate = IdentityDocIssueDate
    def get_IdentityDocIssueCode(self):
        return self.IdentityDocIssueCode
    def set_IdentityDocIssueCode(self, IdentityDocIssueCode):
        self.IdentityDocIssueCode = IdentityDocIssueCode
    def get_IdentityDocIssued(self):
        return self.IdentityDocIssued
    def set_IdentityDocIssued(self, IdentityDocIssued):
        self.IdentityDocIssued = IdentityDocIssued
    def validate_string_10(self, value):
        result = True
        # Validate type string-10, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-10' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_string_6(self, value):
        result = True
        # Validate type string-6, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 6:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-6' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_string_256(self, value):
        result = True
        # Validate type string-256, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 256:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-256' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.IdentityDocName is not None or
            self.IdentityDocSeries is not None or
            self.IdentityDocNumber is not None or
            self.IdentityDocIssueDate is not None or
            self.IdentityDocIssueCode is not None or
            self.IdentityDocIssued is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='PersonIdentityDocInfoType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PersonIdentityDocInfoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PersonIdentityDocInfoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PersonIdentityDocInfoType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PersonIdentityDocInfoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PersonIdentityDocInfoType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='PersonIdentityDocInfoType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.IdentityDocName is not None:
            namespaceprefix_ = self.IdentityDocName_nsprefix_ + ':' if (UseCapturedNS_ and self.IdentityDocName_nsprefix_) else ''
            self.IdentityDocName.export(outfile, level, namespaceprefix_, namespacedef_='', name_='IdentityDocName', pretty_print=pretty_print)
        if self.IdentityDocSeries is not None:
            namespaceprefix_ = self.IdentityDocSeries_nsprefix_ + ':' if (UseCapturedNS_ and self.IdentityDocSeries_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIdentityDocSeries>%s</%sIdentityDocSeries>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.IdentityDocSeries), input_name='IdentityDocSeries')), namespaceprefix_ , eol_))
        if self.IdentityDocNumber is not None:
            namespaceprefix_ = self.IdentityDocNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.IdentityDocNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIdentityDocNumber>%s</%sIdentityDocNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.IdentityDocNumber), input_name='IdentityDocNumber')), namespaceprefix_ , eol_))
        if self.IdentityDocIssueDate is not None:
            namespaceprefix_ = self.IdentityDocIssueDate_nsprefix_ + ':' if (UseCapturedNS_ and self.IdentityDocIssueDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIdentityDocIssueDate>%s</%sIdentityDocIssueDate>%s' % (namespaceprefix_ , self.gds_format_date(self.IdentityDocIssueDate, input_name='IdentityDocIssueDate'), namespaceprefix_ , eol_))
        if self.IdentityDocIssueCode is not None:
            namespaceprefix_ = self.IdentityDocIssueCode_nsprefix_ + ':' if (UseCapturedNS_ and self.IdentityDocIssueCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIdentityDocIssueCode>%s</%sIdentityDocIssueCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.IdentityDocIssueCode), input_name='IdentityDocIssueCode')), namespaceprefix_ , eol_))
        if self.IdentityDocIssued is not None:
            namespaceprefix_ = self.IdentityDocIssued_nsprefix_ + ':' if (UseCapturedNS_ and self.IdentityDocIssued_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIdentityDocIssued>%s</%sIdentityDocIssued>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.IdentityDocIssued), input_name='IdentityDocIssued')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'IdentityDocName':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.IdentityDocName = obj_
            obj_.original_tagname_ = 'IdentityDocName'
        elif nodeName_ == 'IdentityDocSeries':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'IdentityDocSeries')
            value_ = self.gds_validate_string(value_, node, 'IdentityDocSeries')
            self.IdentityDocSeries = value_
            self.IdentityDocSeries_nsprefix_ = child_.prefix
            # validate type string-10
            self.validate_string_10(self.IdentityDocSeries)
        elif nodeName_ == 'IdentityDocNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'IdentityDocNumber')
            value_ = self.gds_validate_string(value_, node, 'IdentityDocNumber')
            self.IdentityDocNumber = value_
            self.IdentityDocNumber_nsprefix_ = child_.prefix
            # validate type string-10
            self.validate_string_10(self.IdentityDocNumber)
        elif nodeName_ == 'IdentityDocIssueDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.IdentityDocIssueDate = dval_
            self.IdentityDocIssueDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'IdentityDocIssueCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'IdentityDocIssueCode')
            value_ = self.gds_validate_string(value_, node, 'IdentityDocIssueCode')
            self.IdentityDocIssueCode = value_
            self.IdentityDocIssueCode_nsprefix_ = child_.prefix
            # validate type string-6
            self.validate_string_6(self.IdentityDocIssueCode)
        elif nodeName_ == 'IdentityDocIssued':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'IdentityDocIssued')
            value_ = self.gds_validate_string(value_, node, 'IdentityDocIssued')
            self.IdentityDocIssued = value_
            self.IdentityDocIssued_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.IdentityDocIssued)
# end class PersonIdentityDocInfoType


class ChildInfoType(GeneratedsSuper):
    """Сведения о ребёнке"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ChildSurname=None, ChildName=None, ChildMiddleName=None, ChildBirthDate=None, ChildBirthDocRF=None, ChildBirthDocForeign=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.ChildSurname = ChildSurname
        self.validate_string_256(self.ChildSurname)
        self.ChildSurname_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ChildSurname')
        self.ChildName = ChildName
        self.validate_string_256(self.ChildName)
        self.ChildName_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ChildName')
        self.ChildMiddleName = ChildMiddleName
        self.validate_string_256(self.ChildMiddleName)
        self.ChildMiddleName_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ChildMiddleName')
        if isinstance(ChildBirthDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(ChildBirthDate, '%Y-%m-%d').date()
        else:
            initvalue_ = ChildBirthDate
        self.ChildBirthDate = initvalue_
        self.ChildBirthDate_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ChildBirthDate')
        self.ChildBirthDocRF = ChildBirthDocRF
        self.ChildBirthDocRF_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ChildBirthDocRF')
        self.ChildBirthDocForeign = ChildBirthDocForeign
        self.ChildBirthDocForeign_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ChildBirthDocForeign')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ChildInfoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ChildInfoType.subclass:
            return ChildInfoType.subclass(*args_, **kwargs_)
        else:
            return ChildInfoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ChildSurname(self):
        return self.ChildSurname
    def set_ChildSurname(self, ChildSurname):
        self.ChildSurname = ChildSurname
    def get_ChildName(self):
        return self.ChildName
    def set_ChildName(self, ChildName):
        self.ChildName = ChildName
    def get_ChildMiddleName(self):
        return self.ChildMiddleName
    def set_ChildMiddleName(self, ChildMiddleName):
        self.ChildMiddleName = ChildMiddleName
    def get_ChildBirthDate(self):
        return self.ChildBirthDate
    def set_ChildBirthDate(self, ChildBirthDate):
        self.ChildBirthDate = ChildBirthDate
    def get_ChildBirthDocRF(self):
        return self.ChildBirthDocRF
    def set_ChildBirthDocRF(self, ChildBirthDocRF):
        self.ChildBirthDocRF = ChildBirthDocRF
    def get_ChildBirthDocForeign(self):
        return self.ChildBirthDocForeign
    def set_ChildBirthDocForeign(self, ChildBirthDocForeign):
        self.ChildBirthDocForeign = ChildBirthDocForeign
    def validate_string_256(self, value):
        result = True
        # Validate type string-256, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 256:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-256' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.ChildSurname is not None or
            self.ChildName is not None or
            self.ChildMiddleName is not None or
            self.ChildBirthDate is not None or
            self.ChildBirthDocRF is not None or
            self.ChildBirthDocForeign is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='ChildInfoType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ChildInfoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ChildInfoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ChildInfoType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ChildInfoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ChildInfoType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='ChildInfoType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ChildSurname is not None:
            namespaceprefix_ = self.ChildSurname_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildSurname_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChildSurname>%s</%sChildSurname>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ChildSurname), input_name='ChildSurname')), namespaceprefix_ , eol_))
        if self.ChildName is not None:
            namespaceprefix_ = self.ChildName_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChildName>%s</%sChildName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ChildName), input_name='ChildName')), namespaceprefix_ , eol_))
        if self.ChildMiddleName is not None:
            namespaceprefix_ = self.ChildMiddleName_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildMiddleName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChildMiddleName>%s</%sChildMiddleName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ChildMiddleName), input_name='ChildMiddleName')), namespaceprefix_ , eol_))
        if self.ChildBirthDate is not None:
            namespaceprefix_ = self.ChildBirthDate_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildBirthDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChildBirthDate>%s</%sChildBirthDate>%s' % (namespaceprefix_ , self.gds_format_date(self.ChildBirthDate, input_name='ChildBirthDate'), namespaceprefix_ , eol_))
        if self.ChildBirthDocRF is not None:
            namespaceprefix_ = self.ChildBirthDocRF_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildBirthDocRF_nsprefix_) else ''
            self.ChildBirthDocRF.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ChildBirthDocRF', pretty_print=pretty_print)
        if self.ChildBirthDocForeign is not None:
            namespaceprefix_ = self.ChildBirthDocForeign_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildBirthDocForeign_nsprefix_) else ''
            self.ChildBirthDocForeign.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ChildBirthDocForeign', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ChildSurname':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChildSurname')
            value_ = self.gds_validate_string(value_, node, 'ChildSurname')
            self.ChildSurname = value_
            self.ChildSurname_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.ChildSurname)
        elif nodeName_ == 'ChildName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChildName')
            value_ = self.gds_validate_string(value_, node, 'ChildName')
            self.ChildName = value_
            self.ChildName_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.ChildName)
        elif nodeName_ == 'ChildMiddleName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChildMiddleName')
            value_ = self.gds_validate_string(value_, node, 'ChildMiddleName')
            self.ChildMiddleName = value_
            self.ChildMiddleName_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.ChildMiddleName)
        elif nodeName_ == 'ChildBirthDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.ChildBirthDate = dval_
            self.ChildBirthDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'ChildBirthDocRF':
            obj_ = ChildBirthDocRFType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ChildBirthDocRF = obj_
            obj_.original_tagname_ = 'ChildBirthDocRF'
        elif nodeName_ == 'ChildBirthDocForeign':
            obj_ = ChildBirthDocForeignType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ChildBirthDocForeign = obj_
            obj_.original_tagname_ = 'ChildBirthDocForeign'
# end class ChildInfoType


class ChildBirthDocRFType(GeneratedsSuper):
    """Свидетельство о рождении РФ"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ChildBirthDocSeries=None, ChildBirthDocNumber=None, ChildBirthDocIssueDate=None, ChildBirthDocActNumber=None, ChildBirthDocActDate=None, ChildBirthDocIssued=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.ChildBirthDocSeries = ChildBirthDocSeries
        self.validate_string_10(self.ChildBirthDocSeries)
        self.ChildBirthDocSeries_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ChildBirthDocSeries')
        self.ChildBirthDocNumber = ChildBirthDocNumber
        self.validate_string_10(self.ChildBirthDocNumber)
        self.ChildBirthDocNumber_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ChildBirthDocNumber')
        if isinstance(ChildBirthDocIssueDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(ChildBirthDocIssueDate, '%Y-%m-%d').date()
        else:
            initvalue_ = ChildBirthDocIssueDate
        self.ChildBirthDocIssueDate = initvalue_
        self.ChildBirthDocIssueDate_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ChildBirthDocIssueDate')
        self.ChildBirthDocActNumber = ChildBirthDocActNumber
        self.validate_string_21(self.ChildBirthDocActNumber)
        self.ChildBirthDocActNumber_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ChildBirthDocActNumber')
        if isinstance(ChildBirthDocActDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(ChildBirthDocActDate, '%Y-%m-%d').date()
        else:
            initvalue_ = ChildBirthDocActDate
        self.ChildBirthDocActDate = initvalue_
        self.ChildBirthDocActDate_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ChildBirthDocActDate')
        self.ChildBirthDocIssued = ChildBirthDocIssued
        self.validate_string_256(self.ChildBirthDocIssued)
        self.ChildBirthDocIssued_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ChildBirthDocIssued')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ChildBirthDocRFType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ChildBirthDocRFType.subclass:
            return ChildBirthDocRFType.subclass(*args_, **kwargs_)
        else:
            return ChildBirthDocRFType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ChildBirthDocSeries(self):
        return self.ChildBirthDocSeries
    def set_ChildBirthDocSeries(self, ChildBirthDocSeries):
        self.ChildBirthDocSeries = ChildBirthDocSeries
    def get_ChildBirthDocNumber(self):
        return self.ChildBirthDocNumber
    def set_ChildBirthDocNumber(self, ChildBirthDocNumber):
        self.ChildBirthDocNumber = ChildBirthDocNumber
    def get_ChildBirthDocIssueDate(self):
        return self.ChildBirthDocIssueDate
    def set_ChildBirthDocIssueDate(self, ChildBirthDocIssueDate):
        self.ChildBirthDocIssueDate = ChildBirthDocIssueDate
    def get_ChildBirthDocActNumber(self):
        return self.ChildBirthDocActNumber
    def set_ChildBirthDocActNumber(self, ChildBirthDocActNumber):
        self.ChildBirthDocActNumber = ChildBirthDocActNumber
    def get_ChildBirthDocActDate(self):
        return self.ChildBirthDocActDate
    def set_ChildBirthDocActDate(self, ChildBirthDocActDate):
        self.ChildBirthDocActDate = ChildBirthDocActDate
    def get_ChildBirthDocIssued(self):
        return self.ChildBirthDocIssued
    def set_ChildBirthDocIssued(self, ChildBirthDocIssued):
        self.ChildBirthDocIssued = ChildBirthDocIssued
    def validate_string_10(self, value):
        result = True
        # Validate type string-10, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-10' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_string_21(self, value):
        result = True
        # Validate type string-21, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 21:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-21' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_string_256(self, value):
        result = True
        # Validate type string-256, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 256:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-256' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.ChildBirthDocSeries is not None or
            self.ChildBirthDocNumber is not None or
            self.ChildBirthDocIssueDate is not None or
            self.ChildBirthDocActNumber is not None or
            self.ChildBirthDocActDate is not None or
            self.ChildBirthDocIssued is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='ChildBirthDocRFType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ChildBirthDocRFType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ChildBirthDocRFType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ChildBirthDocRFType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ChildBirthDocRFType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ChildBirthDocRFType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='ChildBirthDocRFType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ChildBirthDocSeries is not None:
            namespaceprefix_ = self.ChildBirthDocSeries_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildBirthDocSeries_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChildBirthDocSeries>%s</%sChildBirthDocSeries>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ChildBirthDocSeries), input_name='ChildBirthDocSeries')), namespaceprefix_ , eol_))
        if self.ChildBirthDocNumber is not None:
            namespaceprefix_ = self.ChildBirthDocNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildBirthDocNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChildBirthDocNumber>%s</%sChildBirthDocNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ChildBirthDocNumber), input_name='ChildBirthDocNumber')), namespaceprefix_ , eol_))
        if self.ChildBirthDocIssueDate is not None:
            namespaceprefix_ = self.ChildBirthDocIssueDate_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildBirthDocIssueDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChildBirthDocIssueDate>%s</%sChildBirthDocIssueDate>%s' % (namespaceprefix_ , self.gds_format_date(self.ChildBirthDocIssueDate, input_name='ChildBirthDocIssueDate'), namespaceprefix_ , eol_))
        if self.ChildBirthDocActNumber is not None:
            namespaceprefix_ = self.ChildBirthDocActNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildBirthDocActNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChildBirthDocActNumber>%s</%sChildBirthDocActNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ChildBirthDocActNumber), input_name='ChildBirthDocActNumber')), namespaceprefix_ , eol_))
        if self.ChildBirthDocActDate is not None:
            namespaceprefix_ = self.ChildBirthDocActDate_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildBirthDocActDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChildBirthDocActDate>%s</%sChildBirthDocActDate>%s' % (namespaceprefix_ , self.gds_format_date(self.ChildBirthDocActDate, input_name='ChildBirthDocActDate'), namespaceprefix_ , eol_))
        if self.ChildBirthDocIssued is not None:
            namespaceprefix_ = self.ChildBirthDocIssued_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildBirthDocIssued_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChildBirthDocIssued>%s</%sChildBirthDocIssued>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ChildBirthDocIssued), input_name='ChildBirthDocIssued')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ChildBirthDocSeries':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChildBirthDocSeries')
            value_ = self.gds_validate_string(value_, node, 'ChildBirthDocSeries')
            self.ChildBirthDocSeries = value_
            self.ChildBirthDocSeries_nsprefix_ = child_.prefix
            # validate type string-10
            self.validate_string_10(self.ChildBirthDocSeries)
        elif nodeName_ == 'ChildBirthDocNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChildBirthDocNumber')
            value_ = self.gds_validate_string(value_, node, 'ChildBirthDocNumber')
            self.ChildBirthDocNumber = value_
            self.ChildBirthDocNumber_nsprefix_ = child_.prefix
            # validate type string-10
            self.validate_string_10(self.ChildBirthDocNumber)
        elif nodeName_ == 'ChildBirthDocIssueDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.ChildBirthDocIssueDate = dval_
            self.ChildBirthDocIssueDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'ChildBirthDocActNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChildBirthDocActNumber')
            value_ = self.gds_validate_string(value_, node, 'ChildBirthDocActNumber')
            self.ChildBirthDocActNumber = value_
            self.ChildBirthDocActNumber_nsprefix_ = child_.prefix
            # validate type string-21
            self.validate_string_21(self.ChildBirthDocActNumber)
        elif nodeName_ == 'ChildBirthDocActDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.ChildBirthDocActDate = dval_
            self.ChildBirthDocActDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'ChildBirthDocIssued':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChildBirthDocIssued')
            value_ = self.gds_validate_string(value_, node, 'ChildBirthDocIssued')
            self.ChildBirthDocIssued = value_
            self.ChildBirthDocIssued_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.ChildBirthDocIssued)
# end class ChildBirthDocRFType


class ChildBirthDocForeignType(GeneratedsSuper):
    """Другой документ"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ChildBirthDocName=None, ChildBirthDocSeries=None, ChildBirthDocNumber=None, ChildBirthDocIssueDate=None, ChildBirthDocIssued=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.ChildBirthDocName = ChildBirthDocName
        self.validate_string_256(self.ChildBirthDocName)
        self.ChildBirthDocName_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ChildBirthDocName')
        self.ChildBirthDocSeries = ChildBirthDocSeries
        self.validate_string_10(self.ChildBirthDocSeries)
        self.ChildBirthDocSeries_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ChildBirthDocSeries')
        self.ChildBirthDocNumber = ChildBirthDocNumber
        self.validate_string_50(self.ChildBirthDocNumber)
        self.ChildBirthDocNumber_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ChildBirthDocNumber')
        if isinstance(ChildBirthDocIssueDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(ChildBirthDocIssueDate, '%Y-%m-%d').date()
        else:
            initvalue_ = ChildBirthDocIssueDate
        self.ChildBirthDocIssueDate = initvalue_
        self.ChildBirthDocIssueDate_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ChildBirthDocIssueDate')
        self.ChildBirthDocIssued = ChildBirthDocIssued
        self.validate_string_256(self.ChildBirthDocIssued)
        self.ChildBirthDocIssued_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ChildBirthDocIssued')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ChildBirthDocForeignType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ChildBirthDocForeignType.subclass:
            return ChildBirthDocForeignType.subclass(*args_, **kwargs_)
        else:
            return ChildBirthDocForeignType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ChildBirthDocName(self):
        return self.ChildBirthDocName
    def set_ChildBirthDocName(self, ChildBirthDocName):
        self.ChildBirthDocName = ChildBirthDocName
    def get_ChildBirthDocSeries(self):
        return self.ChildBirthDocSeries
    def set_ChildBirthDocSeries(self, ChildBirthDocSeries):
        self.ChildBirthDocSeries = ChildBirthDocSeries
    def get_ChildBirthDocNumber(self):
        return self.ChildBirthDocNumber
    def set_ChildBirthDocNumber(self, ChildBirthDocNumber):
        self.ChildBirthDocNumber = ChildBirthDocNumber
    def get_ChildBirthDocIssueDate(self):
        return self.ChildBirthDocIssueDate
    def set_ChildBirthDocIssueDate(self, ChildBirthDocIssueDate):
        self.ChildBirthDocIssueDate = ChildBirthDocIssueDate
    def get_ChildBirthDocIssued(self):
        return self.ChildBirthDocIssued
    def set_ChildBirthDocIssued(self, ChildBirthDocIssued):
        self.ChildBirthDocIssued = ChildBirthDocIssued
    def validate_string_256(self, value):
        result = True
        # Validate type string-256, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 256:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-256' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_string_10(self, value):
        result = True
        # Validate type string-10, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-10' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_string_50(self, value):
        result = True
        # Validate type string-50, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-50' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.ChildBirthDocName is not None or
            self.ChildBirthDocSeries is not None or
            self.ChildBirthDocNumber is not None or
            self.ChildBirthDocIssueDate is not None or
            self.ChildBirthDocIssued is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='ChildBirthDocForeignType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ChildBirthDocForeignType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ChildBirthDocForeignType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ChildBirthDocForeignType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ChildBirthDocForeignType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ChildBirthDocForeignType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='ChildBirthDocForeignType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ChildBirthDocName is not None:
            namespaceprefix_ = self.ChildBirthDocName_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildBirthDocName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChildBirthDocName>%s</%sChildBirthDocName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ChildBirthDocName), input_name='ChildBirthDocName')), namespaceprefix_ , eol_))
        if self.ChildBirthDocSeries is not None:
            namespaceprefix_ = self.ChildBirthDocSeries_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildBirthDocSeries_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChildBirthDocSeries>%s</%sChildBirthDocSeries>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ChildBirthDocSeries), input_name='ChildBirthDocSeries')), namespaceprefix_ , eol_))
        if self.ChildBirthDocNumber is not None:
            namespaceprefix_ = self.ChildBirthDocNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildBirthDocNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChildBirthDocNumber>%s</%sChildBirthDocNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ChildBirthDocNumber), input_name='ChildBirthDocNumber')), namespaceprefix_ , eol_))
        if self.ChildBirthDocIssueDate is not None:
            namespaceprefix_ = self.ChildBirthDocIssueDate_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildBirthDocIssueDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChildBirthDocIssueDate>%s</%sChildBirthDocIssueDate>%s' % (namespaceprefix_ , self.gds_format_date(self.ChildBirthDocIssueDate, input_name='ChildBirthDocIssueDate'), namespaceprefix_ , eol_))
        if self.ChildBirthDocIssued is not None:
            namespaceprefix_ = self.ChildBirthDocIssued_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildBirthDocIssued_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChildBirthDocIssued>%s</%sChildBirthDocIssued>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ChildBirthDocIssued), input_name='ChildBirthDocIssued')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ChildBirthDocName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChildBirthDocName')
            value_ = self.gds_validate_string(value_, node, 'ChildBirthDocName')
            self.ChildBirthDocName = value_
            self.ChildBirthDocName_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.ChildBirthDocName)
        elif nodeName_ == 'ChildBirthDocSeries':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChildBirthDocSeries')
            value_ = self.gds_validate_string(value_, node, 'ChildBirthDocSeries')
            self.ChildBirthDocSeries = value_
            self.ChildBirthDocSeries_nsprefix_ = child_.prefix
            # validate type string-10
            self.validate_string_10(self.ChildBirthDocSeries)
        elif nodeName_ == 'ChildBirthDocNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChildBirthDocNumber')
            value_ = self.gds_validate_string(value_, node, 'ChildBirthDocNumber')
            self.ChildBirthDocNumber = value_
            self.ChildBirthDocNumber_nsprefix_ = child_.prefix
            # validate type string-50
            self.validate_string_50(self.ChildBirthDocNumber)
        elif nodeName_ == 'ChildBirthDocIssueDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.ChildBirthDocIssueDate = dval_
            self.ChildBirthDocIssueDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'ChildBirthDocIssued':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChildBirthDocIssued')
            value_ = self.gds_validate_string(value_, node, 'ChildBirthDocIssued')
            self.ChildBirthDocIssued = value_
            self.ChildBirthDocIssued_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.ChildBirthDocIssued)
# end class ChildBirthDocForeignType


class EntryParamsType(GeneratedsSuper):
    """Желаемые параметры зачисления"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, EntryDate=None, Language=None, Schedule=None, AgreementOnFullDayGroup=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        if isinstance(EntryDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(EntryDate, '%Y-%m-%d').date()
        else:
            initvalue_ = EntryDate
        self.EntryDate = initvalue_
        self.EntryDate_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_EntryDate')
        self.Language = Language
        self.Language_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_Language')
        self.Schedule = Schedule
        self.Schedule_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_Schedule')
        self.AgreementOnFullDayGroup = AgreementOnFullDayGroup
        self.AgreementOnFullDayGroup_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_AgreementOnFullDayGroup')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, EntryParamsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if EntryParamsType.subclass:
            return EntryParamsType.subclass(*args_, **kwargs_)
        else:
            return EntryParamsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_EntryDate(self):
        return self.EntryDate
    def set_EntryDate(self, EntryDate):
        self.EntryDate = EntryDate
    def get_Language(self):
        return self.Language
    def set_Language(self, Language):
        self.Language = Language
    def get_Schedule(self):
        return self.Schedule
    def set_Schedule(self, Schedule):
        self.Schedule = Schedule
    def get_AgreementOnFullDayGroup(self):
        return self.AgreementOnFullDayGroup
    def set_AgreementOnFullDayGroup(self, AgreementOnFullDayGroup):
        self.AgreementOnFullDayGroup = AgreementOnFullDayGroup
    def hasContent_(self):
        if (
            self.EntryDate is not None or
            self.Language is not None or
            self.Schedule is not None or
            self.AgreementOnFullDayGroup is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='EntryParamsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('EntryParamsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'EntryParamsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='EntryParamsType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='EntryParamsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='EntryParamsType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='EntryParamsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.EntryDate is not None:
            namespaceprefix_ = self.EntryDate_nsprefix_ + ':' if (UseCapturedNS_ and self.EntryDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEntryDate>%s</%sEntryDate>%s' % (namespaceprefix_ , self.gds_format_date(self.EntryDate, input_name='EntryDate'), namespaceprefix_ , eol_))
        if self.Language is not None:
            namespaceprefix_ = self.Language_nsprefix_ + ':' if (UseCapturedNS_ and self.Language_nsprefix_) else ''
            self.Language.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Language', pretty_print=pretty_print)
        if self.Schedule is not None:
            namespaceprefix_ = self.Schedule_nsprefix_ + ':' if (UseCapturedNS_ and self.Schedule_nsprefix_) else ''
            self.Schedule.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Schedule', pretty_print=pretty_print)
        if self.AgreementOnFullDayGroup is not None:
            namespaceprefix_ = self.AgreementOnFullDayGroup_nsprefix_ + ':' if (UseCapturedNS_ and self.AgreementOnFullDayGroup_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAgreementOnFullDayGroup>%s</%sAgreementOnFullDayGroup>%s' % (namespaceprefix_ , self.gds_format_boolean(self.AgreementOnFullDayGroup, input_name='AgreementOnFullDayGroup'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'EntryDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.EntryDate = dval_
            self.EntryDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'Language':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Language = obj_
            obj_.original_tagname_ = 'Language'
        elif nodeName_ == 'Schedule':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Schedule = obj_
            obj_.original_tagname_ = 'Schedule'
        elif nodeName_ == 'AgreementOnFullDayGroup':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'AgreementOnFullDayGroup')
            ival_ = self.gds_validate_boolean(ival_, node, 'AgreementOnFullDayGroup')
            self.AgreementOnFullDayGroup = ival_
            self.AgreementOnFullDayGroup_nsprefix_ = child_.prefix
# end class EntryParamsType


class AdaptationProgramType(GeneratedsSuper):
    """Направленность группы"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, AdaptationGroup=None, AdaptationGroupType=None, AgreementOnGeneralGroup=None, AgreementOnCareGroup=None, NeedSpecialCareConditions=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.AdaptationGroup = AdaptationGroup
        self.AdaptationGroup_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_AdaptationGroup')
        self.AdaptationGroupType = AdaptationGroupType
        self.AdaptationGroupType_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_AdaptationGroupType')
        self.AgreementOnGeneralGroup = AgreementOnGeneralGroup
        self.AgreementOnGeneralGroup_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_AgreementOnGeneralGroup')
        self.AgreementOnCareGroup = AgreementOnCareGroup
        self.AgreementOnCareGroup_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_AgreementOnCareGroup')
        self.NeedSpecialCareConditions = NeedSpecialCareConditions
        self.NeedSpecialCareConditions_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_NeedSpecialCareConditions')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AdaptationProgramType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AdaptationProgramType.subclass:
            return AdaptationProgramType.subclass(*args_, **kwargs_)
        else:
            return AdaptationProgramType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_AdaptationGroup(self):
        return self.AdaptationGroup
    def set_AdaptationGroup(self, AdaptationGroup):
        self.AdaptationGroup = AdaptationGroup
    def get_AdaptationGroupType(self):
        return self.AdaptationGroupType
    def set_AdaptationGroupType(self, AdaptationGroupType):
        self.AdaptationGroupType = AdaptationGroupType
    def get_AgreementOnGeneralGroup(self):
        return self.AgreementOnGeneralGroup
    def set_AgreementOnGeneralGroup(self, AgreementOnGeneralGroup):
        self.AgreementOnGeneralGroup = AgreementOnGeneralGroup
    def get_AgreementOnCareGroup(self):
        return self.AgreementOnCareGroup
    def set_AgreementOnCareGroup(self, AgreementOnCareGroup):
        self.AgreementOnCareGroup = AgreementOnCareGroup
    def get_NeedSpecialCareConditions(self):
        return self.NeedSpecialCareConditions
    def set_NeedSpecialCareConditions(self, NeedSpecialCareConditions):
        self.NeedSpecialCareConditions = NeedSpecialCareConditions
    def hasContent_(self):
        if (
            self.AdaptationGroup is not None or
            self.AdaptationGroupType is not None or
            self.AgreementOnGeneralGroup is not None or
            self.AgreementOnCareGroup is not None or
            self.NeedSpecialCareConditions is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='AdaptationProgramType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AdaptationProgramType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AdaptationProgramType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AdaptationProgramType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AdaptationProgramType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AdaptationProgramType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='AdaptationProgramType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.AdaptationGroup is not None:
            namespaceprefix_ = self.AdaptationGroup_nsprefix_ + ':' if (UseCapturedNS_ and self.AdaptationGroup_nsprefix_) else ''
            self.AdaptationGroup.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AdaptationGroup', pretty_print=pretty_print)
        if self.AdaptationGroupType is not None:
            namespaceprefix_ = self.AdaptationGroupType_nsprefix_ + ':' if (UseCapturedNS_ and self.AdaptationGroupType_nsprefix_) else ''
            self.AdaptationGroupType.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AdaptationGroupType', pretty_print=pretty_print)
        if self.AgreementOnGeneralGroup is not None:
            namespaceprefix_ = self.AgreementOnGeneralGroup_nsprefix_ + ':' if (UseCapturedNS_ and self.AgreementOnGeneralGroup_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAgreementOnGeneralGroup>%s</%sAgreementOnGeneralGroup>%s' % (namespaceprefix_ , self.gds_format_boolean(self.AgreementOnGeneralGroup, input_name='AgreementOnGeneralGroup'), namespaceprefix_ , eol_))
        if self.AgreementOnCareGroup is not None:
            namespaceprefix_ = self.AgreementOnCareGroup_nsprefix_ + ':' if (UseCapturedNS_ and self.AgreementOnCareGroup_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAgreementOnCareGroup>%s</%sAgreementOnCareGroup>%s' % (namespaceprefix_ , self.gds_format_boolean(self.AgreementOnCareGroup, input_name='AgreementOnCareGroup'), namespaceprefix_ , eol_))
        if self.NeedSpecialCareConditions is not None:
            namespaceprefix_ = self.NeedSpecialCareConditions_nsprefix_ + ':' if (UseCapturedNS_ and self.NeedSpecialCareConditions_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNeedSpecialCareConditions>%s</%sNeedSpecialCareConditions>%s' % (namespaceprefix_ , self.gds_format_boolean(self.NeedSpecialCareConditions, input_name='NeedSpecialCareConditions'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'AdaptationGroup':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AdaptationGroup = obj_
            obj_.original_tagname_ = 'AdaptationGroup'
        elif nodeName_ == 'AdaptationGroupType':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AdaptationGroupType = obj_
            obj_.original_tagname_ = 'AdaptationGroupType'
        elif nodeName_ == 'AgreementOnGeneralGroup':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'AgreementOnGeneralGroup')
            ival_ = self.gds_validate_boolean(ival_, node, 'AgreementOnGeneralGroup')
            self.AgreementOnGeneralGroup = ival_
            self.AgreementOnGeneralGroup_nsprefix_ = child_.prefix
        elif nodeName_ == 'AgreementOnCareGroup':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'AgreementOnCareGroup')
            ival_ = self.gds_validate_boolean(ival_, node, 'AgreementOnCareGroup')
            self.AgreementOnCareGroup = ival_
            self.AgreementOnCareGroup_nsprefix_ = child_.prefix
        elif nodeName_ == 'NeedSpecialCareConditions':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'NeedSpecialCareConditions')
            ival_ = self.gds_validate_boolean(ival_, node, 'NeedSpecialCareConditions')
            self.NeedSpecialCareConditions = ival_
            self.NeedSpecialCareConditions_nsprefix_ = child_.prefix
# end class AdaptationProgramType


class MedicalReportType(GeneratedsSuper):
    """Реквизиты документа, подтверждающего группу коменсирующей
    направленности"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DocName=None, DocSeries=None, DocNumber=None, DocIssueDate=None, DocIssued=None, DocExpirationDate=None, DocFile=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.DocName = DocName
        self.DocName_nsprefix_ = None
        self.DocSeries = DocSeries
        self.validate_string_20(self.DocSeries)
        self.DocSeries_nsprefix_ = None
        self.DocNumber = DocNumber
        self.validate_string_20(self.DocNumber)
        self.DocNumber_nsprefix_ = None
        if isinstance(DocIssueDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(DocIssueDate, '%Y-%m-%d').date()
        else:
            initvalue_ = DocIssueDate
        self.DocIssueDate = initvalue_
        self.DocIssueDate_nsprefix_ = None
        self.DocIssued = DocIssued
        self.validate_string_256(self.DocIssued)
        self.DocIssued_nsprefix_ = None
        if isinstance(DocExpirationDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(DocExpirationDate, '%Y-%m-%d').date()
        else:
            initvalue_ = DocExpirationDate
        self.DocExpirationDate = initvalue_
        self.DocExpirationDate_nsprefix_ = None
        if DocFile is None:
            self.DocFile = []
        else:
            self.DocFile = DocFile
        self.DocFile_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, MedicalReportType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if MedicalReportType.subclass:
            return MedicalReportType.subclass(*args_, **kwargs_)
        else:
            return MedicalReportType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DocName(self):
        return self.DocName
    def set_DocName(self, DocName):
        self.DocName = DocName
    def get_DocSeries(self):
        return self.DocSeries
    def set_DocSeries(self, DocSeries):
        self.DocSeries = DocSeries
    def get_DocNumber(self):
        return self.DocNumber
    def set_DocNumber(self, DocNumber):
        self.DocNumber = DocNumber
    def get_DocIssueDate(self):
        return self.DocIssueDate
    def set_DocIssueDate(self, DocIssueDate):
        self.DocIssueDate = DocIssueDate
    def get_DocIssued(self):
        return self.DocIssued
    def set_DocIssued(self, DocIssued):
        self.DocIssued = DocIssued
    def get_DocExpirationDate(self):
        return self.DocExpirationDate
    def set_DocExpirationDate(self, DocExpirationDate):
        self.DocExpirationDate = DocExpirationDate
    def get_DocFile(self):
        return self.DocFile
    def set_DocFile(self, DocFile):
        self.DocFile = DocFile
    def add_DocFile(self, value):
        self.DocFile.append(value)
    def insert_DocFile_at(self, index, value):
        self.DocFile.insert(index, value)
    def replace_DocFile_at(self, index, value):
        self.DocFile[index] = value
    def validate_string_20(self, value):
        result = True
        # Validate type string-20, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-20' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_string_256(self, value):
        result = True
        # Validate type string-256, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 256:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-256' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.DocName is not None or
            self.DocSeries is not None or
            self.DocNumber is not None or
            self.DocIssueDate is not None or
            self.DocIssued is not None or
            self.DocExpirationDate is not None or
            self.DocFile
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='MedicalReportType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('MedicalReportType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'MedicalReportType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='MedicalReportType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='MedicalReportType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='MedicalReportType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='MedicalReportType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.DocName is not None:
            namespaceprefix_ = self.DocName_nsprefix_ + ':' if (UseCapturedNS_ and self.DocName_nsprefix_) else ''
            self.DocName.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DocName', pretty_print=pretty_print)
        if self.DocSeries is not None:
            namespaceprefix_ = self.DocSeries_nsprefix_ + ':' if (UseCapturedNS_ and self.DocSeries_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDocSeries>%s</%sDocSeries>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DocSeries), input_name='DocSeries')), namespaceprefix_ , eol_))
        if self.DocNumber is not None:
            namespaceprefix_ = self.DocNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.DocNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDocNumber>%s</%sDocNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DocNumber), input_name='DocNumber')), namespaceprefix_ , eol_))
        if self.DocIssueDate is not None:
            namespaceprefix_ = self.DocIssueDate_nsprefix_ + ':' if (UseCapturedNS_ and self.DocIssueDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDocIssueDate>%s</%sDocIssueDate>%s' % (namespaceprefix_ , self.gds_format_date(self.DocIssueDate, input_name='DocIssueDate'), namespaceprefix_ , eol_))
        if self.DocIssued is not None:
            namespaceprefix_ = self.DocIssued_nsprefix_ + ':' if (UseCapturedNS_ and self.DocIssued_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDocIssued>%s</%sDocIssued>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DocIssued), input_name='DocIssued')), namespaceprefix_ , eol_))
        if self.DocExpirationDate is not None:
            namespaceprefix_ = self.DocExpirationDate_nsprefix_ + ':' if (UseCapturedNS_ and self.DocExpirationDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDocExpirationDate>%s</%sDocExpirationDate>%s' % (namespaceprefix_ , self.gds_format_date(self.DocExpirationDate, input_name='DocExpirationDate'), namespaceprefix_ , eol_))
        for DocFile_ in self.DocFile:
            namespaceprefix_ = self.DocFile_nsprefix_ + ':' if (UseCapturedNS_ and self.DocFile_nsprefix_) else ''
            DocFile_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DocFile', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'DocName':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DocName = obj_
            obj_.original_tagname_ = 'DocName'
        elif nodeName_ == 'DocSeries':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DocSeries')
            value_ = self.gds_validate_string(value_, node, 'DocSeries')
            self.DocSeries = value_
            self.DocSeries_nsprefix_ = child_.prefix
            # validate type string-20
            self.validate_string_20(self.DocSeries)
        elif nodeName_ == 'DocNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DocNumber')
            value_ = self.gds_validate_string(value_, node, 'DocNumber')
            self.DocNumber = value_
            self.DocNumber_nsprefix_ = child_.prefix
            # validate type string-20
            self.validate_string_20(self.DocNumber)
        elif nodeName_ == 'DocIssueDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.DocIssueDate = dval_
            self.DocIssueDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'DocIssued':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DocIssued')
            value_ = self.gds_validate_string(value_, node, 'DocIssued')
            self.DocIssued = value_
            self.DocIssued_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.DocIssued)
        elif nodeName_ == 'DocExpirationDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.DocExpirationDate = dval_
            self.DocExpirationDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'DocFile':
            obj_ = AppliedDocumentType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DocFile.append(obj_)
            obj_.original_tagname_ = 'DocFile'
# end class MedicalReportType


class MedicalReportWithoutFilesType(GeneratedsSuper):
    """Реквизиты документа, подтверждающего группу коменсирующей
    направленности"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DocName=None, DocSeries=None, DocNumber=None, DocIssueDate=None, DocIssued=None, DocExpirationDate=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.DocName = DocName
        self.DocName_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_DocName')
        self.DocSeries = DocSeries
        self.validate_string_20(self.DocSeries)
        self.DocSeries_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_DocSeries')
        self.DocNumber = DocNumber
        self.validate_string_20(self.DocNumber)
        self.DocNumber_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_DocNumber')
        if isinstance(DocIssueDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(DocIssueDate, '%Y-%m-%d').date()
        else:
            initvalue_ = DocIssueDate
        self.DocIssueDate = initvalue_
        self.DocIssueDate_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_DocIssueDate')
        self.DocIssued = DocIssued
        self.validate_string_256(self.DocIssued)
        self.DocIssued_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_DocIssued')
        if isinstance(DocExpirationDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(DocExpirationDate, '%Y-%m-%d').date()
        else:
            initvalue_ = DocExpirationDate
        self.DocExpirationDate = initvalue_
        self.DocExpirationDate_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_DocExpirationDate')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, MedicalReportWithoutFilesType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if MedicalReportWithoutFilesType.subclass:
            return MedicalReportWithoutFilesType.subclass(*args_, **kwargs_)
        else:
            return MedicalReportWithoutFilesType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DocName(self):
        return self.DocName
    def set_DocName(self, DocName):
        self.DocName = DocName
    def get_DocSeries(self):
        return self.DocSeries
    def set_DocSeries(self, DocSeries):
        self.DocSeries = DocSeries
    def get_DocNumber(self):
        return self.DocNumber
    def set_DocNumber(self, DocNumber):
        self.DocNumber = DocNumber
    def get_DocIssueDate(self):
        return self.DocIssueDate
    def set_DocIssueDate(self, DocIssueDate):
        self.DocIssueDate = DocIssueDate
    def get_DocIssued(self):
        return self.DocIssued
    def set_DocIssued(self, DocIssued):
        self.DocIssued = DocIssued
    def get_DocExpirationDate(self):
        return self.DocExpirationDate
    def set_DocExpirationDate(self, DocExpirationDate):
        self.DocExpirationDate = DocExpirationDate
    def validate_string_20(self, value):
        result = True
        # Validate type string-20, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-20' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_string_256(self, value):
        result = True
        # Validate type string-256, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 256:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-256' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.DocName is not None or
            self.DocSeries is not None or
            self.DocNumber is not None or
            self.DocIssueDate is not None or
            self.DocIssued is not None or
            self.DocExpirationDate is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='MedicalReportWithoutFilesType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('MedicalReportWithoutFilesType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'MedicalReportWithoutFilesType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='MedicalReportWithoutFilesType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='MedicalReportWithoutFilesType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='MedicalReportWithoutFilesType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='MedicalReportWithoutFilesType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.DocName is not None:
            namespaceprefix_ = self.DocName_nsprefix_ + ':' if (UseCapturedNS_ and self.DocName_nsprefix_) else ''
            self.DocName.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DocName', pretty_print=pretty_print)
        if self.DocSeries is not None:
            namespaceprefix_ = self.DocSeries_nsprefix_ + ':' if (UseCapturedNS_ and self.DocSeries_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDocSeries>%s</%sDocSeries>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DocSeries), input_name='DocSeries')), namespaceprefix_ , eol_))
        if self.DocNumber is not None:
            namespaceprefix_ = self.DocNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.DocNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDocNumber>%s</%sDocNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DocNumber), input_name='DocNumber')), namespaceprefix_ , eol_))
        if self.DocIssueDate is not None:
            namespaceprefix_ = self.DocIssueDate_nsprefix_ + ':' if (UseCapturedNS_ and self.DocIssueDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDocIssueDate>%s</%sDocIssueDate>%s' % (namespaceprefix_ , self.gds_format_date(self.DocIssueDate, input_name='DocIssueDate'), namespaceprefix_ , eol_))
        if self.DocIssued is not None:
            namespaceprefix_ = self.DocIssued_nsprefix_ + ':' if (UseCapturedNS_ and self.DocIssued_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDocIssued>%s</%sDocIssued>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DocIssued), input_name='DocIssued')), namespaceprefix_ , eol_))
        if self.DocExpirationDate is not None:
            namespaceprefix_ = self.DocExpirationDate_nsprefix_ + ':' if (UseCapturedNS_ and self.DocExpirationDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDocExpirationDate>%s</%sDocExpirationDate>%s' % (namespaceprefix_ , self.gds_format_date(self.DocExpirationDate, input_name='DocExpirationDate'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'DocName':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DocName = obj_
            obj_.original_tagname_ = 'DocName'
        elif nodeName_ == 'DocSeries':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DocSeries')
            value_ = self.gds_validate_string(value_, node, 'DocSeries')
            self.DocSeries = value_
            self.DocSeries_nsprefix_ = child_.prefix
            # validate type string-20
            self.validate_string_20(self.DocSeries)
        elif nodeName_ == 'DocNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DocNumber')
            value_ = self.gds_validate_string(value_, node, 'DocNumber')
            self.DocNumber = value_
            self.DocNumber_nsprefix_ = child_.prefix
            # validate type string-20
            self.validate_string_20(self.DocNumber)
        elif nodeName_ == 'DocIssueDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.DocIssueDate = dval_
            self.DocIssueDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'DocIssued':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DocIssued')
            value_ = self.gds_validate_string(value_, node, 'DocIssued')
            self.DocIssued = value_
            self.DocIssued_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.DocIssued)
        elif nodeName_ == 'DocExpirationDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.DocExpirationDate = dval_
            self.DocExpirationDate_nsprefix_ = child_.prefix
# end class MedicalReportWithoutFilesType


class EduOrganizationType(GeneratedsSuper):
    """Выбранный детский сад"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, code=None, PriorityNumber=None, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.code = _cast(None, code)
        self.code_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_code')
        self.PriorityNumber = _cast(int, PriorityNumber)
        self.PriorityNumber_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_PriorityNumber')
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, EduOrganizationType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if EduOrganizationType.subclass:
            return EduOrganizationType.subclass(*args_, **kwargs_)
        else:
            return EduOrganizationType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_code(self):
        return self.code
    def set_code(self, code):
        self.code = code
    def get_PriorityNumber(self):
        return self.PriorityNumber
    def set_PriorityNumber(self, PriorityNumber):
        self.PriorityNumber = PriorityNumber
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def validate_string_50(self, value):
        # Validate type tns:string-50, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-50' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
    def hasContent_(self):
        if (
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_)
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='EduOrganizationType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('EduOrganizationType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'EduOrganizationType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='EduOrganizationType')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.convert_unicode(self.valueOf_))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='EduOrganizationType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='EduOrganizationType'):
        if self.code is not None and 'code' not in already_processed:
            already_processed.add('code')
            outfile.write(' code=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.code), input_name='code')), ))
        if self.PriorityNumber is not None and 'PriorityNumber' not in already_processed:
            already_processed.add('PriorityNumber')
            outfile.write(' PriorityNumber="%s"' % self.gds_format_integer(self.PriorityNumber, input_name='PriorityNumber'))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='EduOrganizationType', fromsubclass_=False, pretty_print=True):
        pass
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('code', node)
        if value is not None and 'code' not in already_processed:
            already_processed.add('code')
            self.code = value
            self.validate_string_50(self.code)    # validate type string-50
        value = find_attr_value_('PriorityNumber', node)
        if value is not None and 'PriorityNumber' not in already_processed:
            already_processed.add('PriorityNumber')
            self.PriorityNumber = self.gds_parse_integer(value, node, 'PriorityNumber')
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class EduOrganizationType


class EduOrganizationsType(GeneratedsSuper):
    """Выбранные детские сады"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, EduOrganization=None, AllowOfferOther=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        if EduOrganization is None:
            self.EduOrganization = []
        else:
            self.EduOrganization = EduOrganization
        self.EduOrganization_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_EduOrganization')
        self.AllowOfferOther = AllowOfferOther
        self.AllowOfferOther_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_AllowOfferOther')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, EduOrganizationsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if EduOrganizationsType.subclass:
            return EduOrganizationsType.subclass(*args_, **kwargs_)
        else:
            return EduOrganizationsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_EduOrganization(self):
        return self.EduOrganization
    def set_EduOrganization(self, EduOrganization):
        self.EduOrganization = EduOrganization
    def add_EduOrganization(self, value):
        self.EduOrganization.append(value)
    def insert_EduOrganization_at(self, index, value):
        self.EduOrganization.insert(index, value)
    def replace_EduOrganization_at(self, index, value):
        self.EduOrganization[index] = value
    def get_AllowOfferOther(self):
        return self.AllowOfferOther
    def set_AllowOfferOther(self, AllowOfferOther):
        self.AllowOfferOther = AllowOfferOther
    def hasContent_(self):
        if (
            self.EduOrganization or
            self.AllowOfferOther is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='EduOrganizationsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('EduOrganizationsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'EduOrganizationsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='EduOrganizationsType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='EduOrganizationsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='EduOrganizationsType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='EduOrganizationsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for EduOrganization_ in self.EduOrganization:
            namespaceprefix_ = self.EduOrganization_nsprefix_ + ':' if (UseCapturedNS_ and self.EduOrganization_nsprefix_) else ''
            EduOrganization_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='EduOrganization', pretty_print=pretty_print)
        if self.AllowOfferOther is not None:
            namespaceprefix_ = self.AllowOfferOther_nsprefix_ + ':' if (UseCapturedNS_ and self.AllowOfferOther_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAllowOfferOther>%s</%sAllowOfferOther>%s' % (namespaceprefix_ , self.gds_format_boolean(self.AllowOfferOther, input_name='AllowOfferOther'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'EduOrganization':
            obj_ = EduOrganizationType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.EduOrganization.append(obj_)
            obj_.original_tagname_ = 'EduOrganization'
        elif nodeName_ == 'AllowOfferOther':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'AllowOfferOther')
            ival_ = self.gds_validate_boolean(ival_, node, 'AllowOfferOther')
            self.AllowOfferOther = ival_
            self.AllowOfferOther_nsprefix_ = child_.prefix
# end class EduOrganizationsType


class BrotherSisterInfoType(GeneratedsSuper):
    """Сведения об обучении братьев или сестер ребенка в выбранных
    организациях"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ChildSurname=None, ChildName=None, ChildMiddleName=None, EduOrganization=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.ChildSurname = ChildSurname
        self.validate_string_256(self.ChildSurname)
        self.ChildSurname_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ChildSurname')
        self.ChildName = ChildName
        self.validate_string_256(self.ChildName)
        self.ChildName_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ChildName')
        self.ChildMiddleName = ChildMiddleName
        self.validate_string_256(self.ChildMiddleName)
        self.ChildMiddleName_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ChildMiddleName')
        self.EduOrganization = EduOrganization
        self.EduOrganization_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_EduOrganization')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, BrotherSisterInfoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if BrotherSisterInfoType.subclass:
            return BrotherSisterInfoType.subclass(*args_, **kwargs_)
        else:
            return BrotherSisterInfoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ChildSurname(self):
        return self.ChildSurname
    def set_ChildSurname(self, ChildSurname):
        self.ChildSurname = ChildSurname
    def get_ChildName(self):
        return self.ChildName
    def set_ChildName(self, ChildName):
        self.ChildName = ChildName
    def get_ChildMiddleName(self):
        return self.ChildMiddleName
    def set_ChildMiddleName(self, ChildMiddleName):
        self.ChildMiddleName = ChildMiddleName
    def get_EduOrganization(self):
        return self.EduOrganization
    def set_EduOrganization(self, EduOrganization):
        self.EduOrganization = EduOrganization
    def validate_string_256(self, value):
        result = True
        # Validate type string-256, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 256:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-256' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.ChildSurname is not None or
            self.ChildName is not None or
            self.ChildMiddleName is not None or
            self.EduOrganization is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='BrotherSisterInfoType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('BrotherSisterInfoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'BrotherSisterInfoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='BrotherSisterInfoType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='BrotherSisterInfoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='BrotherSisterInfoType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='BrotherSisterInfoType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ChildSurname is not None:
            namespaceprefix_ = self.ChildSurname_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildSurname_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChildSurname>%s</%sChildSurname>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ChildSurname), input_name='ChildSurname')), namespaceprefix_ , eol_))
        if self.ChildName is not None:
            namespaceprefix_ = self.ChildName_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChildName>%s</%sChildName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ChildName), input_name='ChildName')), namespaceprefix_ , eol_))
        if self.ChildMiddleName is not None:
            namespaceprefix_ = self.ChildMiddleName_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildMiddleName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChildMiddleName>%s</%sChildMiddleName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ChildMiddleName), input_name='ChildMiddleName')), namespaceprefix_ , eol_))
        if self.EduOrganization is not None:
            namespaceprefix_ = self.EduOrganization_nsprefix_ + ':' if (UseCapturedNS_ and self.EduOrganization_nsprefix_) else ''
            self.EduOrganization.export(outfile, level, namespaceprefix_, namespacedef_='', name_='EduOrganization', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ChildSurname':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChildSurname')
            value_ = self.gds_validate_string(value_, node, 'ChildSurname')
            self.ChildSurname = value_
            self.ChildSurname_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.ChildSurname)
        elif nodeName_ == 'ChildName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChildName')
            value_ = self.gds_validate_string(value_, node, 'ChildName')
            self.ChildName = value_
            self.ChildName_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.ChildName)
        elif nodeName_ == 'ChildMiddleName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChildMiddleName')
            value_ = self.gds_validate_string(value_, node, 'ChildMiddleName')
            self.ChildMiddleName = value_
            self.ChildMiddleName_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.ChildMiddleName)
        elif nodeName_ == 'EduOrganization':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.EduOrganization = obj_
            obj_.original_tagname_ = 'EduOrganization'
# end class BrotherSisterInfoType


class BenefitInfoType(GeneratedsSuper):
    """Сведения о документе, подтверждающем право на получение мер специальной
    поддержки"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, BenefitCategory=None, BenefitDocInfo=None, BenefitFile=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.BenefitCategory = BenefitCategory
        self.BenefitCategory_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_BenefitCategory')
        self.BenefitDocInfo = BenefitDocInfo
        self.BenefitDocInfo_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_BenefitDocInfo')
        if BenefitFile is None:
            self.BenefitFile = []
        else:
            self.BenefitFile = BenefitFile
        self.BenefitFile_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_BenefitFile')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, BenefitInfoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if BenefitInfoType.subclass:
            return BenefitInfoType.subclass(*args_, **kwargs_)
        else:
            return BenefitInfoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_BenefitCategory(self):
        return self.BenefitCategory
    def set_BenefitCategory(self, BenefitCategory):
        self.BenefitCategory = BenefitCategory
    def get_BenefitDocInfo(self):
        return self.BenefitDocInfo
    def set_BenefitDocInfo(self, BenefitDocInfo):
        self.BenefitDocInfo = BenefitDocInfo
    def get_BenefitFile(self):
        return self.BenefitFile
    def set_BenefitFile(self, BenefitFile):
        self.BenefitFile = BenefitFile
    def add_BenefitFile(self, value):
        self.BenefitFile.append(value)
    def insert_BenefitFile_at(self, index, value):
        self.BenefitFile.insert(index, value)
    def replace_BenefitFile_at(self, index, value):
        self.BenefitFile[index] = value
    def hasContent_(self):
        if (
            self.BenefitCategory is not None or
            self.BenefitDocInfo is not None or
            self.BenefitFile
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='BenefitInfoType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('BenefitInfoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'BenefitInfoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='BenefitInfoType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='BenefitInfoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='BenefitInfoType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='BenefitInfoType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.BenefitCategory is not None:
            namespaceprefix_ = self.BenefitCategory_nsprefix_ + ':' if (UseCapturedNS_ and self.BenefitCategory_nsprefix_) else ''
            self.BenefitCategory.export(outfile, level, namespaceprefix_, namespacedef_='', name_='BenefitCategory', pretty_print=pretty_print)
        if self.BenefitDocInfo is not None:
            namespaceprefix_ = self.BenefitDocInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.BenefitDocInfo_nsprefix_) else ''
            self.BenefitDocInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='BenefitDocInfo', pretty_print=pretty_print)
        for BenefitFile_ in self.BenefitFile:
            namespaceprefix_ = self.BenefitFile_nsprefix_ + ':' if (UseCapturedNS_ and self.BenefitFile_nsprefix_) else ''
            BenefitFile_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='BenefitFile', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'BenefitCategory':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.BenefitCategory = obj_
            obj_.original_tagname_ = 'BenefitCategory'
        elif nodeName_ == 'BenefitDocInfo':
            obj_ = DocInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.BenefitDocInfo = obj_
            obj_.original_tagname_ = 'BenefitDocInfo'
        elif nodeName_ == 'BenefitFile':
            obj_ = AppliedDocumentType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.BenefitFile.append(obj_)
            obj_.original_tagname_ = 'BenefitFile'
# end class BenefitInfoType


class BenefitInfoWithoutFilesType(GeneratedsSuper):
    """Сведения о документе, подтверждающем право на получение мер специальной
    поддержки"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, BenefitCategory=None, BenefitDocInfo=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.BenefitCategory = BenefitCategory
        self.BenefitCategory_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_BenefitCategory')
        self.BenefitDocInfo = BenefitDocInfo
        self.BenefitDocInfo_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_BenefitDocInfo')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, BenefitInfoWithoutFilesType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if BenefitInfoWithoutFilesType.subclass:
            return BenefitInfoWithoutFilesType.subclass(*args_, **kwargs_)
        else:
            return BenefitInfoWithoutFilesType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_BenefitCategory(self):
        return self.BenefitCategory
    def set_BenefitCategory(self, BenefitCategory):
        self.BenefitCategory = BenefitCategory
    def get_BenefitDocInfo(self):
        return self.BenefitDocInfo
    def set_BenefitDocInfo(self, BenefitDocInfo):
        self.BenefitDocInfo = BenefitDocInfo
    def hasContent_(self):
        if (
            self.BenefitCategory is not None or
            self.BenefitDocInfo is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='BenefitInfoWithoutFilesType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('BenefitInfoWithoutFilesType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'BenefitInfoWithoutFilesType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='BenefitInfoWithoutFilesType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='BenefitInfoWithoutFilesType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='BenefitInfoWithoutFilesType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='BenefitInfoWithoutFilesType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.BenefitCategory is not None:
            namespaceprefix_ = self.BenefitCategory_nsprefix_ + ':' if (UseCapturedNS_ and self.BenefitCategory_nsprefix_) else ''
            self.BenefitCategory.export(outfile, level, namespaceprefix_, namespacedef_='', name_='BenefitCategory', pretty_print=pretty_print)
        if self.BenefitDocInfo is not None:
            namespaceprefix_ = self.BenefitDocInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.BenefitDocInfo_nsprefix_) else ''
            self.BenefitDocInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='BenefitDocInfo', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'BenefitCategory':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.BenefitCategory = obj_
            obj_.original_tagname_ = 'BenefitCategory'
        elif nodeName_ == 'BenefitDocInfo':
            obj_ = DocInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.BenefitDocInfo = obj_
            obj_.original_tagname_ = 'BenefitDocInfo'
# end class BenefitInfoWithoutFilesType


class ApplicationType(GeneratedsSuper):
    """Подача заявления для направления в дошкольную организацию."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, orderId=None, ServicesType=None, FilingDate=None, PersonInfo=None, PersonIdentityDocInfo=None, ChildInfo=None, Address=None, EntryParams=None, AdaptationProgram=None, MedicalReport=None, EduOrganizations=None, BrotherSisterInfo=None, BenefitInfo=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.orderId = orderId
        self.orderId_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_orderId')
        self.ServicesType = ServicesType
        self.validate_stringNN_20(self.ServicesType)
        self.ServicesType_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ServicesType')
        if isinstance(FilingDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(FilingDate, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = FilingDate
        self.FilingDate = initvalue_
        self.FilingDate_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_FilingDate')
        self.PersonInfo = PersonInfo
        self.PersonInfo_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_PersonInfo')
        self.PersonIdentityDocInfo = PersonIdentityDocInfo
        self.PersonIdentityDocInfo_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_PersonIdentityDocInfo')
        self.ChildInfo = ChildInfo
        self.ChildInfo_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ChildInfo')
        self.Address = Address
        self.Address_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_Address')
        self.EntryParams = EntryParams
        self.EntryParams_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_EntryParams')
        self.AdaptationProgram = AdaptationProgram
        self.AdaptationProgram_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_AdaptationProgram')
        self.MedicalReport = MedicalReport
        self.MedicalReport_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_MedicalReport')
        self.EduOrganizations = EduOrganizations
        self.EduOrganizations_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_EduOrganizations')
        if BrotherSisterInfo is None:
            self.BrotherSisterInfo = []
        else:
            self.BrotherSisterInfo = BrotherSisterInfo
        self.BrotherSisterInfo_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_BrotherSisterInfo')
        self.BenefitInfo = BenefitInfo
        self.BenefitInfo_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_BenefitInfo')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ApplicationType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ApplicationType.subclass:
            return ApplicationType.subclass(*args_, **kwargs_)
        else:
            return ApplicationType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_orderId(self):
        return self.orderId
    def set_orderId(self, orderId):
        self.orderId = orderId
    def get_ServicesType(self):
        return self.ServicesType
    def set_ServicesType(self, ServicesType):
        self.ServicesType = ServicesType
    def get_FilingDate(self):
        return self.FilingDate
    def set_FilingDate(self, FilingDate):
        self.FilingDate = FilingDate
    def get_PersonInfo(self):
        return self.PersonInfo
    def set_PersonInfo(self, PersonInfo):
        self.PersonInfo = PersonInfo
    def get_PersonIdentityDocInfo(self):
        return self.PersonIdentityDocInfo
    def set_PersonIdentityDocInfo(self, PersonIdentityDocInfo):
        self.PersonIdentityDocInfo = PersonIdentityDocInfo
    def get_ChildInfo(self):
        return self.ChildInfo
    def set_ChildInfo(self, ChildInfo):
        self.ChildInfo = ChildInfo
    def get_Address(self):
        return self.Address
    def set_Address(self, Address):
        self.Address = Address
    def get_EntryParams(self):
        return self.EntryParams
    def set_EntryParams(self, EntryParams):
        self.EntryParams = EntryParams
    def get_AdaptationProgram(self):
        return self.AdaptationProgram
    def set_AdaptationProgram(self, AdaptationProgram):
        self.AdaptationProgram = AdaptationProgram
    def get_MedicalReport(self):
        return self.MedicalReport
    def set_MedicalReport(self, MedicalReport):
        self.MedicalReport = MedicalReport
    def get_EduOrganizations(self):
        return self.EduOrganizations
    def set_EduOrganizations(self, EduOrganizations):
        self.EduOrganizations = EduOrganizations
    def get_BrotherSisterInfo(self):
        return self.BrotherSisterInfo
    def set_BrotherSisterInfo(self, BrotherSisterInfo):
        self.BrotherSisterInfo = BrotherSisterInfo
    def add_BrotherSisterInfo(self, value):
        self.BrotherSisterInfo.append(value)
    def insert_BrotherSisterInfo_at(self, index, value):
        self.BrotherSisterInfo.insert(index, value)
    def replace_BrotherSisterInfo_at(self, index, value):
        self.BrotherSisterInfo[index] = value
    def get_BenefitInfo(self):
        return self.BenefitInfo
    def set_BenefitInfo(self, BenefitInfo):
        self.BenefitInfo = BenefitInfo
    def validate_stringNN_20(self, value):
        result = True
        # Validate type stringNN-20, a restriction on xsd:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on stringNN-20' % {"value": value, "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on stringNN-20' % {"value" : value, "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.orderId is not None or
            self.ServicesType is not None or
            self.FilingDate is not None or
            self.PersonInfo is not None or
            self.PersonIdentityDocInfo is not None or
            self.ChildInfo is not None or
            self.Address is not None or
            self.EntryParams is not None or
            self.AdaptationProgram is not None or
            self.MedicalReport is not None or
            self.EduOrganizations is not None or
            self.BrotherSisterInfo or
            self.BenefitInfo is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='ApplicationType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ApplicationType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ApplicationType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ApplicationType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ApplicationType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ApplicationType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='ApplicationType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.orderId is not None:
            namespaceprefix_ = self.orderId_nsprefix_ + ':' if (UseCapturedNS_ and self.orderId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sorderId>%s</%sorderId>%s' % (namespaceprefix_ , self.gds_format_integer(self.orderId, input_name='orderId'), namespaceprefix_ , eol_))
        if self.ServicesType is not None:
            namespaceprefix_ = self.ServicesType_nsprefix_ + ':' if (UseCapturedNS_ and self.ServicesType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sServicesType>%s</%sServicesType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ServicesType), input_name='ServicesType')), namespaceprefix_ , eol_))
        if self.FilingDate is not None:
            namespaceprefix_ = self.FilingDate_nsprefix_ + ':' if (UseCapturedNS_ and self.FilingDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFilingDate>%s</%sFilingDate>%s' % (namespaceprefix_ , self.gds_format_datetime(self.FilingDate, input_name='FilingDate'), namespaceprefix_ , eol_))
        if self.PersonInfo is not None:
            namespaceprefix_ = self.PersonInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.PersonInfo_nsprefix_) else ''
            self.PersonInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PersonInfo', pretty_print=pretty_print)
        if self.PersonIdentityDocInfo is not None:
            namespaceprefix_ = self.PersonIdentityDocInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.PersonIdentityDocInfo_nsprefix_) else ''
            self.PersonIdentityDocInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PersonIdentityDocInfo', pretty_print=pretty_print)
        if self.ChildInfo is not None:
            namespaceprefix_ = self.ChildInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildInfo_nsprefix_) else ''
            self.ChildInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ChildInfo', pretty_print=pretty_print)
        if self.Address is not None:
            namespaceprefix_ = self.Address_nsprefix_ + ':' if (UseCapturedNS_ and self.Address_nsprefix_) else ''
            self.Address.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Address', pretty_print=pretty_print)
        if self.EntryParams is not None:
            namespaceprefix_ = self.EntryParams_nsprefix_ + ':' if (UseCapturedNS_ and self.EntryParams_nsprefix_) else ''
            self.EntryParams.export(outfile, level, namespaceprefix_, namespacedef_='', name_='EntryParams', pretty_print=pretty_print)
        if self.AdaptationProgram is not None:
            namespaceprefix_ = self.AdaptationProgram_nsprefix_ + ':' if (UseCapturedNS_ and self.AdaptationProgram_nsprefix_) else ''
            self.AdaptationProgram.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AdaptationProgram', pretty_print=pretty_print)
        if self.MedicalReport is not None:
            namespaceprefix_ = self.MedicalReport_nsprefix_ + ':' if (UseCapturedNS_ and self.MedicalReport_nsprefix_) else ''
            self.MedicalReport.export(outfile, level, namespaceprefix_, namespacedef_='', name_='MedicalReport', pretty_print=pretty_print)
        if self.EduOrganizations is not None:
            namespaceprefix_ = self.EduOrganizations_nsprefix_ + ':' if (UseCapturedNS_ and self.EduOrganizations_nsprefix_) else ''
            self.EduOrganizations.export(outfile, level, namespaceprefix_, namespacedef_='', name_='EduOrganizations', pretty_print=pretty_print)
        for BrotherSisterInfo_ in self.BrotherSisterInfo:
            namespaceprefix_ = self.BrotherSisterInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.BrotherSisterInfo_nsprefix_) else ''
            BrotherSisterInfo_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='BrotherSisterInfo', pretty_print=pretty_print)
        if self.BenefitInfo is not None:
            namespaceprefix_ = self.BenefitInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.BenefitInfo_nsprefix_) else ''
            self.BenefitInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='BenefitInfo', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'orderId' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'orderId')
            ival_ = self.gds_validate_integer(ival_, node, 'orderId')
            self.orderId = ival_
            self.orderId_nsprefix_ = child_.prefix
        elif nodeName_ == 'ServicesType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ServicesType')
            value_ = self.gds_validate_string(value_, node, 'ServicesType')
            self.ServicesType = value_
            self.ServicesType_nsprefix_ = child_.prefix
            # validate type stringNN-20
            self.validate_stringNN_20(self.ServicesType)
        elif nodeName_ == 'FilingDate':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.FilingDate = dval_
            self.FilingDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'PersonInfo':
            obj_ = PersonInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PersonInfo = obj_
            obj_.original_tagname_ = 'PersonInfo'
        elif nodeName_ == 'PersonIdentityDocInfo':
            obj_ = PersonIdentityDocInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PersonIdentityDocInfo = obj_
            obj_.original_tagname_ = 'PersonIdentityDocInfo'
        elif nodeName_ == 'ChildInfo':
            obj_ = ChildInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ChildInfo = obj_
            obj_.original_tagname_ = 'ChildInfo'
        elif nodeName_ == 'Address':
            obj_ = AddressType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Address = obj_
            obj_.original_tagname_ = 'Address'
        elif nodeName_ == 'EntryParams':
            obj_ = EntryParamsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.EntryParams = obj_
            obj_.original_tagname_ = 'EntryParams'
        elif nodeName_ == 'AdaptationProgram':
            obj_ = AdaptationProgramType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AdaptationProgram = obj_
            obj_.original_tagname_ = 'AdaptationProgram'
        elif nodeName_ == 'MedicalReport':
            obj_ = MedicalReportType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.MedicalReport = obj_
            obj_.original_tagname_ = 'MedicalReport'
        elif nodeName_ == 'EduOrganizations':
            obj_ = EduOrganizationsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.EduOrganizations = obj_
            obj_.original_tagname_ = 'EduOrganizations'
        elif nodeName_ == 'BrotherSisterInfo':
            obj_ = BrotherSisterInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.BrotherSisterInfo.append(obj_)
            obj_.original_tagname_ = 'BrotherSisterInfo'
        elif nodeName_ == 'BenefitInfo':
            obj_ = BenefitInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.BenefitInfo = obj_
            obj_.original_tagname_ = 'BenefitInfo'
# end class ApplicationType


class ApplicationOrderInfoRequestType(GeneratedsSuper):
    """Подача заявления на получение информации об этапах и результатах
    оказания услуги зачисления в дошкольную организацию"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, orderId=None, ServicesType=None, PersonInfo=None, PersonIdentityDocInfo=None, ChildInfo=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.orderId = orderId
        self.orderId_nsprefix_ = None
        self.ServicesType = ServicesType
        self.validate_stringNN_20(self.ServicesType)
        self.ServicesType_nsprefix_ = None
        self.PersonInfo = PersonInfo
        self.PersonInfo_nsprefix_ = None
        self.PersonIdentityDocInfo = PersonIdentityDocInfo
        self.PersonIdentityDocInfo_nsprefix_ = None
        self.ChildInfo = ChildInfo
        self.ChildInfo_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ApplicationOrderInfoRequestType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ApplicationOrderInfoRequestType.subclass:
            return ApplicationOrderInfoRequestType.subclass(*args_, **kwargs_)
        else:
            return ApplicationOrderInfoRequestType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_orderId(self):
        return self.orderId
    def set_orderId(self, orderId):
        self.orderId = orderId
    def get_ServicesType(self):
        return self.ServicesType
    def set_ServicesType(self, ServicesType):
        self.ServicesType = ServicesType
    def get_PersonInfo(self):
        return self.PersonInfo
    def set_PersonInfo(self, PersonInfo):
        self.PersonInfo = PersonInfo
    def get_PersonIdentityDocInfo(self):
        return self.PersonIdentityDocInfo
    def set_PersonIdentityDocInfo(self, PersonIdentityDocInfo):
        self.PersonIdentityDocInfo = PersonIdentityDocInfo
    def get_ChildInfo(self):
        return self.ChildInfo
    def set_ChildInfo(self, ChildInfo):
        self.ChildInfo = ChildInfo
    def validate_stringNN_20(self, value):
        result = True
        # Validate type stringNN-20, a restriction on xsd:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on stringNN-20' % {"value": value, "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on stringNN-20' % {"value" : value, "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.orderId is not None or
            self.ServicesType is not None or
            self.PersonInfo is not None or
            self.PersonIdentityDocInfo is not None or
            self.ChildInfo is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='ApplicationOrderInfoRequestType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ApplicationOrderInfoRequestType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ApplicationOrderInfoRequestType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ApplicationOrderInfoRequestType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ApplicationOrderInfoRequestType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ApplicationOrderInfoRequestType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='ApplicationOrderInfoRequestType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.orderId is not None:
            namespaceprefix_ = self.orderId_nsprefix_ + ':' if (UseCapturedNS_ and self.orderId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sorderId>%s</%sorderId>%s' % (namespaceprefix_ , self.gds_format_integer(self.orderId, input_name='orderId'), namespaceprefix_ , eol_))
        if self.ServicesType is not None:
            namespaceprefix_ = self.ServicesType_nsprefix_ + ':' if (UseCapturedNS_ and self.ServicesType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sServicesType>%s</%sServicesType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ServicesType), input_name='ServicesType')), namespaceprefix_ , eol_))
        if self.PersonInfo is not None:
            namespaceprefix_ = self.PersonInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.PersonInfo_nsprefix_) else ''
            self.PersonInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PersonInfo', pretty_print=pretty_print)
        if self.PersonIdentityDocInfo is not None:
            namespaceprefix_ = self.PersonIdentityDocInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.PersonIdentityDocInfo_nsprefix_) else ''
            self.PersonIdentityDocInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PersonIdentityDocInfo', pretty_print=pretty_print)
        if self.ChildInfo is not None:
            namespaceprefix_ = self.ChildInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildInfo_nsprefix_) else ''
            self.ChildInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ChildInfo', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'orderId' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'orderId')
            ival_ = self.gds_validate_integer(ival_, node, 'orderId')
            self.orderId = ival_
            self.orderId_nsprefix_ = child_.prefix
        elif nodeName_ == 'ServicesType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ServicesType')
            value_ = self.gds_validate_string(value_, node, 'ServicesType')
            self.ServicesType = value_
            self.ServicesType_nsprefix_ = child_.prefix
            # validate type stringNN-20
            self.validate_stringNN_20(self.ServicesType)
        elif nodeName_ == 'PersonInfo':
            obj_ = PersonInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PersonInfo = obj_
            obj_.original_tagname_ = 'PersonInfo'
        elif nodeName_ == 'PersonIdentityDocInfo':
            obj_ = PersonIdentityDocInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PersonIdentityDocInfo = obj_
            obj_.original_tagname_ = 'PersonIdentityDocInfo'
        elif nodeName_ == 'ChildInfo':
            obj_ = ChildInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ChildInfo = obj_
            obj_.original_tagname_ = 'ChildInfo'
# end class ApplicationOrderInfoRequestType


class Person2InfoType(GeneratedsSuper):
    """Сведения о 2-м родителе"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Person2Surname=None, Person2Name=None, Person2MiddleName=None, Person2Phone=None, Person2Email=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.Person2Surname = Person2Surname
        self.validate_string_256(self.Person2Surname)
        self.Person2Surname_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_Person2Surname')
        self.Person2Name = Person2Name
        self.validate_string_256(self.Person2Name)
        self.Person2Name_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_Person2Name')
        self.Person2MiddleName = Person2MiddleName
        self.validate_string_256(self.Person2MiddleName)
        self.Person2MiddleName_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_Person2MiddleName')
        self.Person2Phone = Person2Phone
        self.validate_string_14(self.Person2Phone)
        self.Person2Phone_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_Person2Phone')
        self.Person2Email = Person2Email
        self.validate_string_256(self.Person2Email)
        self.Person2Email_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_Person2Email')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Person2InfoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Person2InfoType.subclass:
            return Person2InfoType.subclass(*args_, **kwargs_)
        else:
            return Person2InfoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Person2Surname(self):
        return self.Person2Surname
    def set_Person2Surname(self, Person2Surname):
        self.Person2Surname = Person2Surname
    def get_Person2Name(self):
        return self.Person2Name
    def set_Person2Name(self, Person2Name):
        self.Person2Name = Person2Name
    def get_Person2MiddleName(self):
        return self.Person2MiddleName
    def set_Person2MiddleName(self, Person2MiddleName):
        self.Person2MiddleName = Person2MiddleName
    def get_Person2Phone(self):
        return self.Person2Phone
    def set_Person2Phone(self, Person2Phone):
        self.Person2Phone = Person2Phone
    def get_Person2Email(self):
        return self.Person2Email
    def set_Person2Email(self, Person2Email):
        self.Person2Email = Person2Email
    def validate_string_256(self, value):
        result = True
        # Validate type string-256, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 256:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-256' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_string_14(self, value):
        result = True
        # Validate type string-14, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 14:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-14' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Person2Surname is not None or
            self.Person2Name is not None or
            self.Person2MiddleName is not None or
            self.Person2Phone is not None or
            self.Person2Email is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='Person2InfoType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Person2InfoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Person2InfoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Person2InfoType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Person2InfoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Person2InfoType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='Person2InfoType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Person2Surname is not None:
            namespaceprefix_ = self.Person2Surname_nsprefix_ + ':' if (UseCapturedNS_ and self.Person2Surname_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPerson2Surname>%s</%sPerson2Surname>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Person2Surname), input_name='Person2Surname')), namespaceprefix_ , eol_))
        if self.Person2Name is not None:
            namespaceprefix_ = self.Person2Name_nsprefix_ + ':' if (UseCapturedNS_ and self.Person2Name_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPerson2Name>%s</%sPerson2Name>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Person2Name), input_name='Person2Name')), namespaceprefix_ , eol_))
        if self.Person2MiddleName is not None:
            namespaceprefix_ = self.Person2MiddleName_nsprefix_ + ':' if (UseCapturedNS_ and self.Person2MiddleName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPerson2MiddleName>%s</%sPerson2MiddleName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Person2MiddleName), input_name='Person2MiddleName')), namespaceprefix_ , eol_))
        if self.Person2Phone is not None:
            namespaceprefix_ = self.Person2Phone_nsprefix_ + ':' if (UseCapturedNS_ and self.Person2Phone_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPerson2Phone>%s</%sPerson2Phone>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Person2Phone), input_name='Person2Phone')), namespaceprefix_ , eol_))
        if self.Person2Email is not None:
            namespaceprefix_ = self.Person2Email_nsprefix_ + ':' if (UseCapturedNS_ and self.Person2Email_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPerson2Email>%s</%sPerson2Email>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Person2Email), input_name='Person2Email')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Person2Surname':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Person2Surname')
            value_ = self.gds_validate_string(value_, node, 'Person2Surname')
            self.Person2Surname = value_
            self.Person2Surname_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.Person2Surname)
        elif nodeName_ == 'Person2Name':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Person2Name')
            value_ = self.gds_validate_string(value_, node, 'Person2Name')
            self.Person2Name = value_
            self.Person2Name_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.Person2Name)
        elif nodeName_ == 'Person2MiddleName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Person2MiddleName')
            value_ = self.gds_validate_string(value_, node, 'Person2MiddleName')
            self.Person2MiddleName = value_
            self.Person2MiddleName_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.Person2MiddleName)
        elif nodeName_ == 'Person2Phone':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Person2Phone')
            value_ = self.gds_validate_string(value_, node, 'Person2Phone')
            self.Person2Phone = value_
            self.Person2Phone_nsprefix_ = child_.prefix
            # validate type string-14
            self.validate_string_14(self.Person2Phone)
        elif nodeName_ == 'Person2Email':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Person2Email')
            value_ = self.gds_validate_string(value_, node, 'Person2Email')
            self.Person2Email = value_
            self.Person2Email_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.Person2Email)
# end class Person2InfoType


class ApplicationAdmissionRequestType(GeneratedsSuper):
    """Подача заявления о приёме в дошкольную организацию"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, orderId=None, ServicesType=None, PersonInfo=None, PersonIdentityDocInfo=None, Person2Info=None, ChildInfo=None, Address=None, EntryParams=None, AdaptationProgram=None, MedicalReport=None, EduOrganizationCode=None, DocListReview=None, LicenseCharter=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.orderId = orderId
        self.orderId_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_orderId')
        self.ServicesType = ServicesType
        self.validate_stringNN_20(self.ServicesType)
        self.ServicesType_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ServicesType')
        self.PersonInfo = PersonInfo
        self.PersonInfo_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_PersonInfo')
        self.PersonIdentityDocInfo = PersonIdentityDocInfo
        self.PersonIdentityDocInfo_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_PersonIdentityDocInfo')
        self.Person2Info = Person2Info
        self.Person2Info_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_Person2Info')
        self.ChildInfo = ChildInfo
        self.ChildInfo_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ChildInfo')
        self.Address = Address
        self.Address_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_Address')
        self.EntryParams = EntryParams
        self.EntryParams_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_EntryParams')
        self.AdaptationProgram = AdaptationProgram
        self.AdaptationProgram_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_AdaptationProgram')
        self.MedicalReport = MedicalReport
        self.MedicalReport_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_MedicalReport')
        self.EduOrganizationCode = EduOrganizationCode
        self.validate_string_50(self.EduOrganizationCode)
        self.EduOrganizationCode_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_EduOrganizationCode')
        self.DocListReview = DocListReview
        self.DocListReview_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_DocListReview')
        self.LicenseCharter = LicenseCharter
        self.LicenseCharter_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_LicenseCharter')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ApplicationAdmissionRequestType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ApplicationAdmissionRequestType.subclass:
            return ApplicationAdmissionRequestType.subclass(*args_, **kwargs_)
        else:
            return ApplicationAdmissionRequestType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_orderId(self):
        return self.orderId
    def set_orderId(self, orderId):
        self.orderId = orderId
    def get_ServicesType(self):
        return self.ServicesType
    def set_ServicesType(self, ServicesType):
        self.ServicesType = ServicesType
    def get_PersonInfo(self):
        return self.PersonInfo
    def set_PersonInfo(self, PersonInfo):
        self.PersonInfo = PersonInfo
    def get_PersonIdentityDocInfo(self):
        return self.PersonIdentityDocInfo
    def set_PersonIdentityDocInfo(self, PersonIdentityDocInfo):
        self.PersonIdentityDocInfo = PersonIdentityDocInfo
    def get_Person2Info(self):
        return self.Person2Info
    def set_Person2Info(self, Person2Info):
        self.Person2Info = Person2Info
    def get_ChildInfo(self):
        return self.ChildInfo
    def set_ChildInfo(self, ChildInfo):
        self.ChildInfo = ChildInfo
    def get_Address(self):
        return self.Address
    def set_Address(self, Address):
        self.Address = Address
    def get_EntryParams(self):
        return self.EntryParams
    def set_EntryParams(self, EntryParams):
        self.EntryParams = EntryParams
    def get_AdaptationProgram(self):
        return self.AdaptationProgram
    def set_AdaptationProgram(self, AdaptationProgram):
        self.AdaptationProgram = AdaptationProgram
    def get_MedicalReport(self):
        return self.MedicalReport
    def set_MedicalReport(self, MedicalReport):
        self.MedicalReport = MedicalReport
    def get_EduOrganizationCode(self):
        return self.EduOrganizationCode
    def set_EduOrganizationCode(self, EduOrganizationCode):
        self.EduOrganizationCode = EduOrganizationCode
    def get_DocListReview(self):
        return self.DocListReview
    def set_DocListReview(self, DocListReview):
        self.DocListReview = DocListReview
    def get_LicenseCharter(self):
        return self.LicenseCharter
    def set_LicenseCharter(self, LicenseCharter):
        self.LicenseCharter = LicenseCharter
    def validate_stringNN_20(self, value):
        result = True
        # Validate type stringNN-20, a restriction on xsd:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on stringNN-20' % {"value": value, "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on stringNN-20' % {"value" : value, "lineno": lineno} )
                result = False
        return result
    def validate_string_50(self, value):
        result = True
        # Validate type string-50, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-50' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.orderId is not None or
            self.ServicesType is not None or
            self.PersonInfo is not None or
            self.PersonIdentityDocInfo is not None or
            self.Person2Info is not None or
            self.ChildInfo is not None or
            self.Address is not None or
            self.EntryParams is not None or
            self.AdaptationProgram is not None or
            self.MedicalReport is not None or
            self.EduOrganizationCode is not None or
            self.DocListReview is not None or
            self.LicenseCharter is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='ApplicationAdmissionRequestType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ApplicationAdmissionRequestType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ApplicationAdmissionRequestType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ApplicationAdmissionRequestType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ApplicationAdmissionRequestType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ApplicationAdmissionRequestType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='ApplicationAdmissionRequestType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.orderId is not None:
            namespaceprefix_ = self.orderId_nsprefix_ + ':' if (UseCapturedNS_ and self.orderId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sorderId>%s</%sorderId>%s' % (namespaceprefix_ , self.gds_format_integer(self.orderId, input_name='orderId'), namespaceprefix_ , eol_))
        if self.ServicesType is not None:
            namespaceprefix_ = self.ServicesType_nsprefix_ + ':' if (UseCapturedNS_ and self.ServicesType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sServicesType>%s</%sServicesType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ServicesType), input_name='ServicesType')), namespaceprefix_ , eol_))
        if self.PersonInfo is not None:
            namespaceprefix_ = self.PersonInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.PersonInfo_nsprefix_) else ''
            self.PersonInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PersonInfo', pretty_print=pretty_print)
        if self.PersonIdentityDocInfo is not None:
            namespaceprefix_ = self.PersonIdentityDocInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.PersonIdentityDocInfo_nsprefix_) else ''
            self.PersonIdentityDocInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PersonIdentityDocInfo', pretty_print=pretty_print)
        if self.Person2Info is not None:
            namespaceprefix_ = self.Person2Info_nsprefix_ + ':' if (UseCapturedNS_ and self.Person2Info_nsprefix_) else ''
            self.Person2Info.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Person2Info', pretty_print=pretty_print)
        if self.ChildInfo is not None:
            namespaceprefix_ = self.ChildInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildInfo_nsprefix_) else ''
            self.ChildInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ChildInfo', pretty_print=pretty_print)
        if self.Address is not None:
            namespaceprefix_ = self.Address_nsprefix_ + ':' if (UseCapturedNS_ and self.Address_nsprefix_) else ''
            self.Address.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Address', pretty_print=pretty_print)
        if self.EntryParams is not None:
            namespaceprefix_ = self.EntryParams_nsprefix_ + ':' if (UseCapturedNS_ and self.EntryParams_nsprefix_) else ''
            self.EntryParams.export(outfile, level, namespaceprefix_, namespacedef_='', name_='EntryParams', pretty_print=pretty_print)
        if self.AdaptationProgram is not None:
            namespaceprefix_ = self.AdaptationProgram_nsprefix_ + ':' if (UseCapturedNS_ and self.AdaptationProgram_nsprefix_) else ''
            self.AdaptationProgram.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AdaptationProgram', pretty_print=pretty_print)
        if self.MedicalReport is not None:
            namespaceprefix_ = self.MedicalReport_nsprefix_ + ':' if (UseCapturedNS_ and self.MedicalReport_nsprefix_) else ''
            self.MedicalReport.export(outfile, level, namespaceprefix_, namespacedef_='', name_='MedicalReport', pretty_print=pretty_print)
        if self.EduOrganizationCode is not None:
            namespaceprefix_ = self.EduOrganizationCode_nsprefix_ + ':' if (UseCapturedNS_ and self.EduOrganizationCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEduOrganizationCode>%s</%sEduOrganizationCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EduOrganizationCode), input_name='EduOrganizationCode')), namespaceprefix_ , eol_))
        if self.DocListReview is not None:
            namespaceprefix_ = self.DocListReview_nsprefix_ + ':' if (UseCapturedNS_ and self.DocListReview_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDocListReview>%s</%sDocListReview>%s' % (namespaceprefix_ , self.gds_format_boolean(self.DocListReview, input_name='DocListReview'), namespaceprefix_ , eol_))
        if self.LicenseCharter is not None:
            namespaceprefix_ = self.LicenseCharter_nsprefix_ + ':' if (UseCapturedNS_ and self.LicenseCharter_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLicenseCharter>%s</%sLicenseCharter>%s' % (namespaceprefix_ , self.gds_format_boolean(self.LicenseCharter, input_name='LicenseCharter'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'orderId' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'orderId')
            ival_ = self.gds_validate_integer(ival_, node, 'orderId')
            self.orderId = ival_
            self.orderId_nsprefix_ = child_.prefix
        elif nodeName_ == 'ServicesType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ServicesType')
            value_ = self.gds_validate_string(value_, node, 'ServicesType')
            self.ServicesType = value_
            self.ServicesType_nsprefix_ = child_.prefix
            # validate type stringNN-20
            self.validate_stringNN_20(self.ServicesType)
        elif nodeName_ == 'PersonInfo':
            obj_ = PersonInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PersonInfo = obj_
            obj_.original_tagname_ = 'PersonInfo'
        elif nodeName_ == 'PersonIdentityDocInfo':
            obj_ = PersonIdentityDocInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PersonIdentityDocInfo = obj_
            obj_.original_tagname_ = 'PersonIdentityDocInfo'
        elif nodeName_ == 'Person2Info':
            obj_ = Person2InfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Person2Info = obj_
            obj_.original_tagname_ = 'Person2Info'
        elif nodeName_ == 'ChildInfo':
            obj_ = ChildInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ChildInfo = obj_
            obj_.original_tagname_ = 'ChildInfo'
        elif nodeName_ == 'Address':
            obj_ = AddressType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Address = obj_
            obj_.original_tagname_ = 'Address'
        elif nodeName_ == 'EntryParams':
            obj_ = EntryParamsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.EntryParams = obj_
            obj_.original_tagname_ = 'EntryParams'
        elif nodeName_ == 'AdaptationProgram':
            obj_ = AdaptationProgramType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AdaptationProgram = obj_
            obj_.original_tagname_ = 'AdaptationProgram'
        elif nodeName_ == 'MedicalReport':
            obj_ = MedicalReportType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.MedicalReport = obj_
            obj_.original_tagname_ = 'MedicalReport'
        elif nodeName_ == 'EduOrganizationCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EduOrganizationCode')
            value_ = self.gds_validate_string(value_, node, 'EduOrganizationCode')
            self.EduOrganizationCode = value_
            self.EduOrganizationCode_nsprefix_ = child_.prefix
            # validate type string-50
            self.validate_string_50(self.EduOrganizationCode)
        elif nodeName_ == 'DocListReview':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'DocListReview')
            ival_ = self.gds_validate_boolean(ival_, node, 'DocListReview')
            self.DocListReview = ival_
            self.DocListReview_nsprefix_ = child_.prefix
        elif nodeName_ == 'LicenseCharter':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'LicenseCharter')
            ival_ = self.gds_validate_boolean(ival_, node, 'LicenseCharter')
            self.LicenseCharter = ival_
            self.LicenseCharter_nsprefix_ = child_.prefix
# end class ApplicationAdmissionRequestType


class GetApplicationQueueRequestType(GeneratedsSuper):
    """Получение данных о последовательности предоставления мест"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, orderId=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.orderId = orderId
        self.orderId_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_orderId')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetApplicationQueueRequestType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetApplicationQueueRequestType.subclass:
            return GetApplicationQueueRequestType.subclass(*args_, **kwargs_)
        else:
            return GetApplicationQueueRequestType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_orderId(self):
        return self.orderId
    def set_orderId(self, orderId):
        self.orderId = orderId
    def hasContent_(self):
        if (
            self.orderId is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='GetApplicationQueueRequestType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetApplicationQueueRequestType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetApplicationQueueRequestType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetApplicationQueueRequestType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetApplicationQueueRequestType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetApplicationQueueRequestType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='GetApplicationQueueRequestType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.orderId is not None:
            namespaceprefix_ = self.orderId_nsprefix_ + ':' if (UseCapturedNS_ and self.orderId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sorderId>%s</%sorderId>%s' % (namespaceprefix_ , self.gds_format_integer(self.orderId, input_name='orderId'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'orderId' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'orderId')
            ival_ = self.gds_validate_integer(ival_, node, 'orderId')
            self.orderId = ival_
            self.orderId_nsprefix_ = child_.prefix
# end class GetApplicationQueueRequestType


class GetApplicationQueueReasonRequestType(GeneratedsSuper):
    """Получение информации об основаниях изменений последовательности"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, orderId=None, PeriodStart=None, PeriodEnd=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.orderId = orderId
        self.orderId_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_orderId')
        if isinstance(PeriodStart, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(PeriodStart, '%Y-%m-%d').date()
        else:
            initvalue_ = PeriodStart
        self.PeriodStart = initvalue_
        self.PeriodStart_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_PeriodStart')
        if isinstance(PeriodEnd, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(PeriodEnd, '%Y-%m-%d').date()
        else:
            initvalue_ = PeriodEnd
        self.PeriodEnd = initvalue_
        self.PeriodEnd_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_PeriodEnd')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetApplicationQueueReasonRequestType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetApplicationQueueReasonRequestType.subclass:
            return GetApplicationQueueReasonRequestType.subclass(*args_, **kwargs_)
        else:
            return GetApplicationQueueReasonRequestType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_orderId(self):
        return self.orderId
    def set_orderId(self, orderId):
        self.orderId = orderId
    def get_PeriodStart(self):
        return self.PeriodStart
    def set_PeriodStart(self, PeriodStart):
        self.PeriodStart = PeriodStart
    def get_PeriodEnd(self):
        return self.PeriodEnd
    def set_PeriodEnd(self, PeriodEnd):
        self.PeriodEnd = PeriodEnd
    def hasContent_(self):
        if (
            self.orderId is not None or
            self.PeriodStart is not None or
            self.PeriodEnd is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='GetApplicationQueueReasonRequestType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetApplicationQueueReasonRequestType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetApplicationQueueReasonRequestType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetApplicationQueueReasonRequestType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetApplicationQueueReasonRequestType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetApplicationQueueReasonRequestType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='GetApplicationQueueReasonRequestType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.orderId is not None:
            namespaceprefix_ = self.orderId_nsprefix_ + ':' if (UseCapturedNS_ and self.orderId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sorderId>%s</%sorderId>%s' % (namespaceprefix_ , self.gds_format_integer(self.orderId, input_name='orderId'), namespaceprefix_ , eol_))
        if self.PeriodStart is not None:
            namespaceprefix_ = self.PeriodStart_nsprefix_ + ':' if (UseCapturedNS_ and self.PeriodStart_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPeriodStart>%s</%sPeriodStart>%s' % (namespaceprefix_ , self.gds_format_date(self.PeriodStart, input_name='PeriodStart'), namespaceprefix_ , eol_))
        if self.PeriodEnd is not None:
            namespaceprefix_ = self.PeriodEnd_nsprefix_ + ':' if (UseCapturedNS_ and self.PeriodEnd_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPeriodEnd>%s</%sPeriodEnd>%s' % (namespaceprefix_ , self.gds_format_date(self.PeriodEnd, input_name='PeriodEnd'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'orderId' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'orderId')
            ival_ = self.gds_validate_integer(ival_, node, 'orderId')
            self.orderId = ival_
            self.orderId_nsprefix_ = child_.prefix
        elif nodeName_ == 'PeriodStart':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.PeriodStart = dval_
            self.PeriodStart_nsprefix_ = child_.prefix
        elif nodeName_ == 'PeriodEnd':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.PeriodEnd = dval_
            self.PeriodEnd_nsprefix_ = child_.prefix
# end class GetApplicationQueueReasonRequestType


class GetApplicationRequestType(GeneratedsSuper):
    """Запрос для получения данных заявления"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, orderId=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.orderId = orderId
        self.orderId_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_orderId')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetApplicationRequestType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetApplicationRequestType.subclass:
            return GetApplicationRequestType.subclass(*args_, **kwargs_)
        else:
            return GetApplicationRequestType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_orderId(self):
        return self.orderId
    def set_orderId(self, orderId):
        self.orderId = orderId
    def hasContent_(self):
        if (
            self.orderId is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='GetApplicationRequestType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetApplicationRequestType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetApplicationRequestType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetApplicationRequestType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetApplicationRequestType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetApplicationRequestType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='GetApplicationRequestType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.orderId is not None:
            namespaceprefix_ = self.orderId_nsprefix_ + ':' if (UseCapturedNS_ and self.orderId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sorderId>%s</%sorderId>%s' % (namespaceprefix_ , self.gds_format_integer(self.orderId, input_name='orderId'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'orderId' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'orderId')
            ival_ = self.gds_validate_integer(ival_, node, 'orderId')
            self.orderId = ival_
            self.orderId_nsprefix_ = child_.prefix
# end class GetApplicationRequestType


class GetApplicationAdmissionRequestType(GeneratedsSuper):
    """Запрос для получения данных для подачи заявления на приём"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, orderId=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.orderId = orderId
        self.orderId_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_orderId')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetApplicationAdmissionRequestType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetApplicationAdmissionRequestType.subclass:
            return GetApplicationAdmissionRequestType.subclass(*args_, **kwargs_)
        else:
            return GetApplicationAdmissionRequestType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_orderId(self):
        return self.orderId
    def set_orderId(self, orderId):
        self.orderId = orderId
    def hasContent_(self):
        if (
            self.orderId is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='GetApplicationAdmissionRequestType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetApplicationAdmissionRequestType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetApplicationAdmissionRequestType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetApplicationAdmissionRequestType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetApplicationAdmissionRequestType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetApplicationAdmissionRequestType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='GetApplicationAdmissionRequestType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.orderId is not None:
            namespaceprefix_ = self.orderId_nsprefix_ + ':' if (UseCapturedNS_ and self.orderId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sorderId>%s</%sorderId>%s' % (namespaceprefix_ , self.gds_format_integer(self.orderId, input_name='orderId'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'orderId' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'orderId')
            ival_ = self.gds_validate_integer(ival_, node, 'orderId')
            self.orderId = ival_
            self.orderId_nsprefix_ = child_.prefix
# end class GetApplicationAdmissionRequestType


class ApplicationRejectionRequestType(GeneratedsSuper):
    """Отказ от предложенной дошкольной организации"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, orderId=None, comment=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.orderId = orderId
        self.orderId_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_orderId')
        self.comment = comment
        self.validate_string_2048(self.comment)
        self.comment_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_comment')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ApplicationRejectionRequestType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ApplicationRejectionRequestType.subclass:
            return ApplicationRejectionRequestType.subclass(*args_, **kwargs_)
        else:
            return ApplicationRejectionRequestType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_orderId(self):
        return self.orderId
    def set_orderId(self, orderId):
        self.orderId = orderId
    def get_comment(self):
        return self.comment
    def set_comment(self, comment):
        self.comment = comment
    def validate_string_2048(self, value):
        result = True
        # Validate type string-2048, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 2048:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-2048' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.orderId is not None or
            self.comment is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='ApplicationRejectionRequestType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ApplicationRejectionRequestType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ApplicationRejectionRequestType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ApplicationRejectionRequestType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ApplicationRejectionRequestType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ApplicationRejectionRequestType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='ApplicationRejectionRequestType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.orderId is not None:
            namespaceprefix_ = self.orderId_nsprefix_ + ':' if (UseCapturedNS_ and self.orderId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sorderId>%s</%sorderId>%s' % (namespaceprefix_ , self.gds_format_integer(self.orderId, input_name='orderId'), namespaceprefix_ , eol_))
        if self.comment is not None:
            namespaceprefix_ = self.comment_nsprefix_ + ':' if (UseCapturedNS_ and self.comment_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scomment>%s</%scomment>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.comment), input_name='comment')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'orderId' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'orderId')
            ival_ = self.gds_validate_integer(ival_, node, 'orderId')
            self.orderId = ival_
            self.orderId_nsprefix_ = child_.prefix
        elif nodeName_ == 'comment':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'comment')
            value_ = self.gds_validate_string(value_, node, 'comment')
            self.comment = value_
            self.comment_nsprefix_ = child_.prefix
            # validate type string-2048
            self.validate_string_2048(self.comment)
# end class ApplicationRejectionRequestType


class cancelRequestType(GeneratedsSuper):
    """Запрос на отмену заявления для направления"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, orderId=None, reason=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.orderId = orderId
        self.orderId_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_orderId')
        self.reason = reason
        self.validate_string_2048(self.reason)
        self.reason_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_reason')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, cancelRequestType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if cancelRequestType.subclass:
            return cancelRequestType.subclass(*args_, **kwargs_)
        else:
            return cancelRequestType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_orderId(self):
        return self.orderId
    def set_orderId(self, orderId):
        self.orderId = orderId
    def get_reason(self):
        return self.reason
    def set_reason(self, reason):
        self.reason = reason
    def validate_string_2048(self, value):
        result = True
        # Validate type string-2048, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 2048:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-2048' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.orderId is not None or
            self.reason is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='cancelRequestType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('cancelRequestType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'cancelRequestType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='cancelRequestType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='cancelRequestType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='cancelRequestType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='cancelRequestType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.orderId is not None:
            namespaceprefix_ = self.orderId_nsprefix_ + ':' if (UseCapturedNS_ and self.orderId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sorderId>%s</%sorderId>%s' % (namespaceprefix_ , self.gds_format_integer(self.orderId, input_name='orderId'), namespaceprefix_ , eol_))
        if self.reason is not None:
            namespaceprefix_ = self.reason_nsprefix_ + ':' if (UseCapturedNS_ and self.reason_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sreason>%s</%sreason>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.reason), input_name='reason')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'orderId' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'orderId')
            ival_ = self.gds_validate_integer(ival_, node, 'orderId')
            self.orderId = ival_
            self.orderId_nsprefix_ = child_.prefix
        elif nodeName_ == 'reason':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'reason')
            value_ = self.gds_validate_string(value_, node, 'reason')
            self.reason = value_
            self.reason_nsprefix_ = child_.prefix
            # validate type string-2048
            self.validate_string_2048(self.reason)
# end class cancelRequestType


class orderIdType(GeneratedsSuper):
    """Номер заявки в ЛК ЕПГУ"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, pguId=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.pguId = pguId
        self.pguId_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_pguId')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, orderIdType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if orderIdType.subclass:
            return orderIdType.subclass(*args_, **kwargs_)
        else:
            return orderIdType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_pguId(self):
        return self.pguId
    def set_pguId(self, pguId):
        self.pguId = pguId
    def hasContent_(self):
        if (
            self.pguId is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='orderIdType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('orderIdType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'orderIdType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='orderIdType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='orderIdType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='orderIdType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='orderIdType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.pguId is not None:
            namespaceprefix_ = self.pguId_nsprefix_ + ':' if (UseCapturedNS_ and self.pguId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spguId>%s</%spguId>%s' % (namespaceprefix_ , self.gds_format_integer(self.pguId, input_name='pguId'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'pguId' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'pguId')
            ival_ = self.gds_validate_integer(ival_, node, 'pguId')
            self.pguId = ival_
            self.pguId_nsprefix_ = child_.prefix
# end class orderIdType


class statusCodeType(GeneratedsSuper):
    """Статус заявления"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, orgCode=None, techCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.orgCode = orgCode
        self.validate_string_50(self.orgCode)
        self.orgCode_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_orgCode')
        self.techCode = techCode
        self.techCode_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_techCode')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, statusCodeType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if statusCodeType.subclass:
            return statusCodeType.subclass(*args_, **kwargs_)
        else:
            return statusCodeType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_orgCode(self):
        return self.orgCode
    def set_orgCode(self, orgCode):
        self.orgCode = orgCode
    def get_techCode(self):
        return self.techCode
    def set_techCode(self, techCode):
        self.techCode = techCode
    def validate_string_50(self, value):
        result = True
        # Validate type string-50, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-50' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.orgCode is not None or
            self.techCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='statusCodeType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('statusCodeType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'statusCodeType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='statusCodeType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='statusCodeType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='statusCodeType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='statusCodeType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.orgCode is not None:
            namespaceprefix_ = self.orgCode_nsprefix_ + ':' if (UseCapturedNS_ and self.orgCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sorgCode>%s</%sorgCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.orgCode), input_name='orgCode')), namespaceprefix_ , eol_))
        if self.techCode is not None:
            namespaceprefix_ = self.techCode_nsprefix_ + ':' if (UseCapturedNS_ and self.techCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stechCode>%s</%stechCode>%s' % (namespaceprefix_ , self.gds_format_integer(self.techCode, input_name='techCode'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'orgCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'orgCode')
            value_ = self.gds_validate_string(value_, node, 'orgCode')
            self.orgCode = value_
            self.orgCode_nsprefix_ = child_.prefix
            # validate type string-50
            self.validate_string_50(self.orgCode)
        elif nodeName_ == 'techCode' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'techCode')
            ival_ = self.gds_validate_integer(ival_, node, 'techCode')
            self.techCode = ival_
            self.techCode_nsprefix_ = child_.prefix
# end class statusCodeType


class changeOrderInfoType(GeneratedsSuper):
    """Информация для изменения статуса заявления для направления в ЛК ЕПГУ"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, orderId=None, statusCode=None, comment=None, cancelAllowed=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.orderId = orderId
        self.orderId_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_orderId')
        self.statusCode = statusCode
        self.statusCode_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_statusCode')
        self.comment = comment
        self.validate_string_2048(self.comment)
        self.comment_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_comment')
        self.cancelAllowed = cancelAllowed
        self.cancelAllowed_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_cancelAllowed')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, changeOrderInfoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if changeOrderInfoType.subclass:
            return changeOrderInfoType.subclass(*args_, **kwargs_)
        else:
            return changeOrderInfoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_orderId(self):
        return self.orderId
    def set_orderId(self, orderId):
        self.orderId = orderId
    def get_statusCode(self):
        return self.statusCode
    def set_statusCode(self, statusCode):
        self.statusCode = statusCode
    def get_comment(self):
        return self.comment
    def set_comment(self, comment):
        self.comment = comment
    def get_cancelAllowed(self):
        return self.cancelAllowed
    def set_cancelAllowed(self, cancelAllowed):
        self.cancelAllowed = cancelAllowed
    def validate_string_2048(self, value):
        result = True
        # Validate type string-2048, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 2048:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-2048' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.orderId is not None or
            self.statusCode is not None or
            self.comment is not None or
            self.cancelAllowed is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='changeOrderInfoType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('changeOrderInfoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'changeOrderInfoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='changeOrderInfoType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='changeOrderInfoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='changeOrderInfoType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='changeOrderInfoType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.orderId is not None:
            namespaceprefix_ = self.orderId_nsprefix_ + ':' if (UseCapturedNS_ and self.orderId_nsprefix_) else ''
            self.orderId.export(outfile, level, namespaceprefix_, namespacedef_='', name_='orderId', pretty_print=pretty_print)
        if self.statusCode is not None:
            namespaceprefix_ = self.statusCode_nsprefix_ + ':' if (UseCapturedNS_ and self.statusCode_nsprefix_) else ''
            self.statusCode.export(outfile, level, namespaceprefix_, namespacedef_='', name_='statusCode', pretty_print=pretty_print)
        if self.comment is not None:
            namespaceprefix_ = self.comment_nsprefix_ + ':' if (UseCapturedNS_ and self.comment_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scomment>%s</%scomment>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.comment), input_name='comment')), namespaceprefix_ , eol_))
        if self.cancelAllowed is not None:
            namespaceprefix_ = self.cancelAllowed_nsprefix_ + ':' if (UseCapturedNS_ and self.cancelAllowed_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scancelAllowed>%s</%scancelAllowed>%s' % (namespaceprefix_ , self.gds_format_boolean(self.cancelAllowed, input_name='cancelAllowed'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'orderId':
            obj_ = orderIdType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.orderId = obj_
            obj_.original_tagname_ = 'orderId'
        elif nodeName_ == 'statusCode':
            obj_ = statusCodeType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.statusCode = obj_
            obj_.original_tagname_ = 'statusCode'
        elif nodeName_ == 'comment':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'comment')
            value_ = self.gds_validate_string(value_, node, 'comment')
            self.comment = value_
            self.comment_nsprefix_ = child_.prefix
            # validate type string-2048
            self.validate_string_2048(self.comment)
        elif nodeName_ == 'cancelAllowed':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'cancelAllowed')
            ival_ = self.gds_validate_boolean(ival_, node, 'cancelAllowed')
            self.cancelAllowed = ival_
            self.cancelAllowed_nsprefix_ = child_.prefix
# end class changeOrderInfoType


class ApplicationQueueResponseType(GeneratedsSuper):
    """Данные о позиции при распределении"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, orderId=None, Position=None, Total=None, WithoutQueue=None, FirstQueue=None, AdvantageQueue=None, RelevantDT=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.orderId = orderId
        self.orderId_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_orderId')
        self.Position = Position
        self.Position_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_Position')
        self.Total = Total
        self.Total_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_Total')
        self.WithoutQueue = WithoutQueue
        self.WithoutQueue_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_WithoutQueue')
        self.FirstQueue = FirstQueue
        self.FirstQueue_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_FirstQueue')
        self.AdvantageQueue = AdvantageQueue
        self.AdvantageQueue_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_AdvantageQueue')
        if isinstance(RelevantDT, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(RelevantDT, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = RelevantDT
        self.RelevantDT = initvalue_
        self.RelevantDT_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_RelevantDT')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ApplicationQueueResponseType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ApplicationQueueResponseType.subclass:
            return ApplicationQueueResponseType.subclass(*args_, **kwargs_)
        else:
            return ApplicationQueueResponseType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_orderId(self):
        return self.orderId
    def set_orderId(self, orderId):
        self.orderId = orderId
    def get_Position(self):
        return self.Position
    def set_Position(self, Position):
        self.Position = Position
    def get_Total(self):
        return self.Total
    def set_Total(self, Total):
        self.Total = Total
    def get_WithoutQueue(self):
        return self.WithoutQueue
    def set_WithoutQueue(self, WithoutQueue):
        self.WithoutQueue = WithoutQueue
    def get_FirstQueue(self):
        return self.FirstQueue
    def set_FirstQueue(self, FirstQueue):
        self.FirstQueue = FirstQueue
    def get_AdvantageQueue(self):
        return self.AdvantageQueue
    def set_AdvantageQueue(self, AdvantageQueue):
        self.AdvantageQueue = AdvantageQueue
    def get_RelevantDT(self):
        return self.RelevantDT
    def set_RelevantDT(self, RelevantDT):
        self.RelevantDT = RelevantDT
    def hasContent_(self):
        if (
            self.orderId is not None or
            self.Position is not None or
            self.Total is not None or
            self.WithoutQueue is not None or
            self.FirstQueue is not None or
            self.AdvantageQueue is not None or
            self.RelevantDT is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='ApplicationQueueResponseType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ApplicationQueueResponseType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ApplicationQueueResponseType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ApplicationQueueResponseType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ApplicationQueueResponseType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ApplicationQueueResponseType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='ApplicationQueueResponseType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.orderId is not None:
            namespaceprefix_ = self.orderId_nsprefix_ + ':' if (UseCapturedNS_ and self.orderId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sorderId>%s</%sorderId>%s' % (namespaceprefix_ , self.gds_format_integer(self.orderId, input_name='orderId'), namespaceprefix_ , eol_))
        if self.Position is not None:
            namespaceprefix_ = self.Position_nsprefix_ + ':' if (UseCapturedNS_ and self.Position_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPosition>%s</%sPosition>%s' % (namespaceprefix_ , self.gds_format_integer(self.Position, input_name='Position'), namespaceprefix_ , eol_))
        if self.Total is not None:
            namespaceprefix_ = self.Total_nsprefix_ + ':' if (UseCapturedNS_ and self.Total_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTotal>%s</%sTotal>%s' % (namespaceprefix_ , self.gds_format_integer(self.Total, input_name='Total'), namespaceprefix_ , eol_))
        if self.WithoutQueue is not None:
            namespaceprefix_ = self.WithoutQueue_nsprefix_ + ':' if (UseCapturedNS_ and self.WithoutQueue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWithoutQueue>%s</%sWithoutQueue>%s' % (namespaceprefix_ , self.gds_format_integer(self.WithoutQueue, input_name='WithoutQueue'), namespaceprefix_ , eol_))
        if self.FirstQueue is not None:
            namespaceprefix_ = self.FirstQueue_nsprefix_ + ':' if (UseCapturedNS_ and self.FirstQueue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFirstQueue>%s</%sFirstQueue>%s' % (namespaceprefix_ , self.gds_format_integer(self.FirstQueue, input_name='FirstQueue'), namespaceprefix_ , eol_))
        if self.AdvantageQueue is not None:
            namespaceprefix_ = self.AdvantageQueue_nsprefix_ + ':' if (UseCapturedNS_ and self.AdvantageQueue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAdvantageQueue>%s</%sAdvantageQueue>%s' % (namespaceprefix_ , self.gds_format_integer(self.AdvantageQueue, input_name='AdvantageQueue'), namespaceprefix_ , eol_))
        if self.RelevantDT is not None:
            namespaceprefix_ = self.RelevantDT_nsprefix_ + ':' if (UseCapturedNS_ and self.RelevantDT_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRelevantDT>%s</%sRelevantDT>%s' % (namespaceprefix_ , self.gds_format_datetime(self.RelevantDT, input_name='RelevantDT'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'orderId' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'orderId')
            ival_ = self.gds_validate_integer(ival_, node, 'orderId')
            self.orderId = ival_
            self.orderId_nsprefix_ = child_.prefix
        elif nodeName_ == 'Position' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Position')
            ival_ = self.gds_validate_integer(ival_, node, 'Position')
            self.Position = ival_
            self.Position_nsprefix_ = child_.prefix
        elif nodeName_ == 'Total' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Total')
            ival_ = self.gds_validate_integer(ival_, node, 'Total')
            self.Total = ival_
            self.Total_nsprefix_ = child_.prefix
        elif nodeName_ == 'WithoutQueue' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'WithoutQueue')
            ival_ = self.gds_validate_integer(ival_, node, 'WithoutQueue')
            self.WithoutQueue = ival_
            self.WithoutQueue_nsprefix_ = child_.prefix
        elif nodeName_ == 'FirstQueue' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'FirstQueue')
            ival_ = self.gds_validate_integer(ival_, node, 'FirstQueue')
            self.FirstQueue = ival_
            self.FirstQueue_nsprefix_ = child_.prefix
        elif nodeName_ == 'AdvantageQueue' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'AdvantageQueue')
            ival_ = self.gds_validate_integer(ival_, node, 'AdvantageQueue')
            self.AdvantageQueue = ival_
            self.AdvantageQueue_nsprefix_ = child_.prefix
        elif nodeName_ == 'RelevantDT':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.RelevantDT = dval_
            self.RelevantDT_nsprefix_ = child_.prefix
# end class ApplicationQueueResponseType


class GetApplicationQueueReasonResponseType(GeneratedsSuper):
    """Информация об основаниях изменений последовательности"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, orderId=None, IncreaseQueue=None, GotAPlace=None, IncreaseBenefits=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.orderId = orderId
        self.orderId_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_orderId')
        self.IncreaseQueue = IncreaseQueue
        self.IncreaseQueue_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_IncreaseQueue')
        self.GotAPlace = GotAPlace
        self.GotAPlace_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_GotAPlace')
        self.IncreaseBenefits = IncreaseBenefits
        self.IncreaseBenefits_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_IncreaseBenefits')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetApplicationQueueReasonResponseType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetApplicationQueueReasonResponseType.subclass:
            return GetApplicationQueueReasonResponseType.subclass(*args_, **kwargs_)
        else:
            return GetApplicationQueueReasonResponseType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_orderId(self):
        return self.orderId
    def set_orderId(self, orderId):
        self.orderId = orderId
    def get_IncreaseQueue(self):
        return self.IncreaseQueue
    def set_IncreaseQueue(self, IncreaseQueue):
        self.IncreaseQueue = IncreaseQueue
    def get_GotAPlace(self):
        return self.GotAPlace
    def set_GotAPlace(self, GotAPlace):
        self.GotAPlace = GotAPlace
    def get_IncreaseBenefits(self):
        return self.IncreaseBenefits
    def set_IncreaseBenefits(self, IncreaseBenefits):
        self.IncreaseBenefits = IncreaseBenefits
    def hasContent_(self):
        if (
            self.orderId is not None or
            self.IncreaseQueue is not None or
            self.GotAPlace is not None or
            self.IncreaseBenefits is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='GetApplicationQueueReasonResponseType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetApplicationQueueReasonResponseType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetApplicationQueueReasonResponseType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetApplicationQueueReasonResponseType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetApplicationQueueReasonResponseType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetApplicationQueueReasonResponseType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='GetApplicationQueueReasonResponseType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.orderId is not None:
            namespaceprefix_ = self.orderId_nsprefix_ + ':' if (UseCapturedNS_ and self.orderId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sorderId>%s</%sorderId>%s' % (namespaceprefix_ , self.gds_format_integer(self.orderId, input_name='orderId'), namespaceprefix_ , eol_))
        if self.IncreaseQueue is not None:
            namespaceprefix_ = self.IncreaseQueue_nsprefix_ + ':' if (UseCapturedNS_ and self.IncreaseQueue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIncreaseQueue>%s</%sIncreaseQueue>%s' % (namespaceprefix_ , self.gds_format_integer(self.IncreaseQueue, input_name='IncreaseQueue'), namespaceprefix_ , eol_))
        if self.GotAPlace is not None:
            namespaceprefix_ = self.GotAPlace_nsprefix_ + ':' if (UseCapturedNS_ and self.GotAPlace_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGotAPlace>%s</%sGotAPlace>%s' % (namespaceprefix_ , self.gds_format_integer(self.GotAPlace, input_name='GotAPlace'), namespaceprefix_ , eol_))
        if self.IncreaseBenefits is not None:
            namespaceprefix_ = self.IncreaseBenefits_nsprefix_ + ':' if (UseCapturedNS_ and self.IncreaseBenefits_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIncreaseBenefits>%s</%sIncreaseBenefits>%s' % (namespaceprefix_ , self.gds_format_integer(self.IncreaseBenefits, input_name='IncreaseBenefits'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'orderId' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'orderId')
            ival_ = self.gds_validate_integer(ival_, node, 'orderId')
            self.orderId = ival_
            self.orderId_nsprefix_ = child_.prefix
        elif nodeName_ == 'IncreaseQueue' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'IncreaseQueue')
            ival_ = self.gds_validate_integer(ival_, node, 'IncreaseQueue')
            self.IncreaseQueue = ival_
            self.IncreaseQueue_nsprefix_ = child_.prefix
        elif nodeName_ == 'GotAPlace' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'GotAPlace')
            ival_ = self.gds_validate_integer(ival_, node, 'GotAPlace')
            self.GotAPlace = ival_
            self.GotAPlace_nsprefix_ = child_.prefix
        elif nodeName_ == 'IncreaseBenefits' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'IncreaseBenefits')
            ival_ = self.gds_validate_integer(ival_, node, 'IncreaseBenefits')
            self.IncreaseBenefits = ival_
            self.IncreaseBenefits_nsprefix_ = child_.prefix
# end class GetApplicationQueueReasonResponseType


class GetApplicationResponseType(GeneratedsSuper):
    """Ответ с данными заявления"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, orderId=None, PersonInfo=None, PersonIdentityDocInfo=None, ChildInfo=None, Address=None, EntryParams=None, AdaptationProgram=None, MedicalReport=None, EduOrganizations=None, BrotherSisterInfo=None, BenefitInfo=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.orderId = orderId
        self.orderId_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_orderId')
        self.PersonInfo = PersonInfo
        self.PersonInfo_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_PersonInfo')
        self.PersonIdentityDocInfo = PersonIdentityDocInfo
        self.PersonIdentityDocInfo_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_PersonIdentityDocInfo')
        self.ChildInfo = ChildInfo
        self.ChildInfo_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ChildInfo')
        self.Address = Address
        self.Address_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_Address')
        self.EntryParams = EntryParams
        self.EntryParams_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_EntryParams')
        self.AdaptationProgram = AdaptationProgram
        self.AdaptationProgram_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_AdaptationProgram')
        self.MedicalReport = MedicalReport
        self.MedicalReport_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_MedicalReport')
        self.EduOrganizations = EduOrganizations
        self.EduOrganizations_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_EduOrganizations')
        if BrotherSisterInfo is None:
            self.BrotherSisterInfo = []
        else:
            self.BrotherSisterInfo = BrotherSisterInfo
        self.BrotherSisterInfo_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_BrotherSisterInfo')
        self.BenefitInfo = BenefitInfo
        self.BenefitInfo_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_BenefitInfo')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetApplicationResponseType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetApplicationResponseType.subclass:
            return GetApplicationResponseType.subclass(*args_, **kwargs_)
        else:
            return GetApplicationResponseType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_orderId(self):
        return self.orderId
    def set_orderId(self, orderId):
        self.orderId = orderId
    def get_PersonInfo(self):
        return self.PersonInfo
    def set_PersonInfo(self, PersonInfo):
        self.PersonInfo = PersonInfo
    def get_PersonIdentityDocInfo(self):
        return self.PersonIdentityDocInfo
    def set_PersonIdentityDocInfo(self, PersonIdentityDocInfo):
        self.PersonIdentityDocInfo = PersonIdentityDocInfo
    def get_ChildInfo(self):
        return self.ChildInfo
    def set_ChildInfo(self, ChildInfo):
        self.ChildInfo = ChildInfo
    def get_Address(self):
        return self.Address
    def set_Address(self, Address):
        self.Address = Address
    def get_EntryParams(self):
        return self.EntryParams
    def set_EntryParams(self, EntryParams):
        self.EntryParams = EntryParams
    def get_AdaptationProgram(self):
        return self.AdaptationProgram
    def set_AdaptationProgram(self, AdaptationProgram):
        self.AdaptationProgram = AdaptationProgram
    def get_MedicalReport(self):
        return self.MedicalReport
    def set_MedicalReport(self, MedicalReport):
        self.MedicalReport = MedicalReport
    def get_EduOrganizations(self):
        return self.EduOrganizations
    def set_EduOrganizations(self, EduOrganizations):
        self.EduOrganizations = EduOrganizations
    def get_BrotherSisterInfo(self):
        return self.BrotherSisterInfo
    def set_BrotherSisterInfo(self, BrotherSisterInfo):
        self.BrotherSisterInfo = BrotherSisterInfo
    def add_BrotherSisterInfo(self, value):
        self.BrotherSisterInfo.append(value)
    def insert_BrotherSisterInfo_at(self, index, value):
        self.BrotherSisterInfo.insert(index, value)
    def replace_BrotherSisterInfo_at(self, index, value):
        self.BrotherSisterInfo[index] = value
    def get_BenefitInfo(self):
        return self.BenefitInfo
    def set_BenefitInfo(self, BenefitInfo):
        self.BenefitInfo = BenefitInfo
    def hasContent_(self):
        if (
            self.orderId is not None or
            self.PersonInfo is not None or
            self.PersonIdentityDocInfo is not None or
            self.ChildInfo is not None or
            self.Address is not None or
            self.EntryParams is not None or
            self.AdaptationProgram is not None or
            self.MedicalReport is not None or
            self.EduOrganizations is not None or
            self.BrotherSisterInfo or
            self.BenefitInfo is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='GetApplicationResponseType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetApplicationResponseType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetApplicationResponseType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetApplicationResponseType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetApplicationResponseType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetApplicationResponseType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='GetApplicationResponseType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.orderId is not None:
            namespaceprefix_ = self.orderId_nsprefix_ + ':' if (UseCapturedNS_ and self.orderId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sorderId>%s</%sorderId>%s' % (namespaceprefix_ , self.gds_format_integer(self.orderId, input_name='orderId'), namespaceprefix_ , eol_))
        if self.PersonInfo is not None:
            namespaceprefix_ = self.PersonInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.PersonInfo_nsprefix_) else ''
            self.PersonInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PersonInfo', pretty_print=pretty_print)
        if self.PersonIdentityDocInfo is not None:
            namespaceprefix_ = self.PersonIdentityDocInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.PersonIdentityDocInfo_nsprefix_) else ''
            self.PersonIdentityDocInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PersonIdentityDocInfo', pretty_print=pretty_print)
        if self.ChildInfo is not None:
            namespaceprefix_ = self.ChildInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildInfo_nsprefix_) else ''
            self.ChildInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ChildInfo', pretty_print=pretty_print)
        if self.Address is not None:
            namespaceprefix_ = self.Address_nsprefix_ + ':' if (UseCapturedNS_ and self.Address_nsprefix_) else ''
            self.Address.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Address', pretty_print=pretty_print)
        if self.EntryParams is not None:
            namespaceprefix_ = self.EntryParams_nsprefix_ + ':' if (UseCapturedNS_ and self.EntryParams_nsprefix_) else ''
            self.EntryParams.export(outfile, level, namespaceprefix_, namespacedef_='', name_='EntryParams', pretty_print=pretty_print)
        if self.AdaptationProgram is not None:
            namespaceprefix_ = self.AdaptationProgram_nsprefix_ + ':' if (UseCapturedNS_ and self.AdaptationProgram_nsprefix_) else ''
            self.AdaptationProgram.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AdaptationProgram', pretty_print=pretty_print)
        if self.MedicalReport is not None:
            namespaceprefix_ = self.MedicalReport_nsprefix_ + ':' if (UseCapturedNS_ and self.MedicalReport_nsprefix_) else ''
            self.MedicalReport.export(outfile, level, namespaceprefix_, namespacedef_='', name_='MedicalReport', pretty_print=pretty_print)
        if self.EduOrganizations is not None:
            namespaceprefix_ = self.EduOrganizations_nsprefix_ + ':' if (UseCapturedNS_ and self.EduOrganizations_nsprefix_) else ''
            self.EduOrganizations.export(outfile, level, namespaceprefix_, namespacedef_='', name_='EduOrganizations', pretty_print=pretty_print)
        for BrotherSisterInfo_ in self.BrotherSisterInfo:
            namespaceprefix_ = self.BrotherSisterInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.BrotherSisterInfo_nsprefix_) else ''
            BrotherSisterInfo_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='BrotherSisterInfo', pretty_print=pretty_print)
        if self.BenefitInfo is not None:
            namespaceprefix_ = self.BenefitInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.BenefitInfo_nsprefix_) else ''
            self.BenefitInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='BenefitInfo', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'orderId' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'orderId')
            ival_ = self.gds_validate_integer(ival_, node, 'orderId')
            self.orderId = ival_
            self.orderId_nsprefix_ = child_.prefix
        elif nodeName_ == 'PersonInfo':
            obj_ = PersonInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PersonInfo = obj_
            obj_.original_tagname_ = 'PersonInfo'
        elif nodeName_ == 'PersonIdentityDocInfo':
            obj_ = PersonIdentityDocInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PersonIdentityDocInfo = obj_
            obj_.original_tagname_ = 'PersonIdentityDocInfo'
        elif nodeName_ == 'ChildInfo':
            obj_ = ChildInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ChildInfo = obj_
            obj_.original_tagname_ = 'ChildInfo'
        elif nodeName_ == 'Address':
            obj_ = AddressType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Address = obj_
            obj_.original_tagname_ = 'Address'
        elif nodeName_ == 'EntryParams':
            obj_ = EntryParamsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.EntryParams = obj_
            obj_.original_tagname_ = 'EntryParams'
        elif nodeName_ == 'AdaptationProgram':
            obj_ = AdaptationProgramType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AdaptationProgram = obj_
            obj_.original_tagname_ = 'AdaptationProgram'
        elif nodeName_ == 'MedicalReport':
            obj_ = MedicalReportWithoutFilesType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.MedicalReport = obj_
            obj_.original_tagname_ = 'MedicalReport'
        elif nodeName_ == 'EduOrganizations':
            obj_ = EduOrganizationsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.EduOrganizations = obj_
            obj_.original_tagname_ = 'EduOrganizations'
        elif nodeName_ == 'BrotherSisterInfo':
            obj_ = BrotherSisterInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.BrotherSisterInfo.append(obj_)
            obj_.original_tagname_ = 'BrotherSisterInfo'
        elif nodeName_ == 'BenefitInfo':
            obj_ = BenefitInfoWithoutFilesType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.BenefitInfo = obj_
            obj_.original_tagname_ = 'BenefitInfo'
# end class GetApplicationResponseType


class GetApplicationAdmissionResponseType(GeneratedsSuper):
    """Ответ с данными для подачи заявления на приём"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, orderId=None, PersonInfo=None, PersonIdentityDocInfo=None, ChildInfo=None, Address=None, EntryParams=None, AdaptationProgram=None, MedicalReport=None, EduOrganizationCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.orderId = orderId
        self.orderId_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_orderId')
        self.PersonInfo = PersonInfo
        self.PersonInfo_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_PersonInfo')
        self.PersonIdentityDocInfo = PersonIdentityDocInfo
        self.PersonIdentityDocInfo_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_PersonIdentityDocInfo')
        self.ChildInfo = ChildInfo
        self.ChildInfo_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ChildInfo')
        self.Address = Address
        self.Address_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_Address')
        self.EntryParams = EntryParams
        self.EntryParams_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_EntryParams')
        self.AdaptationProgram = AdaptationProgram
        self.AdaptationProgram_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_AdaptationProgram')
        self.MedicalReport = MedicalReport
        self.MedicalReport_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_MedicalReport')
        self.EduOrganizationCode = EduOrganizationCode
        self.validate_string_50(self.EduOrganizationCode)
        self.EduOrganizationCode_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_EduOrganizationCode')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetApplicationAdmissionResponseType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetApplicationAdmissionResponseType.subclass:
            return GetApplicationAdmissionResponseType.subclass(*args_, **kwargs_)
        else:
            return GetApplicationAdmissionResponseType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_orderId(self):
        return self.orderId
    def set_orderId(self, orderId):
        self.orderId = orderId
    def get_PersonInfo(self):
        return self.PersonInfo
    def set_PersonInfo(self, PersonInfo):
        self.PersonInfo = PersonInfo
    def get_PersonIdentityDocInfo(self):
        return self.PersonIdentityDocInfo
    def set_PersonIdentityDocInfo(self, PersonIdentityDocInfo):
        self.PersonIdentityDocInfo = PersonIdentityDocInfo
    def get_ChildInfo(self):
        return self.ChildInfo
    def set_ChildInfo(self, ChildInfo):
        self.ChildInfo = ChildInfo
    def get_Address(self):
        return self.Address
    def set_Address(self, Address):
        self.Address = Address
    def get_EntryParams(self):
        return self.EntryParams
    def set_EntryParams(self, EntryParams):
        self.EntryParams = EntryParams
    def get_AdaptationProgram(self):
        return self.AdaptationProgram
    def set_AdaptationProgram(self, AdaptationProgram):
        self.AdaptationProgram = AdaptationProgram
    def get_MedicalReport(self):
        return self.MedicalReport
    def set_MedicalReport(self, MedicalReport):
        self.MedicalReport = MedicalReport
    def get_EduOrganizationCode(self):
        return self.EduOrganizationCode
    def set_EduOrganizationCode(self, EduOrganizationCode):
        self.EduOrganizationCode = EduOrganizationCode
    def validate_string_50(self, value):
        result = True
        # Validate type string-50, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-50' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.orderId is not None or
            self.PersonInfo is not None or
            self.PersonIdentityDocInfo is not None or
            self.ChildInfo is not None or
            self.Address is not None or
            self.EntryParams is not None or
            self.AdaptationProgram is not None or
            self.MedicalReport is not None or
            self.EduOrganizationCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='GetApplicationAdmissionResponseType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetApplicationAdmissionResponseType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetApplicationAdmissionResponseType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetApplicationAdmissionResponseType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetApplicationAdmissionResponseType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetApplicationAdmissionResponseType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='GetApplicationAdmissionResponseType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.orderId is not None:
            namespaceprefix_ = self.orderId_nsprefix_ + ':' if (UseCapturedNS_ and self.orderId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sorderId>%s</%sorderId>%s' % (namespaceprefix_ , self.gds_format_integer(self.orderId, input_name='orderId'), namespaceprefix_ , eol_))
        if self.PersonInfo is not None:
            namespaceprefix_ = self.PersonInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.PersonInfo_nsprefix_) else ''
            self.PersonInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PersonInfo', pretty_print=pretty_print)
        if self.PersonIdentityDocInfo is not None:
            namespaceprefix_ = self.PersonIdentityDocInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.PersonIdentityDocInfo_nsprefix_) else ''
            self.PersonIdentityDocInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PersonIdentityDocInfo', pretty_print=pretty_print)
        if self.ChildInfo is not None:
            namespaceprefix_ = self.ChildInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildInfo_nsprefix_) else ''
            self.ChildInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ChildInfo', pretty_print=pretty_print)
        if self.Address is not None:
            namespaceprefix_ = self.Address_nsprefix_ + ':' if (UseCapturedNS_ and self.Address_nsprefix_) else ''
            self.Address.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Address', pretty_print=pretty_print)
        if self.EntryParams is not None:
            namespaceprefix_ = self.EntryParams_nsprefix_ + ':' if (UseCapturedNS_ and self.EntryParams_nsprefix_) else ''
            self.EntryParams.export(outfile, level, namespaceprefix_, namespacedef_='', name_='EntryParams', pretty_print=pretty_print)
        if self.AdaptationProgram is not None:
            namespaceprefix_ = self.AdaptationProgram_nsprefix_ + ':' if (UseCapturedNS_ and self.AdaptationProgram_nsprefix_) else ''
            self.AdaptationProgram.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AdaptationProgram', pretty_print=pretty_print)
        if self.MedicalReport is not None:
            namespaceprefix_ = self.MedicalReport_nsprefix_ + ':' if (UseCapturedNS_ and self.MedicalReport_nsprefix_) else ''
            self.MedicalReport.export(outfile, level, namespaceprefix_, namespacedef_='', name_='MedicalReport', pretty_print=pretty_print)
        if self.EduOrganizationCode is not None:
            namespaceprefix_ = self.EduOrganizationCode_nsprefix_ + ':' if (UseCapturedNS_ and self.EduOrganizationCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEduOrganizationCode>%s</%sEduOrganizationCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EduOrganizationCode), input_name='EduOrganizationCode')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'orderId' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'orderId')
            ival_ = self.gds_validate_integer(ival_, node, 'orderId')
            self.orderId = ival_
            self.orderId_nsprefix_ = child_.prefix
        elif nodeName_ == 'PersonInfo':
            obj_ = PersonInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PersonInfo = obj_
            obj_.original_tagname_ = 'PersonInfo'
        elif nodeName_ == 'PersonIdentityDocInfo':
            obj_ = PersonIdentityDocInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PersonIdentityDocInfo = obj_
            obj_.original_tagname_ = 'PersonIdentityDocInfo'
        elif nodeName_ == 'ChildInfo':
            obj_ = ChildInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ChildInfo = obj_
            obj_.original_tagname_ = 'ChildInfo'
        elif nodeName_ == 'Address':
            obj_ = AddressType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Address = obj_
            obj_.original_tagname_ = 'Address'
        elif nodeName_ == 'EntryParams':
            obj_ = EntryParamsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.EntryParams = obj_
            obj_.original_tagname_ = 'EntryParams'
        elif nodeName_ == 'AdaptationProgram':
            obj_ = AdaptationProgramType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AdaptationProgram = obj_
            obj_.original_tagname_ = 'AdaptationProgram'
        elif nodeName_ == 'MedicalReport':
            obj_ = MedicalReportWithoutFilesType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.MedicalReport = obj_
            obj_.original_tagname_ = 'MedicalReport'
        elif nodeName_ == 'EduOrganizationCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EduOrganizationCode')
            value_ = self.gds_validate_string(value_, node, 'EduOrganizationCode')
            self.EduOrganizationCode = value_
            self.EduOrganizationCode_nsprefix_ = child_.prefix
            # validate type string-50
            self.validate_string_50(self.EduOrganizationCode)
# end class GetApplicationAdmissionResponseType


class cancelResponseType(GeneratedsSuper):
    """Ответ на запрос отмены заявления для направления"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, orderId=None, result=None, comment=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.orderId = orderId
        self.orderId_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_orderId')
        self.result = result
        self.validate_CancelResultType(self.result)
        self.result_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_result')
        self.comment = comment
        self.validate_string_2048(self.comment)
        self.comment_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_comment')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, cancelResponseType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if cancelResponseType.subclass:
            return cancelResponseType.subclass(*args_, **kwargs_)
        else:
            return cancelResponseType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_orderId(self):
        return self.orderId
    def set_orderId(self, orderId):
        self.orderId = orderId
    def get_result(self):
        return self.result
    def set_result(self, result):
        self.result = result
    def get_comment(self):
        return self.comment
    def set_comment(self, comment):
        self.comment = comment
    def validate_CancelResultType(self, value):
        result = True
        # Validate type CancelResultType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['CANCELLED', 'IN_PROGRESS', 'REJECTED']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on CancelResultType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_string_2048(self, value):
        result = True
        # Validate type string-2048, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 2048:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-2048' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.orderId is not None or
            self.result is not None or
            self.comment is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='cancelResponseType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('cancelResponseType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'cancelResponseType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='cancelResponseType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='cancelResponseType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='cancelResponseType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='cancelResponseType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.orderId is not None:
            namespaceprefix_ = self.orderId_nsprefix_ + ':' if (UseCapturedNS_ and self.orderId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sorderId>%s</%sorderId>%s' % (namespaceprefix_ , self.gds_format_integer(self.orderId, input_name='orderId'), namespaceprefix_ , eol_))
        if self.result is not None:
            namespaceprefix_ = self.result_nsprefix_ + ':' if (UseCapturedNS_ and self.result_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sresult>%s</%sresult>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.result), input_name='result')), namespaceprefix_ , eol_))
        if self.comment is not None:
            namespaceprefix_ = self.comment_nsprefix_ + ':' if (UseCapturedNS_ and self.comment_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scomment>%s</%scomment>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.comment), input_name='comment')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'orderId' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'orderId')
            ival_ = self.gds_validate_integer(ival_, node, 'orderId')
            self.orderId = ival_
            self.orderId_nsprefix_ = child_.prefix
        elif nodeName_ == 'result':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'result')
            value_ = self.gds_validate_string(value_, node, 'result')
            self.result = value_
            self.result_nsprefix_ = child_.prefix
            # validate type CancelResultType
            self.validate_CancelResultType(self.result)
        elif nodeName_ == 'comment':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'comment')
            value_ = self.gds_validate_string(value_, node, 'comment')
            self.comment = value_
            self.comment_nsprefix_ = child_.prefix
            # validate type string-2048
            self.validate_string_2048(self.comment)
# end class cancelResponseType


class FormDataType(GeneratedsSuper):
    """Заявление для направления в дошкольную организацию
    или заявление на получение информации об этапах и результатах оказания
    услуги зачисления в дошкольную организацию
    или заявление на приём в дошкольную организацию
    или запрос получения информации о последовательности предоставления мест
    или запрос получения информации об основаниях изменения последовательности
    предоставления мест
    или запрос получения данных заявления для редактирования
    или запрос получения данных для подачи заявления на приём
    или отказ от предложенной дошкольной организации
    или запрос на отмену заявления для направления в дошкольную организацию"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, oktmo=None, ApplicationRequest=None, ApplicationOrderInfoRequest=None, ApplicationAdmissionRequest=None, GetApplicationQueueRequest=None, GetApplicationQueueReasonRequest=None, GetApplicationRequest=None, GetApplicationAdmissionRequest=None, ApplicationRejectionRequest=None, cancelRequest=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.oktmo = _cast(None, oktmo)
        self.oktmo_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_oktmo')
        self.ApplicationRequest = ApplicationRequest
        self.ApplicationRequest_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ApplicationRequest')
        self.ApplicationOrderInfoRequest = ApplicationOrderInfoRequest
        self.ApplicationOrderInfoRequest_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ApplicationOrderInfoRequest')
        self.ApplicationAdmissionRequest = ApplicationAdmissionRequest
        self.ApplicationAdmissionRequest_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ApplicationAdmissionRequest')
        self.GetApplicationQueueRequest = GetApplicationQueueRequest
        self.GetApplicationQueueRequest_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_GetApplicationQueueRequest')
        self.GetApplicationQueueReasonRequest = GetApplicationQueueReasonRequest
        self.GetApplicationQueueReasonRequest_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_GetApplicationQueueReasonRequest')
        self.GetApplicationRequest = GetApplicationRequest
        self.GetApplicationRequest_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_GetApplicationRequest')
        self.GetApplicationAdmissionRequest = GetApplicationAdmissionRequest
        self.GetApplicationAdmissionRequest_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_GetApplicationAdmissionRequest')
        self.ApplicationRejectionRequest = ApplicationRejectionRequest
        self.ApplicationRejectionRequest_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_ApplicationRejectionRequest')
        self.cancelRequest = cancelRequest
        self.cancelRequest_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_cancelRequest')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, FormDataType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if FormDataType.subclass:
            return FormDataType.subclass(*args_, **kwargs_)
        else:
            return FormDataType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ApplicationRequest(self):
        return self.ApplicationRequest
    def set_ApplicationRequest(self, ApplicationRequest):
        self.ApplicationRequest = ApplicationRequest
    def get_ApplicationOrderInfoRequest(self):
        return self.ApplicationOrderInfoRequest
    def set_ApplicationOrderInfoRequest(self, ApplicationOrderInfoRequest):
        self.ApplicationOrderInfoRequest = ApplicationOrderInfoRequest
    def get_ApplicationAdmissionRequest(self):
        return self.ApplicationAdmissionRequest
    def set_ApplicationAdmissionRequest(self, ApplicationAdmissionRequest):
        self.ApplicationAdmissionRequest = ApplicationAdmissionRequest
    def get_GetApplicationQueueRequest(self):
        return self.GetApplicationQueueRequest
    def set_GetApplicationQueueRequest(self, GetApplicationQueueRequest):
        self.GetApplicationQueueRequest = GetApplicationQueueRequest
    def get_GetApplicationQueueReasonRequest(self):
        return self.GetApplicationQueueReasonRequest
    def set_GetApplicationQueueReasonRequest(self, GetApplicationQueueReasonRequest):
        self.GetApplicationQueueReasonRequest = GetApplicationQueueReasonRequest
    def get_GetApplicationRequest(self):
        return self.GetApplicationRequest
    def set_GetApplicationRequest(self, GetApplicationRequest):
        self.GetApplicationRequest = GetApplicationRequest
    def get_GetApplicationAdmissionRequest(self):
        return self.GetApplicationAdmissionRequest
    def set_GetApplicationAdmissionRequest(self, GetApplicationAdmissionRequest):
        self.GetApplicationAdmissionRequest = GetApplicationAdmissionRequest
    def get_ApplicationRejectionRequest(self):
        return self.ApplicationRejectionRequest
    def set_ApplicationRejectionRequest(self, ApplicationRejectionRequest):
        self.ApplicationRejectionRequest = ApplicationRejectionRequest
    def get_cancelRequest(self):
        return self.cancelRequest
    def set_cancelRequest(self, cancelRequest):
        self.cancelRequest = cancelRequest
    def get_oktmo(self):
        return self.oktmo
    def set_oktmo(self, oktmo):
        self.oktmo = oktmo
    def validate_stringNN_11(self, value):
        # Validate type tns:stringNN-11, a restriction on xsd:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 11:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on stringNN-11' % {"value": value, "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on stringNN-11' % {"value" : value, "lineno": lineno} )
                result = False
    def hasContent_(self):
        if (
            self.ApplicationRequest is not None or
            self.ApplicationOrderInfoRequest is not None or
            self.ApplicationAdmissionRequest is not None or
            self.GetApplicationQueueRequest is not None or
            self.GetApplicationQueueReasonRequest is not None or
            self.GetApplicationRequest is not None or
            self.GetApplicationAdmissionRequest is not None or
            self.ApplicationRejectionRequest is not None or
            self.cancelRequest is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='FormDataType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('FormDataType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'FormDataType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='FormDataType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='FormDataType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='FormDataType'):
        if self.oktmo is not None and 'oktmo' not in already_processed:
            already_processed.add('oktmo')
            outfile.write(' oktmo=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.oktmo), input_name='oktmo')), ))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='FormDataType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ApplicationRequest is not None:
            namespaceprefix_ = self.ApplicationRequest_nsprefix_ + ':' if (UseCapturedNS_ and self.ApplicationRequest_nsprefix_) else ''
            self.ApplicationRequest.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ApplicationRequest', pretty_print=pretty_print)
        if self.ApplicationOrderInfoRequest is not None:
            namespaceprefix_ = self.ApplicationOrderInfoRequest_nsprefix_ + ':' if (UseCapturedNS_ and self.ApplicationOrderInfoRequest_nsprefix_) else ''
            self.ApplicationOrderInfoRequest.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ApplicationOrderInfoRequest', pretty_print=pretty_print)
        if self.ApplicationAdmissionRequest is not None:
            namespaceprefix_ = self.ApplicationAdmissionRequest_nsprefix_ + ':' if (UseCapturedNS_ and self.ApplicationAdmissionRequest_nsprefix_) else ''
            self.ApplicationAdmissionRequest.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ApplicationAdmissionRequest', pretty_print=pretty_print)
        if self.GetApplicationQueueRequest is not None:
            namespaceprefix_ = self.GetApplicationQueueRequest_nsprefix_ + ':' if (UseCapturedNS_ and self.GetApplicationQueueRequest_nsprefix_) else ''
            self.GetApplicationQueueRequest.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GetApplicationQueueRequest', pretty_print=pretty_print)
        if self.GetApplicationQueueReasonRequest is not None:
            namespaceprefix_ = self.GetApplicationQueueReasonRequest_nsprefix_ + ':' if (UseCapturedNS_ and self.GetApplicationQueueReasonRequest_nsprefix_) else ''
            self.GetApplicationQueueReasonRequest.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GetApplicationQueueReasonRequest', pretty_print=pretty_print)
        if self.GetApplicationRequest is not None:
            namespaceprefix_ = self.GetApplicationRequest_nsprefix_ + ':' if (UseCapturedNS_ and self.GetApplicationRequest_nsprefix_) else ''
            self.GetApplicationRequest.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GetApplicationRequest', pretty_print=pretty_print)
        if self.GetApplicationAdmissionRequest is not None:
            namespaceprefix_ = self.GetApplicationAdmissionRequest_nsprefix_ + ':' if (UseCapturedNS_ and self.GetApplicationAdmissionRequest_nsprefix_) else ''
            self.GetApplicationAdmissionRequest.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GetApplicationAdmissionRequest', pretty_print=pretty_print)
        if self.ApplicationRejectionRequest is not None:
            namespaceprefix_ = self.ApplicationRejectionRequest_nsprefix_ + ':' if (UseCapturedNS_ and self.ApplicationRejectionRequest_nsprefix_) else ''
            self.ApplicationRejectionRequest.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ApplicationRejectionRequest', pretty_print=pretty_print)
        if self.cancelRequest is not None:
            namespaceprefix_ = self.cancelRequest_nsprefix_ + ':' if (UseCapturedNS_ and self.cancelRequest_nsprefix_) else ''
            self.cancelRequest.export(outfile, level, namespaceprefix_, namespacedef_='', name_='cancelRequest', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('oktmo', node)
        if value is not None and 'oktmo' not in already_processed:
            already_processed.add('oktmo')
            self.oktmo = value
            self.validate_stringNN_11(self.oktmo)    # validate type stringNN-11
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ApplicationRequest':
            obj_ = ApplicationType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ApplicationRequest = obj_
            obj_.original_tagname_ = 'ApplicationRequest'
        elif nodeName_ == 'ApplicationOrderInfoRequest':
            obj_ = ApplicationOrderInfoRequestType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ApplicationOrderInfoRequest = obj_
            obj_.original_tagname_ = 'ApplicationOrderInfoRequest'
        elif nodeName_ == 'ApplicationAdmissionRequest':
            obj_ = ApplicationAdmissionRequestType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ApplicationAdmissionRequest = obj_
            obj_.original_tagname_ = 'ApplicationAdmissionRequest'
        elif nodeName_ == 'GetApplicationQueueRequest':
            obj_ = GetApplicationQueueRequestType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GetApplicationQueueRequest = obj_
            obj_.original_tagname_ = 'GetApplicationQueueRequest'
        elif nodeName_ == 'GetApplicationQueueReasonRequest':
            obj_ = GetApplicationQueueReasonRequestType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GetApplicationQueueReasonRequest = obj_
            obj_.original_tagname_ = 'GetApplicationQueueReasonRequest'
        elif nodeName_ == 'GetApplicationRequest':
            obj_ = GetApplicationRequestType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GetApplicationRequest = obj_
            obj_.original_tagname_ = 'GetApplicationRequest'
        elif nodeName_ == 'GetApplicationAdmissionRequest':
            obj_ = GetApplicationAdmissionRequestType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GetApplicationAdmissionRequest = obj_
            obj_.original_tagname_ = 'GetApplicationAdmissionRequest'
        elif nodeName_ == 'ApplicationRejectionRequest':
            obj_ = ApplicationRejectionRequestType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ApplicationRejectionRequest = obj_
            obj_.original_tagname_ = 'ApplicationRejectionRequest'
        elif nodeName_ == 'cancelRequest':
            obj_ = cancelRequestType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.cancelRequest = obj_
            obj_.original_tagname_ = 'cancelRequest'
# end class FormDataType


class FormDataResponseType(GeneratedsSuper):
    """Ответ с изменением статуса заявления
    или информация о последовательности предоставления мест
    или информация об основаниях изменения последо"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, changeOrderInfo=None, GetApplicationQueueResponse=None, GetApplicationQueueReasonResponse=None, GetApplicationResponse=None, GetApplicationAdmissionResponse=None, cancelResponse=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.changeOrderInfo = changeOrderInfo
        self.changeOrderInfo_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_changeOrderInfo')
        self.GetApplicationQueueResponse = GetApplicationQueueResponse
        self.GetApplicationQueueResponse_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_GetApplicationQueueResponse')
        self.GetApplicationQueueReasonResponse = GetApplicationQueueReasonResponse
        self.GetApplicationQueueReasonResponse_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_GetApplicationQueueReasonResponse')
        self.GetApplicationResponse = GetApplicationResponse
        self.GetApplicationResponse_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_GetApplicationResponse')
        self.GetApplicationAdmissionResponse = GetApplicationAdmissionResponse
        self.GetApplicationAdmissionResponse_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_GetApplicationAdmissionResponse')
        self.cancelResponse = cancelResponse
        self.cancelResponse_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_cancelResponse')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, FormDataResponseType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if FormDataResponseType.subclass:
            return FormDataResponseType.subclass(*args_, **kwargs_)
        else:
            return FormDataResponseType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_changeOrderInfo(self):
        return self.changeOrderInfo
    def set_changeOrderInfo(self, changeOrderInfo):
        self.changeOrderInfo = changeOrderInfo
    def get_GetApplicationQueueResponse(self):
        return self.GetApplicationQueueResponse
    def set_GetApplicationQueueResponse(self, GetApplicationQueueResponse):
        self.GetApplicationQueueResponse = GetApplicationQueueResponse
    def get_GetApplicationQueueReasonResponse(self):
        return self.GetApplicationQueueReasonResponse
    def set_GetApplicationQueueReasonResponse(self, GetApplicationQueueReasonResponse):
        self.GetApplicationQueueReasonResponse = GetApplicationQueueReasonResponse
    def get_GetApplicationResponse(self):
        return self.GetApplicationResponse
    def set_GetApplicationResponse(self, GetApplicationResponse):
        self.GetApplicationResponse = GetApplicationResponse
    def get_GetApplicationAdmissionResponse(self):
        return self.GetApplicationAdmissionResponse
    def set_GetApplicationAdmissionResponse(self, GetApplicationAdmissionResponse):
        self.GetApplicationAdmissionResponse = GetApplicationAdmissionResponse
    def get_cancelResponse(self):
        return self.cancelResponse
    def set_cancelResponse(self, cancelResponse):
        self.cancelResponse = cancelResponse
    def hasContent_(self):
        if (
            self.changeOrderInfo is not None or
            self.GetApplicationQueueResponse is not None or
            self.GetApplicationQueueReasonResponse is not None or
            self.GetApplicationResponse is not None or
            self.GetApplicationAdmissionResponse is not None or
            self.cancelResponse is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='FormDataResponseType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('FormDataResponseType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'FormDataResponseType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='FormDataResponseType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='FormDataResponseType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='FormDataResponseType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"', name_='FormDataResponseType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.changeOrderInfo is not None:
            namespaceprefix_ = self.changeOrderInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.changeOrderInfo_nsprefix_) else ''
            self.changeOrderInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='changeOrderInfo', pretty_print=pretty_print)
        if self.GetApplicationQueueResponse is not None:
            namespaceprefix_ = self.GetApplicationQueueResponse_nsprefix_ + ':' if (UseCapturedNS_ and self.GetApplicationQueueResponse_nsprefix_) else ''
            self.GetApplicationQueueResponse.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GetApplicationQueueResponse', pretty_print=pretty_print)
        if self.GetApplicationQueueReasonResponse is not None:
            namespaceprefix_ = self.GetApplicationQueueReasonResponse_nsprefix_ + ':' if (UseCapturedNS_ and self.GetApplicationQueueReasonResponse_nsprefix_) else ''
            self.GetApplicationQueueReasonResponse.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GetApplicationQueueReasonResponse', pretty_print=pretty_print)
        if self.GetApplicationResponse is not None:
            namespaceprefix_ = self.GetApplicationResponse_nsprefix_ + ':' if (UseCapturedNS_ and self.GetApplicationResponse_nsprefix_) else ''
            self.GetApplicationResponse.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GetApplicationResponse', pretty_print=pretty_print)
        if self.GetApplicationAdmissionResponse is not None:
            namespaceprefix_ = self.GetApplicationAdmissionResponse_nsprefix_ + ':' if (UseCapturedNS_ and self.GetApplicationAdmissionResponse_nsprefix_) else ''
            self.GetApplicationAdmissionResponse.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GetApplicationAdmissionResponse', pretty_print=pretty_print)
        if self.cancelResponse is not None:
            namespaceprefix_ = self.cancelResponse_nsprefix_ + ':' if (UseCapturedNS_ and self.cancelResponse_nsprefix_) else ''
            self.cancelResponse.export(outfile, level, namespaceprefix_, namespacedef_='', name_='cancelResponse', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'changeOrderInfo':
            obj_ = changeOrderInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.changeOrderInfo = obj_
            obj_.original_tagname_ = 'changeOrderInfo'
        elif nodeName_ == 'GetApplicationQueueResponse':
            obj_ = ApplicationQueueResponseType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GetApplicationQueueResponse = obj_
            obj_.original_tagname_ = 'GetApplicationQueueResponse'
        elif nodeName_ == 'GetApplicationQueueReasonResponse':
            obj_ = GetApplicationQueueReasonResponseType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GetApplicationQueueReasonResponse = obj_
            obj_.original_tagname_ = 'GetApplicationQueueReasonResponse'
        elif nodeName_ == 'GetApplicationResponse':
            obj_ = GetApplicationResponseType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GetApplicationResponse = obj_
            obj_.original_tagname_ = 'GetApplicationResponse'
        elif nodeName_ == 'GetApplicationAdmissionResponse':
            obj_ = GetApplicationAdmissionResponseType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GetApplicationAdmissionResponse = obj_
            obj_.original_tagname_ = 'GetApplicationAdmissionResponse'
        elif nodeName_ == 'cancelResponse':
            obj_ = cancelResponseType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.cancelResponse = obj_
            obj_.original_tagname_ = 'cancelResponse'
# end class FormDataResponseType


GDSClassesMapping = {
    'FormData': FormDataType,
    'FormDataResponse': FormDataResponseType,
}


USAGE_TEXT = """
Usage: python <Parser>.py [ -s ] <in_xml_file>
"""


def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def get_root_tag(node):
    tag = Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = GDSClassesMapping.get(tag)
    if rootClass is None:
        rootClass = globals().get(tag)
    return tag, rootClass


def get_required_ns_prefix_defs(rootNode):
    '''Get all name space prefix definitions required in this XML doc.
    Return a dictionary of definitions and a char string of definitions.
    '''
    nsmap = {
        prefix: uri
        for node in rootNode.iter()
        for (prefix, uri) in node.nsmap.items()
        if prefix is not None
    }
    namespacedefs = ' '.join([
        'xmlns:{}="{}"'.format(prefix, uri)
        for prefix, uri in nsmap.items()
    ])
    return nsmap, namespacedefs


def parse(inFileName, silence=False, print_warnings=True):
    global CapturedNsmap_
    gds_collector = GdsCollector_()
    parser = None
    doc = parsexml_(inFileName, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DataElementType'
        rootClass = DataElementType
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    CapturedNsmap_, namespacedefs = get_required_ns_prefix_defs(rootNode)
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_=namespacedefs,
            pretty_print=True)
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(
            len(gds_collector.get_messages()), ))
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj


def parseEtree(inFileName, silence=False, print_warnings=True,
               mapping=None, nsmap=None):
    parser = None
    doc = parsexml_(inFileName, parser)
    gds_collector = GdsCollector_()
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DataElementType'
        rootClass = DataElementType
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if mapping is None:
        mapping = {}
    rootElement = rootObj.to_etree(
        None, name_=rootTag, mapping_=mapping, nsmap_=nsmap)
    reverse_mapping = rootObj.gds_reverse_node_mapping(mapping)
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        content = etree_.tostring(
            rootElement, pretty_print=True,
            xml_declaration=True, encoding="utf-8")
        sys.stdout.write(str(content))
        sys.stdout.write('\n')
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(
            len(gds_collector.get_messages()), ))
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj, rootElement, mapping, reverse_mapping


def parseString(inString, silence=False, print_warnings=True):
    '''Parse a string, create the object tree, and export it.

    Arguments:
    - inString -- A string.  This XML fragment should not start
      with an XML declaration containing an encoding.
    - silence -- A boolean.  If False, export the object.
    Returns -- The root object in the tree.
    '''
    parser = None
    rootNode= parsexmlstring_(inString, parser)
    gds_collector = GdsCollector_()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DataElementType'
        rootClass = DataElementType
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1"')
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(
            len(gds_collector.get_messages()), ))
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj


def parseLiteral(inFileName, silence=False, print_warnings=True):
    parser = None
    doc = parsexml_(inFileName, parser)
    gds_collector = GdsCollector_()
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DataElementType'
        rootClass = DataElementType
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from kinder_conc import *\n\n')
        sys.stdout.write('import kinder_conc as model_\n\n')
        sys.stdout.write('rootObj = model_.rootClass(\n')
        rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
        sys.stdout.write(')\n')
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(
            len(gds_collector.get_messages()), ))
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj


def main():
    args = sys.argv[1:]
    if len(args) == 1:
        parse(args[0])
    else:
        usage()


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()

RenameMappings_ = {
}

#
# Mapping of namespaces to types defined in them
# and the file in which each is defined.
# simpleTypes are marked "ST" and complexTypes "CT".
NamespaceToDefMappings_ = {'http://epgu.gosuslugi.ru/concentrator/kindergarten/3.2.1': [('stringNN-11',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'ST'),
                                                              ('stringNN-20',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'ST'),
                                                              ('string-6',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'ST'),
                                                              ('string-10',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'ST'),
                                                              ('string-20',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'ST'),
                                                              ('string-21',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'ST'),
                                                              ('string-14',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'ST'),
                                                              ('string-50',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'ST'),
                                                              ('string-256',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'ST'),
                                                              ('string-1024',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'ST'),
                                                              ('string-2048',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'ST'),
                                                              ('CancelResultType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'ST'),
                                                              ('DataElementType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('AddressType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('AppliedDocumentType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('DocInfoType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('PersonInfoType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('OtherRepresentativeType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('PersonIdentityDocInfoType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('ChildInfoType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('ChildBirthDocRFType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('ChildBirthDocForeignType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('EntryParamsType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('AdaptationProgramType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('MedicalReportType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('MedicalReportWithoutFilesType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('EduOrganizationType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('EduOrganizationsType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('BrotherSisterInfoType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('BenefitInfoType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('BenefitInfoWithoutFilesType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('ApplicationType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('ApplicationOrderInfoRequestType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('Person2InfoType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('ApplicationAdmissionRequestType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('GetApplicationQueueRequestType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('GetApplicationQueueReasonRequestType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('GetApplicationRequestType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('GetApplicationAdmissionRequestType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('ApplicationRejectionRequestType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('cancelRequestType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('orderIdType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('statusCodeType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('changeOrderInfoType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('ApplicationQueueResponseType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('GetApplicationQueueReasonResponseType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('GetApplicationResponseType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('GetApplicationAdmissionResponseType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('cancelResponseType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('FormDataType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT'),
                                                              ('FormDataResponseType',
                                                               'concentrator/smev3_v321/templates/schema/concentrator-kindergarten.xsd',
                                                               'CT')]}

__all__ = [
    "AdaptationProgramType",
    "AddressType",
    "ApplicationAdmissionRequestType",
    "ApplicationOrderInfoRequestType",
    "ApplicationQueueResponseType",
    "ApplicationRejectionRequestType",
    "ApplicationType",
    "AppliedDocumentType",
    "BenefitInfoType",
    "BenefitInfoWithoutFilesType",
    "BrotherSisterInfoType",
    "ChildBirthDocForeignType",
    "ChildBirthDocRFType",
    "ChildInfoType",
    "DataElementType",
    "DocInfoType",
    "EduOrganizationType",
    "EduOrganizationsType",
    "EntryParamsType",
    "FormDataResponseType",
    "FormDataType",
    "GetApplicationAdmissionRequestType",
    "GetApplicationAdmissionResponseType",
    "GetApplicationQueueReasonRequestType",
    "GetApplicationQueueReasonResponseType",
    "GetApplicationQueueRequestType",
    "GetApplicationRequestType",
    "GetApplicationResponseType",
    "MedicalReportType",
    "MedicalReportWithoutFilesType",
    "OtherRepresentativeType",
    "Person2InfoType",
    "PersonIdentityDocInfoType",
    "PersonInfoType",
    "cancelRequestType",
    "cancelResponseType",
    "changeOrderInfoType",
    "orderIdType",
    "statusCodeType"
]
