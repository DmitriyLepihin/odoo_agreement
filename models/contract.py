import logging
from odoo import api, fields, models, _
from datetime import date
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Contract(models.Model):
    _name = "contract"
    _description = "Договор"
    _inherit = ["mail.thread", "mail.activity.mixin"]


    number = fields.Char(string="Номер договора", required=True, readonly=True,
                         default=lambda self: _("New"), tracking=True)
    kind_id = fields.Many2one("type.contracts", string="Тип договора", tracking=True)
    partner_id = fields.Many2one("res.partner", string="Клиент", tracking=True)
    author_id = fields.Many2one("res.users", string="Пользователь создавший договор", tracking=True)
    state = fields.Selection([("draft", "черновик"), ("in_approve", "на согласовании"), ("active", "активен"),
                              ("completed", "завершен")], default="draft", string="Статус", tracking=True)
    start_date = fields.Date(default=date.today(), string="Дата начала", tracking=True)
    end_date = fields.Date(default=date.today(), string="Дата завершения", tracking=True)
    is_author = fields.Boolean(compute='check_author')
    is_head = fields.Boolean(compute='check_group_user')

    @api.depends('author_id')
    def check_group_user(self):
        self.is_head = self.env.user.has_group('agreement.head')

    @api.depends('author_id')
    def check_author(self):
        self.is_author = self.env.user.id != self.author_id.id

    @api.depends()
    def _get_current_user(self):
        self.update({"current_user_id": self.env.user.id})

    def set_state_in_approve(self):
        self.state = "in_approve"

    def set_state_active(self):
        self.state = "active"

    def set_state_draft(self):
        self.state = "draft"
        if self.author_id.email:
            mail_template = self.env.ref('agreement.email_template_name')
            mail_template.send_mail(self.id, force_send=True)

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

    def set_status_completed(self):
        """cron method"""
        contract_ids = self.env["contract"].search([("state", "=", "active"), ("end_date", ">", date.today())])
        for contract in contract_ids:
            contract.write(
                {
                    "state": "completed"
                }
            )
