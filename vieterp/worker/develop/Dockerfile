FROM gcr.io/<PROJECT>/odoo:<BRANCH>-<SHA>
LABEL maintainer="Sang <sang@vieterp.net>"

RUN rm /etc/odoo/odoo.conf && rm /etc/supervisor/conf.d/supervisord.conf

COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY ./odoo.conf /etc/odoo/odoo.conf

RUN chown odoo:odoo /etc/odoo/odoo.conf

# /etc/odoo for config and log files
VOLUME ["/var/lib/odoo/.local/share/Odoo/filestore", "/opt/venv"]

# Expose Odoo services
EXPOSE 8069 8071

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]