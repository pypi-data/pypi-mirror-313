# Copyright 2023-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Helpdesk tickets board view logistics improvements",
    "version": "12.0.1.0.1",
    "depends": [
        "helpdesk_mgmt",
    ],
    "author": """
        Som It Cooperatiu SCCL,
        Som Connexió SCCL,
        Odoo Community Association (OCA)",
    """,
    "category": "Helpdesk",
    "website": "https://gitlab.com/somitcoop/erp-research/odoo-helpdesk",
    "license": "AGPL-3",
    "summary": """
        ODOO module to customize logistics from the helpdesk ticket kanban view.
    """,
    "data": [
        "data/helpdesk_ticket_team.xml",
        "views/helpdesk_dashboard_view.xml",
        "views/helpdesk_ticket_view.xml",
    ],
    "demo": [],
    "application": False,
    "installable": True,
    "post_init_hook": "post_init_hook",
}
