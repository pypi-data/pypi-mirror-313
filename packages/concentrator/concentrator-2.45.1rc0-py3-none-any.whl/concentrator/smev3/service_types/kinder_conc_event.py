#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Fri Oct  9 11:58:48 2020 by generateDS.py version 2.36.2.
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
    from .kinder_conc_event_namespaces import GenerateDSNamespaceDefs as GenerateDSNamespaceDefs_
except ImportError:
    GenerateDSNamespaceDefs_ = {}
try:
    from .kinder_conc_event_namespaces import GenerateDSNamespaceTypePrefixes as GenerateDSNamespaceTypePrefixes_
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


class EnvType(str, Enum):
    DEV='DEV'
    UAT='UAT'
    EXUAT='EXUAT'
    SVCDEV='SVCDEV'
    TCOD='TCOD'
    PROD='PROD'


class statusCodeType(GeneratedsSuper):
    """Новый статус заявления"""
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
        self.validate_string_20(self.orgCode)
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
    def hasContent_(self):
        if (
            self.orgCode is not None or
            self.techCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"', name_='statusCodeType', pretty_print=True):
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
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"', name_='statusCodeType', fromsubclass_=False, pretty_print=True):
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
            # validate type string-20
            self.validate_string_20(self.orgCode)
        elif nodeName_ == 'techCode' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'techCode')
            ival_ = self.gds_validate_integer(ival_, node, 'techCode')
            self.techCode = ival_
            self.techCode_nsprefix_ = child_.prefix
# end class statusCodeType


