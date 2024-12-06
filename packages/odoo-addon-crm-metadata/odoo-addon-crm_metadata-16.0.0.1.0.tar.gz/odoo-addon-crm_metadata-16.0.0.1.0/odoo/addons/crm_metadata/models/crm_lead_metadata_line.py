from odoo import models, fields
from odoo.tools.translate import _


class CrmLeadMetadataLine(models.Model):
    _name = 'crm.lead.metadata.line'
    _inherit = 'metadata.line'

    crm_lead_id = fields.Many2one(
        'crm.lead', string=_("Lead"), ondelete='cascade')
