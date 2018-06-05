from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class SubscriptionWizard(models.TransientModel):
    _name="sport.subscription_wizard"

    def _default_session(self):
        return self.env['sport.session'].browse(self._context.get('active_ids'))

    client_ids = fields.Many2many(comodel_name='res.partner', string='Clients à inscrire')
    session_ids = fields.Many2many(comodel_name='sport.session', default=_default_session)

    def subscribe_client(self):
        _logger.info("wizard")
        for wizard in self:
            for session in wizard.session_ids:
                for client in wizard.client_ids:
                    vals = {
                        'client_id':client.id,
                        'session_id':session.id,
                    }    
                    self.env['sport.subscription'].create(vals)
