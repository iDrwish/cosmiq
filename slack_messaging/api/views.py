import json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from braces.views import CsrfExemptMixin
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class UpdateMessage(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    @csrf_exempt
    def post(self, request, format=None):
        load = json.loads(request.data['payload'])
        if load['type'] == 'interactive_message':
            # callback_id = load.get('callback_id')
            # response_url = load.get('response_url')
            # channel_name = load.get('channel', {}).get('name')
            user_id= load.get('user', {}).get('id')
            original_message = load.get('original_message')
            original_message['replace_original'] = True
            original_message["text"] = ":white_check_mark: <@{}> *marked this done.*".format(user_id)
            return Response(original_message, status=200)
        return HttpResponse(status=200)
