from chalice import Chalice
import json
import logging

import chalicelib.demo as demo

app = Chalice(app_name='storm-name-matching-ec2')
app.log.setLevel(logging.DEBUG)

@app.route('/match/{name}')
def index(name):
    demo.username = name
    logger = app.log
    return demo.sm(logger, name)