import json
import jwt
import logging
import requests
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response

logger = logging.getLogger(__name__)
def auth_check(get_response):
    # One-time configuration and initialization.

    def checking(request, *args, **kwargs):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # token = request.META.get('HTTP_AUTHORIZATION')
        jwt_token = request.headers.get('Authorization')

        if jwt_token is not None:
            url = 'https://api.umkt.ac.id/'
            try:
                payload = jwt.decode(jwt_token.split(' ')[1], algorithms=['HS256'],
                                                options=({"verify_signature": False, 'verify_exp': True}), )
            except:
                return Response({'message': 'Token is expired'}, status=status.HTTP_401_UNAUTHORIZED)
            uniid = payload['user']
            if payload['user'] != '':
                try:
                    user = User.objects.get(username=uniid)
                except User.DoesNotExist:
                    if uniid[0].isdigit():
                        auth_url = url + 'mahasiswa-notoken/nim/' + uniid
                    else:
                        auth_url = url + 'pegawai-notoken/username/' + uniid

                    headers = {'token': '95d6a4e57c47891c96d8c20ce7feecee8ffc25d07abd9751b189224b252e32c0'}

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
                response = get_response(request, *args, **kwargs)
                return response
            else:
                return Response({'message': 'user doest not exists'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'Token not exist'}, status=status.HTTP_401_UNAUTHORIZED)

        # Code to be executed for each request/response after
        # the view is called.
    return checking
