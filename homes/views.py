from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from homes.management import *
from user.management import *

from core.util.custom_exceptions import *

from core.util.common import *

class HomeAdminAPI(APIView):

    def get(self, request):

        homes_management = HomesManagement()
        token_auth = TokenAuthentication()
        token_key = token_auth.extract_bearer(request.META[idf.HTTP_AUTHORIZATION])
        user_instance =token_auth.decode_token(token_key)
        homes_list = homes_management.find_all(userId=user_instance[idf.OBJ_ID])
      
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data=homes_list,
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
    

class HomeAPI(APIView):

    def get(self, request):

        user_homes_management = HomeUserAccessManagement()
        token_auth = TokenAuthentication()
        token_key = token_auth.extract_bearer(request.META[idf.HTTP_AUTHORIZATION])
        user_instance =token_auth.decode_token(token_key)
        homes_list = user_homes_management.get_user_house(userId=user_instance[idf.OBJ_ID])
      
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data=homes_list,
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
    
    def post(self, request):
        homes_management = HomesManagement()
        token_auth = TokenAuthentication()
        access = HomeUserAccessManagement()
        token_key = token_auth.extract_bearer(request.META[idf.HTTP_AUTHORIZATION])
        user_instance =token_auth.decode_token(token_key)
        home = homes_management.add_house(data=request.data)
        access_resp = access.add_user_house(userId=user_instance['id'], homeId=home.id, role=1, status=1)
      
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data=request.data,
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
    
    def put(self, request):
        homes_management = HomesManagement()
        home_data = request.data
        home = homes_management.edit_house(data=home_data)
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data={},
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
    
    def delete(self, request, home_id):
        homes_management = HomesManagement()
        home = homes_management.delete_home(id=home_id)
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data={},
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
 

class RoomAPI(APIView):

    def post(self, request):
        room_management = RoomManagement()
        rooms = room_management.add_rooms_by_house(request.data)
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data=request.data,
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
    
    def put(self, request):
        room_management = RoomManagement()
        rooms = room_management.edit_room(request.data)
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data={},
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
    
    def delete(self, request, room_id):
        room_management = RoomManagement()
        rooms = room_management.delete_room(room_id)
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data={},
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)

class UserAPI(APIView):

    def post(self, request, home_id):
        home_user_access = HomeUserAccessManagement()
        user_mgnt = UserManagement()
        user = user_mgnt.find_by_username(username=request.data[idf.OBJ_USERNAME][1:])
        home_access = home_user_access.invite_home_member(home_id=home_id, user=user)
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data=request.data,
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
    
    def put(self, request, home_id):
        home_user_access = HomeUserAccessManagement()
        user_mgnt = UserManagement()
        home_access = home_user_access.update_user_role(home_id=home_id, user=request.data)
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data={},
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
    
    def delete(self, request, home_id, member_id):
        home_user_access = HomeUserAccessManagement()
        user_mgnt = UserManagement()
        home_user_access.delete_user_access(homeId=home_id, userId=member_id)
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data={},
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)

 

class HomeGeneralSettingsAPI(APIView):

    def post(self, request):
        homes_management = HomesManagement()
        homes_list = homes_management.add_house(data=request.data)
      
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data=homes_list,
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
 


class HomeNotification(APIView):
    def get(self, request):

        user_homes_management = HomeUserAccessManagement()
        token_auth = TokenAuthentication()
        token_key = token_auth.extract_bearer(request.META[idf.HTTP_AUTHORIZATION])
        user_instance =token_auth.decode_token(token_key)
        homes_list = user_homes_management.get_user_house_invite(userId=user_instance[idf.OBJ_ID])
      
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data=homes_list,
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
      
    def post(self, request, invite_status):

        user_homes_management = HomeUserAccessManagement()
        token_auth = TokenAuthentication()
        token_key = token_auth.extract_bearer(request.META[idf.HTTP_AUTHORIZATION])
        user_instance =token_auth.decode_token(token_key)
        user_homes_management.update_user_house_invite(userId=user_instance[idf.OBJ_ID], data=request.data, status=invite_status)
      
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data={},
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
