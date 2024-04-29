# pdfapp/views.py
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.chatbot.api.serializer import PDFDocumentSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import parsers, renderers, serializers, status
from django.conf import settings
from apps.chatbot.tasks.tasks import parse_and_save_document
import base64
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Documents
from rest_framework.generics import GenericAPIView

class PDFUploadView(GenericAPIView):
    serializer_class=PDFDocumentSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=PDFDocumentSerializer,
        operation_description="Upload a PDF document",
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        pdf_file_reader=serializer.validated_data["document"].read()
        pdf_file_name=serializer.validated_data["document"].name
        pdf_document = Documents(document=pdf_file_reader, document_filename=pdf_file_name, user=request.user)
        pdf_document.save()

        encoded_string = base64.b64encode(pdf_file_reader).decode('utf-8')
        if settings.USE_CUSTOM_FUNCTION=="True":
            task = parse_and_save_document.delay(
                pdf_document.id,encoded_string, debug=True
            )
        else:
            task = parse_and_save_document.delay(
                pdf_document.id,encoded_string, 
            )

        return Response({"status":"file_uploaded","document_id":pdf_document.id}, status=status.HTTP_201_CREATED)

       
