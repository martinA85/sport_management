from odoo import api, fields, models
from datetime import datetime
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)
class PlanningTmpl(models.Model):
    _name = 'sport.planning_tmpl'
    _description = 'Planning Template'

    name = fields.Char(string="Nom")
    session_tmpl_ids = fields.One2many('sport.session_tmpl', 'planning_tmpl_id')

    #funtion called by cron to create the planning for X week later
    def generate_planning(self):
        for planning in self:
            now = datetime.now()
            #Week where the planning must be created
            next_week = now + timedelta(weeks=1)
            #Mondy of this week
            monday_date = next_week + timedelta(days=-next_week.weekday())
            #generate for monday
            planning._generate_one_day(monday_date)
            #generate for each day of the week
            for i in range(1,5):
                planning._generate_one_day(monday_date + timedelta(days=i))
        
    #Function that generate the planning for a day
    def _generate_one_day(self, day_date):
        for planning in self:
            session_tmpl_ids = self.env['sport.session_tmpl'].search([['planning_tmpl_id','=',planning.id],['day','=',day_date.weekday()]])
            for session in session_tmpl_ids:
                start_date = day_date
                hour_session = datetime.strptime(session.start_hour, '%H:%M')
                start_date = day_date.replace(hour=hour_session.hour, minute=hour_session.minute, second=0, microsecond=0)
                _logger.info(start_date)
                vals = {
                    "name" : session.activity_id.name,
                    "activity_id" : session.activity_id.id,
                    "start_date" : start_date,
                    "room" : session.room,
                    "coach_id" : session.coach_id.id,
                }
                try:
                    new_session = self.env["sport.session"].create(vals)
                except Exception:
                    _logging.info("error")
                new_session._compute_end_date()