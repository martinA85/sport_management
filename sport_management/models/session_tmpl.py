from odoo import api, fields, models
from datetime import datetime
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)
class SessionTmpl(models.Model):
    _name = 'sport.session_tmpl'
    _description = 'Session Template'


    name = fields.Char()
    start_hour = fields.Char(string="Heure de debut : HH:MM")
    day = fields.Selection(string="Jour",
        selection=[('0', 'Lundi'), ('1', 'Mardi'), ('2', 'Mercredi'), ('3', 'Jeudi'), ('4', 'Vendredi'), ('5', 'Samedi') ])
    room = fields.Selection(string='Lieux', required=False,
                             selection=[('sport', 'Salle Sport'), ('pool', 'Piscine'), ('cardio', 'Salle Cardio')])
    coach_id = fields.Many2one('res.partner', string="Coach")
    activity_id = fields.Many2one('sport.activity', string="Activitées") 
    planning_tmpl_id = fields.Many2one('sport.planning_tmpl')