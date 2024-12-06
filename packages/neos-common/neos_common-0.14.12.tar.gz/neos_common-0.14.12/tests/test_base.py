import pytest

from neos_common import error
from neos_common.base import ResourceBase, ResourceReader


class Resource(ResourceBase):
    @classmethod
    def get_resource_id_template(cls):
        return "{resource_id}"

    @classmethod
    def format_resource_id(cls, *args):
        return cls.get_resource_id_template().format(resource_id=args[0])


class TestResource:
    def test_resource_creation(self):
        resource = Resource(partition="ksa", service="iam")
        assert resource.urn == "urn:ksa:iam:::"

    def test_resource_creation_with_all_fields(self):
        resource = Resource(
            partition="ksa",
            service="iam",
            identifier="id",
            account_id="account",
            resource_type="resource_type",
        )
        assert resource.urn == "urn:ksa:iam:id:account:resource_type"

    def test_resource_creation_with_resource(self):
        resource = Resource(
            partition="ksa",
            service="iam",
            identifier="id",
            account_id="account",
            resource_type="resource_type",
            resource_id="resource_id",
        )
        assert resource.urn == "urn:ksa:iam:id:account:resource_type:resource_id"

    def test_urn_template(self):
        resource = Resource()
        assert resource.urn_template == "urn:::::"

    def test_urn_template_star(self):
        resource = Resource(all_="*")
        assert resource.urn_template == "*"

    def test_urn_template_with_fields(self):
        resource = Resource(
            partition="ksa",
            service="iam",
            identifier="id",
            account_id="account",
            resource_type="resource_type",
        )
        assert resource.urn_template == "urn:ksa:iam:id:account:resource_type"

    def test_urn_template_with_resource_id(self):
        resource = Resource(
            partition="ksa",
            service="iam",
            identifier="id",
            account_id="account",
            resource_type="resource_type",
            resource_id="resource_id",
        )
        assert resource.urn_template == "urn:ksa:iam:id:account:resource_type:{resource_id}"

    def test_urn_template_with_resource_id_and_sub_type(self):
        resource = Resource(
            partition="ksa",
            service="iam",
            identifier="id",
            account_id="account",
            resource_type="resource_type",
            sub_type="user",
            resource_id="resource_id",
        )
        assert resource.urn_template == "urn:ksa:iam:id:account:resource_type:user:{resource_id}"

    @pytest.mark.parametrize(
        ("resource_id", "expected_resource_id"),
        [
            ("", ""),
            ("string", "string"),
            (("This", "is", "tuple"), "This"),  # See the realization of the Resource
        ],
    )
    async def test_resource_generation(self, resource_id, expected_resource_id):
        resource = Resource.generate(
            partition="ksa",
            service="core",
            identifier="id",
            account_id="account",
            resource_type="resource_type",
            resource_id=resource_id,
        )
        assert resource == Resource(
            partition="ksa",
            service="core",
            identifier="id",
            account_id="account",
            resource_type="resource_type",
            resource_id=expected_resource_id,
        )


class TestResourceParse:
    @pytest.mark.parametrize(
        "resource_str",
        [
            # Allow all
            ("*"),
            # All fields used and urn/nrn
            ("nrn:ksa:core:sc:root:product:my-dp"),
            ("urn:ksa:core:sc:root:product:my-dp"),
            # Allow any resource_id
            ("urn:ksa:core:sc:root:product:*"),
            # Null sector (identifier)
            ("urn:ksa:iam::root:user:ann"),
            # Null owner (account_id)
            ("urn:ksa:iam:sc::user:ann"),
            # Resource_type and resource_id subgroups
            ("urn:ksa:iam::root:policy:user:something"),
            # Resource_type and resource_id all
            ("urn:ksa:iam::root:policy:user:*"),
            # All nulls
            ("urn:ksa:amazingsvc:::amazingrt:amazinrid"),
        ],
    )
    async def test_should_parse(self, resource_str):
        resource = Resource.parse(resource_str)
        assert resource

        assert resource.urn == resource_str

    @pytest.mark.parametrize(
        "resource_str",
        [
            (""),
            ("*rn:ksa:core:sc:root:product:my-dp"),
            ("arn:ksa:core:sc:root:product:my-dp"),
            ("urn:ksa:core:sc:root:product:my-dp-with-*"),
            ("really_bad_resource"),
            # If we ever decide to use pathlike resource_type/resource_id
            ("urn:ksa:core:sc:root:product/*"),
            ("urn:ksa:iam::root:groups:group-id/something"),
            ("urn:ksa:iam::root:groups/group-id/something"),
        ],
    )
    async def test_should_not_parse(self, resource_str):
        with pytest.raises(error.InvalidResourceFormatError):
            Resource.parse(resource_str)


