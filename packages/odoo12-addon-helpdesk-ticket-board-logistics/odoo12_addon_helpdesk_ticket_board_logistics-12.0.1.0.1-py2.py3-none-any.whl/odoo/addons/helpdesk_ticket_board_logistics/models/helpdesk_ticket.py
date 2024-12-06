from odoo import api, fields, models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    closed = fields.Boolean(related="stage_id.closed", store=True)

    def write(self, vals):
        if vals.get("team_id") is False:
            vals["team_id"] = self.env.ref(
                "helpdesk_ticket_board_logistics.unassigned_team"
            ).id
        return super().write(vals)

    @api.model
    def create(self, vals):
        if not vals.get("team_id"):
            vals["team_id"] = self.env.ref(
                "helpdesk_ticket_board_logistics.unassigned_team"
            ).id
        return super().create(vals)
