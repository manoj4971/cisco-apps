import random
import redis
import os
import requests
from utils import logger
import time
from datetime import datetime


from flask import Flask, request, jsonify
import socket
import json

# Logging
log = logger('booking', '{}/booking.log'.format(os.getcwd()))
serviceName = "Booking"
# Default serve delay
global serve_delay
serve_delay = 1

# Define services endpoints

try:
    redis_service = os.environ['REDIS_SERVICE']
except:
    redis_service = '127.0.0.1'

try:
    redis_port = os.environ['REDIS_PORT']
except:
    redis_port = '6379'

try:
    external_service = os.environ['EXT_SERVICE']
except:
    external_service = "HTTPS://AMEX-FSO-PAYMENT-GW-SIM.AZUREWEBSITES.NET/API/PAYMENT"


log.info('Redis target is: {}'.format(redis_service))
log.info('External Service URL is {}'.format(external_service))


# Redis support in version 2
db = redis.Redis(host=redis_service, port=redis_port,db=0, socket_connect_timeout=2)


# Flask app object
app = Flask(__name__)

# Log application started
log.info('APPSTART: Booking started')


@app.route('/booking', methods=['POST'])
def booking():
    log.info('Incoming booking request from: {}'.format(request.remote_addr))
    delay = random.randint(0, 1000) / 1000.0  # time in seconds
    log.info("Adding {} seconds of delay ".format(delay))
    time.sleep(delay)
    creditCard = str(request.json['creditcard'])
    log.info("CreditCard selected {}".format(creditCard))

    try:
        result = {
            "name": str(request.json['name']),
            "lastname": str(request.json['lastname']),
            "mobile": request.json['mobile'],
            "date": request.json['date'],
            "doctor": request.json['doctor'],
            "price": request.json['price'],
            "age": request.json['age'],
            "gender": request.json['gender'],
            "creditcard": request.json['creditcard'],
            "category": request.json['category']
        }
        try:
            log.info("Adding patient:" + str(json.dumps(result)) + ", to DB " + str(redis_service))
            # Log transactions
            db.rpush('transactions', str(json.dumps(result)))
            log.info('Logged transaction in database...')
            log.info('Waiting {} seconds before serving...'.format(serve_delay))
            time.sleep(serve_delay)
        except:
            log.warning(
                'REDIS: {} is not reachable. Will not log this transaction.'.format(redis_service))
            pass
        try:
            # Check if CreditCard is Amex, to call external service
            if creditCard == 'Amex':
                log.info('Calling external service {}'.format(external_service))
                # Make a request to an external payment to simulate interaction
                r = requests.get(external_service)
                log.info('Called external service {}'.format(external_service))
                log.info("Status Code {}".format(r.status_code))
                r.raise_for_status()
                log.info('Calling external service {}'.format(external_service))
        except Exception as e:
            #log.error('Unable to call the ext service {}'.format(external_service))
            log.error("Error: " + str(e) )
            result = {'success': False, 'error': {'type': r.status_code, 'message': r.reason}}

        return jsonify(result)
    except:
        log.error('Can\'t return payload, something is wrong')


# Kubernetes health checks
@app.route('/healthz', methods=['GET'])
def healthz():
    return "I'm fine"

# Serve delay views


@app.route('/delay01', methods=['GET'])
def delay01():
    global serve_delay
    serve_delay = 0.1
    return "Set serve delay to 0.1 second - Timestamp: {} - serve_delay: {}".format(datetime.now(), serve_delay)


@app.route('/delay1', methods=['GET'])
def delay1():
    global serve_delay
    serve_delay = 1
    return "Set serve delay to 1 second - Timestamp: {} - serve_delay: {}".format(datetime.now(), serve_delay)


@app.route('/delay3', methods=['GET'])
def delay3():
    global serve_delay
    serve_delay = 3
    return "Set serve delay to 3 second - Timestamp: {} - serve_delay: {}".format(datetime.now(), serve_delay)


@app.route('/delay5', methods=['GET'])
def delay5():
    global serve_delay
    serve_delay = 5
    return "Set serve delay to 5 seconds - Timestamp: {} - serve_delay: {}".format(datetime.now(), serve_delay)


@app.route('/delay10', methods=['GET'])
def delay10():
    global serve_delay
    serve_delay = 10
    return "Set serve delay to 10 seconds - Timestamp: {} - serve_delay: {}".format(datetime.now(), serve_delay)


@app.route('/getDelay', methods=['GET'])
def getDelay():
    return f'The current delay is set to: {serve_delay}'


@app.route('/log', methods=['GET'])
def showlog():
    with open('{}/booking.log'.format(os.getcwd())) as logfile:
        return logfile.read()


# Run Flask
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5001, threaded=True)
