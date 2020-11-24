FROM tensorflow/tensorflow

# Install Packages
RUN pip install sklearn pandas tensorflow keras django

# Install Application
CMD mkdir -p /app
WORKDIR /app
COPY . .

# Env Variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# Start Command
CMD python manage.py runserver 0.0.0.0:$PORT