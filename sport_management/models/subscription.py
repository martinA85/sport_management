from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


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
        ('waiting', 'Waiting'),
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
        # self.email_subscription()
        # _logger.info(self.email_subscription())

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

    @api.multi
    def email_subscription(self):
        _logger.info('email_subscription.in')
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
            _logger.info('email_subscription.try.compose_form_id : ')
            _logger.info(compose_form_id)
        except ValueError:
            _logger.info('email_subscription.except')
            compose_form_id = False

        template_id = self.env['mail.template'].search([
            ('name', '=', 'sport.subscription.email_subscription')
        ],
            limit=1
        )

        ctx = dict()
        ctx.update({
            'default_model': 'sport.subscription',
            'default_res_id': False,
            'default_use_template': True,
            'default_template_id': template_id.id or False,
            'default_composition_mode': 'comment',
            'skip_notification': True,
        })

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
