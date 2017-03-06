FROM python:2

COPY main.py /usr/src/app/
COPY config.yml /usr/src/app/

RUN pip install requests pyyaml schedule pyopenssl

WORKDIR /usr/src/app

CMD ["python", "./main.py"]