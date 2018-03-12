from odoo import api, fields, models


class TypeCourse(models.Model):
    _name = 'sport.type_course'
    _description = 'New Description'

    name = fields.Char(string='Name')
    price = fields.Float(string='Course price')
    product_id = fields.Many2one(comodel_name='product.template', string='Product for quotation', required=False)
    
