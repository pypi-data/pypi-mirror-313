from odoo import models, fields, api


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    name = fields.Char(string="Title", required=True, size=100)
    message_emails_ids = fields.One2many(
        "mail.message", compute="_compute_emails", string="Messages"
    )
    color_row = fields.Char("Color Row", default="#000000")
    color_background_row = fields.Char("Color Background Row", default="#FFFFFF")
    partner_category_id = fields.Many2many(
        related="partner_id.category_id", string="Partner Category", readonly=True
    )

    partner_contact_phone = fields.Char(
        related="partner_id.phone",
        string="Partner Phone",
        readonly=True,
    )

    @api.one
    @api.depends("message_ids")
    def _compute_emails(self):
        self.message_emails_ids = [
            msg_id.id
            for msg_id in self.message_ids
            if msg_id.message_type in ("email", "comment")
        ]

    def mail_compose_message_action(self):
        """
        Open new communication sales according to requirements
        """
        action = self.env.ref(
            "helpdesk_ticket_mail_message." "action_mail_compose_message_wizard"
        ).read()[0]
        ctx = self.env.context.copy() or {}
        ctx.update(
            {
                "default_composition_mode": "mass_mail",
                "default_template_id": self.env.ref(
                    "helpdesk_ticket_mail_message.created_response_ticket_template"
                ).id
                or False,
                "default_email_to": self.partner_email,
                "default_subject": "The Ticket %s" % self.number,
                "default_body": self.description,
                "default_message_type_mail": "email_sent",
                "active_model": self._name,
                "active_id": self.id,
                "active_ids": [self.id],
                "skip_onchange_template_id": True,
            }
        )
        action["context"] = ctx
        return action

    def mail_compose_message_action_note(self):
        """
        Open new communication sales according to requirements
        """
        action = self.env.ref(
            "helpdesk_ticket_mail_message." "action_mail_compose_message_wizard"
        ).read()[0]
        ctx = self.env.context.copy() or {}
        ctx.update(
            {
                "default_composition_mode": "comment",
                "default_is_log": True,
                "active_model": self._name,
                "active_id": self.id,
                "active_ids": [self.id],
                "default_subject": self.name,
            }
        )
        action["context"] = ctx
        return action

    @api.multi
    def message_get_default_recipients(self, res_model=None, res_ids=None):
        """
        Override for helpdesk tickets (as in crm.lead) to avoid the email composer
        to suggest addresses based on ticket partners, since it was causing duplicates
        for gmail accounts.
        """
        return {r.id: {"partner_ids": []} for r in self.sudo()}
