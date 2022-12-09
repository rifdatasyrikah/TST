FROM python:3.9
WORKDIR /TST
COPY requirements.txt /TST/requirements.txt
RUN pip install -r requirements.txt
COPY . /TST
EXPOSE 8000
CMD ["python", "main.py"]