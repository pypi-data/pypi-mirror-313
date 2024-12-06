# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Footer Extra Info Base",
    "summary": "Base module to include extra info in PDF footer",
    "version": "16.0.1.0.0",
    "category": "Report",
    "website": "https://github.com/sygel-technology/sy-web",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "web",
    ],
    "data": [
        "views/report_templates.xml",
    ],
}
