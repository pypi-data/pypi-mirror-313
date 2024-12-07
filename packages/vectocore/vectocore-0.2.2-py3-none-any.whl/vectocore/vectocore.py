import os
import json
import requests


class Vectocore:
    def __init__(self, tenant_key=""):
        # 변수 은닉화
        self.__VECTOR_URL = "https://api.vectocore.com"
        self.__tenant_key = os.environ.get("VECTOCORE_TENANT_KEY", tenant_key)
        if self.__tenant_key == "" or self.__tenant_key is None:
            raise ValueError("Tenant key is none")

    def __request_post(self, data):
        headers = {"Content-Type": "application/json", "x-api-key": self.__tenant_key}
        response = requests.post(url=self.__VECTOR_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def put_index(self, index_name: str, desc=""):
        data = {"command": "put_index", "index_name": index_name, "index_desc": desc}
        result = self.__request_post(data)
        return result

    def delete_index(self, index_name: str):
        data = {
            "command": "delete_index",
            "index_name": index_name,
        }
        result = self.__request_post(data)
        return result

    def list_index(self):
        data = {"command": "list_index"}
        result = self.__request_post(data)
        return result

    def put_extream_data(self, index_name: str, doc_body: dict):
        data = {"command": "put_extream_data", "index_name": index_name, "doc_body": doc_body}
        result = self.__request_post(data)
        return result

    def get_extream_data(self, index_name: str, document_id: str):
        data = {"command": "get_extream_data", "index_name": index_name, "document_id": document_id}
        result = self.__request_post(data)
        return result

    def list_extream_data(self, index_name: str, last_key=None):
        data = {"command": "list_extream_data", "index_name": index_name}
        if last_key is not None:
            data["last_key"] = last_key
        result = self.__request_post(data)
        return result

    def delete_extream_data(self, index_name: str, document_id: str):
        data = {"command": "delete_extream_data", "index_name": index_name, "document_id": document_id}
        result = self.__request_post(data)
        return result

    def extream_search(self, question: str, index_name="", max_count=10, mode="VECTOR"):
        data = {"command": "extream_search", "question": question, "index_name": index_name, "max_count": max_count, "mode": mode}
        result = self.__request_post(data)
        return result

    def web_search(self, question: str):
        data = {"command": "web_search", "question": question}
        result = self.__request_post(data)
        return result


class Lens:
    def __init__(self, tenant_key="", role=None, rule=None, output_format=None, mode=None):
        # 변수 은닉화
        self.__VECTOR_URL = "https://api.vectocore.com"
        self.__AI_URL = "https://ai.vectocore.com"
        self.__tenant_key = os.environ.get("VECTOCORE_TENANT_KEY", tenant_key)
        if self.__tenant_key == "" or self.__tenant_key is None:
            raise ValueError("Tenant key is none")
        self.role = role
        self.rule = rule
        self.output_format = output_format
        self.mode = mode

    def __request_stream(self, data):
        headers = {"x-api-key": self.__tenant_key}
        response = requests.post(url=self.__AI_URL, headers=headers, json=data, stream=True)
        return response

    def chat(self, question, stream=False):
        data = {"command": "lensChat", "question": question}
        if self.role is not None:
            data["role"] = self.role
        if self.rule is not None:
            data["rule"] = self.rule
        if self.output_format is not None:
            data["outputFormat"] = self.output_format
        if self.mode is not None:
            data["mode"] = self.mode
        result = self.__request_stream(data)
        return result
