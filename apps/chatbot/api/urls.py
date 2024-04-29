from django.urls import path

from apps.chatbot.api.views import chatbot_api,pdf_upload_api

urlpatterns = [
    path(
        "chatbot/",
        chatbot_api.ChatDetailAPI.as_view(),
        name="chatbot"
    ),
    path(
        "pdfupload/",
        pdf_upload_api.PDFUploadView.as_view(),
        name="pdf_upload"
    )

]
