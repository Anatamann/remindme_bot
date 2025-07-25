FROM python:3.13-slim

WORKDIR /home/remindme_bot

COPY requirements.txt /home/remindme_bot

RUN pip install --no-cache-dir -r requirements.txt 
RUN python -m spacy download en_core_web_sm

COPY . /home/remindme_bot/

CMD ["python", "-m", "remindme_bot"]