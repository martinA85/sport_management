window.onload = init;

function init(){

    console.log("init Calendar.js");
    calendar_printer();
}


function calendar_printer(){

    odoo.define("sport.my_js", function(require) { 'use strict';

        var ajax = require('web.ajax');
        var rpc = require('web.rpc');
        var weContext = require('web_editor.context');

        rpc.query({
            model : 'sport.session',
            method : 'search_read',
            context : weContext.get(),
        }).then(function(data){
            
            var sessions = '[';
            var json_len = Object.keys(data).length;
            for(var i=0;i<json_len;i++){
                var start = new Date(data[i].start_date);
                var end = new Date(data[i].end_date);
                var session = '{"title":"'+ data[i].name +'","start":"'+start+'","end":"'+end+'","allDay":false,"color":"'+data[i].color+'"},';
                sessions += session;
            }
            sessions = sessions.substring(0, sessions.length -1)
            sessions += "]";
            sessions = JSON.parse(sessions);

            $('#calendar').fullCalendar({
                height : 650,
                themeSystem: 'bootstrap4',
                weekNumbers : true,
                locale: 'fr',
                header:{
                    left:'prev,today,next',
                    center:'title',
                    right:'month,agendaWeek,agendaDay,listWeek'
                },
                editable:false,
                events : sessions,
                eventClick: function(event){
                    console.log("click");
                }
            })


        })
    });
}