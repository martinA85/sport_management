from odoo import api, fields, models
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)

class SportBadge(models.Model):
    _name = 'sport.badge'
    _description = 'Sport Badge'

    name = fields.Char(string='Name')
    barcode = fields.Char(string='Barcode', copy=False, oldname='ean13')
    validity = fields.Datetime(default=datetime.now() + timedelta(days=365))
    account_id = fields.Many2one('sport.account')
    client_id = fields.Many2one('res.partner')
    credit_count = fields.Integer(compute="_compute_credit_count")


    @api.depends('account_id')
    @api.onchange('account_id')
    def _compute_credit_count(self):
        for badge in self:
            badge.credit_count = badge.account_id.credit_count

    def scan_card(self):
        message = ""
        for badge in self:
            client = badge.client_id
            now = datetime.now()
            hour = now + timedelta(hours=24)
            lst_subscriptions = client.sub_ids

            for sub in lst_subscriptions:
                date = datetime.strptime(sub.session_id.start_date, '%Y-%m-%d %H:%M:%S')

                _logger.info(date <= hour)
                if date >= now and date <= hour:
                    if sub.state == "valid":
                        message = 1
                    else :
                        if badge.credit_count > 0:
                            badge.account_id.remove_credit()
                            message = 0
                            sub.state = "valid"
                        else:
                            message = 2
                else:
                    message = 3
            return message
                
                