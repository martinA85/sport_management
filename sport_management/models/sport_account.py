from odoo import api, fields, models


class SportAccount(models.Model):
    _name = 'sport.account'
    _description = 'Seance account for sport module'

    name = fields.Char(string='Name')
    client_id = fields.Many2one('res.partner')
    date_create = fields.Datetime(string = 'Creation date', default=fields.Datetime.now)
    credit_ids = fields.One2many('sport.credit', 'account_id', string="account's credit list")
    card_ids = fields.One2many('sport.sport_card', 'account_id', string="account's cards list")


    def _add_credit(self):
        pass

    def _remove_credit(self):
        pass
