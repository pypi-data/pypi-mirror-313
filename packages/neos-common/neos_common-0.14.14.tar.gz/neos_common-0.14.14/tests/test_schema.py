import pytest

from neos_common import base, schema


@pytest.mark.parametrize(
    ("effect", "expected"),
    [
        (base.EffectEnum.allow, True),
        (base.EffectEnum.deny, False),
    ],
)
def test_statement_is_allowed(effect, expected):
    s = schema.Statement(
        sid="sid",
        principal=["principal"],
        action=["action"],
        resource=[],
        condition=["condition"],
        effect=effect,
    )

    assert s.is_allowed() == expected


def test_get_principal_ids():
    p = schema.Principals(
        principals=[
            schema.Principal(
                principal_id=str(i),
                principal_type=schema.PrincipalType.user,
            )
            for i in range(5)
        ],
    )

    assert p.get_principal_ids() == ["0", "1", "2", "3", "4"]


def test_error_code_model_dump():
    ec = schema.ErrorCode(
        class_name="class-name",
        type="error-type",
        title="title",
    )

    assert ec.model_dump() == {"class_name": "class-name", "type": "error-type", "title": "title"}
