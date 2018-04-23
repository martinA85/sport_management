from odoo import api, fields, models

class SubscriptionWizard(models.TransientModel):
    _name="sport.sub_wizard"

    client_id = fields.Many2one('res.partner')
    session_id = fields.Many2one('sport.session')
    sub_date = fields.Datetime()

    def create_subscription(self):
        pass

