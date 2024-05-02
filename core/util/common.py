#
#
# Copyright 2020 NEC Telecom Software Phils., Inc.
# All Rights Reserved.
#
# This software is confidential and proprietary information of
# NEC Telecom Software Phils., Inc. You shall not disclose this
# and use it only in accordance with the terms of the license
# agreement you entered into with NEC Telecom Software Phils., Inc.
#
#
# Project name: Automation Result Visualization
# File Name : urls.py
#
#
# Class Name   : <class name>
# Description  : <description>
#
# Revision History
#    Release Version     Date              Engineer             Contents
#    v1.0.6              9/17/2020         largosa.jr
#
import ast
import os
import stat
import json as native_json
import logging
import math
from datetime import datetime, timedelta
from django.http import request
from django.conf import settings
from core.constants.identifer import RESP_BODY, RESP_RESPONSE_DETAILS
from core.constants import identifer as idf
from rest_framework import status
from django.utils.dateparse import parse_datetime
from pytz import timezone
from core.auth.token_authentication import TokenAuthentication

LOGGER = logging.getLogger('arv_logger')


def get_value(key, obj):
    """Extracts a key value from from dictionary"""
    result = None

    try:
        result = obj[key]
    except (KeyError, TypeError):
        LOGGER.info(
            f"Value for '{key}' key is not found. Defaulting to 'None'.")
    return result


def get_headers(request):
    """
    Extracts headers from request
    """
    return request[idf.REQ_HEADER]


def get_data(request):
    """
    Extracts the data from request
    """
    return request[idf.REQ_BODY][idf.REQ_DATA]


def create_response_details(exit_code=0, message_id=0):
    """Creation of response details

    Returns:
        - dictionary with exit_code and message in it.
    """

    return {
        idf.EXIT_CODE: exit_code,
        idf.ID_MESSAGE: message_id,
    }


def create_response_header(request, **kwargs):
    LOGGER.debug("Creating Response Headers")

    token_auth = TokenAuthentication()

    token_key = token_auth.extract_bearer(
        request.META[idf.HTTP_AUTHORIZATION])

    user_instance = token_auth.decode_token(token_key)

    # user_mgmt = UserManagement()

    # user_instance = user_mgmt.get_user_by_uid(
    #     user_instance[idf.OBJ_ONESIGN_UID])

    resp_header = {
        idf.REQ_TOKEN: "user_instance[idf.OBJ_ACCESS_TOKEN]",
    }

    for key, value in kwargs.items():
        resp_header[key] = value

    return resp_header


def create_response_data(**kwargs):
    resp_data = {}
    for key, value in kwargs.items():
        resp_data[key] = value

    return resp_data


def create_response_error_details(**kwargs):
    errors_list = []
    error_data = {}
    for key, value in kwargs.items():
        error_data[key] = value

    # TODO: Support for multiple errors
    errors_list.append(error_data)

    return {
        idf.RESP_ERRORS: json.dumps(errors_list)
    }


def create_response(resp_header=None,
                    resp_data=None,
                    resp_details=None):
    """
    Utility for creating the HTTP Response

    Args:
        header ([type], optional): Header of the Response. Defaults to None.
        data ([type], required): Body of the Response. Defaults to None.
        response_details ([type], optional): Response details. Defaults to None.
    """
    if resp_details is None:
        resp = ""
    else:
        resp = resp_details

    return {
        idf.RESP_HEADER: resp_header,
        idf.RESP_BODY: {idf.RESP_DATA: resp_data},
        idf.RESP_RESPONSE_DETAILS: resp_details,
    }


def read_file(file_dir):

    try:
        with open(file_dir, "r") as f:
            file_data = f.read()

        return file_data

    except FileNotFoundError:
        LOGGER.debug("[File not found]")
        LOGGER.debug(f"{file_dir}")
        raise

    except native_json.decoder.JSONDecodeError:
        LOGGER.debug("JSON Schema Validation failed")
        raise


def read_json_file(file_dir):
    """Reads json file from given directory"""
    data = {}

    try:
        mode = os.stat(file_dir)
        hasRead = mode.st_mode & stat.S_IRUSR

        if hasRead == stat.S_IRUSR:
            LOGGER.debug("file has read permission for owner file:")
            with open(file_dir, "r", encoding="utf-8") as json_file:
                json_load_file = json.load(json_file)
                data = json_load_file
        else:
            LOGGER.debug("[ERROR] JSON file has no read permission")
            raise FileNotFoundError

    except FileNotFoundError:
        LOGGER.debug("[ERROR] File not found")
        LOGGER.debug(f"{file_dir}")
        raise

    except native_json.decoder.JSONDecodeError:
        LOGGER.debug("[ERROR] JSON Schema Validation failed")
        raise

    return data


def string_to_dict(str_data):
    """
    Converts string to dictionary
    """
    obj = {}
    obj_str = ""

    try:
        obj = json.loads(str_data)
    except native_json.decoder.JSONDecodeError:
        # If json is in single quotes
        # it will raise an error
        # replace all single with double quotes
        # json.loads will raise an error if there are escaped character, hence below line is added.
        obj_str = str_data.replace("\n", "").replace("\r", "").replace("\\", "").replace("\'", "\"")
        obj = json.loads(obj_str)
    except TypeError:
        obj = str_data

    return obj


def extract_key_value(obj, obj_key):
    result = {}

    for key, value in obj.items():
        if obj_key != key:
            result[key] = value

    return result


def extract_key_pair_none(obj):
    result = {}

    for key, value in obj.items():
        if value is not None:
            result[key] = value

    return result


