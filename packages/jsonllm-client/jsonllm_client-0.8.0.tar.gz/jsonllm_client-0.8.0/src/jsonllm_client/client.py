import urllib.parse
from pathlib import Path
from typing import Optional, List, Dict, Union

import requests
from tqdm.auto import tqdm


def _raise_error_if_bad_status_code(response):
    if 400 <= response.status_code < 500:
        raise ValueError(response.text)
    elif 500 <= response.status_code < 600:
        raise ValueError(response.text)




class JsonLLM:

    def __init__(self, api_key: str, url: str = "https://jsonllm.com"):
        self.api_key = api_key
        self.url = url

    def extract(
            self,
            model: str,
            project: str,
            filenames: List[str],
            texts: Optional[List[str]] = None,
            subset: Optional[List[str]] = None,
            detach: Optional[bool] = None,
            n_jobs: Optional[int] = 1,
    ) -> Dict:
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        body = {
            "project": project,
            "model": model,
            "filenames": filenames,
            "subset": subset,
            "texts": texts,
            "detach": detach,
            "n_jobs": n_jobs,
        }
        response = requests.post(f"{self.url}/api/extract/", headers=headers, json=body)
        _raise_error_if_bad_status_code(response)
        return response.json()



    def upload(self, project: str, paths: List[Union[str, Path]]):
        if isinstance(paths, str):
            paths = [Path(paths)]
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        files = {}
        for path in paths:
            path = Path(path)
            files[path.name] = path.read_bytes()
        encoded_project = urllib.parse.quote(project)
        response = requests.post(f"{self.url}/api/project/{encoded_project}/document/", files=files, headers=headers)
        _raise_error_if_bad_status_code(response)
        return response.json()

    def add_text(self, project: str, filename: str, text: str):
        if not filename.endswith(".txt"):
            filename += ".txt"
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        files = {
            filename: text.encode('utf-8')
        }
        encoded_project = urllib.parse.quote(project)
        response = requests.post(f"{self.url}/api/project/{encoded_project}/document/", files=files, headers=headers)
        _raise_error_if_bad_status_code(response)
        return response.json()

    def add_texts(self, project: str, filenames: List[str], texts: List[str], batch_size: int = None):
        if not batch_size:
            return self._add_texts_batch(project, filenames, texts)
        for start in tqdm(range(0, len(filenames), batch_size)):
            end = start + batch_size
            self._add_texts_batch(project, filenames[start:end], texts[start:end])

    def _add_texts_batch(self, project, filenames, texts):
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        files = {filename: text for filename, text in zip(filenames, texts)}
        encoded_project = urllib.parse.quote(project)
        response = requests.post(f"{self.url}/api/project/{encoded_project}/document/", files=files, headers=headers)
        _raise_error_if_bad_status_code(response)
        return response.json()

    def list_documents(self, project: str) -> List[Dict]:
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        encoded_project = urllib.parse.quote(project)
        response = requests.get(f"{self.url}/api/project/{encoded_project}/document/", headers=headers)
        _raise_error_if_bad_status_code(response)
        return response.json()["filenames"]

    def delete_document(self, project: str, filename: str):
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        encoded_project = urllib.parse.quote(project)
        encoded_filename = urllib.parse.quote(filename)
        response = requests.delete(f"{self.url}/api/project/{encoded_project}/document/{encoded_filename}", headers=headers)
        _raise_error_if_bad_status_code(response)
        return response.json()

    def get_extraction(self, project: str, request_id: str) -> Dict:
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        url = f'{self.url}/api/project/{project}/extraction/{request_id}'
        response = requests.get(url, headers=headers)
        _raise_error_if_bad_status_code(response)
        return response.json()

    def clear_project(self, project: str) -> Dict:
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        url = f'{self.url}/api/project/{project}/document/'
        response = requests.delete(url, headers=headers)
        _raise_error_if_bad_status_code(response)
        return response.json()

    def create_project(self, project: str) -> Dict:
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        url = f'{self.url}/api/project/{project}'
        response = requests.post(url, headers=headers)
        _raise_error_if_bad_status_code(response)
        return response.json()

    def delete_project(self, project: str) -> Dict:
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        url = f'{self.url}/api/project/{project}'
        response = requests.delete(url, headers=headers)
        _raise_error_if_bad_status_code(response)
        return response.json()

    def cancel_request(self, request_id: str) -> Dict:
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        url = f'{self.url}/api/request/{request_id}/cancel/'
        response = requests.post(url, headers=headers)
        _raise_error_if_bad_status_code(response)
        return response.json()