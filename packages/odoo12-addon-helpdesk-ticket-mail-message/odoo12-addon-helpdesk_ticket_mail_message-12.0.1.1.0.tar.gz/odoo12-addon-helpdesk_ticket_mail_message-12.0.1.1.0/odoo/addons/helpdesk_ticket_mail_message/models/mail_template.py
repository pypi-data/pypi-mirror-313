from odoo import models, fields


class MailTemplate(models.Model):
    _inherit = "mail.template"

    helpdesk_ticket_tag_ids = fields.Many2many(
        "helpdesk.ticket.tag", help="Helpdesk Tags related to this template."
    )
