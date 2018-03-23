window.onload = init;

function init(){
    // launching calendar function
    calendar_printer();
}


function calendar_printer(){

    odoo.define("sport.my_js", function(require) { 'use strict';
        // loading odoo ressources
        var rpc = require('web.rpc');
        var weContext = require('web_editor.context');

        // we are loading our sessions with odoo rpc api
        rpc.query({
            model : 'sport.session',
            method : 'search_read',
            context : weContext.get(),
        }).then(function(data){
            
            // ou session are in data, we are parsing them to use them in our calendar
            var sessions = '[';
            var json_len = Object.keys(data).length;
            for(var i=0;i<json_len;i++){
                var start = new Date(data[i].start_date);
                var end = new Date(data[i].end_date);
                // data format for fullcalendar : { "title" : title, "start" : start_date, "end" : end_date, "color" : color}
                var session = '{"title":"'+ data[i].name +'","start":"'+start+'","end":"'+end+'","allDay":false,"color":"'+data[i].color+'"},';
                sessions += session;
            }
            sessions = sessions.substring(0, sessions.length -1)
            sessions += "]";
            sessions = JSON.parse(sessions);
            
            // init calendar
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