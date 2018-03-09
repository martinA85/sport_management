from odoo import api, fields, models

#credit model, use to keep history of credit on the account
class SportCredit(models.Model):
    _name = 'sport.credit'
    _description = 'New Description'

    name = fields.Char(string='Name')
    type_id = fields.Many2one('sport.type_course')
    account_id = fields.Many2one('sport.account')
    date_valid = fields.Datetime()
    number = fields.Integer()
    total = fields.Float(compute='_compute_total')
    quotation_ids = fields.One2many('sale.order', 'credit_id')
    status = fields.Selection([
        ('valid', 'Valid'),
        ('invalid', 'Invalid'),
    ], string="Credit status", default="valid")

    
    @api.depends('number', 'type_id')
    def _compute_total(self):
        for credit in self:
            credit.total = credit.number * credit.type_id.price

    @api.depends('status')
    def _set_invalid(self):
        for credit in self:
            credit.status = "invalid"


    @api.depends('status')
    def _toogle_validity(self):
        for credit in self:
            if credit.status == "invalid":
                credit.status = "valid"
            else:
                credit.status = "invalid"
