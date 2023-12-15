FROM python:3
ARG api_key
ARG refresh_token
ENV API_KEY $api_key
ENV REFRESH_TOKEN $refresh_token
ADD  humidity_monitor.py /
RUN pip install schedule requests
CMD [ "python", "./humidity_monitor.py" ]