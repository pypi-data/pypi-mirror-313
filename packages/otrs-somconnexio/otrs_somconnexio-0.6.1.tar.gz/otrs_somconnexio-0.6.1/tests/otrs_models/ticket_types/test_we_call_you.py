from otrs_somconnexio.otrs_models.configurations.querys.we_call_you import (
    WeCallYouCATConfiguration,
    WeCallYouESConfiguration,
)
from otrs_somconnexio.otrs_models.ticket_types.we_call_you_ticket import WeCallYouTicket


class TestCaseWeCallYou:
    fields_dict = {
        "name": "name surname",
        "schedule": "12h-14h",
        "language": "ca_ES",
        "phone": "642525377",
        "reason": "call me baby",
    }

    def test_create_CAT(self, mocker):
        self._execute_and_assert_create(mocker, WeCallYouCATConfiguration)

    def test_create_ES(self, mocker):
        self.fields_dict["language"] = "es_ES"
        self._execute_and_assert_create(mocker, WeCallYouESConfiguration)

    def _execute_and_assert_create(self, mocker, config):
        OTRSClientMock = mocker.patch(
            "otrs_somconnexio.otrs_models.ticket_types.base_ticket.OTRSClient",
            return_value=mocker.Mock(),
        )
        TicketMock = mocker.patch(
            "otrs_somconnexio.otrs_models.ticket_types.base_ticket.Ticket",
            return_value=mocker.Mock(),
        )
        DynamicFieldMock = mocker.patch(
            "otrs_somconnexio.otrs_models.ticket_types.base_ticket.DynamicField",
            return_value=mocker.Mock(),
        )
        ArticleMock = mocker.patch(
            "otrs_somconnexio.otrs_models.ticket_types.base_ticket.Article",
            return_value=mocker.Mock(),
        )

        expected_ticket_data = {
            "Title": config.subject,
            "QueueID": config.queue_id,
            "State": config.state,
            "Type": config.type,
            "Priority": config.priority,
            "CustomerUser": "customer",
            "CustomerID": "customer",
        }
        expected_article_data = {
            "Subject": config.subject,
            "Body": "-",
        }
        calls = [
            mocker.call("ProcessManagementProcessID", config.process_id),
            mocker.call(
                "ProcessManagementActivityID",
                config.activity_id,
            ),
            mocker.call("personaContacte", self.fields_dict["name"]),
            mocker.call("horariTrucada", self.fields_dict["schedule"]),
            mocker.call("telefonContacte", self.fields_dict["phone"]),
            mocker.call("motiuTrucada", self.fields_dict["reason"]),
        ]

        WeCallYouTicket(None, "customer", self.fields_dict, [], "").create()

        TicketMock.assert_called_once_with(expected_ticket_data)
        ArticleMock.assert_called_once_with(expected_article_data)
        DynamicFieldMock.assert_has_calls(calls)
        OTRSClientMock.return_value.create_otrs_process_ticket.assert_called_once_with(
            TicketMock.return_value,
            article=ArticleMock.return_value,
            dynamic_fields=[mocker.ANY for call in calls],
            attachments=None,
        )
