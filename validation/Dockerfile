FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN playwright install --with-deps
CMD ["python", "validate.py"]  # For manual run; use cron in production