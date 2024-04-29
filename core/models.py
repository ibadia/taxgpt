from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.user_app.models import AppUser



class BaseModel(models.Model):
    id = models.BigAutoField(primary_key=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Documents(BaseModel):
    document_filename=models.CharField(max_length=100)
    document=models.BinaryField() #storing file in db as w2 form are not that big
    user=models.ForeignKey(AppUser, models.DO_NOTHING, null=True)


class ParsedDocuments(BaseModel):
    parsed_string=models.TextField()
    document=models.ForeignKey("Documents", models.DO_NOTHING)
    parse_type=models.CharField(max_length=100)
    status=models.CharField(max_length=30, null=True)


class APICallLogs(BaseModel):
    vendor=models.CharField(max_length=100)
    document=models.ForeignKey("Documents", models.DO_NOTHING)
    status=models.CharField(max_length=30)


class Chatbot(BaseModel):
    message=models.TextField()
    user=models.ForeignKey(AppUser, models.DO_NOTHING, null=True)
    response=models.TextField()
    document=models.ForeignKey("Documents", models.DO_NOTHING, null=True)