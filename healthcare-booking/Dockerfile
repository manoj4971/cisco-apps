# Use alpine-python-3 appd image
FROM rtortori/ubuntu-python3

# Set the working directory to /
WORKDIR /

# Copy app requirements
ADD requirements.txt /

# Install requirements
RUN pip install -r requirements.txt && pip install -U appdynamics==21.10.0.4495 

# Set Entry point
ENV APP_ENTRY_POINT "python /booking.py"

# Copy app requirements
ADD booking.py utils.py start_with_appd.sh /

# Expose port 5001
EXPOSE 5001/tcp

# Run it
ENTRYPOINT ["./start_with_appd.sh"]
