# Use alpine-python-3 appd image
FROM rtortori/ubuntu-python3

# Set the working directory to /
WORKDIR /

# Copy app requirements
ADD requirements.txt /

# Optionally define proxy environment
#ARG http_proxy=http://proxy-wsa.esl.cisco.com:80
#ARG https_proxy=http://proxy-wsa.esl.cisco.com:80

# Install requirements
RUN pip install -r requirements.txt && pip install -U appdynamics==21.10.0.4495 

# Set Entry point
ENV APP_ENTRY_POINT "python /offers.py"

# Copy app requirements
ADD offers.py utils.py start_with_appd.sh offers.json /

# Expose port 5001
EXPOSE 5051/tcp

# Run it
ENTRYPOINT ["./start_with_appd.sh"]
