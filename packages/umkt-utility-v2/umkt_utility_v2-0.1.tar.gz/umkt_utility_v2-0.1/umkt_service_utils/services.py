import json
import logging
import string

import jwt
import requests
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.http import HttpResponse
from rest_framework.exceptions import NotAuthenticated

from umkt_service_utils.models import Lembaga

logger = logging.getLogger(__name__)


def get_user_id(request):
    jwt_token = request.headers.get('authorization', None)
    try:
        payload = jwt.decode(jwt_token.split(' ')[1], algorithms=['HS256'],
                             options=({"verify_signature": False, 'verify_exp': True}), )
        return payload['user']
    except jwt.ExpiredSignatureError:
        return HttpResponse(json.dumps({"message": "token is expired"}), status=401)


def get_authorization_header(request):
    jwt_token = request.headers.get('authorization', None)
    if not jwt_token:
        raise NotAuthenticated
    return jwt_token.split(' ')[1]

def sync_user(request):
    url = 'https://api.umkt.ac.id/'

    uniid = get_user_id(request)

    if uniid[0].isdigit():
        auth_url = url + 'managemen/mahasiswa/' + uniid
        is_mahasiswa = True
    else:
        auth_url = url + 'managemen/karyawan/' + uniid
        is_mahasiswa = False
    headers = get_authorization_header(request)
    response = requests.get(auth_url, headers=headers)
    if not response.status_code == 200:
        res = response.json()
        logger.info(f"Response {res}")
        return HttpResponse(json.dumps(res), status=401)
    data = response.json()
    userdata = data['rows']['user'][0]
    username = userdata['username']
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create(username=username, first_name=userdata['first_name'],
                                   last_name=userdata['last_name'], email=userdata['email'])
    for groups in data['groups']:
        try:
            group = Group.objects.get(name=groups['name'])
        except Group.DoesNotExist:
            group = Group.objects.create(name=groups['name'])
        user.groups.add(group)
        user.save()
    # if not is_mahasiswa:
    #     lembaga_datas = data['rows']['lembaga']
        # fetch_lembaga(lembaga_datas, user)
        # lembaga_jabatan = data['rows']['jabatan']['lembaga']
        # fetch_lembaga(lembaga_jabatan, user)
    # else:
    #     pass


# def get_lembagas(user: User):
#     return Lembaga.objects.filter(Q(members__in=[user]) | Q(pejabats__in=[user]))
