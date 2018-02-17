FROM python:3

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE "factcoin.settings.production"
ENV PORT 8000
EXPOSE 8000

ENTRYPOINT [ "./run.sh" ]
