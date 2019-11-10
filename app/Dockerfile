FROM python:3.7.4

ENV INSTALL_DIR=/usr/src/app

RUN mkdir -p $INSTALL_DIR

WORKDIR $INSTALL_DIR

ADD requirements.txt $INSTALL_DIR

RUN pip install -r $INSTALL_DIR/requirements.txt

ADD . $INSTALL_DIR

EXPOSE 8005

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
