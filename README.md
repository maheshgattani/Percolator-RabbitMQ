# Percolator-RabbitMQ

This is an example integration of Percolator and RabbitMQ. This app will start allow you to post to percolator and it in turn will post of rabbitMQ
The exhange, exchange type, queue and routing key are configurable.

To Run:
Copy config.yaml.example to config.yaml
Run `python publisher_app.py --config_file config.yaml

You will need to update config.yaml to your values.

Also, goes without saying, you will need percolator and rabbitMQ installed.
Test are run using py.test
