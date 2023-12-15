FROM python:3
ADD  humidity_monitor.py /
RUN pip install schedule requests
CMD [ "python", "./humidity_monitor.py" ]