FROM odoo:19.0

# Copier le module dans le dossier extra-addons
COPY . /mnt/extra-addons/puerto_transit/

# S'assurer que les droits sont corrects
USER root
RUN chown -R odoo:odoo /mnt/extra-addons/puerto_transit
USER odoo
