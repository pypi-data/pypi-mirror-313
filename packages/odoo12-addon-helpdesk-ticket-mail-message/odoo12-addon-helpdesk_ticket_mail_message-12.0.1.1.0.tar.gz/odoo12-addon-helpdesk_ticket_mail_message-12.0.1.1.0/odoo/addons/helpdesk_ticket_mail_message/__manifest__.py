# Copyright 2024-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "SomItCoop Odoo helpdesk ticket mail message",
    "version": "12.0.1.1.0",
    "depends": [
        "helpdesk_mgmt",
        "web_widget_color",
        "widget_list_row_color",
        "widget_list_limit_cell",
        "mail_cc_and_to_text",
        "widget_list_message",
    ],
    "author": """
        Som It Cooperatiu SCCL,
        Som Connexió SCCL,
        Odoo Community Association (OCA)
    """,
    "category": "After-Sales",
    "website": "https://gitlab.com/somitcoop/erp-research/odoo-helpdesk",
    "license": "AGPL-3",
    "summary": "Helpdesk Ticket Mail Message",
    "description": """
        Allows sending an email from the ticket from a new tab where
        the email communications and notes associated with the ticket
        are recorded have been added.
    """,
    "data": [
        "data/helpdesk_data.xml",
        "views/template_view.xml",
        "views/helpdesk_ticket_view.xml",
        "views/mail_template_view.xml",
        "wizard/mail_compose_message_view.xml",
    ],
    "application": False,
    "installable": True,
    "post_init_hook": "post_install_hook",
}
