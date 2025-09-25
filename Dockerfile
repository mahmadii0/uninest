FROM python:3.12.7
LABEL authors="mahmadii0"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "python webApp/manage.py migrate && python webApp/manage.py runserver & python bot/bot.py"]