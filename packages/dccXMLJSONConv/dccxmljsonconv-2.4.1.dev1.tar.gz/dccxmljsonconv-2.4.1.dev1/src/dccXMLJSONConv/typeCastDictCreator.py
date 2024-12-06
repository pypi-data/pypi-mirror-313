import copy
import xml.etree.ElementTree as ET
import warnings
from urllib.parse import urljoin
import json
import os
import requests
from lxml import etree
from io import BytesIO
from importlib import resources  # Python 3.7+ or use importlib_resources backport
import re

class XSDParser:
    def __init__(self, schema_downloader):
        self.schema_downloader = schema_downloader
        self.simple_elements = []
        self.complex_type_names = set()
        self.complex_type_elementNames = {}
        self.restricted_types = []
        self.list_types = []
        self.element_dict = {}
        self.absetype = {}  # Dictionary to map types to their restricted base type
        self.simple_list_elements = []  # List to store elements with list types
        self.simple_non_list_elements = []  # List to store elements with non-list types
        self.processed_non_list_elements = []  # List to store processed non-list elements
        self.processed_list_elements = []  # List to store processed list elements
        self.current_namespace = None  # Track current namespace abbreviation
        self.repeated_elements = []
        self.repeated_elements2 = []
        self.nonRepeated_elements = []
        self.processed_repeated_elements ={}
    def get_namespace_prefix(self, root):
        """
        Extract the namespace prefix from the root element's xmlns definitions.
        """
        namespaces = self.extract_namespaces(root)
        for prefix, uri in namespaces.items():
            if uri == self.get_namespace(root):
                return prefix
        return None

    def extract_namespaces(self, root):
        """
        Extract namespaces and their prefixes from the root element.
        """
        namespaces = {}
        for key, value in root.attrib.items():
            if key.startswith("xmlns"):
                prefix = key[6:] if ":" in key else ""
                namespaces[prefix] = value
        return namespaces

    def parse_xsd_files(self):
        """
        Parse all XSD files according to their hierarchy to extract information.
        """
        for level in self.schema_downloader.hierarchy:
            for schema_name, schema_file, nameSpaceAbbr in level:
                tree = ET.parse(schema_file)
                root = tree.getroot()
                # Extract the current namespace abbreviation from the root
                self.current_namespace = nameSpaceAbbr
                self.parse_xsd_simple_elements(root)
                self.parse_xsd_simple_types(root)
                repeated_elements, non_repeated_elements=self.parse_xsd_repeated_elements(root)
                pass
        # Calculate the absetype dictionary after parsing restricted types
        self.calculate_absetype()
        self.sort_simple_elements()
        self.replace_simpletypes_with_restricted()
        self.consolidate_repeatedElements()
        return

    def parse_xsd_simple_elements(self, root):
        """
        Parse the XSD file and extract a list of tuples of node names (with namespace) and their simple types.
        Only elements with simple types (those without complex types or child nodes) are included.
        """
        # Define the XSD namespace
        xsd_namespace = "{http://www.w3.org/2001/XMLSchema}"

        # Collect all complex types to identify which types to skip, including namespace prefixes
        for complex_type in root.iter(f"{xsd_namespace}complexType"):
            complex_type_name = complex_type.get("name")
            if complex_type_name:
                namespace = self.get_namespace(complex_type)
                qualified_name = f"{{{namespace}}}{complex_type_name}" if namespace else complex_type_name
                qualified_name = self.current_namespace + ':' + complex_type_name
                self.complex_type_names.add(qualified_name)

        # Find all elements that do not contain complex types (leaf elements with truly simple types)
        for element in root.iter(f"{xsd_namespace}element"):
            name = element.get("name")
            simple_type = element.get("type")
            namespace = self.get_namespace(element)

            if name and simple_type:
                # Only add elements where the type is not in complex types
                if simple_type not in self.complex_type_names:
                    qualified_name = self.current_namespace + ':' + name
                    self.simple_elements.append((qualified_name, simple_type))
                elif simple_type in self.complex_type_names:
                    try:
                        qualified_name = self.current_namespace + ':' + name
                        self.complex_type_elementNames[simple_type].add(qualified_name)
                    except KeyError as KE:
                        qualified_name = self.current_namespace + ':' + name
                        self.complex_type_elementNames[simple_type]=set([qualified_name])
        #Within a single schema, the mapping of namespace:name to type is injective. This means:
        #In a single schema, each qualified name (namespace:name) uniquely identifies one type.
        #You cannot have two types with the same namespace:name in the same schema because it would cause a naming conflict.
        return

    #TODO info_dict will become positional arg after texting development
    def parse_xsd_repeated_elements(self, root, parent_name=None,infoDict={'complexType':False,'complexTypeName':None}):
        """
        Parse the XSD file and extract a list of tuples of element names, their types, and their parent elements where maxOccurs is 'unbounded'.
        The repeated elements can be either simple or complex types.
        """
        # Define the XSD namespace
        local_info_dict=copy.deepcopy(infoDict)
        xsd_namespace = "{http://www.w3.org/2001/XMLSchema}"
        # List to store repeated elements and their types
        repeated_elements = []
        repeated_elements2 = []
        non_repeated_elements = []
        name=None
        # Iterate over all elements in the current root
        for element in root:
            if element.tag == f"{xsd_namespace}complexType":
                local_info_dict['complexType']=True
                if element.get('name'):
                    local_info_dict['complexTypeName'] = str(self.current_namespace)+':'+element.get('name')
                else:
                    # this will be None in this case
                    local_info_dict['complexTypeName'] = element.get('name')
            if element.tag == f"{xsd_namespace}element":
                name = element.get("name")
                type_name = element.get("type")
                max_occurs = element.get("maxOccurs")

                # Check if maxOccurs is 'unbounded', which means the element can occur repeatedly
                if max_occurs == "unbounded" and name:
                    if not type_name:
                        # If the type is not explicitly defined, it may be inline
                        complex_type = element.find(f"{xsd_namespace}complexType")
                        if complex_type is not None:
                            type_name = f"{self.current_namespace}:{name}_complex"
                            self.complex_type_names.add(type_name)

                    # Add the repeated element, its type, and parent to the list
                    if type_name:
                        qualified_name = f"{self.current_namespace}:{name}"
                        repeated_elements.append((qualified_name, type_name, f"{self.current_namespace}:{parent_name}",local_info_dict))
                else:
                    if name:
                        if not type_name:
                            # If the type is not explicitly defined, it may be inline
                            complex_type = element.find(f"{xsd_namespace}complexType")
                            if complex_type is not None:
                                type_name = f"{self.current_namespace}:{name}_complex"
                                self.complex_type_names.add(type_name)
                        # Add the non-repeated element to the list
                        if type_name:
                            qualified_name = f"{self.current_namespace}:{name}"
                            non_repeated_elements.append((qualified_name, type_name))

            # Recursively parse child elements, passing the current element's name as the parent if it exists
            if name is None:
                name=parent_name

            child_repeated_elements, child_non_repeated_elements = self.parse_xsd_repeated_elements(element, parent_name=name,infoDict=local_info_dict)
            repeated_elements.extend(child_repeated_elements)
            non_repeated_elements.extend(child_non_repeated_elements)

        # Append the repeated elements to the class variable for further processing
        self.repeated_elements.extend(repeated_elements)
        self.nonRepeated_elements.extend(non_repeated_elements)
        return repeated_elements, non_repeated_elements

    def consolidate_repeatedElements(self):
        """
        Consolidate repeated elements into a single dictionary.
        Generate warnings if elements have the same name but different types or if elements are found in both repeated and non-repeated lists.
        """
        consolidated_dict = {}

        # Create a dictionary to store the element information with types and parent names
        for name, type_name, parent,complexTypeInfo in self.repeated_elements:
            if name not in consolidated_dict:
                consolidated_dict[name] = (type_name, set(),set())
                if complexTypeInfo['complexTypeName']:
                    consolidated_dict[name][2].add(complexTypeInfo['complexTypeName'])
            else:
                # If the type is different, raise a warning
                if consolidated_dict[name][0] != type_name:
                    warnings.warn(f"Conflicting types for repeated element '{name}': '{consolidated_dict[name][0]}' and '{type_name}'")

            consolidated_dict[name][1].add(parent)
            if complexTypeInfo['complexTypeName'] in self.complex_type_elementNames:
                namesWithtihsType=list(self.complex_type_elementNames[complexTypeInfo['complexTypeName']])
                consolidated_dict[name][1].update((namesWithtihsType))

        # Generate warnings for elements that are in both repeated and non-repeated lists
        repeated_names = {name for name, _, _ ,_ in self.repeated_elements}
        non_repeated_names = {name for name, _ in self.nonRepeated_elements}
        common_names = repeated_names.intersection(non_repeated_names)
        for name in common_names:
            warnings.warn(f"Element '{name}' is found in both repeated and non-repeated lists")

        # Convert parent sets to lists in the final dictionary
        final_dict = {name: (type_name, list(parents)) for name, (type_name, parents,info) in consolidated_dict.items()}
        self.processed_repeated_elements=final_dict
        return final_dict

    def get_namespace(self, element):
        """
        Extract the namespace from the given XML element.
        """
        if element.tag.startswith("{"):
            return element.tag.split("}")[0].strip("{")
        return None

    def parse_xsd_simple_types(self, root):
        """
        Parse the XSD file and find all simple types, categorizing them into restricted and list types.
        """
        # Define the XSD namespace
        xsd_namespace = "{http://www.w3.org/2001/XMLSchema}"

        # Iterate over all simpleType elements
        for simple_type in root.iter(f"{xsd_namespace}simpleType"):
            type_name = simple_type.get("name")

            # Check for restriction-based simple types
            restriction = simple_type.find(f"{xsd_namespace}restriction")
            if restriction is not None:
                base_type = restriction.get("base")
                if type_name and base_type:
                    self.restricted_types.append((self.current_namespace + ':' + type_name, base_type))
                continue

            # Check for list-based simple types
            list_element = simple_type.find(f"{xsd_namespace}list")
            if list_element is not None:
                item_type = list_element.get("itemType")
                if type_name and item_type:
                    self.list_types.append((self.current_namespace + ':' + type_name, item_type))
                continue
        return

    def calculate_absetype(self):
        """
        Calculate absetype as a dictionary mapping each restricted type to its base type.
        """
        self.absetype = {name: base for name, base in self.restricted_types}

    def convert_to_dict_with_warnings(self):
        """
        Convert the simple_elements list to a dictionary, with warnings on duplicate names with differing types.
        """
        for name, simple_type in self.simple_elements:
            if name in self.element_dict:
                if self.element_dict[name] != simple_type:
                    warnings.warn(
                        f"Node '{name}' has conflicting types: '{self.element_dict[name]}' and '{simple_type}'")
            self.element_dict[name] = simple_type

    def sort_simple_elements(self):
        """
        Sort simple_elements into lists based on whether they are list types or not,
        and replace types with their restricted base type if possible.
        """
        list_type_names = {name for name, _ in self.list_types}

        for name, simple_type in self.simple_elements:
            # Remove the prefix (if any) from simple_type for comparison
            simple_type_no_prefix = simple_type.split(":")[-1]

            # Replace simple_type with its restricted base if available from absetype
            base_type = self.absetype.get(simple_type, simple_type)

            # Sort into list or non-list based on whether the type is a list type
            if base_type in list_type_names:
                self.simple_list_elements.append((name, base_type))
            else:
                self.simple_non_list_elements.append((name, base_type))

    def replace_simpletypes_with_restricted(self):
        """
        Replace the simple types in simple_non_list_elements and simple_list_elements
        with their corresponding restricted types, if applicable, and store the results
        in processed_non_list_elements and processed_list_elements.
        """
        # Initialize empty lists for processed elements
        self.processed_non_list_elements = []
        self.processed_list_elements = []

        # Process non-list elements
        for name, simple_type in self.simple_non_list_elements:
            # Remove prefix from simple_type for consistent lookup
            simple_type_no_prefix = simple_type.split(":")[-1]
            # Check if there is a restricted base type and replace if available
            base_type = self.absetype.get(simple_type_no_prefix, simple_type)
            self.processed_non_list_elements.append((name, base_type))

        listTypeDict = dict(self.list_types)
        restrictedTypeDict = dict(self.restricted_types)
        # Process list elements
        for name, simple_type in self.simple_list_elements:
            # Remove prefix from simple_type for consistent lookup
            # Check if there is a restricted base type and replace if available
            base_type = listTypeDict.get(simple_type, simple_type)
            try:
                base_type = restrictedTypeDict[simple_type]
            except KeyError:
                if base_type.split(":")[0] != 'xs':
                    try:
                        base_type = self.absetype[base_type]
                    except KeyError:
                        print('ListType ' + base_type + ' does not have an know simple Type and is not xs:')
            self.processed_list_elements.append((name, base_type))

    def create_python_typecast_dict(self):
        """
        Create two typecast dictionaries: one for non-list elements and one for list elements,
        with XML element names as keys and corresponding Python types as values.
        Raise a runtime error if conflicting types are found for the same element name.
        """
        non_list_typecast_dict = {}
        list_typecast_dict = {}
        xs_type_mapping = {
            'xs:string': str,
            'xs:int': int,
            'xs:integer': int,
            'xs:float': float,
            'xs:double': float,
            'xs:boolean': bool,
            'xs:date': 'datetime.date',
            'xs:dateTime': 'datetime.datetime',
            'xs:anyURI': str,
            'xs:duration': 'datetime.timedelta',
            'xs:base64Binary': bytes,
            'string': str,
            'integer': int,
            'base64Binary': bytes
        }

        # Process non-list elements
        for name, simple_type in self.processed_non_list_elements:
            python_type = xs_type_mapping.get(simple_type, None)
            if python_type is None:
                warnings.warn(
                    f"Unknown type mapping for element '{name}' with type '{simple_type}', defaulting to 'str'")
                python_type = str
            if name in non_list_typecast_dict and non_list_typecast_dict[name] != python_type:
                raise RuntimeError(
                    f"Conflicting types for element '{name}': '{non_list_typecast_dict[name]}' and '{python_type}'")
            non_list_typecast_dict[name] = python_type
        nonListElementsTempDict = dict(self.simple_non_list_elements)
        # Process list elements
        for name, simple_type in self.processed_list_elements:
            python_type = xs_type_mapping.get(simple_type, None)
            if python_type is None:
                python_type = nonListElementsTempDict.get(simple_type, None)
                print("DGBUG")
            if name in list_typecast_dict and list_typecast_dict[name] != python_type:
                raise RuntimeError(
                    f"Conflicting types for list element '{name}': '{list_typecast_dict[name]}' and '{python_type}'")
            list_typecast_dict[name] = python_type

        return non_list_typecast_dict, list_typecast_dict,self.processed_repeated_elements

    def serialize_typecast_dict(self, typecast_dict):
        """
        Convert the typecast dictionary to a JSON-serializable format.
        """
        serializable_dict = {}
        for key, value in typecast_dict.items():
            if isinstance(value, type):
                serializable_dict[key] = value.__name__
            else:
                serializable_dict[key] = str(value)
        return serializable_dict

    def deserialize_typecast_dict(self, serialized_dict):
        """
        Convert the JSON-serializable format back to the typecast dictionary.
        """
        xs_type_mapping = {
            'str': str,
            'int': int,
            'float': float,
            'bool': bool,
            'datetime.date': 'datetime.date',
            'datetime.datetime': 'datetime.datetime',
            'datetime.timedelta': 'datetime.timedelta',
            'bytes': bytes
        }
        deserialized_dict = {}
        for key, value in serialized_dict.items():
            deserialized_dict[key] = xs_type_mapping.get(value, str)
        return deserialized_dict

