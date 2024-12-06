# DCC XML<-->JSON Conversion
Thie Package contains an Libary for XML<-->JSON Conversion for the DCC (Digital Calibration Certificate).
Witch contains an Python Module for the conversion. Aswell as an tornador REST-API Server to remote call this conversion.
## Conversion Rules
0. The XML Document ist converted into a nested dict, containing lists for repatable elements. Repeated elements are determined by there name or by the name of the parent Element. [schemaTypeCastCache.json]([typeCastDictCreator.py](src/dccXMLJSONConv/data/schemaTypeCastCache.json)) contains a comprehensive list of the repeated fild names/parent names.
1. The actual `string` Conent of an Element is stored as `string` in the `#text` Element of the JSON-Nodes. If the content is an List of strings, the `#list` Element contains the list of elements vastet to float if posible.  
2. Since JSON Don't support attributes, all attributes are converted to dict Keys Starting with an @
3. Comments are converted to an adition dict key '@_Comment' containing a list of all comments in the coresonding XML-Element, the order ist preserved. The actual position of the comment is not.
4. when converting json to XML if an Element contains a `#list` key, and a '#text' key, the `#text` key is used and the '#list' is discarded. If only the `#list` key is present, the list is converted to a string and convertet.
### Installation
To use the conversion libary, install the package with pip:

```bash
pip install dccXMLJSONConv
```
to use the REST-API server consider cloning the repo and installing the additional requirements from [requirementsServer.txt](requirementsServer.txt)

### Error handling
The Converter does not check any XSD-rules and allways tries to return an response. 

### Conversion example
```xml
<dcc:quantity refType="vib_phase">
	<!-- This is only an example -->
	<dcc:name>
		<dcc:content lang="de">Phasenverzögerung</dcc:content>
		<dcc:content lang="en">Phase delay</dcc:content>
	</dcc:name>
	<!-- This is an additional Comment -->
	<si:realListXMLList>
		<si:valueXMLList>1.7 1.5 1.3 1.1 1.02 0.92 0.83 0.76 0.69 0.63 0.57 0.53 0.48 0.44 0.42 0.38 0.33 0.28 0.39 0.30 0.30 0.15 0.17 0.1 0.1 0.1 0.1</si:valueXMLList>
		<si:unitXMLList>\degree</si:unitXMLList>
		<si:expandedUncXMLList>
			<si:uncertaintyXMLList>1.5 1.0 1.0 1.0 0.70 0.70 0.70 0.70 0.70 0.70 0.70 0.70 0.70 0.70 0.70 0.70 0.70 0.70 0.70 0.70 0.70 0.70 0.70 1.0 1.0 1.0 1.0</si:uncertaintyXMLList>
			<si:coverageFactorXMLList>2.0</si:coverageFactorXMLList>
			<si:coverageProbabilityXMLList>0.95</si:coverageProbabilityXMLList>
			<si:distributionXMLList>normal</si:distributionXMLList>
		</si:expandedUncXMLList>
	</si:realListXMLList>
</dcc:quantity>
```

