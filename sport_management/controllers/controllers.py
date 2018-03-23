# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging
import json

_logger = logging.getLogger(__name__)
class SportController(http.Controller):
    
    @http.route('/sport/sessions',auth='public', website=True, type="http")
    def index(self,**kw):

        env = request.env
        return http.request.render('sport_management.sport_calendar_view')



    @http.route('/sport/get_session',auth='public', website=True, type="json")
    def get_session(self,**kw):
        env = request.env

        lst_start = datetime.now()
        month = relativedelta(months=1)
        lst_end = lst_start + month

        sessions = env['sport.session'].search([('status','like','valid'),('start_date','<=', str(lst_start)),('end_date','<=', str(lst_end))])

        data = '{'
        for session in sessions:
            data += str(session.serialize_json())

        data += '}'

        return json.dumps(data)
            

    @http.route('/sport/test', auth='public', website=True, type="json")
    def testJson(self,**kw):
        
        env = request.env
        sessions = env['sport.session'].search([('status','like','valid')])
        return {"nom" : "Allimonier", "prenom" : "Martin", "att" : "est un f****** Genie"}