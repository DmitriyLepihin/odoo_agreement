import logging
from odoo import api, fields, models
from datetime import date

_logger = logging.getLogger(__name__)


class TypeContracts(models.Model):
    _name = "type.contracts"
    _description = "Вид договора"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Наименование", tracking=True)
    active = fields.Boolean(string="Active", default=True, tracking=True)

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         'Такой "вид договора" уже существуют!\nВыберите необходимое наименование из справочника.'
         ),
    ]
