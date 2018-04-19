from chalice import Chalice
import json
from chalicelib.demo import sm

app = Chalice(app_name='storm-name-matching-ec2')


@app.route('/match/{name}')
def index(name):
    return sm(name)