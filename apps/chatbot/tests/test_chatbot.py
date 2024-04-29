from django.urls import reverse

from apps.chatbot.services.chatbot_service import ChatBotService
from core.factory import UserFactory
from core.models import Documents, ParsedDocuments

"""
Simply checking if the Chatbot base functionality is working
Here we are not making any api calls
"""
def test_message_chaining():
    chat_service=ChatBotService()
    user_result=UserFactory.create()
    doc_obj=Documents.objects.create(document_filename="test.pdf", document=b"hello world", user_id=user_result.user_id)
    parsed_obj=ParsedDocuments.objects.create(document=doc_obj, parsed_string="hello world", status="COMPLETED")
    result=chat_service.process_query(1,"hello world")
    assert (result.find("Hello from custom request")!=-1)