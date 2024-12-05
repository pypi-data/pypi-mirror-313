FROM python:latest

WORKDIR /python-docker

RUN pip3 install flask babylab

CMD [ "python3", "-m" , "flask", "--app", "babylab.main", "run", "--host=127.0.0.1"]