class OrderStatusEventType(GeneratedsSuper):
    """Статус заявления"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, statusCode=None, cancelAllowed=None, sendMessageAllowed=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.statusCode = statusCode
        self.statusCode_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_statusCode')
        self.cancelAllowed = cancelAllowed
        self.cancelAllowed_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_cancelAllowed')
        self.sendMessageAllowed = sendMessageAllowed
        self.sendMessageAllowed_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_sendMessageAllowed')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, OrderStatusEventType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if OrderStatusEventType.subclass:
            return OrderStatusEventType.subclass(*args_, **kwargs_)
        else:
            return OrderStatusEventType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_statusCode(self):
        return self.statusCode
    def set_statusCode(self, statusCode):
        self.statusCode = statusCode
    def get_cancelAllowed(self):
        return self.cancelAllowed
    def set_cancelAllowed(self, cancelAllowed):
        self.cancelAllowed = cancelAllowed
    def get_sendMessageAllowed(self):
        return self.sendMessageAllowed
    def set_sendMessageAllowed(self, sendMessageAllowed):
        self.sendMessageAllowed = sendMessageAllowed
    def hasContent_(self):
        if (
            self.statusCode is not None or
            self.cancelAllowed is not None or
            self.sendMessageAllowed is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"', name_='OrderStatusEventType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('OrderStatusEventType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'OrderStatusEventType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='OrderStatusEventType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='OrderStatusEventType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='OrderStatusEventType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"', name_='OrderStatusEventType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.statusCode is not None:
            namespaceprefix_ = self.statusCode_nsprefix_ + ':' if (UseCapturedNS_ and self.statusCode_nsprefix_) else ''
            self.statusCode.export(outfile, level, namespaceprefix_, namespacedef_='', name_='statusCode', pretty_print=pretty_print)
        if self.cancelAllowed is not None:
            namespaceprefix_ = self.cancelAllowed_nsprefix_ + ':' if (UseCapturedNS_ and self.cancelAllowed_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scancelAllowed>%s</%scancelAllowed>%s' % (namespaceprefix_ , self.gds_format_boolean(self.cancelAllowed, input_name='cancelAllowed'), namespaceprefix_ , eol_))
        if self.sendMessageAllowed is not None:
            namespaceprefix_ = self.sendMessageAllowed_nsprefix_ + ':' if (UseCapturedNS_ and self.sendMessageAllowed_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%ssendMessageAllowed>%s</%ssendMessageAllowed>%s' % (namespaceprefix_ , self.gds_format_boolean(self.sendMessageAllowed, input_name='sendMessageAllowed'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'statusCode':
            obj_ = statusCodeType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.statusCode = obj_
            obj_.original_tagname_ = 'statusCode'
        elif nodeName_ == 'cancelAllowed':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'cancelAllowed')
            ival_ = self.gds_validate_boolean(ival_, node, 'cancelAllowed')
            self.cancelAllowed = ival_
            self.cancelAllowed_nsprefix_ = child_.prefix
        elif nodeName_ == 'sendMessageAllowed':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'sendMessageAllowed')
            ival_ = self.gds_validate_boolean(ival_, node, 'sendMessageAllowed')
            self.sendMessageAllowed = ival_
            self.sendMessageAllowed_nsprefix_ = child_.prefix
# end class OrderStatusEventType


class PaymentType(GeneratedsSuper):
    """Информация о начислении"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, source=None, uin=None, description=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.source = source
        self.validate_string_16(self.source)
        self.source_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_source')
        self.uin = uin
        self.validate_string_256(self.uin)
        self.uin_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_uin')
        self.description = description
        self.validate_string_210(self.description)
        self.description_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_description')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PaymentType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PaymentType.subclass:
            return PaymentType.subclass(*args_, **kwargs_)
        else:
            return PaymentType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_source(self):
        return self.source
    def set_source(self, source):
        self.source = source
    def get_uin(self):
        return self.uin
    def set_uin(self, uin):
        self.uin = uin
    def get_description(self):
        return self.description
    def set_description(self, description):
        self.description = description
    def validate_string_16(self, value):
        result = True
        # Validate type string-16, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 16:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-16' % {"value" : encode_str_2_3(value), "lineno": lineno} )
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
    def validate_string_210(self, value):
        result = True
        # Validate type string-210, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 210:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-210' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.source is not None or
            self.uin is not None or
            self.description is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"', name_='PaymentType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PaymentType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PaymentType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PaymentType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PaymentType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PaymentType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"', name_='PaymentType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.source is not None:
            namespaceprefix_ = self.source_nsprefix_ + ':' if (UseCapturedNS_ and self.source_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%ssource>%s</%ssource>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.source), input_name='source')), namespaceprefix_ , eol_))
        if self.uin is not None:
            namespaceprefix_ = self.uin_nsprefix_ + ':' if (UseCapturedNS_ and self.uin_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%suin>%s</%suin>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.uin), input_name='uin')), namespaceprefix_ , eol_))
        if self.description is not None:
            namespaceprefix_ = self.description_nsprefix_ + ':' if (UseCapturedNS_ and self.description_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdescription>%s</%sdescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.description), input_name='description')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'source':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'source')
            value_ = self.gds_validate_string(value_, node, 'source')
            self.source = value_
            self.source_nsprefix_ = child_.prefix
            # validate type string-16
            self.validate_string_16(self.source)
        elif nodeName_ == 'uin':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'uin')
            value_ = self.gds_validate_string(value_, node, 'uin')
            self.uin = value_
            self.uin_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.uin)
        elif nodeName_ == 'description':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'description')
            value_ = self.gds_validate_string(value_, node, 'description')
            self.description = value_
            self.description_nsprefix_ = child_.prefix
            # validate type string-210
            self.validate_string_210(self.description)
# end class PaymentType


