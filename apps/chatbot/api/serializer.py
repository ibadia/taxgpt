from rest_framework import serializers
from core.models import Documents
from django.core.exceptions import ValidationError

class PDFDocumentSerializer(serializers.ModelSerializer):
    document=serializers.FileField()

    class Meta:
        model=Documents
        exclude=["document_filename"]


    def validate_document(self, value):
        """
        Check if the uploaded file is an Excel file.
        """
        if not value.name.endswith('.pdf'):
            raise ValidationError("Only PDF files (.pdf) are supported.")
        return value