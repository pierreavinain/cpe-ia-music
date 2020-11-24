FROM tensorflow/tensorflow

CMD mkdir -p /var/server
WORKDIR /var/server
COPY . .
RUN pip install sklearn pandas tensorflow keras django

EXPOSE 5058
CMD ["python", "manage.py", "runserver", "0.0.0.0:5058"]