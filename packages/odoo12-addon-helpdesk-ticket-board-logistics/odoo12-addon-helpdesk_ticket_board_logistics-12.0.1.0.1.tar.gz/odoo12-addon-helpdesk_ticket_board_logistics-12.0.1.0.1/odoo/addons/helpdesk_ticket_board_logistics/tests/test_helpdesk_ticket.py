from odoo.tests.common import TransactionCase


class TestHelpdeskTicket(TransactionCase):
    def setUp(self):
        super(TestHelpdeskTicket, self).setUp()
        self.HelpdeskTicket = self.env["helpdesk.ticket"]
        self.unassigned_team = self.env.ref(
            "helpdesk_ticket_board_logistics.unassigned_team"
        )

    def test_create_ticket_without_team_id(self):
        ticket = self.HelpdeskTicket.create(
            {
                "name": "Test Ticket",
                "description": "This is a test ticket without team_id",
            }
        )

        self.assertEqual(ticket.team_id, self.unassigned_team)

    def test_edit_ticket_without_team_id(self):
        ticket = self.env.ref("helpdesk_mgmt.helpdesk_ticket_1")
        ticket.write(
            {
                "team_id": False,
            }
        )

        self.assertEqual(ticket.team_id, self.unassigned_team)
