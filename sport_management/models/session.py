from odoo import api, fields, models
import logging
from datetime import datetime

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
    subscription_ids = fields.One2many('sport.subscription','session_id')
    waiting_attendee_count = fields.Integer(String="Waiting attendee count", compute="_compute_waiting_attendee_count")
    status = fields.Selection(string='status', required=False, selection=[('done', 'Done'), ('cancel', 'Canceled'), ('valid','Valid')], default="valid")
    day = fields.Char(String="Days", compute="_compute_session_day")
    color = fields.Char(compute="_compute_color")
    

    @api.depends('subscription_ids')
    def _compute_attendee_count(self):
        for session in self:
            session.attendee_count = 0
            for sub in session.subscription_ids:
                if sub.status == 'valid':
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
            date = datetime.strptime(session.start_date, '%Y-%m-%d %H:%M:%S')


    def search_all_session(self):
        return self.env['sport.session'].search([('status','like','valid')])

    @api.depends("course_id")
    def _compute_color(self):
        for session in self:
            session.color = session.course_id.color