class PaymentStatusEventType(GeneratedsSuper):
    """Статус начисления"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, status=None, payment=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.status = status
        self.validate_string_16(self.status)
        self.status_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_status')
        if payment is None:
            self.payment = []
        else:
            self.payment = payment
        self.payment_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_payment')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PaymentStatusEventType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PaymentStatusEventType.subclass:
            return PaymentStatusEventType.subclass(*args_, **kwargs_)
        else:
            return PaymentStatusEventType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_status(self):
        return self.status
    def set_status(self, status):
        self.status = status
    def get_payment(self):
        return self.payment
    def set_payment(self, payment):
        self.payment = payment
    def add_payment(self, value):
        self.payment.append(value)
    def insert_payment_at(self, index, value):
        self.payment.insert(index, value)
    def replace_payment_at(self, index, value):
        self.payment[index] = value
    def validate_string_16(self, value):
        result = True
        # Validate type string-16, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 16:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-16' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.status is not None or
            self.payment
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"', name_='PaymentStatusEventType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PaymentStatusEventType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PaymentStatusEventType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PaymentStatusEventType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PaymentStatusEventType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PaymentStatusEventType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"', name_='PaymentStatusEventType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.status is not None:
            namespaceprefix_ = self.status_nsprefix_ + ':' if (UseCapturedNS_ and self.status_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstatus>%s</%sstatus>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.status), input_name='status')), namespaceprefix_ , eol_))
        for payment_ in self.payment:
            namespaceprefix_ = self.payment_nsprefix_ + ':' if (UseCapturedNS_ and self.payment_nsprefix_) else ''
            payment_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='payment', pretty_print=pretty_print)
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
        if nodeName_ == 'status':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'status')
            value_ = self.gds_validate_string(value_, node, 'status')
            self.status = value_
            self.status_nsprefix_ = child_.prefix
            # validate type string-16
            self.validate_string_16(self.status)
        elif nodeName_ == 'payment':
            obj_ = PaymentType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.payment.append(obj_)
            obj_.original_tagname_ = 'payment'
# end class PaymentStatusEventType


class InfoEventType(GeneratedsSuper):
    """Информационное событие"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, code=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.code = code
        self.validate_string_20(self.code)
        self.code_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_code')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, InfoEventType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if InfoEventType.subclass:
            return InfoEventType.subclass(*args_, **kwargs_)
        else:
            return InfoEventType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_code(self):
        return self.code
    def set_code(self, code):
        self.code = code
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
    def hasContent_(self):
        if (
            self.code is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"', name_='InfoEventType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('InfoEventType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'InfoEventType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='InfoEventType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='InfoEventType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='InfoEventType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"', name_='InfoEventType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.code is not None:
            namespaceprefix_ = self.code_nsprefix_ + ':' if (UseCapturedNS_ and self.code_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scode>%s</%scode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.code), input_name='code')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'code':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'code')
            value_ = self.gds_validate_string(value_, node, 'code')
            self.code = value_
            self.code_nsprefix_ = child_.prefix
            # validate type string-20
            self.validate_string_20(self.code)
# end class InfoEventType


class TextMessageEventType(GeneratedsSuper):
    """Текстовое сообщение"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TextMessageEventType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TextMessageEventType.subclass:
            return TextMessageEventType.subclass(*args_, **kwargs_)
        else:
            return TextMessageEventType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def hasContent_(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"', name_='TextMessageEventType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TextMessageEventType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TextMessageEventType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TextMessageEventType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TextMessageEventType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='TextMessageEventType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"', name_='TextMessageEventType', fromsubclass_=False, pretty_print=True):
        pass
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
        pass
# end class TextMessageEventType


class organizationDataType(GeneratedsSuper):
    """Код подразделения и перечень кодов кабинетов/специалистов"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, organizationId=None, areaId=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.organizationId = organizationId
        self.validate_string_50(self.organizationId)
        self.organizationId_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_organizationId')
        if areaId is None:
            self.areaId = []
        else:
            self.areaId = areaId
        self.areaId_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_areaId')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, organizationDataType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if organizationDataType.subclass:
            return organizationDataType.subclass(*args_, **kwargs_)
        else:
            return organizationDataType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_organizationId(self):
        return self.organizationId
    def set_organizationId(self, organizationId):
        self.organizationId = organizationId
    def get_areaId(self):
        return self.areaId
    def set_areaId(self, areaId):
        self.areaId = areaId
    def add_areaId(self, value):
        self.areaId.append(value)
    def insert_areaId_at(self, index, value):
        self.areaId.insert(index, value)
    def replace_areaId_at(self, index, value):
        self.areaId[index] = value
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
            self.organizationId is not None or
            self.areaId
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"', name_='organizationDataType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('organizationDataType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'organizationDataType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='organizationDataType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='organizationDataType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='organizationDataType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"', name_='organizationDataType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.organizationId is not None:
            namespaceprefix_ = self.organizationId_nsprefix_ + ':' if (UseCapturedNS_ and self.organizationId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sorganizationId>%s</%sorganizationId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.organizationId), input_name='organizationId')), namespaceprefix_ , eol_))
        for areaId_ in self.areaId:
            namespaceprefix_ = self.areaId_nsprefix_ + ':' if (UseCapturedNS_ and self.areaId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sareaId>%s</%sareaId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(areaId_), input_name='areaId')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'organizationId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'organizationId')
            value_ = self.gds_validate_string(value_, node, 'organizationId')
            self.organizationId = value_
            self.organizationId_nsprefix_ = child_.prefix
            # validate type string-50
            self.validate_string_50(self.organizationId)
        elif nodeName_ == 'areaId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'areaId')
            value_ = self.gds_validate_string(value_, node, 'areaId')
            self.areaId.append(value_)
            self.areaId_nsprefix_ = child_.prefix
            # validate type string-50
            self.validate_string_50(self.areaId[-1])
