from odoo import models, fields, api, tools


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    helpdesk_ticket_tag_ids = fields.Many2many(
        "helpdesk.ticket.tag",
    )
    available_mail_template_ids = fields.Many2many(
        "mail.template",
        compute="_compute_available_mail_template_ids",
    )
    lang = fields.Selection(string="Language", selection="_get_lang")

    @api.model
    def default_get(self, fields):
        result = super(MailComposeMessage, self).default_get(fields)
        if result.get("composition_mode") and result["composition_mode"] != "comment":
            del result["subject"]

        if result.get("model") == "helpdesk.ticket" and result.get("res_id"):
            ticket = self.env[result.get("model")].browse(result.get("res_id"))
            result["helpdesk_ticket_tag_ids"] = ticket.tag_ids.ids
            result["lang"] = ticket.partner_id.lang

        if self.env.user.signature:
            result["body"] = f"<p>{self.env.user.signature}</p>"

        return result

    @api.multi
    @api.onchange("template_id")
    def onchange_template_id_wrapper(self):
        """
        Prevent onchange from messing with defaults when the template is set from
        the mass mailing wizard in the helpdesk ticket form view
        """
        if self._context and self._context.get("skip_onchange_template_id"):
            return
        super(MailComposeMessage, self).onchange_template_id_wrapper()

    @api.model
    def generate_email_for_composer(self, template_id, res_ids, fields=None):
        """
        Override (for helpdesk tickets only) to avoid the email composer to suggest
        addresses based on ticket partners, since it was causing duplicates for gmail
        accounts. (See also helpdesk_automatic_stage_changes/models/helpdesk_ticket.py)
        """
        template_values = super(MailComposeMessage, self).generate_email_for_composer(
            template_id, res_ids, fields
        )

        # Remove partner_ids from template_values for helpdesk tickets
        if self._context.get("active_model") == "helpdesk.ticket":
            [template_values[res_id].update({"partner_ids": []}) for res_id in res_ids]

        return template_values

    @api.depends("helpdesk_ticket_tag_ids")
    def _compute_available_mail_template_ids(self):
        for record in self:
            domain = [
                (
                    "model_id",
                    "=",
                    self.env.ref("helpdesk_mgmt.model_helpdesk_ticket").id,
                )
            ]
            if record.model == "helpdesk.ticket" and record.helpdesk_ticket_tag_ids:
                domain.append(
                    (
                        "helpdesk_ticket_tag_ids",
                        "in",
                        record.helpdesk_ticket_tag_ids.ids,
                    )
                )

            available_email_ids = self.env["mail.template"].search(domain)

            if available_email_ids:
                record.available_mail_template_ids = available_email_ids.ids

    @api.model
    def _get_lang(self):
        return self.env["res.lang"].get_installed()

    @api.multi
    def onchange_template_id(self, template_id, composition_mode, model, res_id):
        """
        Do not overwrite subject and body html values
        """
        result = super(MailComposeMessage, self).onchange_template_id(
            template_id, composition_mode, model, res_id
        )
        if not template_id:
            return result

        values = result["value"]

        if composition_mode != "comment":
            if values.get("body") and self.body:
                values["body"] = tools.append_content_to_html(
                    self.body, values["body"], plaintext=False
                )
            if values.get("subject") and self.subject:
                values["subject"] = self.subject

        return {"value": values}