```json
{
    "@refType": "vib_phase",
    "dcc:name": {
        "dcc:content": [
            {
                "@lang": "de",
                "#text": "Phasenverz\u00f6gerung"
            },
            {
                "@lang": "en",
                "#text": "Phase delay"
            }
        ]
    },
    "si:realListXMLList": [
        {
            "si:valueXMLList": {
                "#text": "-0.0003 -0.0004 -0.0004 -0.0003 -0.0001 -0.0002 -0.0003 -0.0001 0.0000 0.0002 -0.0002 -0.0002 -0.0000 -0.0000 0.0001 0.0001 0.0000 0.0001 0.0005 0.0003 0.0001 -0.000 0.000 0.000 0.000 0.000 -0.000 -0.000 0.000 -0.034 -0.002",
                "#list": [
                    -0.0003,
                    -0.0004,
                    -0.0004,
                    -0.0003,
                    -0.0001,
                    -0.0002,
                    -0.0003,
                    -0.0001,
                    0,
                    0.0002,
                    -0.0002,
                    -0.0002,
                    0,
                    0,
                    0.0001,
                    0.0001,
                    0,
                    0.0001,
                    0.0005,
                    0.0003,
                    0.0001,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    -0.034,
                    -0.002
                ]
            },
            "si:unitXMLList": {
                "#text": "\\\radian",
                "#list": [
                    "\\\radian"
                ]
            },
            "si:expandedUncXMLList": {
                "si:uncertaintyXMLList": {
                    "#text": "0.0035 0.0035 0.0035 0.0035 0.0035 0.0035 0.0035 0.0035 0.0035 0.0035 0.0035 0.0035 0.0035 0.0035 0.0035 0.0035 0.0035 0.0035 0.0035 0.0035 0.0035 0.009 0.009 0.009 0.009 0.009 0.009 0.009 0.009 0.009 0.009",
                    "#list": [
                        0.0035,
                        0.0035,
                        0.0035,
                        0.0035,
                        0.0035,
                        0.0035,
                        0.0035,
                        0.0035,
                        0.0035,
                        0.0035,
                        0.0035,
                        0.0035,
                        0.0035,
                        0.0035,
                        0.0035,
                        0.0035,
                        0.0035,
                        0.0035,
                        0.0035,
                        0.0035,
                        0.0035,
                        0.009,
                        0.009,
                        0.009,
                        0.009,
                        0.009,
                        0.009,
                        0.009,
                        0.009,
                        0.009,
                        0.009
                    ]
                },
                "si:coverageFactorXMLList": {
                    "#text": "2.0",
                    "#list": [
                        2
                    ]
                },
                "si:coverageProbabilityXMLList": {
                    "#text": "0.95",
                    "#list": [
                        0.95
                    ]
                },
                "si:distributionXMLList": {
                    "#text": "normal",
                    "#list": [
                        "normal"
                    ]
                }
            }
        }
    ]
}```

