from odoo import api, fields, models


class SportCard(models.Model):
    _name = 'sport.sport_card'
    _description = 'Sport card'

    name = fields.Char(string='Name')
    barcode = fields.Char(string='Barcode', copy=False, oldname='ean13')
    validity = fields.Datetime()
    account_id = fields.Many2one('sport.account')
    client_id = fields.Many2one('res.partner')
    credit_count = fields.Integer(compute="_compute_credit_count")


    @api.depends('account_id')
    @api.onchange('account_id')
    def _compute_credit_count(self):
        for card in self:
            card.credit_count = card.account_id.credit_count

    def _scan_card(self):
        pass