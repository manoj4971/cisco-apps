# The offer service returns n offers to the frontend

import os, time
from utils import logger
from flask import Flask, request, jsonify

import socket
import json
import random, string

# Logging
log = logger('offers', '{}/offers.log'.format(os.getcwd()))

# Default serve delay
global serve_delay
serve_delay= 1

# Flask app object
app = Flask(__name__)

# Log application started
log.info('APPSTART: offers started')

# Generate ticket number function
def genid(size):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

# Return payload function
with open('./offers.json') as f:
    payload = json.loads(f.read())

# View function

@app.route('/search', methods=['GET'])
def search():
    log.info('Incoming search request from: {}'.format(request.remote_addr))

    try:
        # Wait 5 seconds before returning the search to simulate big backend data
        delay = random.randint(0, 5000) / 1000.0 # time in seconds
        log.info("Adding {} seconds of delay ".format(delay))
        time.sleep(delay)
        
        log.debug('Waiting {} seconds before returning search'.format(serve_delay))
        #time.sleep(serve_delay)
        log.info('Returning search to {}'.format(request.remote_addr))
        
        
        if(request.args.get('category') ):
            log.info('Filtering output per Category:' + request.args.get('category') )
            category = request.args.get('category')
            # Filter python objects with list comprehensions
            output_json = [x for x in payload if x['category'] == category]
        else:
            output_json = payload

        for offer in payload:
            offer['served_by'] = socket.gethostname()
            offer['version'] = '1'
        log.debug('Payload is: {}'.format(output_json))
        return jsonify(output_json)
    except:
        log.error('Can\'t return payload, something is wrong')




# Kubernetes health checks
@app.route('/healthz', methods=['GET'])
def healthz():
    return "I'm fine"

# Delay views
@app.route('/delay0', methods=['GET'])
def delay0():
    global serve_delay
    serve_delay = 0
    return "Set serve delay to 0 seconds (default)"

@app.route('/delay1', methods=['GET'])
def delay1():
    global serve_delay
    serve_delay = 1
    return "Set serve delay to 1 seconds (default)"

@app.route('/delay3', methods=['GET'])
def delay3():
    global serve_delay
    serve_delay = 3
    return "Set serve delay to 3 seconds"

@app.route('/delay5', methods=['GET'])
def delay5():
    global serve_delay
    serve_delay = 5
    return "Set serve delay to 5 seconds"

@app.route('/getDelay', methods=['GET'])
def getDelay():
    return f'The current delay is set to: {serve_delay}'

# Run Flask
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5051, threaded=True)
