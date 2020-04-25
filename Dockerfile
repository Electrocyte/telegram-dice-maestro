FROM python:3.8

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

ADD diceroller.py ./

CMD [ "python", "diceroller.py" ]
