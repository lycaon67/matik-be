from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from devices.management import DevicesManagement, ChannelsManagement
from core.util.custom_exceptions import *

import json
from core.util.common import *

class DeviceAPI(APIView):
    
    def get(self, request):
    
        device_management = DevicesManagement()
        device_resp = device_management.find_all()

        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data=device_resp,
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
    
    def post(self, request):

        device_management = DevicesManagement()
        device_resp = device_management.create_device(request.data)

        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data={},
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)

class DeviceHomeAPI(APIView):
    
    def get(self, request, home_id):
    
        device_management = DevicesManagement()
        device_resp = device_management.find_by_homeId(home_id=home_id)

        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data=device_resp,
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
    
    def post(self, request, home_id):
        DevicesManagement().add_device_home(home_id=home_id, device_key=request.data['key'])
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data={},
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
    
    
    def delete(self, request, home_id, device_key):
        DevicesManagement().remove_device_home(device_key=device_key)
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data={},
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)


class ChannelAPI(APIView):

    def put(self, request, id):
        ChannelsManagement().updateChannel(id=id, data=request.data)
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data={},
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
    
class DeviceESPAPI(APIView):
    
    def get(self, request):
        
        key = self.request.query_params['key']
        device_management = DevicesManagement()
        channel_management = ChannelsManagement()
        device_resp = device_management.find_by_key(key)
        channel_resp = channel_management.find_by_id_esp(device_resp['id'])
        device_management.update_device_timestamp(device_resp['id'])

        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data=channel_resp,
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
    
    def post(self, request):
        key = self.request.query_params['key']
        device_management = DevicesManagement()
        channel_management = ChannelsManagement()
        device_resp = device_management.find_by_key(key)
        data = json.loads(request.body.decode('utf-8'))
        channel_resp = channel_management.update_temp_by_id(device_resp['id'], data)
        device_management.update_device_timestamp(device_resp['id'])
        
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data=channel_resp,
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)


class DeviceTempAPI(APIView):
    
    def get(self, request, home_id):
        
        device_management = DevicesManagement()
        channel_management = ChannelsManagement()
        device_resp = device_management.find_by_all_temp_homeId(home_id)

        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data=device_resp,
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
    
