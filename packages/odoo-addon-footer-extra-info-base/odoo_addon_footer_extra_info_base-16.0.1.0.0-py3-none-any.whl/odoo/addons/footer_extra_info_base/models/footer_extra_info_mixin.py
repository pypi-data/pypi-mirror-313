# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FooterExtraInfoMixin(models.AbstractModel):
    _name = "footer.extra.info.mixin"
    _description = "Footer Extra Info Mixin"

    footer_extra_info = fields.Text(compute="_compute_footer_extra_info")

    def _compute_footer_extra_info(self):
        raise NotImplementedError()
