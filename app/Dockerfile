FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP="app:create_app"
ENV DATABASE_URL="sqlite:////app/canteen.db"

EXPOSE 5000

CMD sh -c "flask --app app:create_app db upgrade && flask --app app:create_app run --host=0.0.0.0 --port=5000"
