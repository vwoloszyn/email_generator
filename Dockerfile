FROM python:3.8-slim

COPY ./requirements.txt /code/requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt
ADD ./app /code/
WORKDIR /

CMD wget https://storage.googleapis.com/generic-projects/TextCortex/models/gpt2-mod/config.json -P /model
CMD wget https://storage.googleapis.com/generic-projects/TextCortex/models/gpt2-mod/pytorch_model.bin -P /model
CMD ["uvicorn", "code.main:app", "--host", "0.0.0.0", "--port", "8080"]