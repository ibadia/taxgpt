from rest_framework import serializers
from core.models import Documents
from django.core.exceptions import ValidationError

class PDFDocumentSerializer(serializers.ModelSerializer):
    document=serializers.FileField()

    class Meta:
        model=Documents
        exclude=["document_filename", "user"]


    def validate_document(self, value):
        """
        Check if the uploaded file is an Excel file.
        """
        if not value.name.endswith('.pdf'):
            raise ValidationError("Only PDF files (.pdf) are supported.")
        return value
    

class ChatBotSerializerRequest(serializers.Serializer):
    message=serializers.CharField(max_length=10000)
    document_id=serializers.IntegerField()

    def validate_document_id(self, value):
        if value is not None:
            try:
                document=Documents.objects.get(id=value)
                if document.user!=self.context["request"].user:
                    raise ValidationError("You are not authorized to access this document.")
                return value
            except Documents.DoesNotExist:
                raise ValidationError("Document does not exist.")

class ChatBotSerializerResponse(serializers.Serializer):
    response=serializers.CharField(max_length=10000)
    document=serializers.IntegerField()