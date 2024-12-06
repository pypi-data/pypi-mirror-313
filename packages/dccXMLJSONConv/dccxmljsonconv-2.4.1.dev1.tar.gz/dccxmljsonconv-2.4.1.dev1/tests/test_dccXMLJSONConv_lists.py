import warnings
import traceback
from dccXMLJSONConv.dccConv import XMLToJson
# import pytest

def test_missingList():
    # TODO: Why does the missing #list key error happen?

    filePathsWithMissingLists = [
        "./tests/data/private/1_7calibrationanddccsampledata/AndereScheine/grabbedFiles/downloads/DCCUAQuerSchnitMetaData/DCCTableXMLStub.xml",
        # "tests/data/private/1_7calibrationanddccsampledata/AndereScheine/grabbedFiles/downloads/dccQuantities/test_xmlDumpingSingleQuantNoUncer.xml",
        # "tests/data/private/1_7calibrationanddccsampledata/AndereScheine/grabbedFiles/downloads/dccQuantities/test_dccQuantTabXMLDumping.xml",
    ]

    for filePath in filePathsWithMissingLists:
        try:
            with open(filePath) as xml_file:
                xml_data = xml_file.read()
                jsonDict = XMLToJson(xml_data)
                # This is the item you want to be looking at:
                assert jsonDict['dcc:list']['dcc:quantity'][2]['si:realListXMLList']['si:valueXMLList']['#list']
        except FileNotFoundError:
            warnings.warn(RuntimeWarning("Test data file missing!"))





def test_repeatableElementsToList():
    with open('./tests/data/minimalDCC_3_2_1.xml') as xml_file:
        jsonDict = XMLToJson(xml_file.read())
        #check if this is a lsit even if it contains only one itmen
        assert type(jsonDict['dcc:digitalCalibrationCertificate']['dcc:administrativeData']['dcc:dccSoftware']['dcc:software'][0]['dcc:name']['dcc:content']) == list
        # same here
        #okay this fials since dcc:item misses dcc:items as repeating perent entry in the look up ...
        assert type(jsonDict['dcc:digitalCalibrationCertificate']['dcc:administrativeData']['dcc:items']['dcc:item']) == list