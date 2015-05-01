# Tornado-RabbitMQ

This is an example integration of Tornado and RabbitMQ. This app will allow you to post to tornado and it in turn will post of rabbitMQ. The exhange, exchange type, queue and routing key are configurable.

####To Run:

Copy config.yaml.example to config.yaml

Run using `python publisher_app.py --config_file config.yaml`


You will need to update config.yaml to your values.

You will need Tornado and RabbitMQ installed. Test are run using py.test

Python version: 2.6.6 Tornado version: 3.1 Pika version: 0.9.14
