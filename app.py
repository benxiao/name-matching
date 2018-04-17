from chalice import Chalice
import json
#import demo

app = Chalice(app_name='storm-name-matching-ec2')


@app.route('/match/{name}')
def index(name):
    return {"name":name}