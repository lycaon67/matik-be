import jwt
import json
import logging
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError

from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response

from core.constants import identifer as idf
from core.util.common import *

from core.util.custom_exceptions import DefaultError

LOGGER = logging.getLogger("arv_logger")


class ResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        try:
            # All raised exceptions -> automatic status code is 500
            resp_payload = create_response(resp_details=exception.args[0])
            status_code = exception.args[0][idf.ERR][idf.STATUS_CODE]
        except TypeError as err:
            resp_payload = create_response(
                resp_details=DefaultError().err_resp)
            # Append in details the exception err
            resp_payload[idf.REQ_RESPONSE_DETAILS][idf.ERR][idf.ERR_DETAIL] = str(
                exception)
            status_code = 500

        # Append path
        resp_payload[idf.REQ_RESPONSE_DETAILS][idf.ERR][idf.ERR_PATH] = request.path

        return JsonResponse(resp_payload, content_type="application/json", status=status_code)
