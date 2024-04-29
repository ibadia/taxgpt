from io import BytesIO
from tempfile import NamedTemporaryFile
from core.models import ParsedDocuments, Documents,APICallLogs
from celery import shared_task
from django.shortcuts import get_object_or_404
from core import settings
from django.conf import settings
import requests
import json
class CustomResponse:
    def __init__(self, text, status):
        self.text = text
        self.status_code = status

# Example usage:
@shared_task
def parse_and_save_document(db_document_id: int, encoded_string: str, debug=False):
    ## TO DO call an api from here which will send the request to parse pdf and then
    ## json which will be saved in parsed json file. 
   
    document_instance=get_object_or_404(Documents, id=db_document_id)
    parsed_doc_instance = ParsedDocuments.objects.create(document=document_instance, status="IN_PROGRESS", parse_type="VERIFY")
    parsed_doc_instance.save()

    response=send_request(encoded_string, debug=debug)
    
    status_code=response.status_code
    log_instance=APICallLogs.objects.create(document=document_instance, vendor="Verify", status=status_code)
    log_instance.save()

    if (status_code==201):
        parsed_doc_instance.parsed_string=response.text
        parsed_doc_instance.status="COMPLETED"
        parsed_doc_instance.save()
    else:
        parsed_doc_instance.status="FAILED"
        parsed_doc_instance.parsed_string=response.text
        parsed_doc_instance.save()
    return "Done"

def send_request(encoded_string, debug=False):
    if debug:
        return custom_response(encoded_string)
    url=settings.VERIFY_URL
    payload = json.dumps({
        "file_data": encoded_string,
        "max_pages_to_process": 2
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'CLIENT-ID': settings.VERIFY_CLIENT_ID,
        'AUTHORIZATION': settings.VERIFY_TOKEN
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response


def custom_response(encoded_string):
    response = CustomResponse("API key Not Present, For Testing", 201)
    return response





        
        