# end class organizationDataType


class equeueInvitationType(GeneratedsSuper):
    """Приглашение записаться на приём с указанием перечня подразделений и
    кабинетов/специалистов,
    а также интервала дат"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, organizationData=None, startDate=None, endDate=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        if organizationData is None:
            self.organizationData = []
        else:
            self.organizationData = organizationData
        self.organizationData_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_organizationData')
        if isinstance(startDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(startDate, '%Y-%m-%d').date()
        else:
            initvalue_ = startDate
        self.startDate = initvalue_
        self.startDate_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_startDate')
        if isinstance(endDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(endDate, '%Y-%m-%d').date()
        else:
            initvalue_ = endDate
        self.endDate = initvalue_
        self.endDate_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_endDate')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, equeueInvitationType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if equeueInvitationType.subclass:
            return equeueInvitationType.subclass(*args_, **kwargs_)
        else:
            return equeueInvitationType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_organizationData(self):
        return self.organizationData
    def set_organizationData(self, organizationData):
        self.organizationData = organizationData
    def add_organizationData(self, value):
        self.organizationData.append(value)
    def insert_organizationData_at(self, index, value):
        self.organizationData.insert(index, value)
    def replace_organizationData_at(self, index, value):
        self.organizationData[index] = value
    def get_startDate(self):
        return self.startDate
    def set_startDate(self, startDate):
        self.startDate = startDate
    def get_endDate(self):
        return self.endDate
    def set_endDate(self, endDate):
        self.endDate = endDate
    def hasContent_(self):
        if (
            self.organizationData or
            self.startDate is not None or
            self.endDate is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"', name_='equeueInvitationType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('equeueInvitationType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'equeueInvitationType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='equeueInvitationType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='equeueInvitationType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='equeueInvitationType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"', name_='equeueInvitationType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for organizationData_ in self.organizationData:
            namespaceprefix_ = self.organizationData_nsprefix_ + ':' if (UseCapturedNS_ and self.organizationData_nsprefix_) else ''
            organizationData_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='organizationData', pretty_print=pretty_print)
        if self.startDate is not None:
            namespaceprefix_ = self.startDate_nsprefix_ + ':' if (UseCapturedNS_ and self.startDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstartDate>%s</%sstartDate>%s' % (namespaceprefix_ , self.gds_format_date(self.startDate, input_name='startDate'), namespaceprefix_ , eol_))
        if self.endDate is not None:
            namespaceprefix_ = self.endDate_nsprefix_ + ':' if (UseCapturedNS_ and self.endDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sendDate>%s</%sendDate>%s' % (namespaceprefix_ , self.gds_format_date(self.endDate, input_name='endDate'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'organizationData':
            obj_ = organizationDataType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.organizationData.append(obj_)
            obj_.original_tagname_ = 'organizationData'
        elif nodeName_ == 'startDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.startDate = dval_
            self.startDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'endDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.endDate = dval_
            self.endDate_nsprefix_ = child_.prefix
# end class equeueInvitationType


class equeueClosedType(GeneratedsSuper):
    """Наличие тега - закрыть возможность записи на приём"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, equeueClosedType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if equeueClosedType.subclass:
            return equeueClosedType.subclass(*args_, **kwargs_)
        else:
            return equeueClosedType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def hasContent_(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"', name_='equeueClosedType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('equeueClosedType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'equeueClosedType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='equeueClosedType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='equeueClosedType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='equeueClosedType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"', name_='equeueClosedType', fromsubclass_=False, pretty_print=True):
        pass
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
        pass
# end class equeueClosedType


class EqueueEventType(GeneratedsSuper):
    """Приглашение записаться на приём или флаг отмены приглашения"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, equeueInvitation=None, equeueClosed=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.equeueInvitation = equeueInvitation
        self.equeueInvitation_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_equeueInvitation')
        self.equeueClosed = equeueClosed
        self.equeueClosed_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_equeueClosed')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, EqueueEventType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if EqueueEventType.subclass:
            return EqueueEventType.subclass(*args_, **kwargs_)
        else:
            return EqueueEventType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_equeueInvitation(self):
        return self.equeueInvitation
    def set_equeueInvitation(self, equeueInvitation):
        self.equeueInvitation = equeueInvitation
    def get_equeueClosed(self):
        return self.equeueClosed
    def set_equeueClosed(self, equeueClosed):
        self.equeueClosed = equeueClosed
    def hasContent_(self):
        if (
            self.equeueInvitation is not None or
            self.equeueClosed is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"', name_='EqueueEventType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('EqueueEventType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'EqueueEventType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='EqueueEventType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='EqueueEventType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='EqueueEventType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"', name_='EqueueEventType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.equeueInvitation is not None:
            namespaceprefix_ = self.equeueInvitation_nsprefix_ + ':' if (UseCapturedNS_ and self.equeueInvitation_nsprefix_) else ''
            self.equeueInvitation.export(outfile, level, namespaceprefix_, namespacedef_='', name_='equeueInvitation', pretty_print=pretty_print)
        if self.equeueClosed is not None:
            namespaceprefix_ = self.equeueClosed_nsprefix_ + ':' if (UseCapturedNS_ and self.equeueClosed_nsprefix_) else ''
            self.equeueClosed.export(outfile, level, namespaceprefix_, namespacedef_='', name_='equeueClosed', pretty_print=pretty_print)
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
        if nodeName_ == 'equeueInvitation':
            obj_ = equeueInvitationType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.equeueInvitation = obj_
            obj_.original_tagname_ = 'equeueInvitation'
        elif nodeName_ == 'equeueClosed':
            obj_ = equeueClosedType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.equeueClosed = obj_
            obj_.original_tagname_ = 'equeueClosed'
# end class EqueueEventType


class EventType(GeneratedsSuper):
    """Тип события: статус заявления, информация о начислении, информационное
    событие, текстовое сообщение, приглашение записаться на приём"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, orderStatusEvent=None, paymentStatusEvent=None, infoEvent=None, textMessageEvent=None, equeueEvent=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.orderStatusEvent = orderStatusEvent
        self.orderStatusEvent_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_orderStatusEvent')
        self.paymentStatusEvent = paymentStatusEvent
        self.paymentStatusEvent_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_paymentStatusEvent')
        self.infoEvent = infoEvent
        self.infoEvent_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_infoEvent')
        self.textMessageEvent = textMessageEvent
        self.textMessageEvent_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_textMessageEvent')
        self.equeueEvent = equeueEvent
        self.equeueEvent_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_equeueEvent')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, EventType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if EventType.subclass:
            return EventType.subclass(*args_, **kwargs_)
        else:
            return EventType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_orderStatusEvent(self):
        return self.orderStatusEvent
    def set_orderStatusEvent(self, orderStatusEvent):
        self.orderStatusEvent = orderStatusEvent
    def get_paymentStatusEvent(self):
        return self.paymentStatusEvent
    def set_paymentStatusEvent(self, paymentStatusEvent):
        self.paymentStatusEvent = paymentStatusEvent
    def get_infoEvent(self):
        return self.infoEvent
    def set_infoEvent(self, infoEvent):
        self.infoEvent = infoEvent
    def get_textMessageEvent(self):
        return self.textMessageEvent
    def set_textMessageEvent(self, textMessageEvent):
        self.textMessageEvent = textMessageEvent
    def get_equeueEvent(self):
        return self.equeueEvent
    def set_equeueEvent(self, equeueEvent):
        self.equeueEvent = equeueEvent
    def hasContent_(self):
        if (
            self.orderStatusEvent is not None or
            self.paymentStatusEvent is not None or
            self.infoEvent is not None or
            self.textMessageEvent is not None or
            self.equeueEvent is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"', name_='EventType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('EventType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'EventType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='EventType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='EventType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='EventType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"', name_='EventType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.orderStatusEvent is not None:
            namespaceprefix_ = self.orderStatusEvent_nsprefix_ + ':' if (UseCapturedNS_ and self.orderStatusEvent_nsprefix_) else ''
            self.orderStatusEvent.export(outfile, level, namespaceprefix_, namespacedef_='', name_='orderStatusEvent', pretty_print=pretty_print)
        if self.paymentStatusEvent is not None:
            namespaceprefix_ = self.paymentStatusEvent_nsprefix_ + ':' if (UseCapturedNS_ and self.paymentStatusEvent_nsprefix_) else ''
            self.paymentStatusEvent.export(outfile, level, namespaceprefix_, namespacedef_='', name_='paymentStatusEvent', pretty_print=pretty_print)
        if self.infoEvent is not None:
            namespaceprefix_ = self.infoEvent_nsprefix_ + ':' if (UseCapturedNS_ and self.infoEvent_nsprefix_) else ''
            self.infoEvent.export(outfile, level, namespaceprefix_, namespacedef_='', name_='infoEvent', pretty_print=pretty_print)
        if self.textMessageEvent is not None:
            namespaceprefix_ = self.textMessageEvent_nsprefix_ + ':' if (UseCapturedNS_ and self.textMessageEvent_nsprefix_) else ''
            self.textMessageEvent.export(outfile, level, namespaceprefix_, namespacedef_='', name_='textMessageEvent', pretty_print=pretty_print)
        if self.equeueEvent is not None:
            namespaceprefix_ = self.equeueEvent_nsprefix_ + ':' if (UseCapturedNS_ and self.equeueEvent_nsprefix_) else ''
            self.equeueEvent.export(outfile, level, namespaceprefix_, namespacedef_='', name_='equeueEvent', pretty_print=pretty_print)
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
        if nodeName_ == 'orderStatusEvent':
            obj_ = OrderStatusEventType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.orderStatusEvent = obj_
            obj_.original_tagname_ = 'orderStatusEvent'
        elif nodeName_ == 'paymentStatusEvent':
            obj_ = PaymentStatusEventType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.paymentStatusEvent = obj_
            obj_.original_tagname_ = 'paymentStatusEvent'
        elif nodeName_ == 'infoEvent':
            obj_ = InfoEventType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.infoEvent = obj_
            obj_.original_tagname_ = 'infoEvent'
        elif nodeName_ == 'textMessageEvent':
            obj_ = TextMessageEventType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.textMessageEvent = obj_
            obj_.original_tagname_ = 'textMessageEvent'
        elif nodeName_ == 'equeueEvent':
            obj_ = EqueueEventType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.equeueEvent = obj_
            obj_.original_tagname_ = 'equeueEvent'
# end class EventType


class EventServiceRequestType(GeneratedsSuper):
    """Запрос передачи события по заявлению в ЛК ЕПГУ"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, env=None, orderId=None, eventDate=None, eventComment=None, eventAuthor=None, event=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.env = _cast(None, env)
        self.env_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_env')
        self.orderId = orderId
        self.orderId_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_orderId')
        if isinstance(eventDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(eventDate, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = eventDate
        self.eventDate = initvalue_
        self.eventDate_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_eventDate')
        self.eventComment = eventComment
        self.validate_string_2048(self.eventComment)
        self.eventComment_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_eventComment')
        self.eventAuthor = eventAuthor
        self.validate_string_256(self.eventAuthor)
        self.eventAuthor_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_eventAuthor')
        self.event = event
        self.event_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_event')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, EventServiceRequestType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if EventServiceRequestType.subclass:
            return EventServiceRequestType.subclass(*args_, **kwargs_)
        else:
            return EventServiceRequestType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_orderId(self):
        return self.orderId
    def set_orderId(self, orderId):
        self.orderId = orderId
    def get_eventDate(self):
        return self.eventDate
    def set_eventDate(self, eventDate):
        self.eventDate = eventDate
    def get_eventComment(self):
        return self.eventComment
    def set_eventComment(self, eventComment):
        self.eventComment = eventComment
    def get_eventAuthor(self):
        return self.eventAuthor
    def set_eventAuthor(self, eventAuthor):
        self.eventAuthor = eventAuthor
    def get_event(self):
        return self.event
    def set_event(self, event):
        self.event = event
    def get_env(self):
        return self.env
    def set_env(self, env):
        self.env = env
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
    def validate_EnvType(self, value):
        # Validate type tns:EnvType, a restriction on tns:string-16.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['DEV', 'UAT', 'EXUAT', 'SVCDEV', 'TCOD', 'PROD']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on EnvType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) > 16:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on EnvType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
    def hasContent_(self):
        if (
            self.orderId is not None or
            self.eventDate is not None or
            self.eventComment is not None or
            self.eventAuthor is not None or
            self.event is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"', name_='EventServiceRequestType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('EventServiceRequestType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'EventServiceRequestType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='EventServiceRequestType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='EventServiceRequestType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='EventServiceRequestType'):
        if self.env is not None and 'env' not in already_processed:
            already_processed.add('env')
            outfile.write(' env=%s' % (quote_attrib(self.env), ))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"', name_='EventServiceRequestType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.orderId is not None:
            namespaceprefix_ = self.orderId_nsprefix_ + ':' if (UseCapturedNS_ and self.orderId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sorderId>%s</%sorderId>%s' % (namespaceprefix_ , self.gds_format_integer(self.orderId, input_name='orderId'), namespaceprefix_ , eol_))
        if self.eventDate is not None:
            namespaceprefix_ = self.eventDate_nsprefix_ + ':' if (UseCapturedNS_ and self.eventDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%seventDate>%s</%seventDate>%s' % (namespaceprefix_ , self.gds_format_datetime(self.eventDate, input_name='eventDate'), namespaceprefix_ , eol_))
        if self.eventComment is not None:
            namespaceprefix_ = self.eventComment_nsprefix_ + ':' if (UseCapturedNS_ and self.eventComment_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%seventComment>%s</%seventComment>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.eventComment), input_name='eventComment')), namespaceprefix_ , eol_))
        if self.eventAuthor is not None:
            namespaceprefix_ = self.eventAuthor_nsprefix_ + ':' if (UseCapturedNS_ and self.eventAuthor_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%seventAuthor>%s</%seventAuthor>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.eventAuthor), input_name='eventAuthor')), namespaceprefix_ , eol_))
        if self.event is not None:
            namespaceprefix_ = self.event_nsprefix_ + ':' if (UseCapturedNS_ and self.event_nsprefix_) else ''
            self.event.export(outfile, level, namespaceprefix_, namespacedef_='', name_='event', pretty_print=pretty_print)
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
        value = find_attr_value_('env', node)
        if value is not None and 'env' not in already_processed:
            already_processed.add('env')
            self.env = value
            self.validate_EnvType(self.env)    # validate type EnvType
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'orderId' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'orderId')
            ival_ = self.gds_validate_integer(ival_, node, 'orderId')
            self.orderId = ival_
            self.orderId_nsprefix_ = child_.prefix
        elif nodeName_ == 'eventDate':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.eventDate = dval_
            self.eventDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'eventComment':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'eventComment')
            value_ = self.gds_validate_string(value_, node, 'eventComment')
            self.eventComment = value_
            self.eventComment_nsprefix_ = child_.prefix
            # validate type string-2048
            self.validate_string_2048(self.eventComment)
        elif nodeName_ == 'eventAuthor':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'eventAuthor')
            value_ = self.gds_validate_string(value_, node, 'eventAuthor')
            self.eventAuthor = value_
            self.eventAuthor_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.eventAuthor)
        elif nodeName_ == 'event':
            obj_ = EventType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.event = obj_
            obj_.original_tagname_ = 'event'
# end class EventServiceRequestType


class EventServiceResponseType(GeneratedsSuper):
    """Ответ в случае успешной обработки события"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, code=None, message=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.__class__.__name__)
        self.code = code
        self.code_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_code')
        self.message = message
        self.validate_string_256(self.message)
        self.message_nsprefix_ = GenerateDSNamespaceTypePrefixes_.get(f'{self.__class__.__name__}_message')
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, EventServiceResponseType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if EventServiceResponseType.subclass:
            return EventServiceResponseType.subclass(*args_, **kwargs_)
        else:
            return EventServiceResponseType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_code(self):
        return self.code
    def set_code(self, code):
        self.code = code
    def get_message(self):
        return self.message
    def set_message(self, message):
        self.message = message
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
            self.code is not None or
            self.message is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"', name_='EventServiceResponseType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('EventServiceResponseType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'EventServiceResponseType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='EventServiceResponseType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='EventServiceResponseType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='EventServiceResponseType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"', name_='EventServiceResponseType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.code is not None:
            namespaceprefix_ = self.code_nsprefix_ + ':' if (UseCapturedNS_ and self.code_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scode>%s</%scode>%s' % (namespaceprefix_ , self.gds_format_integer(self.code, input_name='code'), namespaceprefix_ , eol_))
        if self.message is not None:
            namespaceprefix_ = self.message_nsprefix_ + ':' if (UseCapturedNS_ and self.message_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%smessage>%s</%smessage>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.message), input_name='message')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'code' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'code')
            ival_ = self.gds_validate_integer(ival_, node, 'code')
            self.code = ival_
            self.code_nsprefix_ = child_.prefix
        elif nodeName_ == 'message':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'message')
            value_ = self.gds_validate_string(value_, node, 'message')
            self.message = value_
            self.message_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.message)
