from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import parsers, renderers, serializers, status
from apps.chatbot.api.serializer import ChatBotSerializerRequest, ChatBotSerializerResponse
from apps.chatbot.services.chatbot_service import ChatBotService
from core.models import Chatbot

class ChatDetailAPI(APIView):
    serializer_class = ChatBotSerializerRequest

    @swagger_auto_schema(
        tags=["chatbot"],
        request_body=ChatBotSerializerRequest,
        response={200: ChatBotSerializerResponse}
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context = {'request':request})
        serializer.is_valid(raise_exception=True)
        document_id=serializer.validated_data["document_id"]
        message=serializer.validated_data["message"]
        chatbot_service=ChatBotService()
        result=chatbot_service.process_query(document_id, message)
        
        return Response(data={"response":result, "document":document_id})


