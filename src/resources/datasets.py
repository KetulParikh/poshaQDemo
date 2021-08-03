import os
from flask_restful import Resource
from flask import request, make_response
from flask_restful import reqparse
import werkzeug
import requests
import json
import pandas as pd

from utils import pixelai
from extension import get_log_instance

log = get_log_instance(__name__)


class insertData(Resource):
    def __init__(self):
        self.dataset_parser = reqparse.RequestParser()
        self.dataset_parser.add_argument('file', type=werkzeug.datastructures.FileStorage,
                                         required=True, case_sensitive=True, location='files', help="Provide file")
        super(insertData, self).__init__()

    def post(self):
        dataset_url = os.environ.get("URL") + "datasets"
        data = self.dataset_parser.parse_args()
        df = pd.read_csv(data["file"], sep=",")
        df.to_csv("data/kdemon.csv", index=False, sep=";")

        files = {"file":  open("data/kdemon.csv", "rb")}
        headers = {
            'Authorization': 'Bearer ' + os.environ.get("PIXELAI_ACCESS_TOKEN"),
            'Content-Type': 'multipart/form-data'
        }

        response = requests.request(
            "POST", dataset_url, headers=headers, files=files)

        if(response.status_code == 401):
            _success, headers_new = pixelai.login()
            if _success:
                headers_new.update({'Content-Type': 'multipart/form-data'})
                response = requests.post(
                    dataset_url, headers=headers_new, data={}, files=files)
            else:
                return "Internel Server Error", 500
        status = response.status_code
        response = json.loads(response.text)

        return response, status


class checkStatus(Resource):
    def __init__(self):
        super(checkStatus, self).__init__()

    def get(self, dataset_id):
        status_url = os.environ.get(
            "URL") + "datasets/"+str(dataset_id)+"/status"
        headers = {
            'Authorization': 'Bearer ' + os.environ.get("PIXELAI_ACCESS_TOKEN")
        }
        response = requests.request(
            "GET", status_url, headers=headers)

        if(response.status_code == 401):
            _success, headers_new = pixelai.login()
            if _success:
                response = requests.request(
                    "GET", status_url, headers=headers_new)
            else:
                return "Internel Server Error", 500

        status = response.status_code
        response = json.loads(response.text)
        return response, status


class autoTag(Resource):
    def __init__(self):
        super(autoTag, self).__init__()

    def post(self, dataset_id):
        url = os.environ.get(
            "URL") + "datasets/"+str(dataset_id)+"/solutions/auto-tag"
        headers = {
            'Authorization': 'Bearer ' + os.environ.get("PIXELAI_ACCESS_TOKEN")
        }
        response = requests.request("GET", url, headers=headers)

        if(response.status_code == 401):
            _success, headers_new = pixelai.login()
            if _success:
                response = requests.request("GET", url, headers=headers_new)
            else:
                return "Internel Server Error", 500

        status = response.status_code
        response = json.loads(response.text)
        return response, status


class autoTagStatus(Resource):
    def __init__(self):
        super(autoTagStatus, self).__init__()

    def get(self, dataset_id):
        url = os.environ.get(
            "URL")+"datasets/"+str(dataset_id)+"/solutions/auto-tag/status"
        headers = {
            'Authorization': 'Bearer ' + os.environ.get("PIXELAI_ACCESS_TOKEN")
        }
        response = requests.request("GET", url, headers=headers)

        if(response.status_code == 401):
            _success, headers_new = pixelai.login()
            if _success:
                response = requests.request("GET", url, headers=headers_new)
            else:
                return "Internel Server Error", 500

        status = response.status_code
        response = json.loads(response.text)
        return response, status


class downloadFile(Resource):
    def __init__(self):
        super(downloadFile, self).__init__()

    def get(self, dataset_id, format):
        url = os.environ.get(
            "URL")+"datasets/"+str(dataset_id)+"/solutions/auto-tag/files/"+str(format)
        headers = {
            'Authorization': 'Bearer ' + os.environ.get("PIXELAI_ACCESS_TOKEN")
        }
        response = requests.request("GET", url, headers=headers)

        if(response.status_code == 401):
            _success, headers_new = pixelai.login()
            if _success:
                response = requests.request(
                    "GET", url, headers=headers_new)
            else:
                return "Internel Server Error", 500

        response = response.text
        if format == "csv":
            try:
                data = make_response(response)
                cd = 'attachment; filename=mycsv.csv'
                data.headers['Content-Disposition'] = cd
                data.mimetype = 'text/csv'

                return data
            except:
                return {"message": "Error"}, 500
        else:
            return json.loads(response), 200