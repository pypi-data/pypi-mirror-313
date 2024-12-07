import pathlib
from dataclasses import dataclass
from unittest import mock

from neos_common.client import email

template_path = pathlib.Path(__file__).resolve().parent / "templates"


@dataclass
class EmailVerify(email.TransactionalEmail):
    template_path = template_path
    template_name = "email_verify"
    subject = "Verify Email."
    token: str
    hostname: str


class TestTransactionalEmail:
    def test_message_generation(self):
        t = EmailVerify(
            to_email="to-email",
            to_name="to-name",
            from_name="from-name",
            from_email="from-email",
            token="ABC123",
            hostname="localhost",
        )
        assert t.message == "Please go to localhost and enter code ABC123."


class TestSMTPEmailHandler:
    def test_init(self):
        eh = email.SMTPEmailHandler(
            config=email.SMTPConfig(
                smtp_server="smtp.server.com",
                smtp_port=25,
                smtp_username="username",
                smtp_password="password",
            ),
            from_email="from_email",
            from_name="from_name",
        )

        assert eh.smtp_server == "smtp.server.com"
        assert eh.smtp_port == 25
        assert eh.smtp_username == "username"
        assert eh.smtp_password == "password"
        assert eh.from_email == "from_email"
        assert eh.from_name == "from_name"

    def test_client_property(self, monkeypatch):
        client = mock.Mock()
        monkeypatch.setattr(
            email.smtplib,
            "SMTP",
            mock.Mock(return_value=client),
        )

        eh = email.SMTPEmailHandler(
            config=email.SMTPConfig(
                smtp_server="smtp.server.com",
                smtp_port=25,
                smtp_username="username",
                smtp_password="password",
            ),
            from_email="from_email",
            from_name="from_name",
        )

        c = eh.client
        assert c == client

        assert email.smtplib.SMTP.call_args == mock.call("smtp.server.com", 25)

    def test_send(self, monkeypatch):
        client = mock.Mock()
        monkeypatch.setattr(
            email.smtplib,
            "SMTP",
            mock.Mock(return_value=client),
        )

        eh = email.SMTPEmailHandler(
            config=email.SMTPConfig(
                smtp_server="smtp.server.com",
                smtp_port=25,
                smtp_username="username",
                smtp_password="password",
            ),
            from_email="from_email",
            from_name="from_name",
        )

        eh.setup()

        eh.send(
            eh["EmailVerify"],
            to_email="test@test.com",
            to_name="mike",
            token="ABC123",
            hostname="localhost",
        )

        assert client.sendmail.call_args == mock.call(
            from_addr="from_email",
            to_addrs=["test@test.com"],
            msg="""Content-Type: text/plain; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
From: from_email
To: test@test.com
Subject: Verify Email.

Please go to localhost and enter code ABC123.""",
        )
