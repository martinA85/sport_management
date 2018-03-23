# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from datetime import datetime
import logging
import json

_logger = logging.getLogger(__name__)
class SportController(http.Controller):
    
    # controller that render our calendar page
    @http.route('/sport/sessions',auth='public', website=True, type="http")
    def index(self,**kw):

        env = request.env
        return http.request.render('sport_management.sport_calendar_view')