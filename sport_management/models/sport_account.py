from odoo import api, fields, models

class SportAccount(models.Model):
    _name = 'sport.account'
    _description = 'Seance account for sport module'

    name = fields.Char(string='Name')
    client_id = fields.Many2one('res.partner')
    date_create = fields.Datetime(string = 'Creation date', default=fields.Datetime.now)
    credit_ids = fields.One2many('sport.credit', 'account_id', string="account's credit list")
    card_ids = fields.One2many('sport.sport_card', 'account_id', string="account's cards list")
    credit_count = fields.Integer(compute="_compute_credit_count")
    card_count = fields.Integer(compute="_compute_card_count")
    active = fields.Boolean(default=True)

    def _add_credit(self):
        pass

    def _remove_credit(self):
        pass


    @api.depends('credit_ids')
    def _compute_credit_count(self):
        for account in self:
            account.credit_count = 0
            for credit in account.credit_ids:
                account.credit_count += credit.number

    def _compute_card_count(self):
        for account in self:
            account.card_count = 0
            for card in account.card_ids:
                account.card_count += 1

    @api.depends('active')
    def toogle_active(self):
        for account in self:
            if account.active == True:
                account.active = False
            else:
                account.active = True

    @api.multi
    def action_view_card(self):
        self.ensure_one()
        action = self.env.ref('sport_management.action_sport_card')
        cards_ids = self.with_context(active_test=False).card_ids.ids

        return{
            'name':action.name,
            'help':action.help,
            'type':action.type,
            'view_type':action.view_type,
            'view_mode':action.view_mode,
            'target':action.target,
            'context': "{'default_card_ids': " + str(cards_ids[0]) + "}",
            'res.model':action.res_model
        }