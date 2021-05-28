FROM python:3

WORKDIR /
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
