FROM alpine

RUN apk update \
 && apk add alpine-sdk linux-headers \
            python py3-pip python3-dev \
            py3-libxml2 libxml2-dev libxslt-dev

# ====================================================================
# All commands below this paragraph are from the quick-start guide at:
# http://airflow.apache.org/installation.html
# ====================================================================

# airflow needs a home, ~/airflow is the default,
# but you can lay foundation somewhere else if you prefer
# (optional)
#ENV AIRFLOW_HOME /airflow/home

# install from pypi using pip
RUN pip3 install apache-airflow

# initialize the database
RUN airflow initdb

# start the web server, default port is 8080
CMD ["airflow", "webserver", "-p", "8080"]