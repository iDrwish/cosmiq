from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

# Create your views here.

class UpdateMessage(APIView):
    def post(self, request, format=None):
        data = JSONParser().parse(request)
        payload_string = data['payload']
        print(type(payload_string))
        print(payload_string)
        # payl
        print(data)