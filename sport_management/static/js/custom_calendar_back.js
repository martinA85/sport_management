odoo.define('sport.backend_calendar', function (require) {
    "use strict";
    var core = require('web.core');
    var CalendarView = require('web.CalendarView');
    var CalendarModel = require('web.CalendarModel');

    CalendarModel.include({

        _getFullCalendarOptions: function(){
            var res = this._super();
            res.minTime = '08:00:00';
            res.maxTime = '19:00:00';
            res.slotDuration = "00:15:00";
            res.slotLabelInterval = "01:00";
            res.timeFormat = "hh:mm";
            res.hiddenDays = [ 0 ];
            return res;
        },

    });

});