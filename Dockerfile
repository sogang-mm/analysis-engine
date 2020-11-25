FROM sogangmm/ubuntu:18.04-mysql-py3

RUN apt-get update \
    && apt-get -y install python3 python3-pip python3-dev \
    git wget ssh vim \
    apt-utils \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip
RUN pip3 install setuptools

WORKDIR /workspace
ADD . .
RUN pip3 install -r requirements.txt

ENV DJANGO_SUPERUSER_USERNAME root
ENV DJANGO_SUPERUSER_EMAIL none@none.com
ENV DJANGO_SUPERUSER_PASSWORD password

COPY docker-compose-env/sshd_config /etc/ssh/sshd_config
#COPY docker-entrypoint.sh /docker-entrypoint.sh
#RUN chmod +x /docker-entrypoint.sh
#ENTRYPOINT ["/docker-entrypoint.sh"]

RUN chmod -R a+w /workspace

EXPOSE 8000
