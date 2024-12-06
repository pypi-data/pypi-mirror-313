from odoo.tests import tagged, common
from mock import patch


@tagged("post_install", "-at_install", "helpdesk_ticket_mail_message")
class TestMailComposeMessage(common.TransactionCase):
    def setUp(self):
        super(TestMailComposeMessage, self).setUp()
        self.helpdesk_ticket = self.env.ref("helpdesk_mgmt.helpdesk_ticket_1")
        self.MailComposeWizard = self.env["mail.compose.message"]
        self.template_id = self.env.ref(
            "helpdesk_ticket_mail_message.created_response_ticket_template"
        )
        self.mail_compose_data = {
            "composition_mode": "comment",
            "partner_ids": [(6, 0, [self.helpdesk_ticket.partner_id.id])],
            "template_id": self.template_id.id,
        }

    @patch(
        "odoo.addons.mail.wizard.mail_compose_message.MailComposer.onchange_template_id_wrapper"
    )
    def test_onchange_template_id_wrapper(self, mock_mail_onchange):
        """Check that original mail onchange wrapper is not called."""

        wizard = self.MailComposeWizard.create(self.mail_compose_data)

        wizard.with_context(
            skip_onchange_template_id=True
        ).onchange_template_id_wrapper()
        mock_mail_onchange.assert_not_called()

        wizard.with_context(
            skip_onchange_template_id=False
        ).onchange_template_id_wrapper()
        mock_mail_onchange.assert_called_once()

    def test_generate_email_for_helpdesk_ticket(self):
        """Check that partner_ids is emptied for helpdesk ticket mail composer."""
        wizard = self.MailComposeWizard.with_context(
            active_model="helpdesk.ticket",
            active_id=self.helpdesk_ticket.id,
        ).create(self.mail_compose_data)

        res_ids = [self.helpdesk_ticket.id]

        # Generate email values
        email_values = wizard.generate_email_for_composer(self.template_id.id, res_ids)

        self.assertFalse(email_values[res_ids[0]]["partner_ids"])
