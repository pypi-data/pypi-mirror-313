Module neos_common.client.email
===============================

Classes
-------

`SMTPConfig(smtp_server: str, smtp_port: int, smtp_username: str, smtp_password: str)`
:   SMTPConfig(smtp_server: 'str', smtp_port: 'int', smtp_username: 'str', smtp_password: 'str')

    ### Class variables

    `smtp_password: str`
    :

    `smtp_port: int`
    :

    `smtp_server: str`
    :

    `smtp_username: str`
    :

`SMTPEmailHandler(*, config: SMTPConfig, from_email: str, from_name: str)`
:   

    ### Instance variables

    `client: smtplib.SMTP`
    :

    ### Methods

    `send(self: typing.Self, template_cls: type[TransactionalEmail], **template_kwargs: str) ‑> None`
    :

    `setup(self) ‑> None`
    :

`TransactionalEmail(to_email: str, to_name: str, from_email: str, from_name: str)`
:   TransactionalEmail(to_email: 'str', to_name: 'str', from_email: 'str', from_name: 'str')

    ### Class variables

    `from_email: str`
    :

    `from_name: str`
    :

    `subject: typing.ClassVar[str]`
    :

    `template_name: typing.ClassVar[str]`
    :

    `template_path: typing.ClassVar[pathlib.Path]`
    :

    `to_email: str`
    :

    `to_name: str`
    :

    ### Instance variables

    `fields: dict[str, str]`
    :

    `message: dict[str, typing.Any]`
    :