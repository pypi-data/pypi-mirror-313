#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on Sun Dec 12 17:02:59 2021 by Thomas Bruns
# This file is part of dcc-xmljsonconv (https://gitlab1.ptb.de/digitaldynamicmeasurement/dcc_XMLJSONConv)
# Copyright 2024 [Thomas Bruns (PTB), Benedikt Seeger(PTB), Vanessa Stehr(PTB)]
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from jinja2 import Template
import lxml.etree as ElementTree
import json
import os
import warnings
from functools import reduce
import operator
import re
import datetime
from dccXMLJSONConv.typeCastDictCreator import XSDParserCacheWrapper

TRACBACKLENGTH = 40

from datetime import datetime, timedelta

class DCCJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return {'__type__': 'datetime', 'value': obj.isoformat()}
        elif isinstance(obj, timedelta):
            # ISO 8601 duration format
            seconds = int(obj.total_seconds())
            days, seconds = divmod(seconds, 86400)
            hours, seconds = divmod(seconds, 3600)
            minutes, seconds = divmod(seconds, 60)
            iso_duration = f"P{days}DT{hours}H{minutes}M{seconds}S"
            return {'__type__': 'timedelta', 'value': iso_duration}
        return super().default(obj)

def dcc_json_decoder(dct):
    if '__type__' in dct:
        if dct['__type__'] == 'datetime':
            return datetime.fromisoformat(dct['value'])
        elif dct['__type__'] == 'timedelta':
            # Parse ISO 8601 duration format
            import re
            pattern = re.compile(
                r'P(?:(\d+)D)?T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
            )
            match = pattern.fullmatch(dct['value'])
            if match:
                days = int(match.group(1) or 0)
                hours = int(match.group(2) or 0)
                minutes = int(match.group(3) or 0)
                seconds = int(match.group(4) or 0)
                return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    return dct


def process_schema_url(url, version=None):
    """
    Processes the schema URL to extract the base URL and version.

    Parameters
    ----------
    url : str
        The schema URL containing the version information.
    version : str, optional
        The pre-provided version. If None, it will be extracted from the URL.

    Returns
    -------
    tuple
        A tuple containing (base_url, version, cache_key).
    """
    # Extract version if not provided
    if version is None:
        match = re.search(r'/v([\d.]+(?:-rc\.\d+)?)', url)
        if match:
            version = match.group(1)
        else:
            version = None  # Default to None if version is not found

    # Remove version directory but keep the file name (e.g., .xsd) in the URL
    base_url = re.sub(r'/v[\d.]+(?:-rc\.\d+)?/', '/', url)

    # Remove 'www.' from the base URL
    base_url = re.sub(r'^https?://www\.', 'https://', base_url)

    # Create a cache key
    cache_key = (base_url, version)
    cache_key_str = json.dumps(cache_key)

    return base_url, version, cache_key_str


