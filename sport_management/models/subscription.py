from odoo import api, fields, models


class Subscription(models.Model):
    _name = 'sport.subscription'
    _description = 'New Description'

    name = fields.Char(string='Name')
    client_id = fields.Many2one('res.partner')
    session_id = fields.Many2one('sport.session')
    sub_date = fields.Datetime()
    status = fields.Selection([
        ('sub', 'Sub'),
        ('valid', 'Valid'),
        ('canceled', 'Canceled'),
        ('waiting', 'Wainting'),
        ('absent', 'Absent'),
    ], string="Credit status", default="valid")

    def set_present(self):
        for sub in self:
            sub.status = 'valid'

    