class SchemaDownloader:
    def __init__(self, main_url, topLevelNamespace):
        self.main_url = main_url
        self.visited = {}
        self.hierarchy = []
        self.schemas = {}
        # TODO this sucks extract toplevel namespace from first xsd.
        self.topLevelNamespace = topLevelNamespace

        # Setup proxies from system environment
        self.session = requests.Session()
        self.session.proxies.update({
            "http": os.getenv("HTTP_PROXY"),
            "https": os.getenv("HTTPS_PROXY"),
            "no_proxy": os.getenv("NO_PROXY"),
        })

    def download_schema(self, url):
        """Downloads the schema file from the given URL and stores it in memory."""
        response = self.session.get(url)
        response.raise_for_status()

        # Store content in memory using BytesIO
        file_content = BytesIO(response.content)

        # Use the filename for reference
        filename = url.split('/')[-1]
        self.schemas[filename] = file_content

        return filename

    def get_schema_dependencies(self, schema_name, base_url, namespace_abbr=None):
        """Gets all schema dependencies (xs:include, xs:import) recursively and records their hierarchy level."""
        if schema_name in self.visited:
            return self.visited[schema_name]

        # Initialize depth to zero if this schema has no dependencies
        depth = 0
        dependencies = []

        # Parse the schema from memory
        schema_file = self.schemas[schema_name]
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(schema_file, parser)
        root = tree.getroot()

        for element in root.findall(".//{http://www.w3.org/2001/XMLSchema}include"):
            schema_location = element.get('schemaLocation')
            deeper_namespace_abbr = self.extract_namespace_abbr(root, element.get('namespace'))

            if schema_location:
                full_url = urljoin(base_url, schema_location)
                dep_schema_name = self.download_schema(full_url)
                # Recursive call to download sub-schema
                dep_depth = self.get_schema_dependencies(dep_schema_name, base_url, namespace_abbr=deeper_namespace_abbr)
                dependencies.append((dep_schema_name, self.schemas[dep_schema_name], namespace_abbr))
                depth = max(depth, dep_depth + 1)

        for element in root.findall(".//{http://www.w3.org/2001/XMLSchema}import"):
            schema_location = element.get('schemaLocation')
            deeper_namespace_abbr = self.extract_namespace_abbr(root, element.get('namespace'))

            if schema_location:
                full_url = urljoin(base_url, schema_location)
                dep_schema_name = self.download_schema(full_url)
                # Recursive call to download sub-schema
                dep_depth = self.get_schema_dependencies(dep_schema_name, base_url, namespace_abbr=deeper_namespace_abbr)
                dependencies.append((dep_schema_name, self.schemas[dep_schema_name], namespace_abbr))
                depth = max(depth, dep_depth + 1)

        # Record the depth for the current schema
        self.visited[schema_name] = depth
        # Ensure current schema is placed in the right hierarchy level
        while len(self.hierarchy) <= depth:
            self.hierarchy.append([])
        self.hierarchy[depth].append((schema_name, self.schemas[schema_name], namespace_abbr))

        return depth

    def extract_namespace_abbr(self, root, namespace_uri):
        """
        Extract the namespace abbreviation from the root element's xmlns definitions for the given namespace URI.
        """
        namespaces = self.extract_namespaces(root)
        for prefix, uri in namespaces.items():
            if uri == namespace_uri:
                return prefix
        return None

    def extract_namespaces(self, root):
        """
        Extract namespaces and their prefixes from the root element.
        """
        namespaces = root.nsmap
        return namespaces

    def download_all_schemas(self):
        """Downloads the main schema and all its dependencies, storing them in memory and creating a hierarchy."""
        # Download the main schema first
        main_schema_name = self.download_schema(self.main_url)

        # Get all schema dependencies recursively
        self.get_schema_dependencies(main_schema_name, "/".join(self.main_url.split('/')[:-1]), namespace_abbr=self.topLevelNamespace)

        # Return the hierarchy list
        return self.hierarchy



