FROM odoo:15 AS odoo_pattern

USER root

RUN apt-get update && apt-get -y install locales locales-all && locale-gen ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU:en
ENV LC_ALL ru_RU.UTF-8

COPY configs/odoo/ etc/odoo/


CMD ["odoo"]
