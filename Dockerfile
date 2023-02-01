FROM python:3
ADD  humidity_monitor.py /
ADD api_data.json /
RUN pip install schedule requests
CMD [ "python", "./humidity_monitor.py" ]