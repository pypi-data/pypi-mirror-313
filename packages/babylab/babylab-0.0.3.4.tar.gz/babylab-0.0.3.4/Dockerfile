FROM python:3.12-slim

WORKDIR /babylab-redcap

RUN pip3 install --upgrade pip && pip install flask babylab

EXPOSE 5000

CMD ["flask", "--app", "babylab.main", "run", "--host=0.0.0.0", "--port=5000"]
