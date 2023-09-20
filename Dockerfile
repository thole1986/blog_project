FROM python:3.10-slim


WORKDIR /techsolution

COPY requirements.txt requirements.txt 
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY apps apps
COPY application.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP application.py
ENV FLASK_CONFIG production


EXPOSE 5000
ENTRYPOINT ["./boot.sh"]