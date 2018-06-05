from odoo import api, fields, models
import logging, json
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class Session(models.Model):
    _name = 'sport.session'
    _description = 'Sport session'

    name = fields.Char(string='Name')
    activity_id = fields.Many2one('sport.activity', string="Activitées")
    start_date = fields.Datetime(string="Start date")
    end_date = fields.Datetime(string="End date")
    coach_id = fields.Many2one('res.partner', string="Coach")
    attendee_count = fields.Integer(String="Attendee number", compute="_compute_attendee_count")
    subscription_ids = fields.One2many('sport.subscription', 'session_id')
    waiting_attendee_count = fields.Integer(String="Waiting attendee count", compute="_compute_waiting_attendee_count")
    canceled_attendee_count = fields.Integer(String="Canceled attendee count",
                                             compute="_compute_canceled_attendee_count")
    state = fields.Selection(string='state', required=False,
                             selection=[('done', 'Done'), ('cancel', 'Canceled'), ('valid', 'Valid')], default="valid")
    day = fields.Char(String="Days", compute="_compute_session_day")
    color = fields.Char(compute="_compute_color")
    max_attendee = fields.Integer(String="Maximum attendee number", compute="_compute_max_attendee")
    remaining_places = fields.Integer(String="Place restante", compute="_compute_remaining_places")
    room = fields.Selection(string='Lieux', required=False,
                             selection=[('sport', 'Salle Sport'), ('pool', 'Piscine'), ('cardio', 'Salle Cardio')])

    @api.onchange('activity_id')
    def set_room(self):
        _logger.info("change_room")
        for session in self:
            _logger.info(session.activity_id.room)
            session.room = session.activity_id.room
            _logger.info(session.room)

    @api.depends('subscription_ids')
    def _compute_attendee_count(self):
        for session in self:
            session.attendee_count = 0
            for sub in session.subscription_ids:
                if sub.state == 'sub':
                    session.attendee_count += 1

    @api.depends('subscription_ids')
    def _compute_waiting_attendee_count(self):
        for session in self:
            session.waiting_attendee_count = 0
            for sub in session.subscription_ids:
                if sub.state == 'waiting':
                    session.waiting_attendee_count += 1

    @api.depends('subscription_ids')
    def _compute_canceled_attendee_count(self):
        for session in self:
            session.canceled_attendee_count = 0
            for sub in session.subscription_ids:
                if sub.state == 'canceled':
                    session.canceled_attendee_count += 1

    @api.onchange('start_date')
    def _compute_session_day(self):
        for session in self:
            if session.start_date:
                date = datetime.strptime(session.start_date, '%Y-%m-%d %H:%M:%S')

    def search_all_session(self):
        return self.env['sport.session'].search([('state', 'like', 'valid')])

    @api.depends("activity_id")
    def _compute_color(self):
        for session in self:
            session.color = session.activity_id.color

    # Auto complet end_date in form field
    @api.onchange('start_date')
    def _compute_end_date(self):
        for session in self:
            if session.activity_id.length:
                length = datetime.strptime(session.activity_id.length, '%H:%M').time()
                date = datetime.strptime(session.start_date, '%Y-%m-%d %H:%M:%S')
                session.end_date = date + timedelta(hours=length.hour, minutes=length.minute)

    # Print calendar to PDF
    @api.multi
    def print_calendar(self):
        print('Print pdf')

    # Returns a json contains all needed sessions data's to build web calendar.
    @api.model
    def search_session_and_subscription(self):
        sessions = []
        for session in self.search([]):
            subscriptions = []
            for subscription in session.subscription_ids:
                subscriptions.append({"id": subscription.id,
                                      "client_id": subscription.client_id.id,
                                      "sub_date": subscription.sub_date,
                                      "state": subscription.state
                                      })

            sessions.append({"id": session.id,
                             "title": session.name,
                             "activity_id": session.activity_id.id,
                             "activity_name": session.activity_id.name,
                             "start": session.start_date,
                             "end": session.end_date,
                             "color": session.color,
                             "coach": session.coach_id.name,
                             "subscriptions": subscriptions
                             })

        return json.dumps(sessions)

    def _compute_max_attendee(self):
        for session in self:
            self.max_attendee = session.activity_id.max_attendee
        
    @api.onchange('activity_id')
    def _update_session_end_date(self):
        for session in self:
            if session.activity_id.length != False and session.start_date != False:
                length = datetime.strptime(session.activity_id.length, '%H:%M').time()
                date = datetime.strptime(session.start_date, '%Y-%m-%d %H:%M:%S')
                session.end_date = date + timedelta(hours=length.hour, minutes=length.minute)

    def _compute_remaining_places(self):
        for session in self:
            session.remaining_places = session.activity_id.max_attendee - session.attendee_count

    #called by cron, look for evry session started 1hour ago and set absent evry one who was not there
    def update_absent_credit_count(self):
        _logger.info("update_absent_credit_count")
        now = datetime.now()
        #our time minus 1 hour
        now_minus_1 = now + timedelta(hours=-1)
        _logger.info(now_minus_1)
        #getting all session statrted 1hour ago
        sessions = self.env['sport.session'].search([('start_date', '<', now.strftime("%Y-%m-%d %H:%M:%S")),('start_date','>', now_minus_1.strftime("%Y-%m-%d %H:%M:%S"))])
        for session in sessions:
            #getting evry subscription of this session with status 'sub'
            absent_ids = self.env['sport.subscription'].search([('session_id','=',session.id),('state','=','sub')])
            for absent in absent_ids:
                #updating status
                absent.state = "absent"
                #getting the older credit
                credit_id = self.env['sport.credit'].search([('account_id', '=', absent.client_id.account_id.id),('type_id','=',session.activity_id.course_type_id.id),('number_actual','>', 0)], order='date_buy asc',limit=1)
                credit_id.number_actual = credit_id.number_actual - 1
                absent.scan_date = datetime.now()
                absent.unit_price = credit_id.product_id.lst_price / credit_id.product_id.qty_course
