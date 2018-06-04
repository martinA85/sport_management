from odoo import api, fields, models
import logging

class SessionTmpl(models.Model):
    _name = 'sport.session_tmpl'
    _description = 'Session Template'


    name = fields.Char()
    start_hour = fields.Char(string="Heure de debut : HH:MM")
    end_hour = fields.Char(string="Heure de fin : HH:MM")
    day = fields.Selection(string="Jour",
        selection=[('lun', 'Lundi'), ('mar', 'Mardi'), ('mer', 'Mercredi'), ('jeu', 'Jeudi'), ('ven', 'Vendredi'), ('sam', 'Samedi') ])
    room = fields.Selection(string='Lieux', required=False,
                             selection=[('sport', 'Salle Sport'), ('pool', 'Piscine'), ('cardio', 'Salle Cardio')])
    coach_id = fields.Many2one('res.partner', string="Coach")
    activity_id = fields.Many2one('sport.activity', string="Activitées") 
    planning_tmpl_id = fields.Many2one('sport.planning_tmpl')