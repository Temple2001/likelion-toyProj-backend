from django.shortcuts import render
from django.shortcuts import get_object_or_404
from guestbooks.models import *

from .serializers import GuestbookSerializer, GuestbookSecureSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class GuestbookList(APIView):
    def get(self, request, format=None):
        guestbooks = Guestbook.objects.all()
        serializer = GuestbookSerializer(guestbooks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = GuestbookSecureSerializer(data=request.data)
        if serializer.is_valid():
            guestbook = serializer.save()
            res_serializer = GuestbookSerializer(guestbook)
            return Response(res_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GuestbookDetail(APIView):
    def get(self, request, id):
        guestbook = get_object_or_404(Guestbook, id=id)
        serializer = GuestbookSerializer(guestbook)
        return Response(serializer.data)

    def delete(self, request, id):
        guestbook = get_object_or_404(Guestbook, id=id)
        raw_password = request.data.get('password')
        if guestbook.check_password(raw_password):
            guestbook.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)