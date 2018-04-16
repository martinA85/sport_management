window.onload = init;

function init() {
    // launching calendar function
    calendar_printer();
}

function calendar_printer() {

    odoo.define("sport.my_js", function (require) {
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
                    if(subscription.client_id == usession.user_id){
                        session.color = "yellow";
                    }
                });
                sessions.push(session);
            });
            console.log(sessions);

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
                eventClick: function (event) {
                    console.log(event);
                    console.log('usession.user_id : ' + usession.user_id);
                    // Get informations of event (day, date, hours start and end
                    var tb_day_str = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
                    var course = event.title;
                    var day = tb_day_str[event.start._d.getUTCDay()];
                    var hours_start = event.start._d.getUTCHours() + ':' + event.start._d.getUTCMinutes();
                    var hours_end = event.end._d.getUTCHours() + ':' + event.end._d.getUTCMinutes();
                    var status_subscription = event.color == "yellow" ? true : false;
                    var msg = (status_subscription) ? 'Are you sure you want to <b>unsubscribe</b> for this course ?' : 'Are you sure you want to <b>subscribe</b> for this course ?';

                    // Add message in dialog box.
                    $('#dialog-msg').html(msg);
                    $('#selected-course').html(
                        '<b>Course : </b>' + course + '<br /><b>On : </b>' + day + '<br /><b>At : </b>' + hours_start + ' - ' + hours_end
                    );
                    $('#dialog-confirm').dialog({
                        resizable: false,
                        height: "auto",
                        width: 400,
                        modal: true,
                        buttons: {
                            "Yes": function () {
                                ajax.jsonRpc('/sport/sessions/subscribe', 'call', {
                                    'user_id': usession.user_id,
                                    'session_id': event.id
                                }).then(function (data) {
                                    console.log(data);
                                });
                                $(this).dialog("close");
                                location.reload();
                            },
                            Cancel: function () {
                                console.log('pas inscrit');
                                $(this).dialog("close");
                            }
                        }
                    });
                }
            });
        });
    });
}