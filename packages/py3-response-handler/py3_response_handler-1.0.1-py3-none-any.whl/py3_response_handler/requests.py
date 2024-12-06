#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from addict import Dict
from bs4 import BeautifulSoup
from requests import Response


class ResponseHandler(object):
    def __init__(self, *args, **kwargs):
        pass

    def response(self, response: Response = None):
        """
        request.Response object
        :param response: request.Response object
        :return:
        """
        return response if isinstance(response, Response) else None

    def content(self, response: Response = None, status_code: int = 200):
        """
        requests.Response object content
        :param response: requests.Response object
        :param status_code: requests.Response object status_code
        :return:
        """
        if isinstance(response, Response) and response.status_code == status_code:
            return response.content
        return None

    def text(self, response: Response = None, status_code: int = 200):
        """
        requests.Response object text
        :param response: requests.Response object
        :param status_code: requests.Response object status_code
        :return:
        """
        if isinstance(response, Response) and response.status_code == status_code:
            return response.text
        return None

    def text_to_beautifulsoup(self, response: Response = None, status_code: int = 200,
                              *args, **kwargs) -> BeautifulSoup:
        """
        requests.Response object text to bs4.Beautifulsoup object
        :param response: requests.Response object
        :param status_code: requests.Response object status_code
        :param args: bs4.Beautifulsoup(*args, **kwargs)
        :param kwargs: bs4.Beautifulsoup(*args, **kwargs)
        :return:
        """
        if self.text(response=response, status_code=status_code):
            return BeautifulSoup(
                response.text,
                *args,
                **kwargs
            )
        return None

    def json(self, response: Response = None, status_code: int = 200, *args, **kwargs):
        """
        requests.Response object json
        :param response: requests.Response object
        :param status_code: requests.Response object status_code
        :param args: requests.Response object json(*args, **kwargs)
        :param kwargs: requests.Response object json(*args, **kwargs)
        :return:
        """
        if isinstance(response, Response) and response.status_code == status_code:
            return response.json(*args, **kwargs)
        return None

    def json_to_addict(self, response: Response = None, status_code: int = 200, *args, **kwargs):
        """
        requests.Response object json to addict.Dict object
        :param response: requests.Response object
        :param status_code: requests.Response object status_code
        :param args: requests.Response object json(*args, **kwargs)
        :param kwargs: requests.Response object json(*args, **kwargs)
        :return:
        """
        if self.json(response=response, status_code=status_code):
            return Dict(response.json(*args, **kwargs))
        return None
