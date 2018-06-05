from odoo import models, fields, api
from datetime import datetime
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)

class PlanningTmplWizard(models.TransientModel):
    _name="sport.planning_tmpl_wizard"

    def _default_planning(self):
        return self.env['sport.planning_tmpl_wizard'].browse(self._context.get('active_id'))

    planning_id = fields.Many2one('sport.planning_tmpl',  default=_default_planning)
    start_date = fields.Date(string="date debut")
    end_date = fields.Date(string="date fin")



    def generate_planning(self):
        for wizard in self:
            planning_tmpl = wizard.planning_id
            day = datetime.strptime(wizard.start_date, "%Y-%m-%d")
            while day != wizard.end_date:
                _logger.info(day.weekday)
                if day.weekday != 0:
                    planning_tmpl._generate_one_day(day)

