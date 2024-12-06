# Copyright 2023-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "version": "12.0.1.0.2",
    "name": "Helpdesk ticket activity ids page view",
    "depends": [
        "mail",
        "mail_activity_team",
        "helpdesk_ticket_mail_message",
    ],
    "author": """
        Som It Cooperatiu SCCL,
        Som Connexió SCCL,
        Odoo Community Association (OCA)
    """,
    "category": "Helpdesk",
    "website": "https://gitlab.com/somitcoop/erp-research/odoo-helpdesk",
    "license": "AGPL-3",
    "summary": """
        Adds a page to check and edit all the activities related to a helpdesk.ticket.
    """,
    "data": [
        "views/helpdesk_ticket.xml",
        "views/mail_activity.xml",
        "views/template_view.xml",
    ],
    "demo": [],
    "application": False,
    "installable": True,
}
