# -*- coding: utf-8 -*-
from odoo import http

# class SportManagement(http.Controller):
#     @http.route('/sport_management/sport_management/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sport_management/sport_management/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sport_management.listing', {
#             'root': '/sport_management/sport_management',
#             'objects': http.request.env['sport_management.sport_management'].search([]),
#         })

#     @http.route('/sport_management/sport_management/objects/<model("sport_management.sport_management"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sport_management.object', {
#             'object': obj
#         })