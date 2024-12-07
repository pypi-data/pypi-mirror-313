from __future__ import annotations

import dataclasses
import logging
import smtplib
import typing
from dataclasses import dataclass
from email.mime.text import MIMEText

import jinja2

if typing.TYPE_CHECKING:
    import pathlib


logger = logging.getLogger(__name__)


@dataclass
class TransactionalEmail:
    to_email: str
    to_name: str
    from_email: str
    from_name: str

    subject: typing.ClassVar[str]
    template_name: typing.ClassVar[str]
    template_path: typing.ClassVar[pathlib.Path]

    @property
    def fields(self: typing.Self) -> dict[str, str]:
        return {
            field.name: str(
                getattr(
                    self,
                    field.name,
                ),
            )
            for field in dataclasses.fields(self)
        }

    @property
    def message(self: typing.Self) -> dict[str, typing.Any]:
        environment = jinja2.Environment(  # noqa: S701
            loader=jinja2.FileSystemLoader(self.template_path),
        )
        template = environment.get_template(self.template_name + ".j2")

        fields = self.fields
        return template.render(**fields)


@dataclasses.dataclass
class SMTPConfig:
    smtp_server: str
    smtp_port: int
    smtp_username: str
    smtp_password: str


class SMTPEmailHandler:
    def __init__(
        self: typing.Self,
        *,
        config: SMTPConfig,
        from_email: str,
        from_name: str,
    ) -> None:
        self.from_email = from_email
        self.from_name = from_name
        self.smtp_server = config.smtp_server
        self.smtp_port = config.smtp_port
        self.smtp_username = config.smtp_username
        self.smtp_password = config.smtp_password

    @property
    def client(self: typing.Self) -> smtplib.SMTP:
        client = smtplib.SMTP(self.smtp_server, self.smtp_port)
        client.login(self.smtp_username, self.smtp_password)
        return client

    def setup(self) -> None:
        self._template_classes = {cls.__name__: cls for cls in TransactionalEmail.__subclasses__()}

    def __getitem__(self: typing.Self, name: str) -> TransactionalEmail:
        """Fetch an email template by name."""
        return self._template_classes[name]

    def send(self: typing.Self, template_cls: type[TransactionalEmail], **template_kwargs: str) -> None:
        template = template_cls(
            from_email=self.from_email,
            from_name=self.from_name,
            **template_kwargs,
        )

        msg = MIMEText(template.message)
        msg["From"] = self.from_email
        msg["To"] = template.to_email
        msg["Subject"] = template.subject

        self.client.sendmail(
            from_addr=self.from_email,
            to_addrs=[template.to_email],
            msg=msg.as_string(),
        )
