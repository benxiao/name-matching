from chalice import Chalice
import json
import demo

app = Chalice(app_name='storm-name-matching-ec2')


@app.route('/match/{name}')
def index(name):
    result = demo.sm(name, top_n=30)
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(result)
    }


