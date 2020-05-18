FROM gcr.io/<PROJECT>/odoo:10.7
LABEL maintainer="Sang <sang@vieterp.net>"

RUN rm /etc/odoo/odoo.conf && rm /etc/supervisor/conf.d/supervisord.conf

COPY ./odoo /opt/odoo/odoo
COPY ./config/docker/vieterp/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY ./config/docker/vieterp/odoo.conf /etc/odoo/odoo.conf

RUN chown odoo:odoo /etc/odoo/odoo.conf

# /etc/odoo for config and log files
VOLUME ["/var/lib/odoo/.local/share/Odoo/filestore", "/opt/venv"]

# Expose Odoo services
EXPOSE 8069 8071

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]