class dcc():
    def __init__(self):
        self.root = None
        self.xml = ""
        self.json = ""
        self.nsmap = {}
        self.nsmap_reversed = {}  # Reversed version of nsmap for prefix lookup
        self.dic = {}
        # Initialize schema attributes to None
        self.schmeaurl = None
        self.schema_name = None
        self.schema_version = None
        self.schema_namespace = None
        self.schema_prefix = None
        self.parsingErrorInRecursionOccured = False  # flag if an error occurred within the recursive parsing
        self.TpComment = Template("\n<!-- {{ comment }} -->\n")  # Jinja template for a comment
        self.TpTag = Template("<{{ name }}{{attributes}}>{{ text }}</{{ name }}>\n")  # jinja template for a tag
        self.XSDParserCacheWrapper = XSDParserCacheWrapper()
        # Attempt to parse the schema and add it to cache

        self.XSD_non_list_dict, self.XSD_list_dict, self.XSD_repeated_elements = self.XSDParserCacheWrapper.parse_with_cache()

    # --------------- generate a dict from (DCC)-XML ---------------
    def read_dcc_file(self, filename):
        """
        Reads the XML-file in filename into self.xml

        Parameters
        ----------
        filename : existing filepath
            Path to an existing XML-file

        Returns
        -------

        """
        print("read_dcc_file:... %s" % filename)
        with open(filename, "r") as file:
            self.xml = file.read()
        return

    def read_dcc_string(self, xml):
        """
        Setter method takes xml and puts it into self.xml

        Parameters
        ----------
        xml : string
            xml-document as string

        Returns
        -------

        """
        self.xml = xml
        return

    def read_json_file(self, filename):
        """
        Reads the JSON-file in filename into self.json

        Parameters
        ----------
        filename : existing filepath
            Path to an existing XML-file

        Returns
        -------

        """
        print("read_json_file:... %s" % filename)
        with open(filename, "r") as file:
            self.json = file.read()
        return

    def read_json_string(self, json):
        """
        Setter method takes xml and puts it into self.xml

        Parameters
        ----------
        xml : string
            xml-document as string

        Returns
        -------

        """
        self.json = json
        return

    def __update_tree__(self):
        """
        Updates self.tree (lxml structure) from self.xml
        Sets self.root, self.nsmap, self.schema_name, self.schema_version, and schema_namespace.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        try:
            parser = ElementTree.XMLParser(recover=True)  # Recover from bad characters
            self.tree = ElementTree.fromstring(self.xml.encode(), parser=parser)  # Encode->bytes necessary!

            if self.tree.nsmap:
                self.nsmap = self.tree.nsmap
                self.nsmap_reversed = {v: k for k, v in self.nsmap.items()}  # Reverse nsmap for prefix lookup
            # Extract schema details if available
            schema_location = self.tree.attrib.get("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation")
            schema_url = None
            if schema_location:
                schema_parts = schema_location.split()
                if len(schema_parts) >= 2:
                    schema_namespace_value = schema_parts[0]  # Known namespace value
                    schema_url = schema_parts[-1]  # Schema URL

                    # Find the key in nsmap corresponding to the value
                    for prefix, namespace in self.nsmap.items():
                        if namespace == schema_namespace_value:
                            self.schema_prefix = prefix
                            break

                    # Process schema URL for schema_name and schema_version
                    self.schema_name, self.schema_version, cache_key_str = process_schema_url(schema_url)
            self.XSD_non_list_dict, self.XSD_list_dict, self.XSD_repeated_elements = self.XSDParserCacheWrapper.parse_with_cache(
                schema_url, namespace=self.schema_prefix)
            return
        except Exception as e:
            print(f"dcc_stuff.__update_tree__() validation failed for the given XML string! Error: {e}")
            return

    def __tree2dict__(self, node):
        """
        traverses the XML-tree starting at the root element and transforms it into
        a python dict of dicts of dicts ...

        Parameters
        ----------
        root : lxml.etree Element (not necessarilly the root of the tree)
            The starting point of traversal. Get it like:

            import lxml.etree as ElementTree
            with open(filename,"r") as file:
                tree = ElementTree.parse(file)
            root = tree.getroot()

        Returns
        -------
        ret : dict
            the information from the xml in a dict of dicts
        forceArrayTopLevel : bool default=False
            flag if the top level is forced to be an array
            the parser found a repeated field on the actual level so the top level must be an array
        """
        dc = {}
        forceArray = False
        forceArrayTopLevel = False
        if node.nsmap and (node == self.tree):
            tmp = {"@xmlns:" + key: node.nsmap[key] for key in node.nsmap}
            self.merge_dicts(dc, tmp)

        if node.attrib:
            tmp = {"@" + self.ns_clean(key): node.attrib[key] for key in node.attrib}
            self.merge_dicts(dc, tmp)

        if isinstance(node, ElementTree._Comment):
            tmp = json.loads(json.dumps({"@_Comment": node.text}))
            self.merge_dicts(dc, tmp)
            return (dc, False)

        elif isinstance(node, ElementTree._Element):

            if node.text:
                if not node.text.isspace():
                    self.merge_dicts(dc, json.loads(json.dumps({"#text": node.text})))
            tag=self.__get_prefixed_tag(node)
            if tag in self.XSD_repeated_elements:  # check if this Element is a repeatable field
                parent = node.getparent()
                parentName = self.__get_prefixed_tag(parent)
                # check if in parent element this node is actually repeated since only the name does not indicate this
                # so a si:realListXML list is repeated in a si:hybrid but not in a dcc:quantity
                listOfRepeatingParents = self.XSD_repeated_elements[tag][1]
                if parentName in listOfRepeatingParents:
                    forceArrayTopLevel = True  # set flag to force the top level to be an array
                else:
                    pass # have somthing to break at while debugging
                    #print(tag+' in Element '+str(parentName)+' is a repeated Type but not in this parent')

            if tag in self.XSD_list_dict:  # check if this Element is a listType
                forceArray = True  # set flag for listForcing
                castType = self.XSD_list_dict[tag]
                try:
                    splitted = node.text.split()
                except AttributeError as e:
                    if not node.text:
                        e.add_note("This probably occurred due to an empty element in the XML.")
                    raise e
                if "" in splitted:
                    warnings.warn(
                        "Space separated field contains excessive white space characters. This is not allowed, the spaces have been stripped!")
                splitted = ' '.join(splitted).split()
                try:
                    # TODO implement parallel processing here
                    casted = [castType(item) for item in splitted]
                except (ValueError, TypeError) as e:
                    warnings.warn(f"Failed to cast elements in list {splitted} to {castType}: {e}")
                self.merge_dicts(dc, {"#list": casted})

            if len(node) > 0:
                for i, child in enumerate(node):
                    cildresult, forceArrayForMemberFlag = self.__tree2dict__(child)
                    self.merge_dicts(dc, cildresult, forceArray=forceArray or forceArrayForMemberFlag)

            return {self.ns_clean(str(node.tag)): dc}, forceArrayTopLevel

    def xml2dict(self):
        """
        takes the self.xml attribute and by using lxml converts it into
        self.tree and by by using self.__tree2dict__ fills the
        self.dic attribute

        Parameters
        ----------
        None

        Returns
        -------
        None

        """

        if self.xml == "":
            print("dcc_stuff.xml2dict: ERROR xml-string is empty!")
            return {}
        else:
            self.__update_tree__()  # update the xml-tree from self.xml
            self.dic, retunFlag = self.__tree2dict__(self.tree)  # pares the tree from root
            return

    def dict2json(self):
        """
        takes self.dic and generates self.json as json-textstring

        Parameters
        ----------
        xml : string
            xml-document as string

        Returns
        -------

        """

        try:
            self.json = json.dumps(self.dic, cls=DCCJSONEncoder)
        except Exception as e:
            print("<ERROR>dcc.dict2json failed in json.dumps()</ERROR>")
            print(e)

    def get_json(self, beauty=True, indent=4):
        """
        returns the (beautyfied) json string of self.

        Parameters
        ----------
        beauty : bool (True)
            sets whether the string is beautyfied (for humans)

        indent : integer
            sets the indentation width for beautification

        Returns
        -------
        json-string

        """

        self.dict2json()  # update the json from self.dic
        if beauty:
            ret = json.dumps(self.dic, indent=indent, cls=DCCJSONEncoder) # dump the dict to string
        else:
            ret = json.dumps(self.dic, cls=DCCJSONEncoder)
        return ret

    def ns_clean(self, tag):
        """
        shortens namespace information in xml-tags

        Parameters
        ----------
        tag : string
            the tag that has to be checked for know namespaces

        Returns
        -------
        tag : string
            the shortened version of the tag.

        """
        for k, v in self.nsmap.items():  # check for the namespaces in nsmap
            if "{" + str(v) + "}" in tag:
                tag = tag.replace("{" + str(v) + "}", k + ":")
                break
        return tag

    def merge_dicts(self, d1, d2, forceArray=False):
        """
        merge dict d2 into d1 without loosing entries in either of both.
        If a key of d2 already exists in d1,
        make the element of d1 an array if neccessary and append the
        value from d2 to that array

        Parameters
        ----------
        d1 : dict
            target of the merger
        d2 : dict
            source of the merger
        forceArray : bool (False)
            sets whether d1 is forced to be an array.
            The default is False.
        Returns
        -------
        d1 : dict
            merged dict

        """
        for k, v in d2.items():  # iterate of d2
            if k in d1:  # emergency array check if keys are doubled it must be an array even if forceArray is False

                if isinstance(d1[k], list):
                    d1[k].append(v)
                else:
                    warnings.warn(
                        str("Key " + str(k) + " is doubled in dict1 and dict2. It will be forced to be an array!"),
                        RuntimeWarning)
                    d1[k] = [d1[k], v]
            elif forceArray:
                d1[k] = [v]  # convert v to list this is the effect of forceArray
            else:
                d1[k] = v
        return d1

    # ------------ Generate XML from dict ---------
    def __dict2attrib__(self, value):
        attrib = ""
        if isinstance(value, dict):
            for k, v in value.items():
                if self.__isattribute__(k):
                    if v[0] != '"':
                        v = '"' + v
                    if v[-1] != '"':
                        v = v + '"'
                    attrib = attrib + (" %s=%s" % (k[1:], v))  # index 1 removes leading @
        if isinstance(value, list):
            for v in value:
                attrib += self.dict2attrib(v)
        return attrib

    def __isattribute__(self, key):
        """
        Checks whether the key is meant to indicate an attribute
        i.e. the first character is "@"

        Parameters
        ----------
        key : dict key
            The Key which is checked for being an attribute

        Returns
        -------
        ret : boolean
            True="the key is an attribute", False="the key is a tag"

        """
        # ret = (key in ["schemaVersion","schemaLocation","lang","id","refType"]) or ("xmlns" in key)
        ret = (str(key)[0] == "@" and str(key) != "@_Comment")
        return ret

    def __dict2text__(self, value):
        # search for "#text" keys and return the value
        text = ""
        if isinstance(value, dict):
            for k, v in value.items():
                if k[0] == "#":
                    text = v

        return text

    def json2dict(self):
        """
        Takes the self.json attribute and parses it to a dict
        sets self.dic to the resulting dict.

        Parameters
        ----------

        Returns
        -------

        """
        self.dic = json.loads(self.json, object_hook=dcc_json_decoder)
        return

    def __dict2xml__(self, dic):
        """
        Takes the dict representation and generates an xml-string
        Operates recursive and return the string, therefore.
        (it does not set self.xml!)

        Parameters
        ----------
        dic : dict with the dcc information

        Returns
        -------

        """

        attribs = ""  # collect the attributes for this tag
        ret = ""  # collect the text in this tag

        try:
            if '#text' in dic and '#list' in dic:
                warnings.warn("Both #text and #list are present in the same tag. #List will be ignored", RuntimeWarning)
                del dic['#list']
            if '#list' in dic and not '#text' in dic:
                warnings.warn("Only #list is present in the tag. #List will be converted to text", RuntimeWarning)
                dic['#text'] = " ".join(str(item) for item in dic['#list'])
                del dic['#list']
            for k, v in dic.items():
                if isinstance(v, list):  # repeated tags of same type
                    for item in v:  # unroll
                        ret += self.__dict2xml__({k: item})  # process each as single dict
                else:
                    if k == "@_Comment":
                        ret += self.TpComment.render(comment=v) + "\n"  # Exceptional case for comments
                    elif k == "#text":
                        ret = str(v)  # exceptional case for the tag-content
                    elif k == "#list":
                        pass  # TODO change parsing to use list if it exists instead of #text
                    else:  # remaining are attributes and usual tags
                        attribs = self.__dict2attrib__(v)  # collect all attributes
                        if k[0] == "@":
                            pass  # ignore attributes here
                        else:  # work on the single tag with template
                            ret += "\n" + self.TpTag.render(name=k,
                                                            attributes=attribs,
                                                            text=self.__dict2xml__(v)) + "\n"
                # print(ret)  debugPrint   add option for that to reactivate
        # Exception Handling
        except Exception as exceptInst:
            if not self.parsingErrorInRecursionOccured:
                # OK we are at the cause of the Error
                self.firstParsingError = str(exceptInst)  # save the fist error Message
                # create an list with the first chars of the dict we ware parsing at the moment
                if len(str(dic)) > TRACBACKLENGTH:
                    self.parsingErrorTraceBack = [str(dic)[:TRACBACKLENGTH].replace('\n', '\\n')]
                else:
                    self.parsingErrorTraceBack = [str(dic).replace('\n', '\\n')]
                self.parsingErrorInRecursionOccured = True
            else:
                # we had an error before so we don't want the error message but the first chars of the dict at this recursion level
                if len(str(dic)) > TRACBACKLENGTH:
                    self.parsingErrorTraceBack.append(str(dic)[:TRACBACKLENGTH].replace('\n', '\\n'))
                else:
                    self.parsingErrorTraceBack.append(str(dic).replace('\n', '\\n'))
            raise exceptInst
        # End Exception Handling
        return ret

    def dict2xml(self):
        """
        Takes the self.dic attribute and generates an xml-string
        and sets it in self.xml
        (calls the recursive privat version __dict2xml__)

        Parameters
        ----------

        Returns
        -------

        """
        xml = self.__dict2xml__(self.dic)  # the private method runs recursively!
        # now remove blank lines in xml
        self.xml = os.linesep.join([s for s in xml.splitlines() if s.strip()])
        return

    def get_xml(self, beauty=True):
        """
        returns the (beautyfied) xml string of self.

        Parameters
        ----------
        beauty : bool (True)
            sets whether the string is beautyfied (for humans)

        Returns
        -------
        xml-string

        """
        self.__update_tree__()  # update the tree from the current self.xml
        try:
            ret = ElementTree.tostring(self.tree, pretty_print=beauty, encoding="unicode")

        except:
            print("<ERROR>dcc_stuff.get_xml() failed </ERROR>")
            ret = self.xml
        return ret

    def __get_prefixed_tag(self, node):
        """
        Returns the prefixed tag for the given XML node.

        Parameters
        ----------
        node : lxml.etree.Element
            The XML element for which to get the prefixed tag.

        Returns
        -------
        str
            The prefixed tag in the format 'prefix:tagname'.
        """
        tag = node.tag
        if '}' in tag:
            uri, local_tag = tag[1:].split('}')
            prefix = self.nsmap_reversed.get(uri, None)
            if prefix:
                return f"{prefix}:{local_tag}"
            else:
                return local_tag
        else:
            return tag


def XMLToJson(xml):
    dccInst = dcc()
    if isinstance(xml, str):
        dccInst.read_dcc_string(xml)
    else:
        dccInst.read_dcc_string(str(xml))
    dccInst.xml2dict()
    return json.loads(dccInst.get_json())


def JSONToXML(jsonData):
    dccInst = dcc()
    if isinstance(jsonData, str):
        dccInst.read_json_string(jsonData)
    elif isinstance(jsonData, dict):
        dccInst.read_json_string(json.dumps(jsonData))
    else:
        dccInst.read_json_string(str(jsonData))
    dccInst.json2dict()
    dccInst.dict2xml()
    return dccInst.get_xml()


def beautify_xml(text):
    parser = ElementTree.XMLParser(remove_blank_text=True, ns_clean=True)
    test = text.replace("\\\"", "\"")
    # print(test)
    try:
        tree = ElementTree.fromstring(test, parser=parser)
        ret = ElementTree.tostring(tree, pretty_print=True, encoding="unicode")
    except:
        ret = "<ERROR>dcc_stuff:beautyfy_xml failed </ERROR>"
    return ret


# TODO Add Unit Test
def getFromDict(dataDict, mapList):
    return reduce(operator.getitem, mapList, dataDict)


# TODO Add Unit Test
def setInDict(dataDict, mapList, value):
    getFromDict(dataDict, mapList[:-1])[mapList[-1]] = value
