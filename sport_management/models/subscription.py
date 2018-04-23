from odoo import api, fields, models


class Subscription(models.Model):
    _name = 'sport.subscription'
    _description = 'New Description'

    name = fields.Char(string='Name')
    client_id = fields.Many2one('res.partner')
    session_id = fields.Many2one('sport.session')
    sub_date = fields.Datetime()
    state = fields.Selection([
        ('sub', 'Sub'),
        ('valid', 'Valid'),
        ('canceled', 'Canceled'),
        ('waiting', 'Wainting'),
        ('absent', 'Absent'),
    ], string="Subscription state", default='sub')
    

    def set_present(self):
        for sub in self:
            sub.state = 'valid'

    @api.depends('state')
    def _on_change_state(self):
        for subscription in self:
            print(subscription.session_id.attendee_count)

    @api.one
    def subscribe(self):
        self.session_id.attendee_count
        self.write({'state': 'sub'})

    @api.one
    def valid(self):
        self.write({'state': 'valid'})

    @api.one
    def cancel(self):
        self.write({'state': 'canceled'})

    @api.one
    def waiting(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'waiting'})
        return True

    @api.one
    def absent(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'absent'})
        return True

