from odoo import api, fields, models
import logging


_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    credit_ids = fields.One2many('sport.credit', 'client_id')
    badge_ids = fields.One2many('sport.badge','client_id')
    sub_ids = fields.One2many('sport.subscription','client_id')
    credit_count = fields.Integer(compute="_compute_credit_count")
    badge_count = fields.Integer(compute="_compute_badge_cout")
    #is_coach = fields.Boolean(default=False)

    @api.depends('badge_ids')
    def _compute_credit_count(self):
        _logger.info('COMPUTE CREDIT COUNT PARTNER')
        for partner in self:
            partner.credit_count = 0
            for badge in partner.badge_ids:
                _logger.info(badge.credit_count)
                partner.credit_count += badge.credit_count

    
    @api.depends('badge_ids')
    def _compute_badge_count(self):
        for partner in self:
            partner.badge_count = 0
            for badge in partner.badge_ids:
                partner.badge_count += 1