class TestResourceReader:
    @pytest.mark.parametrize(
        ("identifier", "account_id", "resource_id"),
        [
            ("0123456789", "root", "*"),
            ("0123456789", "root", "dp"),
            ("0123456789", "", "dp"),
            ("", "root", "dp"),
            ("0123456789", "root", ""),
            ("0123456789", "", ""),
            ("", "root", ""),
            ("", "", ""),
        ],
    )
    def test_slice(self, identifier, account_id, resource_id):
        urn = f"urn:ksa:core:{identifier}:{account_id}:product:{resource_id}".rstrip(":")
        r = ResourceReader.parse(urn)

        assert len(r) == 7

        assert r[0] == "urn"
        assert r[1] == "ksa"
        assert r[2] == "core"
        assert r[3] == identifier
        assert r[4] == account_id
        assert r[5] == "product"

        assert r[6] == resource_id
        assert r[-1] == resource_id

        assert r[0:-1] == f"urn:ksa:core:{identifier}:{account_id}:product"

        assert r.urn == urn

    @pytest.mark.parametrize(
        ("identifier", "account_id", "resource_id"),
        [
            ("0123456789", "root", "*"),
            ("0123456789", "root", "dp"),
            ("0123456789", "", "dp"),
            ("", "root", "dp"),
        ],
    )
    def test_slice_with_subtype(self, identifier, account_id, resource_id):
        urn = f"urn:ksa:core:{identifier}:{account_id}:product:sub-type:{resource_id}".rstrip(":")
        r = ResourceReader.parse(urn)

        assert len(r) == 8

        assert r[0] == "urn"
        assert r[1] == "ksa"
        assert r[2] == "core"
        assert r[3] == identifier
        assert r[4] == account_id
        assert r[5] == "product"
        assert r[6] == "sub-type"

        assert r[7] == resource_id
        assert r[-1] == resource_id

        assert r[0:-1] == f"urn:ksa:core:{identifier}:{account_id}:product"

        assert r.urn == urn

    def test_slice_star(self):
        urn = "*"
        r = ResourceReader.parse(urn)

        assert len(r) == 1
        assert r[0] == "*"
        assert r.urn == urn
        assert r[0:-1] == ""

    def test_is_anies(self):
        r = ResourceReader.parse("*")

        assert r.is_any()
        assert not r.is_any_resource_id()

        r = ResourceReader.parse("urn:ksa:core:123:root:product:*")

        assert not r.is_any()
        assert r.is_any_resource_id()

    @pytest.mark.parametrize(
        ("resource_str", "expected_root"),
        [
            # Allow all
            ("*", "*"),
            # All fields used and urn/nrn
            ("nrn:ksa:core:sc:account:product:my-dp", "nrn:ksa:core:sc:root:product:my-dp"),
            ("urn:ksa:core:sc:account:product:my-dp", "urn:ksa:core:sc:root:product:my-dp"),
            # Allow any resource_id
            ("urn:ksa:core:sc:account:product:*", "urn:ksa:core:sc:root:product:*"),
            # Null sector (identifier)
            ("urn:ksa:iam::account:user:ann", "urn:ksa:iam::root:user:ann"),
            # Null owner (account_id)
            ("urn:ksa:iam:sc::user:ann", "urn:ksa:iam:sc:root:user:ann"),
            # Resource_type and resource_id subgroups
            ("urn:ksa:iam::account:policy:user:something", "urn:ksa:iam::root:policy:user:something"),
            # All nulls
            ("urn:ksa:amazingsvc:::amazingrt:amazinrid", "urn:ksa:amazingsvc::root:amazingrt:amazinrid"),
        ],
    )
    async def test_should_parse(self, resource_str, expected_root):
        resource = ResourceReader.parse(resource_str)

        root_resource = ResourceReader.to_root(resource)

        assert root_resource.urn == expected_root
