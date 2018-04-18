window.onload = init;

function init() {
    // launching calendar function
    calendar_printer();
}

function calendar_printer() {

    if (sessionStorage.getItem('alert')) {
        var data = JSON.parse(sessionStorage.getItem('data'));
        if (data.error) {
            $('#alert-msg').html(data.msg);
            $('#alert-msg').parent().closest('div').css('display', 'block');
        } else if (data.warning) {
            $('#warning-msg').html(data.msg);
            $('#warning-msg').parent().closest('div').css('display', 'block');
        } else {
            $('#info-msg').html(data.msg);
            $('#info-msg').parent().closest('div').css('display', 'block');
        }
        sessionStorage.clear();
    }

    odoo.define('sport.my_js', function (require) {
        'use strict';
        // loading odoo ressources
        var rpc = require('web.rpc');
        var weContext = require('web_editor.context');
        var ajax = require('web.ajax');
        var usession = require('web.session');


        // we are loading our sessions with odoo rpc api
        rpc.query({
            model: 'sport.session',
            // method: 'search_read',
            method: 'search_session_and_subscription',
            context: weContext.get(),
        }).then(function (data) {

            var sessions = [];
            // ou session are in data, we are parsing them to use them in our calendar
            JSON.parse(data).forEach(function (session) {
                session.subscriptions.forEach(function (subscription) {
                    if (subscription.client_id == usession.user_id) {
                        switch (subscription.status) {
                            case 'sub':
                                session.color = '#35b0c6';
                                session['status'] = 'sub';
                                session['msg'] = 'Are you sure you want to <b>unsubscribe</b> for this course ?';
                                break;
                            case 'valid':
                                session.color = 'green';
                                session['status'] = 'valid';
                                session['msg'] = 'This session has passed. You can\'t you unsubscribe.';
                                break;
                            case 'canceled':
                                session.color = 'gray';
                                session['status'] = 'canceled';
                                session['msg'] = 'Are you sure you want to <b>subscribe</b> for this course ?';
                                break;
                            case 'waiting':
                                session.color = 'orange';
                                session['status'] = 'waiting';
                                session['msg'] = 'Are you sure you want to <b>unsubscribe</b> for this course ?';
                                break;
                            case 'absent':
                                session.color = 'red';
                                session['status'] = 'absent';
                                session['msg'] = 'This session has passed. You can\'t you unsubscribe.';
                                break;
                        }
                    }
                });
                sessions.push(session);
            });

            // init calendar
            $('#calendar').fullCalendar({
                height: 650,
                themeSystem: 'bootstrap4',
                weekNumbers: true,
                locale: 'fr',
                header: {
                    left: 'prev,today,next',
                    center: 'title',
                    right: 'years,month,agendaWeek,agendaDay,listWeek'
                },
                editable: false,
                events: sessions,
                timeFormat: 'HH:mm',
                eventClick: function (event) {

                    // Get informations of event (day, date, hours start and end
                    var tb_day_str = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
                    var course = event.title;
                    var day = tb_day_str[event.start._d.getUTCDay()];
                    var hours_start = event.start._d.getUTCHours() + ':' + event.start._d.getUTCMinutes();
                    var hours_end = event.end._d.getUTCHours() + ':' + event.end._d.getUTCMinutes();
                    var msg = event.msg ? event.msg : 'Are you sure you want to <b>subscribe</b> for this course ?';

                    // Exit function if event is outdated
                    if (Date.now() > event.start){
                        return;
                    }

                    if (event.status != 'absent' | event.status != 'valid') {
                        // Add message in dialog box.
                        $('#dialog-msg').html(msg);
                        $('#selected-course').html(
                            '<b>Course : </b>' + course + '<br /><b>On : </b>' + day + '<br /><b>At : </b>' + hours_start + ' - ' + hours_end
                        );
                        $('#dialog-confirm').dialog({
                            resizable: false,
                            height: 'auto',
                            width: 400,
                            modal: true,
                            buttons: {
                                'Yes': function () {
                                    ajax.jsonRpc('/sport/sessions/subscribe', 'call', {
                                        'user_id': usession.user_id,
                                        'session_id': event.id,
                                        'unsubscribe': false
                                    }).then(function (data) {
                                        sessionStorage.clear();
                                        sessionStorage.setItem('alert', true);
                                        sessionStorage.setItem('data', JSON.stringify(data));
                                    });
                                    $(this).dialog('close');
                                    location.reload();
                                },
                                Cancel: function () {
                                    $(this).dialog('close');
                                }
                            }
                        });
                    } else {
                        $('#alert-msg').html(event.msg);
                        $('#alert-msg').parent().closest('div').css('display', 'block');
                    }
                }
            });
        });
    });
}