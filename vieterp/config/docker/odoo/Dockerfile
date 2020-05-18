FROM debian:jessie
LABEL maintainer="Sang <sang@vieterp.net>"

USER root

# Install some deps, lessc and less-plugin-clean-css, and wkhtmltopdf
RUN set -x; \
        apt-get update \
        && apt-get install -y --no-install-recommends \
            ca-certificates \
            curl \
            dirmngr \
            node-less \
            vim supervisor \
            build-essential \
            python-dev \
            python-setuptools \
            librsync-dev \
            telnet \
            libxml2-dev libxmlsec1-dev \
            git ssh-client \
#            python-gevent \
#            python-ldap \
#            python-pip \
#            python-qrcode \
#            python-renderpm \
#            python-support \
#            python-vobject \
#            python-watchdog \
        && curl -o wkhtmltox.deb -sSL https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.2.1/wkhtmltox-0.12.2.1_linux-jessie-amd64.deb \
        && echo 'c81fffae4c0914f95fb12e047a72edda5042b1c6 wkhtmltox.deb' | sha1sum -c - \
        && dpkg --force-depends -i wkhtmltox.deb \
        && apt-get -y install -f --no-install-recommends \
        && easy_install pip \
        && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false -o APT::AutoRemove::SuggestsImportant=false npm \
        && rm -rf /var/lib/apt/lists/*
#        && pip install psycogreen==1.0

#RUN curl -L -o wkhtmltopdf.tar.xz https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.3/wkhtmltox-0.12.3_linux-generic-amd64.tar.xz \
#        && tar -xf wkhtmltopdf.tar.xz \
#        && mv wkhtmltox/bin/wkhtmltopdf /usr/local/bin/wkhtmltopdf \
#        && chmod +x /usr/local/bin/wkhtmltopdf

ENV VIRTUAL_ENV=/opt/venv
RUN /usr/local/bin/pip install --no-cache-dir virtualenv \
    && /usr/bin/python2 -m virtualenv --python=/usr/bin/python2 $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./odoo.conf /etc/odoo/
COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY ./entrypoint.sh /entrypoint.sh

# install latest postgresql-client
RUN set -x; \
        echo 'deb http://apt.postgresql.org/pub/repos/apt/ jessie-pgdg main' > etc/apt/sources.list.d/pgdg.list \
        && export GNUPGHOME="$(mktemp -d)" \
        && repokey='B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8' \
        && gpg --batch --keyserver keyserver.ubuntu.com --recv-keys "${repokey}" \
        && gpg --armor --export "${repokey}" | apt-key add - \
        && rm -rf "$GNUPGHOME" \
        && apt-get update  \
        && apt-get install -y postgresql-client \
        && rm -rf /var/lib/apt/lists/*

# Mount /var/lib/odoo to allow restoring filestore and /opt/odoo for users addons
RUN mkdir -p /opt/odoo && mkdir -p /var/log/odoo && mkdir -p /var/lib/odoo/.local/share/Odoo/filestore/ && mkdir -p /var/lib/odoo/.local/share/Odoo/sessions/ \
        && useradd -m -d /opt/odoo -U -r -s /bin/bash odoo \
        && chown odoo:odoo /etc/odoo/odoo.conf \
        && chown -R odoo:odoo /opt/odoo && chown -R odoo:odoo /var/log/odoo && chown -R odoo:odoo /var/lib/odoo

COPY ./ssh /root/.ssh
RUN chmod 0600 /root/.ssh/*
# COPY ./requirements.txt /opt/odoo/requirements.txt
# RUN /opt/venv/bin/pip2 install -r /opt/odoo/requirements.txt && rm /opt/odoo/requirements.txt

# /etc/odoo for config and log files
VOLUME ["/var/lib/odoo/.local/share/Odoo/filestore", "/opt/odoo", "/opt/venv"]

# Expose Odoo services
EXPOSE 8069 8071

# Set the default config file
ENV ODOO_RC /etc/odoo/odoo.conf

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]