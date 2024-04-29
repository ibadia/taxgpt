# taxgpt
<img width="634" alt="image" src="https://github.com/ibadia/taxgpt/assets/14020143/f120f863-a053-412d-8170-19802e459ed8">


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
1. To deploy simply open an amazon ec2 insance with preferably ubunut
2. Install docker on it.
3. Clone this repository then cd into the repo
4. Run `chmod +x start.sh`
5. Run `./start.sh`
6. Then create a cloudfront on aws with a distribution WITHOUT CACHE and allow forwarding as is.
   1. The only reason for using cloudfront is to allow https requests and prevent ddos
7. You can now access the link on 
