from odoo import api, fields, models


class SportCard(models.Model):
    _name = 'sport.sport_card'
    _description = 'Sport card'

    name = fields.Char(string='Name')
    barcode = fields.Char(string='Barcode', copy=False, oldname='ean13')
    validity = fields.Datetime()
    account_id = fields.Many2one('sport.account')
    client_id = fields.Many2one('res.partner')

    def _scan_card(self):
        pass
