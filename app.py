from chalice import Chalice
import json
from metaphone import DoubleMetaphone

app = Chalice(app_name='storm-name-matching-ec2')


@app.route('/match/{name}')
def index(name):
    return {"name":name, "key": DoubleMetaphone().parse(name)}