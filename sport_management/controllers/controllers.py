# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from datetime import datetime
import logging
import json
from pprint import pprint
_logger = logging.getLogger(__name__)


class SportController(http.Controller):

    # controller that render our calendar page
    @http.route('/sport/sessions', auth='public', website=True, type="http")
    def index(self, **kw):

        env = request.env
        return http.request.render('sport_management.sport_calendar_view')

    @http.route('/sport/sessions/isSubscribe', auth='user', website=True, type='json')
    def isSubscribe(self, **kw):
        cr, context, registry, uid = request.cr, request.context, request.registry, request.uid
        web_client_id = int(kw.get('user_id'))
        web_session_id = int(kw.get('session_id'))

        subscription = request.env['sport.subscription']

        subscription_ids = subscription.search([
            ['session_id','=',web_session_id],
            ['client_id','=',web_client_id]
        ])
        print(subscription_ids.session_id.id)

        return subscription_ids.session_id.id

    @http.route('/sport/sessions/subscribe', auth='user', website=True, type='json')
    def subscribe(self, **kw):
        cr, context, registry, uid = request.cr, request.context, request.registry, request.uid

        web_client_id = int(kw.get('user_id'))
        web_session_id = int(kw.get('session_id'))
        subscribed = False
        response = {'error': False, 'msg': []}

        # Get models
        subscription = request.env['sport.subscription']
        session = request.env['sport.session']

        # Search all subscription of web_client_id
        subscription_ids = subscription.search([
            ['client_id', '=', web_client_id]
        ])

        # Search session of web_session_id
        session_id = session.search([
            ['id', '=', web_session_id]
        ])


        # for each subscriptions of web_client_id
        for subscription_id in subscription_ids:

            # Go to the next loop if subscription is empty
            if not subscription_id.session_id.id:
                continue

            # If session is already subscribed, subscribed get the session subscription
            if subscription_id.session_id.id == web_session_id:
                subscribed = subscription_id
            else:
                # Format string to date
                session_start_date = datetime.strptime(session_id.start_date, '%Y-%m-%d %H:%M:%S')
                session_end_date = datetime.strptime(session_id.end_date, '%Y-%m-%d %H:%M:%S')
                sub_session_start_date = datetime.strptime(subscription_id.session_id.start_date, '%Y-%m-%d %H:%M:%S')
                sub_session_end_date = datetime.strptime(subscription_id.session_id.end_date, '%Y-%m-%d %H:%M:%S')

                # If sessions is not subscribed
                # and start_date of session in subscription is between start_date and end_date of the session subscribed
                # or end_date  of session in subscription is between start_date and end_date of the session subscribed
                # the session can't be subscribing.
                if (session_start_date >= sub_session_start_date and
                    session_start_date <= sub_session_end_date) or \
                        (session_end_date >= sub_session_start_date and
                         session_end_date <= sub_session_end_date):
                    response['error'] = True
                    response['msg'].append(['You already have session at this moment.'])

        # If there is not error
        if not response['error']:

            # If session is not subscribed
            if not subscribed:
                subscription.sudo().create({
                    'name': 'SportController.subscribe.create',
                    'client_id': web_client_id,
                    'session_id': web_session_id,
                    'sub_date': '01/01/2018 00:00:00',
                    'status': 'valid'
                })
                response['msg'].append(['Subscription registered'])
            else:
                subscribed.sudo().unlink()
                response['msg'].append(['Unsubscription registered'])

        return response