def key_exists(obj, key):
    result = None

    if key in obj:
        result = obj[key]

    return result


def is_dict_empty(obj):
    """
    Checks if the dictionary is empty
    """
    return not bool(obj)


def average_list(list_data, sub_count=0):
    result = 0

    denominator = (len(list_data) - sub_count)

    if len(list_data) > 0 and denominator > 0:
        list_data = map(float, list_data)
        result = sum(list_data) / denominator

    return str(truncate(result, 1))

def average_list_untruncated(list_data, sub_count=0):
    result = 0

    denominator = (len(list_data) - sub_count)

    if len(list_data) > 0 and denominator > 0:
        list_data = map(float, list_data)
        result = sum(list_data) / denominator

    return str(result)

def average_list_dash(list_data, sub_count=0):
    result = 0
    #if all entries in list_data are "-", return "-"
    #else remove "-" if there are any in list, and compute averate
    #based on valid valus 0 - 100
    isAllDash = all(e == idf.DASH for e in list_data)
    if isAllDash:
        return str(idf.DASH)
    else:
        list_data = list(filter(lambda x: x != idf.DASH, list_data))
        denominator = (len(list_data) - sub_count)
        if len(list_data) > 0 and denominator > 0:
            list_data = map(float, list_data)
            result = sum(list_data) / denominator
        return str(truncate(result, 1))

def average_list_dash_untruncated(list_data, sub_count=0):
    result = 0
    #if all entries in list_data are "-", return "-"
    #else remove "-" if there are any in list, and compute averate
    #based on valid valus 0 - 100
    isAllDash = all(e == idf.DASH for e in list_data)
    if isAllDash:
        return str(idf.DASH)
    else:
        list_data = list(filter(lambda x: x != idf.DASH, list_data))
        denominator = (len(list_data) - sub_count)
        if len(list_data) > 0 and denominator > 0:
            list_data = map(float, list_data)
            result = sum(list_data) / denominator
        return str(result)


def is_string_empty(str_data):
    """
    Checks if the string is empty or not and returns a
    empty string object
    """
    result = "{}"

    if str_data:
        result = str_data

    return result


def read_all_files(path):
    """
    Reads all filenames in a given path directory
    """
    return os.listdir(path)


def is_key_exists(obj, key):
    """
    Check if key exists, return bool
    """
    flag = False

    if key in obj:
        flag = True

    return flag


def log_pjmp_error(log_content):
    """
    Logs pjmp error
    """
    now = datetime.now()

    file_name = now.strftime("%Y_%m_%d") + '.log'
    file_dir = settings.PJMP_LOG_PATH + file_name

    with open(file_dir, "a", encoding='utf-8') as myfile:
        myfile.write(str(log_content) + "\n\n")


def truncate(number, decimals=0):
    """
    Returns a value truncated to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor


def parse_datetime_and_format(date_to_parse, date_format):
    date_fmt = ""
    try:
        parse_date = parse_datetime(date_to_parse)
        date_tz = parse_date.astimezone(
            timezone(settings.DATE_TIMEZONE))
        date_fmt = date_tz.strftime(date_format)
    except:
        raise
    return date_fmt


def convert_string_to_datetime(date_str, date_format):
    date_fmt = ""
    try:
        convert_date = datetime.strptime(date_str, date_format)
        date_tz = convert_date.astimezone(
            timezone(settings.DATE_TIMEZONE))
        date_fmt = date_tz.strftime(date_format)
    except:
        raise
    return date_fmt


def check_file_exists(file_dir):
    """Check if file exists in given directory"""
    try:
        file = open(file_dir)
        return True
    except IOError:
        return False


def check_dir_exists(file_dir):
    """check if directory exists"""
    return os.path.isdir(file_dir)


def is_float(value):
    """check if str can be converted to float"""
    try:
        float(value)
        return True
    except ValueError:
        return False


def list_fiscal_months(date, starting_month=4):
    """
    Returns list of months in format '%Y%m' within fiscal year that date
    belongs in.
    """
    fiscal_year = date.year
    if date.month < starting_month:
        fiscal_year = fiscal_year - 1
    fiscal_start = datetime(fiscal_year, starting_month, 1)
    months = []
    current_month = date
    while current_month >= fiscal_start:
        months.append(current_month.strftime('%Y%m'))
        current_month = current_month.replace(day=1)
        current_month = current_month - timedelta(days=1)
    months.reverse()
    return months


def get_raw_value(value, unit):
    """ Extract value from string with unit """
    if type(value) is str:
        value = value.replace(unit, '')
        while type(value) not in [int, float] and len(value) > 0:
            try:
                value = ast.literal_eval(value)
            except:
                value = value[:-1]
        if not value:
            return 0

    return value


def format_decimal(value, decimal_place=0, comma=True):
    value = truncate(value, decimal_place)
    if comma:
        return f'{value:,.{decimal_place}f}'
    return f'{value:.{decimal_place}f}'


def get_max_edit_te_config_session():
    if check_file_exists(settings.TOTAL_EFFECT_EDIT_CONF_PATH):
        return read_json_file(settings.TOTAL_EFFECT_EDIT_CONF_PATH)[idf.OBJ_MAX_TOTAL_EFFECT_EDIT_SESSION]

def get_edit_te_config_reminder():
    if check_file_exists(settings.TOTAL_EFFECT_EDIT_CONF_PATH):
        return read_json_file(settings.TOTAL_EFFECT_EDIT_CONF_PATH)[idf.OBJ_TOTAL_EFFECT_EDIT_TIME_LEFT_REMINDER]