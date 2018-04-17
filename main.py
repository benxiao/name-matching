import time
import logging
import json


from demo import sm

# global variables
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class InputParams:
    def __init__(self, name, n):
        self.name = name
        self.n = n


# event: dict -> (result: InputParams, error: Exception)
def read_event(event):
    if not event.get("body"):
        return None,  ValueError("body doesn't exist!")
    body = json.loads(event.get("body"))
    if not body.get("name"):
        return None,  ValueError("name doesn't exist!")
    name = body.get("name")
    n = 20
    if body.get("n"):
        logger.info(f"n found (use {body.get('n')})!")
        n = body.get('n')
    return InputParams(name, n), None


# input: DataFrame -> result: { key: str, val: list } can be easily converted to a json string
# def jsonfy_result(result):
#     return {name: list(result[name]) for name in result.columns}


def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        #logger.info("time taken: {:.2f}s".format(time.time() - start))
        print("time taken: {:.2f}s".format(time.time() - start))
        return ret
    return wrapper


def handler(event, context):
    print("raw_event: ", event)
    print("context: ", context)
    params, error = read_event(event)
    print("start...")
    if error:
        return {
            "statusCode": 400,
            "headers": {},
            "body": ""
    }
    # params must be good
    result = sm(params.name, top_n=params.n)
    return {
       "statusCode": 200,
       "headers": {
           # "Access-Control-Allow-Headers": "content-type",
           # "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
           "Access-Control-Allow-Origin": "*"
       },
       "body": json.dumps(result)
    }


if __name__ == '__main__':
    # sample run
    print(handler({ "body": "{ \"name\": \"Doanld\", \"n\": 50}" }, None))