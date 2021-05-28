FROM python:3

WORKDIR /github/workspace
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ADD entrypoint.sh action-a/entrypoint.sh
RUN chmod +x action-a/entrypoint.sh
ENTRYPOINT ["action-a/entrypoint.sh"]
