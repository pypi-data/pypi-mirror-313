from odoo import api, fields, models
from odoo.tools.translate import _


class CrmLead(models.Model):
    _inherit = "crm.lead"\

    metadata_line_ids = fields.One2many(
        'crm.lead.metadata.line', 'crm_lead_id', string=_("Metadata"))
