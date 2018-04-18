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
            ['session_id', '=', web_session_id],
            ['client_id', '=', web_client_id]
        ])
        print(subscription_ids.session_id.id)

        return subscription_ids.session_id.id

    @http.route('/sport/sessions/subscribe', auth='user', website=True, type='json')
    def subscribe(self, **kw):
        cr, context, registry, uid = request.cr, request.context, request.registry, request.uid

        web_client_id = int(kw.get('user_id'))
        web_session_id = int(kw.get('session_id'))
        subscribed = False
        response = {'error': False, 'warning': False, 'msg': []}

        # Get models
        subscription = request.env['sport.subscription']
        session = request.env['sport.session']
        client = request.env['res.partner']

        client_id = client.search([
            ('id', '=', web_client_id)
        ])

        # Search all subscription of web_client_id
        subscription_ids = subscription.search([
            ('client_id', '=', client_id.id)
        ])

        # Search session of web_session_id
        session_id = session.search([
            ['id', '=', web_session_id]
        ])

        course_max_attendee = session_id.course_id.max_attendee
        session_subscriptions = session_id.attendee_count
        waiting_list = True

        # Check if the max attendee is full
        if course_max_attendee > session_subscriptions:
            waiting_list = False

        subscribed = self.already_subscribed(subscription_ids, session_id)

        # If session is not subscribed
        if not subscribed:
            if self.check_sessions_schedules(subscription_ids, session_id):
                if waiting_list:
                    self.create_subscription(subscription, client_id, session_id, 'waiting')
                    response['warning'] = True
                    response['msg'].append(['This session is full, your subscription is registered in waiting list'])
                else:
                    self.create_subscription(subscription, client_id, session_id, 'sub')
                    response['msg'].append(['Subscription registered'])
            else:
                response['error'] = True
                response['msg'].append(['You already have session at this moment.'])
        elif subscribed.status == 'canceled':
            if self.check_sessions_schedules(subscription_ids, session_id):
                if waiting_list:
                    subscribed.status = 'waiting'
                    response['warning'] = True
                    response['msg'].append(['This session is full, your subscription is registered in waiting list'])
                else:
                    subscribed.status = 'sub'
                    response['msg'].append(['Subscription registered'])
            else:
                response['error'] = True
                response['msg'].append(['You already have session at this moment.'])
        else:
            update_waiting_list = True if subscribed.status == 'sub' else False

            # Change status of subscription to 'canceled'
            subscribed.status = 'canceled'

            # Update waiting list if subscription status was 'sub'
            if update_waiting_list:
                # Get the first record subscription in waiting list
                first_in_waiting_list = subscription.search([
                    ('session_id.id', '=', session_id.id),
                    ('status', '=', 'waiting')
                ],
                    order='sub_date asc',
                    limit=1
                )

                # If recovered record is available, status change to valid
                if first_in_waiting_list.id:
                    first_in_waiting_list.status = 'sub'

            response['msg'].append(['Unsubscription registered'])

        return response

    # check if session is already subscribed
    def already_subscribed(self, subscription_ids, session_id):
        subscribed = False
        # for each subscriptions of web_client_id
        for subscription_id in subscription_ids:

            # Go to the next loop if subscription is empty
            if not subscription_id.session_id.id:
                continue

            # If session is already subscribed, subscribed get the session subscription
            if subscription_id.session_id.id == session_id.id:
                subscribed = subscription_id

        return subscribed

    # Check if the period of session requested is free
    def check_sessions_schedules(self, subscription_ids, session_requested):
        response = True

        for subscription_id in subscription_ids:
            compared_session = subscription_id.session_id

            # Go to the next loop if subscription is empty
            if not subscription_id.session_id.id:
                continue

            # Format string to date
            session_start_date = datetime.strptime(session_requested.start_date, '%Y-%m-%d %H:%M:%S')
            session_end_date = datetime.strptime(session_requested.end_date, '%Y-%m-%d %H:%M:%S')
            sub_session_start_date = datetime.strptime(compared_session.start_date, '%Y-%m-%d %H:%M:%S')
            sub_session_end_date = datetime.strptime(compared_session.end_date, '%Y-%m-%d %H:%M:%S')

            # Check the availability of the schedule
            if session_start_date <= sub_session_end_date and \
                    session_end_date >= sub_session_start_date and \
                    subscription_id.status != 'canceled':
                response = False

        return response

    # create a subscription
    def create_subscription(self, subscription, client, session, status):
        subscription.sudo().create({
            'name': client.name,
            'client_id': client.id,
            'session_id': session.id,
            'sub_date': datetime.now(),
            'status': status
        })


    # controller that render the client courses list
    # return a view
    @http.route('/my/courses', auth='public', website=True, type="http")
    def client_web_interface(self, **kw):

        env = request.env
        partner = request.env.user.partner_id
        client = env['res.partner']
        subscription = env['sport.subscription']

        now = datetime.now()

        subscription_ids = subscription.search([
            ('client_id', '=', partner.id),
        ])
        
        _logger.info(subscription_ids)

        for subscription in subscription_ids:
            sub_date = subscription.session_id.start_date
            sub_date = datetime.strptime(sub_date, '%Y-%m-%d %H:%M:%S')
            _logger.info("date : " + str(sub_date))

        values = {
            'subscriptions':subscription_ids,
        }
        
        return http.request.render('sport_management.client_courses', values)
