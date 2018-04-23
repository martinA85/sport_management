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

    # function to change state of subscription
    @api.one
    def subscribe(self):
        self.session_id.attendee_count
        self.write({'state': 'sub'})
        self.email_subscription()

    # function to change state of subscription
    @api.one
    def valid(self):
        self.write({'state': 'valid'})
        self.email_validation()

    # function to change state of subscription
    @api.one
    def cancel(self):
        self.write({'state': 'canceled'})
        self.email_cancellation()

    # function to change state of subscription
    @api.one
    def waiting(self):
        self.write({'state': 'waiting'})
        self.email_waiting()

    # function to change state of subscription
    @api.one
    def absent(self):
        self.write({'state': 'absent'})
        self.email_absent()

    # function to prepare an absent email, it call send_mail() function to create and send it
    @api.multi
    def email_subscription(self):
        subject = 'Your subscription has been registered'
        email_to = self.client_id.email
        body = '<p>Dear ' + self.client_id.name + ', <br /> <br />  You has been registered to the ' \
               + self.session_id.name + ' session at ' + self.session_id.start_date + ' for ' \
               + self.session_id.course_id.length + '.</p>'

        self.send_mail(subject, email_to, body)

    # function to prepare an absent email, it call send_mail() function to create and send it
    @api.multi
    def email_validation(self):
        subject = 'Thank you !'
        email_to = self.client_id.email
        body = '<p>Dear ' + self.client_id.name + ', <br /><br />' + \
               'You has been participated to the ' + self.session_id.name + \
               ' session at ' + self.session_id.start_date + ' for ' \
               + str(self.session_id.course_id.length) + '. <br /> <br />' + \
               'Thank you for your participation and see you later !</p>'

        self.send_mail(subject, email_to, body)

    # function to prepare an absent email, it call send_mail() function to create and send it
    @api.multi
    def email_waiting(self):
        subject = 'You has been registered in waiting list'
        email_to = self.client_id.email
        body = '<p>Dear ' + self.client_id.name + ', <br /><br />' + \
               'You has been registered in waiting list to the ' + self.session_id.name + \
               ' session at ' + self.session_id.start_date + ' for ' \
               + str(self.session_id.course_id.length) + '. <br /> <br />' + \
               'If a place becomes vacant, an email will be sent to inform you.</p>'

        self.send_mail(subject, email_to, body)

    # function to prepare an absent email, it call send_mail() function to create and send it
    @api.multi
    def email_cancellation(self):
        subject = 'You has been canceled your registration'
        email_to = self.client_id.email
        body = '<p>Dear ' + self.client_id.name + ', <br /><br />' + \
               'You has been canceled your registration to the ' + self.session_id.name + \
               ' session at ' + self.session_id.start_date + ' for ' \
               + str(self.session_id.course_id.length) + '.</p>'

        self.send_mail(subject, email_to, body)

    # function to prepare an absent email, it call send_mail() function to create and send it
    @api.multi
    def email_absent(self):
        subject = 'You has been absent.'
        email_to = self.client_id.email
        body = '<p>Dear ' + self.client_id.name + ', <br /><br />' + \
               'You were absent at the ' + self.session_id.name + \
               ' session at ' + self.session_id.start_date + ' for ' \
               + str(self.session_id.course_id.length) + '.</p>'

        self.send_mail(subject, email_to, body)

    # function called by over function to send create and email
    @api.multi
    def send_mail(self, subject, email_to, body):
        mail_pool = self.env['mail.mail']

        values = {}
        values.update({'subject': subject})
        values.update({'email_to': email_to})
        values.update({'body_html': body})

        msg_id = mail_pool.create(values)

        if msg_id:
            mail_pool.send([msg_id])
