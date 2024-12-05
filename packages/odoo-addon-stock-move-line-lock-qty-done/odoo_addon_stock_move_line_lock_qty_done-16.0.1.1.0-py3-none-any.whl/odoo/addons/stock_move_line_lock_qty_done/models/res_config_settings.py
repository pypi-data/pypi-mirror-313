# Copyright 2024 Quartile
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    lock_qty_done = fields.Boolean(
        related="company_id.lock_qty_done",
        readonly=False,
        string="Limit Updates to Done Quantity After Validation",
        help="Only users in the 'Can Edit Done Quantity for Done Stock Moves' group"
        " are allowed to edit the 'done' quantity for validated transfer.",
    )
