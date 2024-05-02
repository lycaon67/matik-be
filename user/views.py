from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from user.management import UserManagement
from homes.management import HomesManagement
from devices.management import DevicesManagement

from core.util.custom_exceptions import *

from core.util.common import *

class UserLogin(APIView):
    
    def post(self, request):

        user_management = UserManagement()
        user_login = user_management.login(request=request.data)
      
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data=user_login,
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
    
class UserRegister(APIView):

    def post(self, request):
        user_management = UserManagement()
        user_registered = user_management.register(request=request.data)

        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data=user_registered,
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
  


class UserView(APIView):

    def get(self, request):
    
        user_management = UserManagement()
        user_login = user_management.find_all()

        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data=user_login,
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
    
    def post(self, request):

        user_management = UserManagement()
        user_login = user_management.login(request=request.data)
      
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data=user_login,
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)


class AdminView(APIView):

    def get(self, request):
    
        user_management = UserManagement()
        home_management = HomesManagement()
        device_management = DevicesManagement()
        user_list = user_management.find_all()
        home_list = home_management.find_all()
        device_list = device_management.find_all()
        resp_data = {"user_list":len(user_list), "home_list":len(home_list), "device_list":len(device_list)}
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data=resp_data,
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)




# class UserRegister(APIView):

#     def post(self, request):

#         return Response({"message":"hi fuc"})
