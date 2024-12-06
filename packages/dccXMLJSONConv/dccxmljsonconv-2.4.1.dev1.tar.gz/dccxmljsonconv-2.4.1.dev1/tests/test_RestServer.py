import os
import json
import pytest
from fastapi.testclient import TestClient
from dccXMLJSONConv.dccServer import app

client = TestClient(app)

# Base directory where test data files are expected
base_dir = os.path.dirname(__file__)
data_dir = os.path.join(base_dir, "data")


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello!\nBetter use the URL /json2dcc/?js={...} \n or /dcc2json (POST method)"}


@pytest.mark.skipif(not os.path.exists(os.path.join(data_dir, "APITestXMLStub.xml")), reason="Test XML file not found")
def test_dcc2json_with_valid_xml():
    xml_data_path = os.path.join(data_dir, "APITestXMLStub.xml")
    with open(xml_data_path, "r") as f:
        xml_data = f.read()

    response = client.post("/dcc2json/", json={"xml": xml_data})
    response_json = response.json()

    assert response.status_code == 200
    assert response_json == json.loads(open(os.path.join(data_dir, "APITestJSONStub.json"), "r").read())


def test_dcc2json_with_empty_xml():
    response = client.post("/dcc2json/", json={"xml": ""})
    assert response.status_code == 400  # returns 400 Bad Request


@pytest.mark.skipif(not os.path.exists(os.path.join(data_dir, "APITestJSONStub.json")),
                    reason="Test JSON file not found")
def test_json2dcc_with_valid_json():
    json_data_path = os.path.join(data_dir, "APITestJSONStub.json")
    with open(json_data_path, "r") as f:
        json_data = json.load(f)

    response = client.post("/json2dcc/", json={"js": json_data})
    assert response.status_code == 200
    assert response.text == open(os.path.join(data_dir, "unindentedJSONTOXMLRespons.xml"), "r").read()


def test_json2dcc_with_empty_json():
    response = client.post("/json2dcc/", json={"js": {}})
    assert response.status_code == 400  # Assuming it's not successful; adjust based on your error handling
