"""CAS authentication middleware"""
import json
import jwt
import logging
import requests
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse


__all__ = ["UMKTJWTMiddleware"]

from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)


def create_response(request_id, code, message):
    """
    Function to create a response to be sent back via the API
    :param request_id:Id fo the request
    :param code:Error Code to be used
    :param message:Message to be sent via the APi
    :return:Dict with the above given params
    """

    try:
        req = str(request_id)
        data = {"data": message, "code": int(code), "request_id": req}
        return data
    except Exception as creation_error:
        logger.error(f'create_response:{creation_error}')

class UMKTJWTMiddleware(MiddlewareMixin):
    """Middleware that allows CAS authentication on admin pages"""

    def process_request(self, request):
        # sumber request dari browser atau api
        user_agent = request.META.get('HTTP_USER_AGENT')
        referer = request.META.get('HTTP_REFERER')
        if user_agent and referer:
            if 'Mozilla' in user_agent and referer.startswith('http'):
                pass
            else:
                jwt_token = request.headers.get('authorization')
                logger.info(f"request received for endpoint {str(request.path)}")
                if jwt_token  is not None:
                    try:
                        url = 'https://api.umkt.ac.id/'
                        try:
                            payload = jwt.decode(jwt_token.split(' ')[1], algorithms=['HS256'],
                                                options=({"verify_signature": False, 'verify_exp': True}), )
                        except:
                            return JsonResponse({'message': 'Token is expired'}, status=401)
                        uniid = payload['user']
                        
                        if payload['user'] != '':
                            try:
                                user = User.objects.get(username=uniid)
                            except User.DoesNotExist:
                                if uniid[0].isdigit():
                                    auth_url = url + 'managemen/mahasiswa/' + uniid
                                else:
                                    auth_url = url + 'managemen/karyawan/' + uniid
                                headers = {"Authorization": jwt_token}
                                response = requests.get(auth_url, headers=headers)
                                if not response.status_code == 200:
                                    res = response.json()
                                    logger.info(f"Response {res}")
                                    return HttpResponse(json.dumps(res), status=401)
                                data = response.json()
                                userdata = data['rows']['user'][0]
                                username = userdata['username']
                                user = User.objects.create(username=username, first_name=userdata['first_name'],
                                                        last_name=userdata['last_name'], email=userdata['email'])
                            request.user_umkt = user
                        else:
                            return JsonResponse({'message': 'Username doest not exists'}, status=401)
                    except:
                        return JsonResponse({'message': 'Token Not Valid'}, status=401)
                else:
                    return JsonResponse({'message': 'Please insert Token'}, status=401)
                   

        
