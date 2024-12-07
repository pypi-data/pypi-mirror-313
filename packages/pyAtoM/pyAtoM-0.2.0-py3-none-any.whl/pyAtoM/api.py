"""
pyAtoM library for working with the AtoM API

author:     James Carr
licence:    Apache License 2.0

"""
import json
import os
import platform
import sys
from enum import Enum
from typing import Generator

import requests
from requests import Session
from requests.auth import HTTPBasicAuth

import pyAtoM

API_KEY_HEADER = "REST-API-Key"


class Authentication:

    def __str__(self):
        return f"pyAtoM version: {pyAtoM.__version__}  (Access To Memory 2.8 Compatible) Connected to: {self.server}"

    def __repr__(self):
        return self.__str__()

    def __init__(self, username: str = None, password: str = None, api_key: str = None, server: str = None,
                 protocol: str = "https"):
        """

        :param username:  username of the account for basic authentication. Optional if using API KEY
        :param password:  password of the account for basic authentication. Optional if using API KEY
        :param api_key:   The API key if not using basic authentication
        :param server:    The URL of the AtoM server
        """

        self.server: str = server
        self.session: Session = requests.Session()
        self.api_token = api_key

        headers = {"Accept": "application/json"}
        if (username is not None) and (password is not None):
            self.auth = HTTPBasicAuth(username, password)
        else:
            if self.api_token is not None:
                headers['REST-API-Key'] = self.api_token
            self.auth = None

        self.session.headers.update({'User-Agent': f'pyAtoM SDK/({pyAtoM.__version__}) '
                                                   f' ({platform.platform()}/{os.name}/{sys.platform})'})

        self.base_url = f"{protocol}://{self.server}"
        path = "/api/informationobjects"
        url = f"{self.base_url}{path}"
        response = self.session.get(url, auth=self.auth, headers=headers)
        if response.status_code != requests.codes.ok:
            raise RuntimeError("Not Authenticated")

class QueryField(Enum):
    all: str = "_all"
    title: str = "title"
    identifier: str = "identifier"
    referenceCode: str = "referenceCode"
    scopeAndContent: str = "scopeAndContent"
    archivalHistory: str = "archivalHistory"
    extentAndMedium: str = "extentAndMedium"
    genre: str = "genre"
    subject: str = "subject"
    name: str = "name"
    place: str = "place"

class QueryOperator(Enum):
    and_terms: str = "and"
    or_terms: str = "or"
    not_terms: str = "not"

class Query:
    value: str
    operator: QueryOperator
    field: QueryField

    def __init__(self, query_value: str = "*", query_field: QueryField = QueryField.all, query_operator: QueryOperator = QueryOperator.and_terms):
        self.value = query_value
        self.field = query_field
        self.operator = query_operator


class AccessToMemory(Authentication):


    def download(self, slug: str, filename: str = None):
        """
        This endpoint will stream the content of the master digital object associated with the archival description whose slug is provided.

        :return: filename
        """

        CHUNK_SIZE: int = 16 * 1024

        headers = {'Content-Type': 'application/octet-stream'}
        if self.api_token is not None:
            headers['REST-API-Key'] = self.api_token
        path = f"/api/informationobjects/{slug}/digitalobject"
        url = f"{self.base_url}{path}"
        with self.session.get(url, auth=self.auth, headers=headers, stream=True) as response:
            if response.status_code == requests.codes.ok:
                if 'Content-Disposition' in response.headers:
                    disposition: str = response.headers['Content-Disposition']
                    filename = disposition.replace("attachment; filename=", "")
                with open(filename, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                        file.write(chunk)
                        file.flush()
        return filename


    def search(self, query_terms: list[Query] = None,  digital_object: bool = False, sf_culture: str = None) -> Generator:
        """
        Search the repository for information objects matching the search


        :param digital_object: Include descriptions with a digital object
        :param query_terms: List of one or more query terms
        :param sf_culture:  ISO 639-1 language code defaults to the default culture of the application.
        :return: A dict object containing the ISAD(g) metadata
        """
        headers = {"Accept": "application/json"}
        if self.api_token is not None:
            headers['REST-API-Key'] = self.api_token
        path = "/api/informationobjects"
        url = f"{self.base_url}{path}"
        params = {}
        if digital_object:
            params['onlyMedia'] = 1
        if sf_culture is not None:
            params['sf_culture'] = sf_culture
        q_i: int = 0
        if query_terms is not None:
            for q in query_terms:
                params[f"sq{q_i}"] = q.value
                params[f"so{q_i}"] = q.operator.value
                params[f"sf{q_i}"] = q.field.value
                q_i = q_i + 1
        response = self.session.get(url, auth=self.auth, headers=headers, params=params)
        params['skip'] = 0
        if response.status_code == requests.codes.ok:
            document = response.content.decode("utf-8")
            results_dict = json.loads(document)
            total_hits = int(results_dict['total'])
            results = results_dict['results']
            for r in results:
                yield r
            found: int = len(results)
            while total_hits > found:
                params['skip'] = found
                response = self.session.get(url, auth=self.auth, headers=headers, params=params)
                if response.status_code == requests.codes.ok:
                    document = response.content.decode("utf-8")
                    results_dict = json.loads(document)
                    results = results_dict['results']
                    for r in results:
                        yield r
                    found = found + len(results)



    def get_by_identifier(self, identifier: str, sf_culture: str = None) -> dict | None:
        """
        Return an information object by its identifier, not the slug


        :param identifier:
        :param sf_culture:  ISO 639-1 language code defaults to the default culture of the application.
        :return: A dict object containing the ISAD(g) metadata
        """

        headers = {"Accept": "application/json"}
        if self.api_token is not None:
            headers['REST-API-Key'] = self.api_token
        path = "/api/informationobjects"
        url = f"{self.base_url}{path}"
        params = {'sq0': f'\"{identifier}\"', 'sf0': "identifier", 'sort': 'identifier', 'sf_culture': sf_culture}
        response = self.session.get(url, auth=self.auth, headers=headers, params=params)
        if response.status_code == requests.codes.ok:
            document = response.content.decode("utf-8")
            return json.loads(document)

    def get_parent(self, slug: str, sf_culture: str = None) -> dict | None:
        """
        This method will obtain all information object data available for the parent of the given slug


        :param slug:        the slug of the child object
        :param sf_culture:  ISO 639-1 language code defaults to the default culture of the application.
        :return: A dict object containing the ISAD(g) metadata
        """

        item: dict = self.get(slug, sf_culture=sf_culture)
        if item is not None:
            if 'parent' in item:
                return self.get(item['parent'])

        return None

    def get(self, slug: str, sf_culture: str = None) -> dict:
        """
        This method will obtain all information object data available for a particular slug

        :param slug:        the slug of the information object
        :param sf_culture:  ISO 639-1 language code defaults to the default culture of the application.
        :return: A dict object containing the ISAD(g) metadata
        """
        headers = {"Accept": "application/json"}
        if self.api_token is not None:
            headers['REST-API-Key'] = self.api_token
        path = "/api/informationobjects"
        url = f"{self.base_url}{path}/{slug}"
        response = self.session.get(url, auth=self.auth, headers=headers, params={'sf_culture': sf_culture})
        if response.status_code == requests.codes.ok:
            document = response.content.decode("utf-8")
            d: dict = json.loads(document)
            d['slug'] = slug
            return d
