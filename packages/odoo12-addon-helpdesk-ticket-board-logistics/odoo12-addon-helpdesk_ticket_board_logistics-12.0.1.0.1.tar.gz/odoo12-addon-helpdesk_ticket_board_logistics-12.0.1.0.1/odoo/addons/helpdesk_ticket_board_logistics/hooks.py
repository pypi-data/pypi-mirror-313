from odoo import SUPERUSER_ID, api


def post_init_hook(cr, _):
    env = api.Environment(cr, SUPERUSER_ID, {})
    unassigned_team = env.ref("helpdesk_ticket_board_logistics.unassigned_team")
    unassigned_tickets = env["helpdesk.ticket"].search([("team_id", "=", False)])

    for ticket in unassigned_tickets:
        ticket.team_id = unassigned_team.id
