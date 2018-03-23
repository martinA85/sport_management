from odoo import api, fields, models


class Course(models.Model):
    _name = 'sport.course'
    _description = 'New Description'

    name = fields.Char(string='Name')
    lenght = fields.Char(String="cours lenght (HH:MM)")
    max_attendee = fields.Integer(String="Maximum attendee number")
    course_type_id = fields.Many2one('sport.type_course', string="Course Type")
