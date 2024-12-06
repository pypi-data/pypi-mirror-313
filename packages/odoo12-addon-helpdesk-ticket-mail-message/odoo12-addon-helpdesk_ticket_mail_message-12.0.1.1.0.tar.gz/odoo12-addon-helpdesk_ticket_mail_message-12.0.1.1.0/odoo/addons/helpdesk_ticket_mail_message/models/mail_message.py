from odoo import api, models, fields, _


class Message(models.Model):
    """Messages model: system notification (replacing res.log notifications),
    comments (OpenChatter discussion) and incoming emails."""

    _inherit = "mail.message"

    color_row = fields.Char("Color Row", default="#000000")
    color_background_row = fields.Char("Color Background Row", default="#FFFFFF")
    date_subject = fields.Text("Date/Subject", compute="_compute_date_subject")
    message_type_mail = fields.Selection(
        selection=[
            ("email_sent", _("Mail sent")),
            ("email_received", _("Email received")),
            ("note", _("Note")),
        ],
        string="Message type",
    )

    @api.one
    @api.depends("date", "subject")
    def _compute_date_subject(self):
        for mail in self:
            mail.date_subject = (
                f" {mail.date.strftime('%Y-%m-%d %H:%M:%S')} \n" f" {mail.subject}"
            )

    @api.model
    def create(self, values):
        """
        When creating a new message, color it depending of its type
        (sent, recieved, note) and update its ticket if it is related to one
        """
        if values.get("model") == "helpdesk.ticket" and values.get("res_id"):
            ticket = self.env["helpdesk.ticket"].browse(values.get("res_id"))
            if not ticket:
                return super(Message, self).create(values)

            if values.get("message_type") == "email":
                values["color_row"] = "#FFFFFF"
                if (
                    self._context.get("default_message_type_mail") == "email_sent"
                    or self.env.user.company_id.email == values.get("email_from")
                ):
                    values["message_type_mail"] = "email_sent"
                    values["color_background_row"] = "#FF0000"
                else:
                    values["message_type_mail"] = "email_received"
                    values["color_background_row"] = "#000000"
            elif values.get("message_type") == "comment":
                values["message_type_mail"] = "note"
                values["color_background_row"] = "#23FF00"

        return super(Message, self).create(values)

    def mail_compose_action(self):
        if self.message_type == "email":
            return self.mail_compose_message_action()
        elif self.message_type == "comment":
            return self.mail_compose_message_action_note()
        else:
            return False

    def _prepare_action_mail_compose_with_context(self, composition_mode):
        """
        Prepare action mail_compose_message for tickets with context,
        depending on the composition_mode and other parameters
        """
        ctx = self.env.context.copy() or {}
        ctx.update(
            {
                "default_composition_mode": composition_mode,
                "default_email_from": self.env.user.company_id.email,
                "default_email_to": self.email_from,
                "default_no_atuto_thread": True,
                "default_reply_to": self.email_from,
                "default_parent_id": self.id,
                "default_body": f"\n\n\n---- [{self.date}] {self.email_from} :\n"
                + self.body,
                "default_template_id": False,
                "active_model": self.model,
                "active_id": self.res_id,
                "active_ids": [self.res_id],
                "default_subject": self.subject,
                "default_message_type_mail": "email_sent",
            }
        )
        if composition_mode == "comment":
            ctx["default_is_log"] = True

        if self.model == "helpdesk.ticket":
            ticket = self.env["helpdesk.ticket"].browse(self.res_id)
            ctx.update(
                {
                    "default_subject": (
                        self.subject
                        if "Re:" in self.subject
                        else f"Re:[{ticket.number}] {self.subject}"
                    ),
                }
            )

        action = self.env.ref(
            "helpdesk_ticket_mail_message.action_mail_compose_message_wizard"
        ).read()[0]
        action.update(
            {
                "src_model": "helpdesk.ticket",
                "context": ctx,
            }
        )

        return action

    def mail_compose_message_action(self):
        """
        Open new communication to send mail
        """
        return self._prepare_action_mail_compose_with_context("mass_mail")

    def mail_compose_message_action_all(self):
        """
        Open new communication to send mail with CC
        """
        action = self._prepare_action_mail_compose_with_context("mass_mail")
        action["context"].update({"default_email_cc": self.origin_email_cc})
        return action

    def mail_compose_message_action_resend(self):
        """
        Open new communication to reply
        """
        return self._prepare_action_mail_compose_with_context("mass_mail")

    def mail_compose_message_action_note(self):
        """
        Open new communication to create a note
        """
        return self._prepare_action_mail_compose_with_context("comment")
