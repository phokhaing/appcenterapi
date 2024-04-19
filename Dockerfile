FROM python

# WORKDIR .
# COPY . ./ftb_supportdesk_api
COPY . ./ftb_supportdesk_api

RUN pip3 freeze > requirements.txt
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /ftb_supportdesk_api/src

CMD python3 manage.py makemigrations \
   && python3 manage.py migrate \
   && python3 manage.py runserver 0.0.0.0:3001
# CMD [ "python3", "manage.py", "makemigrations" ]
# CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]
EXPOSE 3001