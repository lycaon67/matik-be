import jwt
from django.conf import settings
from django.utils import timezone
from datetime import timedelta, datetime
from core.constants import identifer as idf
# from user.management import UserManagement


class TokenAuthentication():

    def set_expiry(self):
        """
        Sets token expiration
        """
        return timezone.now() + timedelta(minutes=settings.SESSION_TOKEN_EXPIRY)

    def expire(self):
        """
        Sets token expiration
        """
        return timezone.now()

    def extract_bearer(self, auth_string):
        """
        Extacts token from bearer string

        Sample:

        "Bearer eyJ0eXAiOiJKV1QiLCJh"

        """
        return auth_string.split(idf.SPACE)[1]

    def encode_token(self, user):
       
        data = {}
        # Append expiry on token
        data[idf.OBJ_ID] = user[idf.OBJ_ID]
        data[idf.OBJ_FIRST_NAME] = user[idf.OBJ_FIRST_NAME]
        data[idf.OBJ_LAST_NAME] = user[idf.OBJ_LAST_NAME]
        data[idf.OBJ_USERNAME] = user[idf.OBJ_USERNAME]
        data[idf.OBJ_ROLE] = user[idf.OBJ_ROLE]
        data[idf.OBJ_EXP] = self.set_expiry()

        # Encode token
        token = jwt.encode(data, settings.SECRET_KEY)
        return token.decode('UTF-8')
    

    def decode_token(self, token):
        """
        Decode token without checking the expiration
        """
        return jwt.decode(token, settings.SECRET_KEY,
                          options={"verify_exp": False})

    def encrypt_pass(self, password):
        return jwt.encode({idf.OBJ_PASSWORD: password}, settings.SECRET_KEY, algorithm="HS256") 
    
    def decrypt_pass(self, user_pass):
        return jwt.decode({idf.OBJ_PASSWORD: user_pass}, settings.SECRET_KEY, algorithm="HS256",
                          options={"verify_exp": False})

    def get_sso_id(self, request):
        """
        Return sso_id from given request
        """
        token_key = self.extract_bearer(
            request.META[idf.HTTP_AUTHORIZATION])

        user_obj = self.decode_token(token_key)

        return user_obj[idf.OBJ_ONESIGN_UID]
