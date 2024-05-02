from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from homes.management import *
from admin.management import *

from core.util.custom_exceptions import *

from core.util.common import *
from user.management import *
from devices.management import *

class UserListAPI(APIView):
    
    #Display User list
    def get(self, request):
        user_management = UserManagement()
        user_list = user_management.find_all()
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data=user_list,
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
    
    #Add User
    def post(self, request):
        user_management = UserManagement()
        user_management.add_user(data=request.data)
        resp_details = create_response_details()
        resp_payload = create_response( 
                                       resp_data={},
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
    
    #Update User
    def put(self, request):
        user_management = UserManagement()
        res_data = user_management.edit_user(data=request.data)
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data=res_data,
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
    
    #Delete User
    def delete(self, request, user_id):
        user_management = UserManagement()
        user_management.deleteUser(userId=user_id)
        
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data=[],
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)


    


class HomeListAPI(APIView):
    def get(self, request):
        admin_management = AdminManagement()
        home_list = admin_management.get_home_list()
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data=home_list,
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
    
    def post(self, request):
        admin_management = AdminManagement()
        admin_management.add_home(data=request.data)
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data={},
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
    
    def put(self, request):
        admin_management = AdminManagement()
        admin_management.add_home(data=request.data)
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data={},
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
    
    def delete(self, request, home_id):
        admin_management = AdminManagement()
        admin_management.delete_home(id=home_id)

        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data={},
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)

    

class AdminDeviceAPI(APIView):
    
    #Display Device list
    def get(self, request):
        device_management = DevicesManagement()
        device_list = device_management.find_all()
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data=device_list,
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
    
    # #Add Device
    def post(self, request):
        device_management = DevicesManagement()
        device_list = device_management.create_device(data=request.data)
        resp_details = create_response_details()
        resp_payload = create_response( 
                                       resp_data={},
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
    
    # #Update Device
    def put(self, request):
        device_management = DevicesManagement()
        device_list = device_management.update_device(data=request.data)
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data={},
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
    
    # #Delete Device
    def delete(self, request, device_id):
        device_management = DevicesManagement()
        device_management.deleteDevice(device_id=device_id)
        
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data=[],
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)