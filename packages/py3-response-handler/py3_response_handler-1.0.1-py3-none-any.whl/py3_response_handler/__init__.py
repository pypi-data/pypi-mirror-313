#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from typing import Union

from py3_response_handler.requests import ResponseHandler as RequestsResponseHandler


class HandlerType:
    """
    requests.Response Handler
    """
    REQUESTS_RESPONSE_HANDLER = 1


class Handler:
    @staticmethod
    def instance(types: int = HandlerType.REQUESTS_RESPONSE_HANDLER, *args, **kwargs) -> Union[
        RequestsResponseHandler, None]:
        if types == HandlerType.REQUESTS_RESPONSE_HANDLER:
            return RequestsResponseHandler()
        raise TypeError(f"types:{types} is not a valid handler type")