class XSDParserCacheWrapper:
    def __init__(self, json_storage_path=None):
        with resources.open_text('dccXMLJSONConv.data', 'schemaTypeCastCache.json') as f:
            self.cache = json.load(f)

        # If the user provides a JSON storage path, load and merge any additional schemas
        if json_storage_path and os.path.exists(json_storage_path):
            with open(json_storage_path, 'r') as f:
                user_cache = json.load(f)
                self.cache.update(user_cache)

        # Save the path for later use
        self.json_storage_path = json_storage_path

    def parse_with_cache(self, url=None, namespace='dcc', version=None):
        """
        Parse the schema with caching to prevent re-parsing of already parsed schemas.

        Parameters:
            url (str): URL of the main schema.
            namespace (str): Namespace abbreviation.
            version (str or None): Version of the schema.

        Returns:
            tuple: Non-list typecast dictionary and list typecast dictionary.
        """
        # Extract version from URL if not provided
        #TODO get namespace from initial XSD
        #1 get targetNamespace attr from xsd root.
        #2 parse all xmlns:* attrs
        #3 find xmlns:* attr that contains targetNamespace url
        #4 the xmlns:NAMESPACE is our namespace abrv
        if url is None:
            # Handling default case
            defaultKey = list(self.cache.keys())[0]
            non_list_typecast_dict = self.deserialize_typecast_dict(self.cache[defaultKey]['non_list_typecast_dict'])
            list_typecast_dict = self.deserialize_typecast_dict(self.cache[defaultKey]['list_typecast_dict'])
            repeated_elements_list = self.cache[defaultKey]['repeated_elements']
            return non_list_typecast_dict, list_typecast_dict, repeated_elements_list

        if version is None:
            match = re.search(r'/v([\d.]+(?:-rc\.\d+)?)', url)
            if match:
                version = match.group(1)
            else:
                version = 'default_version'

        # Remove version and 'www.' from the URL to create a base URL
        base_url = re.sub(r'/v[\d.]+(?:-rc\.\d+)?', '', url)  # Remove version
        base_url = re.sub(r'^https?://www\.', 'https://', base_url)  # Remove 'www.' from the base URL

        cache_key = (base_url, version)
        cache_key_str = json.dumps(cache_key)

        # Check if schema has already been parsed
        if cache_key_str in self.cache:
            non_list_typecast_dict = self.deserialize_typecast_dict(self.cache[cache_key_str]['non_list_typecast_dict'])
            list_typecast_dict = self.deserialize_typecast_dict(self.cache[cache_key_str]['list_typecast_dict'])
            repeated_elements_list = self.cache[cache_key_str]['repeated_elements']
        else:
            # Schema not in cache, parse it
            schema_downloader = SchemaDownloader(url, topLevelNamespace=namespace)
            schema_hierarchy = schema_downloader.download_all_schemas()
            parser = XSDParser(schema_downloader)
            parser.parse_xsd_files()

            # Generate typecast dictionaries
            non_list_typecast_dict, list_typecast_dict, repeated_elements_list = parser.create_python_typecast_dict()

            # Serialize the dictionaries before saving to cache
            serialized_non_list = parser.serialize_typecast_dict(non_list_typecast_dict)
            serialized_list = parser.serialize_typecast_dict(list_typecast_dict)
            # Save parsed data to the cache
            self.cache[cache_key_str] = {
                'non_list_typecast_dict': serialized_non_list,
                'list_typecast_dict': serialized_list,
                'repeated_elements': repeated_elements_list
            }

            # Update the storage file if a path is provided
            if self.json_storage_path:
                self.save_cache()

        return non_list_typecast_dict, list_typecast_dict, repeated_elements_list

    def save_cache(self, output_path):
        """
        Save the current cache to a JSON file.

        Parameters:
            output_path (str or None): Path to save the JSON file. If None, save to the original storage path.
        """

        with open(output_path, 'w') as f:
            json.dump(self.cache, f, indent=2,sort_keys=True)


    def extract_base_namespace(self, root):
        """
        Extract the base namespace from the root element's xmlns definitions.
        """
        namespaces = root.nsmap
        for prefix, uri in namespaces.items():
            if prefix == "":  # Default namespace
                return uri
        return None

    def deserialize_typecast_dict(self, serialized_dict):
        """
        Convert the JSON-serializable format back to the typecast dictionary.
        """
        xs_type_mapping = {
            'str': str,
            'int': int,
            'float': float,
            'bool': bool,
            'datetime.date': 'datetime.date',
            'datetime.datetime': 'datetime.datetime',
            'datetime.timedelta': 'datetime.timedelta',
            'bytes': bytes
        }
        deserialized_dict = {}
        for key, value in serialized_dict.items():
            deserialized_dict[key] = xs_type_mapping.get(value, str)
        return deserialized_dict

if __name__=='__main__':
# Example usage of the wrapper class
    cache_wrapper = XSDParserCacheWrapper()
    schmaURLS=['https://www.ptb.de/dcc/dcc.xsd','https://www.ptb.de/dcc/v3.3.0/dcc.xsd','https://www.ptb.de/dcc/v3.0.0-rc.2/dcc.xsd','https://www.ptb.de/dcc/v3.2.1/dcc.xsd','https://www.ptb.de/dcc/v3.1.0/dcc.xsd','https://ptb.de/dcc/v3.2.0/dcc.xsd','https://www.ptb.de/dcc/v2.4.0/dcc.xsd']
    for schmeaURL in schmaURLS:
        non_list_typecast_dict, list_typecast_dict, repeated_elements = cache_wrapper.parse_with_cache(schmeaURL, namespace='dcc')
    cache_wrapper.save_cache('./src/dccXMLJSONConv/data/schemaTypeCastCache.json')