import logging
import jwt

from core.repository.repository import Repository
from core.repository.repository import Module
from django.db.models import Q as QueryFilter, Value
from core.constants import identifer as idf
from user.models import *
from user.serializers import *
import json
from django.conf import settings
from core.util.custom_exceptions import *

from homes.management import *


from core.util import common
from core.auth.token_authentication import TokenAuthentication

class UserManagement(Repository):
    """
    Handles CRUD Logic Functionalities for User
    """

    def __init__(self):
        
        module = Module(name="User",
                        model=User,
                        serializer=UserSerializer)
        super().__init__(module=module)

    def find_by_username(self, username):
        try:
            criteria = QueryFilter(username=username)
            response = super().find_by_criteria(criteria)
            resp_data = common.get_value(idf.SERIALIZED, response)[0]
        except Exception as error:
            print("[Error] Username not Found", error)
            raise UserNotFoundError

        return resp_data
    
    def find_by_id(self, user_id):
        try:
            criteria = QueryFilter(id=user_id)
            response = super().find_by_criteria(criteria)
            resp_data = common.get_value(idf.SERIALIZED, response)[0]
        except Exception as error:
            print("[Error] Username not Found", error)
            raise HTTP401Error

        return resp_data
    
    def find_all(self):
        resp_data = []
        try:
            resp_data = super().find_all()
            for row in resp_data:
                row[idf.NAME] = row[idf.OBJ_FIRST_NAME] + " " + row[idf.OBJ_LAST_NAME]
                row[idf.OBJ_PASSWORD] = "12345678"
        except Exception as error:
            print("[ERROR][USERS] Error")
           
        return resp_data
    
    def find_by_home_id(self):

        return []
    
    def add_user(self, data):
        resp_data = []
        try:
            # resp_data = super().find_all()
            token_auth = TokenAuthentication()
            userInfoDecoded = jwt.decode(data['userInfo'], settings.SECRET_KEY)
            self.createUser(request=userInfoDecoded['userInfo'])
        except Exception as error:
            print("[Error]", error)
            raise error
           
        return userInfoDecoded

    def edit_user(self, data):
        resp_data = []
        try:
            userInfoDecoded = jwt.decode(data['userInfo'], settings.SECRET_KEY)['userInfo']
            criteria = QueryFilter(id=userInfoDecoded['id'])
            response = super().find_by_criteria(criteria)
            instance = common.get_value(idf.INSTANCES, response)[0]
            serialized = common.get_value(idf.SERIALIZED, response)[0]
            if userInfoDecoded[idf.OBJ_PASSWORD] == '12345678':
                userInfoDecoded[idf.OBJ_PASSWORD] = serialized[idf.OBJ_PASSWORD]
                super().update(userInfoDecoded, instance)
            else:
                userInfoDecoded[idf.OBJ_PASSWORD] = str(jwt.encode({idf.OBJ_PASSWORD: userInfoDecoded[idf.OBJ_PASSWORD]}, settings.SECRET_KEY), 'utf-8')
                resp_data = super().update(userInfoDecoded, instance)
            
            resp_data = self.login(request=serialized)

        except Exception as error:
            print("[Error]", error)
            raise error
        print("[hehe]", resp_data)
        return resp_data

    def login(self, request):
        resp_data={}
        token_auth = TokenAuthentication()
        try:
            user = self.find_by_username(request[idf.OBJ_USERNAME])
            req_pass = jwt.decode(request[idf.OBJ_PASSWORD].encode('UTF-8'), settings.SECRET_KEY)
            decrypted_pass = jwt.decode(user[idf.OBJ_PASSWORD].encode('UTF-8'), settings.SECRET_KEY)
            if(not decrypted_pass[idf.OBJ_PASSWORD] == req_pass[idf.OBJ_PASSWORD]):
                raise HTTP401Error
            resp_data[idf.TOKEN] = token_auth.encode_token(user)
        except Exception as error:
            print("[Error]", error)
            raise HTTP401Error

        return resp_data

    def register(self, request):
        resp_data={}
        data_obj = {
            idf.OBJ_FIRST_NAME: request[idf.OBJ_FIRST_NAME],
            idf.OBJ_LAST_NAME: request[idf.OBJ_LAST_NAME],
            idf.OBJ_USERNAME: request[idf.OBJ_USERNAME],
            idf.OBJ_PASSWORD: request[idf.OBJ_PASSWORD],
            idf.ROLE: request[idf.OBJ_ROLE] or 0,
        }
        try:
            user = super().save(data_obj)
            default_home =HomesManagement().add_house({idf.NAME: data_obj[idf.OBJ_FIRST_NAME] + "'s home", idf.OBJ_ADDRESS: 'My Address', idf.OBJ_CREATED_BY: user.id,idf.OBJ_ROOMS: [{idf.OBJ_TYPE: 2, idf.NAME: "My Room"}]})
            home_access = HomeUserAccessManagement().add_user_house(userId=user.id, homeId=default_home.id, role=1, status=1) # Add User to Home 
            resp_data = self.login(request=request)
            
        except Exception as error:
            print("[Error]", error)
            raise error 
        return resp_data
    
    
    def createUser(self, request):
        resp_data={}
        data_obj = {
            idf.OBJ_FIRST_NAME: request[idf.OBJ_FIRST_NAME],
            idf.OBJ_LAST_NAME: request[idf.OBJ_LAST_NAME],
            idf.OBJ_USERNAME: request[idf.OBJ_USERNAME],
            idf.OBJ_PASSWORD: request[idf.OBJ_PASSWORD],
            idf.ROLE: request[idf.OBJ_ROLE] or 0,
        }
        try:
            user = super().save(data_obj)
            default_home =HomesManagement().add_house({idf.NAME:"My Home", idf.OBJ_ADDRESS: 'My Address', idf.OBJ_CREATED_BY: user.id, idf.OBJ_ROOMS: [{idf.OBJ_TYPE: 2, idf.NAME: "My Room"}]})
            HomeUserAccessManagement().add_user_house(userId=user.id, homeId=default_home.id, role=1, status=1) # Add User to Home 
            
        except Exception as error:
            print("[Error]", error)
            raise error 
        return resp_data
    

    def deleteUser(self, userId):
        resp_data = {}
        try:
            home_access_mgnt = HomeUserAccessManagement()
            home_access_mgnt.delete_all_user_access(userId=userId)

            criteria = QueryFilter(id=userId)
            response = super().delete(criteria)
            resp_data = common.get_value(idf.SERIALIZED, response)
        except Exception as error:
            print("[Error] Username not Found", error)
            raise HTTP401Error
        return resp_data
