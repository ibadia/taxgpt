import datetime
from core.models import Chatbot, ParsedDocuments
from groq import Groq
from django.utils import timezone
from django.conf import settings
class GroqSingleton:
    _instance = None
    def __new__(cls, *args, **kwargs)-> Groq:
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance = Groq(api_key=settings.GROQ_API_KEY)
        return cls._instance

class ChatBotService:
    def __init__(self):
        pass

    def process_query(self, document_id, query):
        parsed_doc=ParsedDocuments.objects.get(document_id=document_id)
        if parsed_doc.status=="FAILED":
            raise Exception("Document parsing failed")
        elif parsed_doc.status=="COMPLETED":
            chat_history=self.get_chat_history(document_id)
            messages=self.format_in_chatbot_format(chat_history, parsed_doc.parsed_string)
            messages.append({"role":"user", "content":query})
            response=self.send_request(messages)
            self.save_response_to_db(document_id, query, response)
            return response
        else:
            raise Exception("Document parsing is in progress, please retry later")

    def save_response_to_db(self, document_id, query, response):
        chatbot_db_instance=Chatbot.objects.create( message=query, response=response, document_id=document_id)
        chatbot_db_instance.save()

    def get_chat_history(self,document_id: int):
        current_time = datetime.datetime.now()
        
        start_time = current_time - datetime.timedelta(hours=3)


        start_time = timezone.make_aware(start_time)
        current_time = timezone.make_aware(current_time)

        
        results = Chatbot.objects.filter(document_id=document_id, 
                      created_at__range=(start_time, current_time)).order_by('created_at')
        
        chat_history = [(result.message, result.response) for result in results]
        
        # Return the chat history
        return chat_history
    

    def format_in_chatbot_format(self, chat_history, document_parsed_string):
        message_obj={"role":"system", }
        
        messages=[{"role":"system","content":document_parsed_string}]
        for chat in chat_history:
            messages.append({"role":"user", "content":chat[0]})
            messages.append({"role":"system", "content":chat[1]})
        return messages
    
    def custom_request(self, messages):
        return messages[-1]["content"]+" -- Hello from custom request\n"
    

    def send_request(self, messages):
        if settings.USE_CUSTOM_FUNCTION=="True":
            return self.custom_request( messages)
        completion = GroqSingleton().chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=messages,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        complete_response="".join([chunk.choices[0].delta.content or "" for chunk in completion])
        return complete_response