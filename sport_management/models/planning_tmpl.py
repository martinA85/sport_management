from odoo import api, fields, models
import logging

class PlanningTmpl(models.Model):
    _name = 'sport.planning_tmpl'
    _description = 'Planning Template'

    name = fields.Char(string="Nom")
    session_tmpl_ids = fields.One2many('sport.session_tmpl', 'planning_tmpl_id')