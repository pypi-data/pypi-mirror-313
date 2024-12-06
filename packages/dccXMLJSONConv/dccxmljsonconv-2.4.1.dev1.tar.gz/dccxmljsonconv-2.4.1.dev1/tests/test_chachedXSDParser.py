import os
import json
import pytest
from dccXMLJSONConv.typeCastDictCreator import XSDParserCacheWrapper
@pytest.fixture
def setup_wrapper():
    # Set up a temporary JSON file to simulate cache
    test_cache_file = "test_cache.json"
    if os.path.exists(test_cache_file):
        os.remove(test_cache_file)
    with open(test_cache_file, 'w') as f:
        json.dump({}, f)

    # Initialize the XSDParserCacheWrapper with the test cache file
    wrapper = XSDParserCacheWrapper(test_cache_file)
    yield wrapper, test_cache_file

    # Clean up the temporary JSON file after tests
    if os.path.exists(test_cache_file):
        os.remove(test_cache_file)

#TODO fix this test new cahce is merged an does not replace existing one
def test_parse_with_cache_no_cache(setup_wrapper):
    wrapper, _ = setup_wrapper

    # Test with a schema that is not in the cache
    url = 'https://www.ptb.de/dcc/v3.3.0/dcc.xsd'
    namespace = 'dcc'
    version = None

    # Attempt to parse the schema and add it to cache
    non_list_dict, list_dict, repeated_elements = wrapper.parse_with_cache(url, namespace, version)

    # Check if dictionaries are populated (basic check)
    assert isinstance(non_list_dict, dict)
    assert isinstance(list_dict, dict)
    assert len(non_list_dict) > 0
    assert len(list_dict) > 0


def test_parse_with_cache_existing_cache(setup_wrapper):
    wrapper, test_cache_file = setup_wrapper

    # Add a dummy entry to the cache file
    dummy_key = json.dumps(('https://www.ptb.de/dcc/', '3.3.0'))
    dummy_value = {
        'non_list_typecast_dict': json.dumps({'element1': 'str'}),
        'list_typecast_dict': json.dumps({'element2': 'int'})
    }
    with open(test_cache_file, 'w') as f:
        json.dump({dummy_key: dummy_value}, f)

    # Attempt to parse the schema with the same URL and version
    url = 'https://www.ptb.de/dcc/v3.3.0/dcc.xsd'
    namespace = 'dcc'
    version = '3.3.0'

    non_list_dict, list_dict, repeated_elements = wrapper.parse_with_cache(url, namespace, version)

    # Check if the returned dictionaries match the dummy data
    assert isinstance(non_list_dict, dict)
    assert isinstance(list_dict, dict)
    assert not 'element1' in non_list_dict
    assert non_list_dict['ds:HMACOutputLength'] == int
    assert list_dict['si:labelXMLList'] == str


if __name__ == '__main__':
    pytest.main()
