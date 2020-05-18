FROM vieterp/odoo:10.0
MAINTAINER Sang <sang@vieterp.net>

USER root

ARG CI_COMMIT_REF_NAME=production

# Copy entrypoint script and Odoo configuration file
COPY ./config/production/odoo.conf /etc/odoo/odoo.conf
COPY ./config/${CI_COMMIT_REF_NAME}/odoo.* /etc/odoo/

RUN chown odoo:odoo /etc/odoo/odoo.conf
COPY ./config/production/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Mount /opt/odoo/odoo for customize folders
RUN rm -rf /usr/lib/python2.7/dist-packages/odoo
COPY ./odoo /opt/odoo/odoo
COPY ./requirements.txt /opt/odoo/requirements.txt
RUN /usr/local/bin/pip install -r /opt/odoo/requirements.txt && rm /opt/odoo/requirements.txt
RUN chown -R odoo. /opt/odoo

# Expose Odoo services
EXPOSE 8069 8071

# Set the default config file
ENV ODOO_RC /etc/odoo/odoo.conf

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]