# end class EventServiceResponseType


GDSClassesMapping = {
    'eventServiceRequest': EventServiceRequestType,
    'eventServiceResponse': EventServiceResponseType,
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
        rootTag = 'statusCodeType'
        rootClass = statusCodeType
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
        rootTag = 'statusCodeType'
        rootClass = statusCodeType
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
        rootTag = 'statusCodeType'
        rootClass = statusCodeType
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"')
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
        rootTag = 'statusCodeType'
        rootClass = statusCodeType
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from kinder_conc_event import *\n\n')
        sys.stdout.write('import kinder_conc_event as model_\n\n')
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
NamespaceToDefMappings_ = {'http://epgu.gosuslugi.ru/lk/order/event/3.1.1': [('string-16',
                                                    './event.xsd',
                                                    'ST'),
                                                   ('string-20',
                                                    './event.xsd',
                                                    'ST'),
                                                   ('string-50',
                                                    './event.xsd',
                                                    'ST'),
                                                   ('string-210',
                                                    './event.xsd',
                                                    'ST'),
                                                   ('string-256',
                                                    './event.xsd',
                                                    'ST'),
                                                   ('string-2048',
                                                    './event.xsd',
                                                    'ST'),
                                                   ('EnvType',
                                                    './event.xsd',
                                                    'ST'),
                                                   ('statusCodeType',
                                                    './event.xsd',
                                                    'CT'),
                                                   ('OrderStatusEventType',
                                                    './event.xsd',
                                                    'CT'),
                                                   ('PaymentType',
                                                    './event.xsd',
                                                    'CT'),
                                                   ('PaymentStatusEventType',
                                                    './event.xsd',
                                                    'CT'),
                                                   ('InfoEventType',
                                                    './event.xsd',
                                                    'CT'),
                                                   ('TextMessageEventType',
                                                    './event.xsd',
                                                    'CT'),
                                                   ('organizationDataType',
                                                    './event.xsd',
                                                    'CT'),
                                                   ('equeueInvitationType',
                                                    './event.xsd',
                                                    'CT'),
                                                   ('equeueClosedType',
                                                    './event.xsd',
                                                    'CT'),
                                                   ('EqueueEventType',
                                                    './event.xsd',
                                                    'CT'),
                                                   ('EventType',
                                                    './event.xsd',
                                                    'CT'),
                                                   ('EventServiceRequestType',
                                                    './event.xsd',
                                                    'CT'),
                                                   ('EventServiceResponseType',
                                                    './event.xsd',
                                                    'CT')]}

__all__ = [
    "EqueueEventType",
    "EventServiceRequestType",
    "EventServiceResponseType",
    "EventType",
    "InfoEventType",
    "OrderStatusEventType",
    "PaymentStatusEventType",
    "PaymentType",
    "TextMessageEventType",
    "equeueClosedType",
    "equeueInvitationType",
    "organizationDataType",
    "statusCodeType"
]
