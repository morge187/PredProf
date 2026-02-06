FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Явно говорим Flask CLI, что запускать
ENV FLASK_APP="app:create_app"

# Чтобы config точно получил URI (у вас Settings читает DATABASE_URL)
ENV DATABASE_URL="sqlite:////app/canteen.db"

EXPOSE 5000

# Миграции при старте контейнера (рекомендуется)
CMD sh -c "flask --app app:create_app db upgrade && python app/main.py"
