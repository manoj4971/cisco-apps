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


log.info( 'Redis target is: {}'.format(redis_service))
log.info( 'External Service URL is {}'.format(external_service))



# Redis support in version 2
db = redis.Redis(host=redis_service, port=redis_port,
                db=0, socket_connect_timeout=2)


# Flask app object
app = Flask(__name__)

# Log application started
log.info('APPSTART: Booking started')




@app.route('/booking', methods=['POST'])
def booking():
    log.info('Incoming booking request from: {}'.format(request.remote_addr))
    delay = random.randint(0, 2300) / 1000.0 # time in seconds
    log.info("Adding {} seconds of delay ".format(delay))
    time.sleep(delay)
    creditCard = str(request.form['creditcard'])
    

    try:
         result = buildAppointment(request.form) 


    except:
        log.error('--------------[Can\'t return payload, something is wrong')
        return jsonify('--------------[Can\'t return payload, something is wrong')



    try:
        if creditCard == 'Amex':
            log.info("found credit card {}".format( request.form['creditcard']) )
            log.info('Calling external service {}'.format(external_service))
            r = requests.get(external_service)
            log.info('Called external service {}'.format(external_service))
            log.info("Status Code {}".format(r.status_code))
            r.raise_for_status()
    except:
        log.error('--------------[Unable to call the ext service {}'.format(external_service))
        return jsonify("bad"), r.status_code 

    try:
        if creditCard == 'Amex':
            log.info("found credit card {}".format( request.form['creditcard']) )
            log.info('Calling external service {}'.format(external_service))
            r = requests.get(external_service)
            log.info('Called external service {}'.format(external_service))
            log.info("Status Code {}".format(r.status_code))
            #r.raise_for_status()
    except:
        log.error('--------------[Unable to call the ext service {}'.format(external_service))
        return jsonify("bad"), r.status_code 

    
    
    return jsonify("all good")
    
    

def buildAppointment(appointment):
    # Process incoming dict as an array for data prep
    log.info("buildAppointment function")
    app = {
        "name": appointment['name'],
        "lastname": appointment['lastname'],
        "mobile": appointment['mobile'],
        "date": appointment['date'],
        "doctor": appointment['doctor'],
        "price": appointment['price'],
        "age": appointment['age'],
        "gender": appointment['gender'],
        "creditcard": appointment['creditcard'],
        "category": appointment['category']
    }
    return app


# Run Flask
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5001, threaded=True)





