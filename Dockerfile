FROM python:3.6-alpine

WORKDIR /web

COPY . .

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    rm -rf requirements.txt

EXPOSE 8888

CMD ["/bin/sh", "-c", "python trans_server.py"]