# Using the libary
Hint! The Repo [dccXMLJSONConvGUI](https://gitlab1.ptb.de/digitaldynamicmeasurement/dcc_XMLJSONConvGUI) contains a dockerfile to deploy the dcc_XMLJSONConv running on port 8000 as well as an GUI. Using this is an easy deployment option.
## Installing system dependencies:
Ubuntu:
```bash
sudo apt-get install libxml2-dev libxslt-dev python-lxml
```
Fedora:
```bash
sudo dnf install libxml2-devel libxslt-devel python-lxml
```
## Installation
Methode 1. Using Git-Repo
Clone Repo and install Python dependencies:
```
git clone https://gitlab1.ptb.de/digitaldynamicmeasurement/dcc_XMLJSONConv.git
cd dcc_XMLJSONConv
pip install -r ./requirements.txt
```
Methode 2. Use Python Pacakge
2. Alternativly install the converter as python package with pip:
```bash
pip install -e git+https://pipPull:jLBHrAnhPp9s1-qHvB5A@gitlab1.ptb.de/digitaldynamicmeasurement/dcc_XMLJSONConv.git@release#egg=dcc-XMLJSONConv
```

# Usage of local conversion Libary:

```python
#Imports
import json
from dccXMLJSONConv.dccConv import XMLToJson,JSONToXML


jsonDict=json.loads('COPY CONTENT FROM EXAMPLE ABOVE')
xmlSTr='COPY CONTENT FROM EXAMPLE ABOVE'
xmltoJsonDict=XMLToJson(xmlSTr)
jsontoXMLStr=JSONToXML(jsonDict)
```



# Using the dcc_rest_server

1. Install Additional requrenments , namly `fastapi~=0.70.0` and `uvicorn~=0.27.1` from [requirementsServer.txt](requirementsServer.txt)
```bash
pip install -r requirementsServer.txt
```
2. Start the dcc_server with

```bash
cd ~/repos/dcc_XMLJSONConv/src/dccXMLJSONConv
(venv) seeger01@n23017:~/repos/dccXMLJSONConv/src/dcc_XMLJSONConv$ uvicorn dccServer:app --reload
INFO:     Will watch for changes in these directories: ['/home/seeger01/repos/dccXMLJSONConv/src/dccXMLJSONConv']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [16614] using StatReload
INFO:     Started server process [16616]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```
The REST-Server is now runing on Port `8000` use the `--port ` and `--host` params to change port and host.

```bash
(venv) seeger01@n23017:~/repos/dccXMLJSONConv/src/dccXMLJSONConv$ uvicorn dccServer:app --reload --port 8001 --host 127.0.0.2
INFO:     Will watch for changes in these directories: ['/home/seeger01/repos/dccXMLJSONConv/src/dccXMLJSONConv']
INFO:     Uvicorn running on http://127.0.0.2:8001 (Press CTRL+C to quit)
```

# REST API Documentation

This document outlines the REST API endpoints available in the application, detailing the request methods, endpoints, expected request bodies, and response formats.

## Endpoints

| Endpoint       | Method | Description                                            | Request Body                                                      | Response                                           |
|----------------|--------|--------------------------------------------------------|-------------------------------------------------------------------|----------------------------------------------------|
| `/`            | GET    | Returns a greeting message and usage instructions.     | N/A                                                               | `{ "message": "<instructions>" }`                  |
| `/dcc2json/`   | POST   | Converts XML string input to JSON format.              | `{ "xml": "<XML string>" }`                                       | JSON object representing the original XML.         |
| `/json2dcc/`   | POST   | Converts JSON input to XML string format.              | `{ "js": <JSON object> }`                                         | XML string representing the original JSON.         |

## Details

### `/`

- **Method**: GET
- **Description**: Provides a greeting message along with instructions for using the available endpoints.
- **Request Body**: None
- **Response**: 
  - **Status Code**: 200 OK
  - **Body**: 
    ```json
    {
      "message": "Hello!\nBetter use the URL /json2dcc/?js={...} \n or /dcc2json (POST method)"
    }
    ```

### `/dcc2json/`

- **Method**: POST
- **Description**: Accepts an XML string and converts it into a JSON representation.
- **Request Body**: Required. The body should contain an XML string within a JSON object under the key `"xml"`.
- **Response**:
  - **Status Code**: 200 OK for successful conversion; 400 Bad Request for empty input.
  - **Body**: JSON object representing the parsed XML.

### `/json2dcc/`

- **Method**: POST
- **Description**: Accepts a JSON object and converts it into an XML string.
- **Request Body**: Required. The body should contain a JSON object under the key `"js"`.
- **Response**:
  - **Status Code**: 200 OK for successful conversion; 400 Bad Request for empty input.
  - **Body**: XML string representing the JSON object.

## Further usage examples

For detailed usage examples, including request and response examples, refer to the automated tests provided in[test_dccXMLJSONConv.py](test/test_dccXMLJSONConv.py) and [test_dcc_server.py](test/test_dcc_server.py) .

## Update repeatable Fieldnames from schema URL
The skript [listTypeFinder.py][src/dcc_XMLJSONConv/listTypeFinder.py] can be used to update the list of repeated fields.
Either with the functions in the skript (see Docstings for further Information)
or calling the script with the XSD Url and optinal the output path like
```bash
(venv) user@host:~/repos/dccXMLJSONConv/src/dccXMLJSONConv$ python3 ./listTypeFinder.py https://ptb.de/dcc/v3.2.1/dcc.xsd tmp.json
List types have been written to tmp.json
```

# dcc_rest_server debugging and launching with Pycharm
For Pycharm debuigging see : [https://www.jetbrains.com/help/pycharm/fastapi-project.html#run-debug-configuration}(https://www.jetbrains.com/help/pycharm/fastapi-project.html#run-debug-configuration)
Create new fastApi launch configuration instead of python 
