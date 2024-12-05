# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    company_group_id = fields.Many2one(
        related="partner_id.company_group_id", store=True
    )
