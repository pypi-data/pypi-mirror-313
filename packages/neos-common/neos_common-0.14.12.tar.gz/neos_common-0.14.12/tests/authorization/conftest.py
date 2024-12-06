from neos_common.base import ResourceBase


class Resource(ResourceBase):
    @classmethod
    def get_resource_id_template(cls):
        return "{resource_id}"

    @classmethod
    def format_resource_id(cls, *args):
        return cls.get_resource_id_template().format(resource_id=args[0])
