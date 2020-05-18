FROM vieterp/odoo:tuanhuy
MAINTAINER Sang <sang@vieterp.net>

COPY ./supervisord.conf* /etc/supervisor/conf.d/supervisord.conf

# Expose Odoo services
EXPOSE 8069 8071

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]