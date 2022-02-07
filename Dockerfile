FROM gcr.io/google-appengine/python

COPY ./requirements.txt /code/requirements.txt
RUN apt-get update
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip

#
#RUN pip install https://github.com/KumaTea/tensorflow-aarch64/releases/download/v2.6/tensorflow-2.6.0-cp38-cp38-linux_aarch64.whl

RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt
ADD ./app /code/
WORKDIR /code

CMD wget https://storage.googleapis.com/generic-projects/TextCortex/models/gpt2-mod/config.json -P /model
CMD wget https://storage.googleapis.com/generic-projects/TextCortex/models/gpt2-mod/pytorch_model.bin -P /model
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]