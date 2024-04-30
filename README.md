# taxgpt

<img width="822" alt="image" src="https://github.com/ibadia/taxgpt/assets/14020143/0661d8b0-618c-4bf1-8485-3c5a16cd8211">


## Architecture:
First lets understand the architecture of our application:
We have two repositories:
1. Taxgpt
2. Taxgpt-frontend

Taxgpt is written in django and have the backend code.
Taxgpt-frontend is written in react and have the frontend code.

Taxgpt-backend is deployed on AWS ec2 instance via simple docker file and start.sh script
Taxgpt-frontend is deployed on netlify

Our backend interacts with frontend with a cloudfront layer in between to allow https requests and prevent DDOS attacks to our website.
## Installing Celery:
1. For installing celery first install docker on your local computer and then run
2.  `docker run --name taxgpt-redis -d redis`
3.  Then follow the steps in Setup Project and celery will be automatically installed when you run `pip install -r requirements.txt`
4.  Then open a terminal or command prompt and run `celery -A core worker -l INFO`
5.  Here INFO implies that it will log only info related logs for debugging please run `celery -A core worker -l DEBUG` instead
6.  In .env file set the following
```.env
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/1
```
## Local Installation Guide
1. First install python3.9 using anaconda or directly
2. Then install `pip` 
3. Then run `pip install -r requirements.txt`  this will install all the relevant packages required.
4. Rename the `.env.example` file to `.env`
5. Set the `USE_LOCAL` parameter to be True
   1. This will ensure that when you are running this on local, you do not need to install postgresql but can easily run the application using sqlite in order to improve productivity
6. The open a new terminal and run `celery -A core worker -l DEBUG`
   1. This will run the celery instance
7. Then run `python manage.py migrate`
8. Then run `python manage.py runserver 8000`


## Deployment Guide:
1. To deploy simply open an amazon ec2 insance with preferably ubuntu
2. Create a REDIS cache 
3. Create AWS RDS db instance and get its id and password
4. Install docker in your ec2.
5. Clone this repository then cd into the repo 
6. Put redis cache link in .env file for the celery
7. Put postgres id and password
8. Put Groq ID and verify API token in .env
9. Run `chmod +x start.sh`
10. Run `./start.sh`
11. Then create a cloudfront on aws with a distribution WITHOUT CACHE and allow forwarding as is.
   1. The only reason for using cloudfront is to allow https requests and prevent ddos
12. You can now access the link on cloud
13. frontend can be simply deployed on netlify and backend can be accesed via cloud front link


## External Dependencies:
1. We are using groq https://groq.com/ for our chat feature with `model="mixtral-8x7b-32768"` 
2. We are using https://www.veryfi.com/ for PDF parsing and ocr
   1. The basic purpose of using verifi is to parse pdf and give us a JSON result which can then be feed to the chatbot for question answering.
   2. Verify cost about `0.16 $` per document. Hence it adds an additional cost of 0.16 USD per USER assuming each user only uploads one w2 form.
   3. Verify have the feature to specifically process W2 form, either in image form or in normal pdf.
3. The json generated by verify is then passed to chatbot as the first context message.




## Core Flow Explanation:
1. We have created the following tables.
   1. Documents
   2. ParsedDocuments
   3. APICallLogs
   4. Chatbot
2. Whenever user uploads a document, a background job is run on CELERY which will send the request to VERIFI to parse the document, the result will be saved in ParsedDocument table along with the reference to the actual document.
   1. We are using a background job because VERIFI can sometimes take time to process.
   2. Once the background job is run, we will also log the API call to APICALL logs
   3. The reason for logging all external api calls to APICALLLOGS is because these API are paid per request and it is essential to know when and what api calls are made.
3. Then if user wants to CHAT regarding the document he have uploaded.
   1. The frontend will call the chatbot api we have exposed along with the document_id (the one that user have uploaded).
   2. The Chatbot will then call groq api and will log it to api calls.
   3. The context will be given to groq which will be the JSON that verify have generated.
   4. Whole user chat history will be saved in Chatbot table.
   5. If user dissapears for some time then re initiate the chat, the backend will get the previous chat records for the last 3 hours and chain it along with previous chats.



## LINKS GIVEN:
### Github Repository
1. https://github.com/ibadia/taxgpt
2. 2. https://github.com/ibadia/taxgpt-frontend

### Access Links:
1. https://nimble-taiyaki-cb3e5a.netlify.app/ (FOR FRONTEND APPLICATION ACCESS)
2. https://d198bemxyz9el2.cloudfront.net/docs/ (CLOUD FRONT LINK  FOR ACCESSING SWAGGER DOCS) (FOR ACCESSING BACKEND APIS)


## Loom Video:
