from odoo.tests.common import TransactionCase


class TestHelpdeskTicket(TransactionCase):
    def setUp(self):
        super(TestHelpdeskTicket, self).setUp()
        self.HelpdeskTicket = self.env["helpdesk.ticket"]
        self.mail_activity_form_view = self.env.ref(
            "mail.mail_activity_view_form_popup"
        )
        self.helpdesk_model_id = self.env.ref("helpdesk_mgmt.model_helpdesk_ticket").id

    def test_action_new_activity(self):
        ticket = self.HelpdeskTicket.create(
            {
                "name": "Test Ticket",
                "description": "Test Description",
            }
        )

        result = ticket.action_new_activity()

        self.assertIsInstance(result, dict)
        self.assertEqual(result.get("type"), "ir.actions.act_window")
        self.assertEqual(result.get("name"), "New Activity")
        self.assertEqual(result.get("res_model"), "mail.activity")
        self.assertEqual(result.get("view_type"), "form")
        self.assertEqual(result.get("view_mode"), "form")
        self.assertEqual(result.get("view_id"), self.mail_activity_form_view.id)
        self.assertEqual(result.get("target"), "new")

        context = result.get("context")
        self.assertEqual(context.get("default_res_id"), ticket.id)
        self.assertEqual(context.get("default_res_model"), "helpdesk.ticket")
        self.assertEqual(context.get("default_res_model_id"), self.helpdesk_model_id)
        self.assertNotIn("default_team_id", context)
