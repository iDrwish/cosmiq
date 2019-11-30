import json
import pdb
import boto3
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from braces.views import CsrfExemptMixin
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from datetime import datetime as dt


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class UpdateMessage(APIView):
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    @csrf_exempt
    def post(self, request, format=None):
        load = json.loads(request.data['payload'])
        if load['type'] == 'interactive_message':
            # callback_id = load.get('callback_id')
            # response_url = load.get('response_url')
            # channel_name = load.get('channel', {}).get('name')
            user_id = load.get('user', {}).get('id')
            original_message = load.get('original_message')
            original_message['replace_original'] = True
            original_message["text"] = ":white_check_mark: <@{}> *marked this done.*".format(
                user_id)
            _a, attch2 = original_message.get('attachments')
            attch2.pop('actions')
            return Response(original_message, status=200)
        return HttpResponse(status=200)


def getOS(request):
    a = request.META.get('HTTP_USER_AGENT')
    if ('iphone' in a.lower()) or ('macintosh' in a.lower()) or ('ipad' in a.lower()):
        return redirect('https://apps.apple.com/app/halan-driver/id1463180488')
    else:
        return redirect('https://play.google.com/store/apps/details?id=com.halan.halandriver')


def adjustParameters(request):
    queryParameters = request.GET.dict()
    if queryParameters:
        s3 = boto3.client('s3')
        timeNow = dt.now()
        Key = timeNow.strftime('%Y/%m/%d/')
        params = {'adid': queryParameters.get('adid', None),
                  'tracker': queryParameters.get('tracker', None),
                  'timestamp': int(timeNow.timestamp()*1000),
                  'installed_at': queryParameters.get('installed_at', None)}
        fileName = '{timestamp}-{adid}-{tracker}-{installed_at}'.format(
            **params)
        s3.put_object(Body=json.dumps(queryParameters),
                      Bucket='halan-adjust-callback', Key=Key+fileName+'.json')
    return HttpResponse(status=200)
