From python:3.9

WORKDIR /chatbot-app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./app

EXPOSE 8013

CMD ["python","./app/app.py"]