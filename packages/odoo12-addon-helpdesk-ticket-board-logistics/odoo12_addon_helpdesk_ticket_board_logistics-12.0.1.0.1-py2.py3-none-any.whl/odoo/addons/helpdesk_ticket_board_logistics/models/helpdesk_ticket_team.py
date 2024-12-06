from odoo import models, fields, api


class HelpdeskTicketTeam(models.Model):
    _inherit = "helpdesk.ticket.team"

    name = fields.Char(
        required=True,
        translate=True,
    )

    todo_ticket_count_my_tickets = fields.Integer(compute="_compute_todo_tickets")

    @api.depends("ticket_ids", "ticket_ids.stage_id")
    def _compute_todo_tickets(self):
        super(HelpdeskTicketTeam, self)._compute_todo_tickets()
        user_id = self.env.uid
        ticket_model = self.env["helpdesk.ticket"]

        my_tickets = ticket_model.search(
            [
                ("team_id", "in", self.ids),
                ("closed", "=", False),
                ("user_id", "=", user_id),
            ],
        )

        for team in self:
            team.todo_ticket_count_my_tickets = len(
                my_tickets.filtered(lambda t: t.team_id.id == team.id)
            )
