from odoo import api, fields, models
import logging, json
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class Session(models.Model):
    _name = 'sport.session'
    _description = 'New Description'

    name = fields.Char(string='Name')
    course_id = fields.Many2one('sport.course', string="Course")
    start_date = fields.Datetime(string="Start date")
    end_date = fields.Datetime(string="End date")
    coach_id = fields.Many2one('res.partner', string="Coach")
    attendee_count = fields.Integer(String="Attendee number", compute="_compute_attendee_count")
    subscription_ids = fields.One2many('sport.subscription', 'session_id')
    waiting_attendee_count = fields.Integer(String="Waiting attendee count", compute="_compute_waiting_attendee_count")
    status = fields.Selection(string='status', required=False,
                              selection=[('done', 'Done'), ('cancel', 'Canceled'), ('valid', 'Valid')], default="valid")
    day = fields.Char(String="Days", compute="_compute_session_day")
    color = fields.Char(compute="_compute_color")

    @api.depends('subscription_ids')
    def _compute_attendee_count(self):
        for session in self:
            session.attendee_count = 0
            for sub in session.subscription_ids:
                if sub.status == 'sub':
                    session.attendee_count += 1

    @api.depends('subscription_ids')
    def _compute_waiting_attendee_count(self):
        _logger.info('_compute_waiting_attendee_count')
        for session in self:
            session.attendee_count = 0
            for sub in session.subscription_ids:
                if sub.status == 'waiting':
                    session.waiting_attendee_count += 1

    @api.onchange('start_date')
    def _compute_session_day(self):
        for session in self:
            if session.start_date:
                date = datetime.strptime(session.start_date, '%Y-%m-%d %H:%M:%S')

    def search_all_session(self):
        return self.env['sport.session'].search([('status', 'like', 'valid')])

    @api.depends("course_id")
    def _compute_color(self):
        for session in self:
            session.color = session.course_id.color

    # Auto complet end_date in form field
    @api.onchange('start_date')
    def _compute_end_date(self):
        for session in self:
            if session.course_id.lenght:
                length = datetime.strptime(session.course_id.lenght, '%H:%M').time()
                date = datetime.strptime(session.start_date, '%Y-%m-%d %H:%M:%S')
                session.end_date = date + timedelta(hours=length.hour, seconds=length.second)

    # Print calendar to PDF
    @api.multi
    def print_calendar(self):
        print('Print pdf')

    # Returns a json contains all needed sessions data's to build web calendar.
    # @api.returns('sport.session')
    @api.model
    def search_session_and_subscription(self):
        sessions = []
        for session in self.search([]):
            subscriptions = []
            for subscription in session.subscription_ids:   
                subscriptions.append({"id": subscription.id,
                                      "client_id": subscription.client_id.id,
                                      "sub_date": subscription.sub_date,
                                      "status": subscription.status
                                      })

            sessions.append({"id": session.id,
                             "title": session.name,
                             "start": session.start_date,
                             "end": session.end_date,
                             "color": session.color,
                             "coach": session.coach_id.name,
                             "subscriptions": subscriptions
                             })

        return json.dumps(sessions)

    @api.onchange('attendee_count')
    def _send_mail_on_unsubscribe(self):
        for session in self:
            if session.attendee_count < session.course_id.max_attendee:
                if session.waiting_attendee_count > 0:
                    pass
                    # waiting_attendee_list = session.subscription_ids.