from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

class ChatDetailAPI(APIView):
    serializer_class = None

  

    @swagger_auto_schema(
        tags=["chatbot"],
    )
    def get(self, request):
        """
        Sample Hello world
        """
        return Response(data={"hello":"world"})