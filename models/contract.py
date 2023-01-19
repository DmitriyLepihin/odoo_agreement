import logging
from odoo import api, fields, models, _
from datetime import date

_logger = logging.getLogger(__name__)


class Contract(models.Model):
    _name = "contract"
    _description = "Договор"
    _inherit = ["mail.thread", "mail.activity.mixin"]


    number = fields.Char(string="Номер договора", required=True,
                         readonly=True, default=lambda self: _("New"), tracking=True)
    partner_id = fields.Many2one("res.partner", string="Клиент", tracking=True)
    author_id = fields.Many2one("res.users",
                                string="Пользователь создавший договор", tracking=True)
    state = fields.Selection([("draft", "черновик"),
                              ("in_approve", "на согласовании"),
                              ("active", "активен"),
                              ("completed", "завершен")], default="draft", string="Статус", tracking=True)
    start_date = fields.Date(default=date.today(), string="", tracking=True)
    end_date = fields.Date(default=date.today(), string="", tracking=True)

    def set_state_in_approve(self):
        self.state = "in_approve"

    def set_state_active(self):
        self.state = "active"

    def set_state_draft(self):
        self.state = "draft"

    @api.model
    def create(self, vals):
        if vals.get("number", _("New")) == _("New"):
            vals["number"] = self.env["ir.sequence"].next_by_code(
                "contract") or _("New")
        res = super(Contract, self).create(vals)
        return res

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, "%s" % f"Договор № {rec.number}"))
        return res

