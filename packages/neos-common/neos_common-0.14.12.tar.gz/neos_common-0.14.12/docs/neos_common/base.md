Module neos_common.base
=======================

Classes
-------

`Action(*args, **kwds)`
:   Action class base.
    
    When implementing IAM actions in a service, extend this class.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `account_create`
    :

    `account_delete`
    :

    `account_manage`
    :

    `account_member`
    :

    `core_access`
    :

    `core_announce`
    :

    `core_manage`
    :

    `core_migrate`
    :

    `core_register`
    :

    `data_product_browse`
    :

    `data_product_create`
    :

    `data_product_manage`
    :

    `data_product_read`
    :

    `data_source_browse`
    :

    `data_source_create`
    :

    `data_source_manage`
    :

    `data_source_read`
    :

    `data_system_browse`
    :

    `data_system_create`
    :

    `data_system_manage`
    :

    `data_system_read`
    :

    `data_unit_browse`
    :

    `data_unit_create`
    :

    `data_unit_manage`
    :

    `data_unit_read`
    :

    `dataset_read`
    :

    `group_browse`
    :

    `group_create`
    :

    `group_manage`
    :

    `group_read`
    :

    `journal_note_manage`
    :

    `key_manage`
    :

    `minio_manage`
    :

    `minio_read`
    :

    `minio_write`
    :

    `notification_manage`
    :

    `notification_read`
    :

    `output_browse`
    :

    `output_create`
    :

    `output_manage`
    :

    `output_read`
    :

    `policy_browse`
    :

    `policy_create`
    :

    `policy_manage`
    :

    `policy_read`
    :

    `postgres_manage`
    :

    `postgres_read`
    :

    `postgres_write`
    :

    `principal_browse`
    :

    `product_consume`
    :

    `product_register`
    :

    `product_remove`
    :

    `product_subscribe`
    :

    `product_update`
    :

    `resource_browse`
    :

    `secret_browse`
    :

    `secret_create`
    :

    `secret_manage`
    :

    `secret_read`
    :

    `self`
    :

    `service_core`
    :

    `spark_develop`
    :

    `star`
    :

    `statement_browse`
    :

    `tag_browse`
    :

    `tag_create`
    :

    `tag_manage`
    :

    `user_browse`
    :

    `user_create`
    :

    `user_delete`
    :

    `user_manage`
    :

    `validate`
    :

`EffectEnum(*args, **kwds)`
:   Default effect enum for use with IAM actions.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `allow`
    :

    `deny`
    :

`Partition(*args, **kwds)`
:   Create a collection of name/value pairs.
    
    Example enumeration:
    
    >>> class Color(Enum):
    ...     RED = 1
    ...     BLUE = 2
    ...     GREEN = 3
    
    Access them by:
    
    - attribute access:
    
      >>> Color.RED
      <Color.RED: 1>
    
    - value lookup:
    
      >>> Color(1)
      <Color.RED: 1>
    
    - name lookup:
    
      >>> Color['RED']
      <Color.RED: 1>
    
    Enumerations can be iterated over, and know how many members they have:
    
    >>> len(Color)
    3
    
    >>> list(Color)
    [<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]
    
    Methods can be added to enumerations, and members can have their own
    attributes -- see the documentation for details.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `ksa`
    :

`ResourceBase(all_: str | None = None, xrn: str = 'urn', partition: str = '', service: str = '', identifier: str = '', account_id: str = '', resource_type: str = '', sub_type: str = '', resource_id: str | None = None)`
:   Resource class contains information about resource.
    
    Args:
    ----
        partition (str): geographic location of the system
        service (str): name of the service, for the core-gateway it is fixed to the core
        identifier (t.Union[str, None]): identifier of the core
        account_id (t.Union[str, None]): owner id of the core
        resource_type (str): name of the resource type
        resource_id (t.Union[str, None]): identificator of the resource, can have a nested structure

    ### Ancestors (in MRO)

    * abc.ABC
    * neos_common.base.ResourceLike

    ### Static methods

    `format_resource_id(*args) ‑> str`
    :

    `generate(xrn: str = 'urn', partition: str = 'partition', service: str = 'service', identifier: str = 'identifier', account_id: str = 'owner', resource_type: str = 'resource_type', sub_type: str = '', resource_id: str | tuple | None = None, all_: str | None = None) ‑> ~RB`
    :   Generate Resource.

    `get_resource_id_template() ‑> str`
    :

    ### Instance variables

    `urn_template: str`
    :

`ResourceLike(all_: str | None = None, xrn: str = 'urn', partition: str = '', service: str = '', identifier: str = '', account_id: str = '', resource_type: str = '', sub_type: str = '', resource_id: str | None = None)`
:   ResourceLike(all_: str | None = None, xrn: str = 'urn', partition: str = '', service: str = '', identifier: str = '', account_id: str = '', resource_type: str = '', sub_type: str = '', resource_id: str | None = None)

    ### Descendants

    * neos_common.base.ResourceBase
    * neos_common.base.ResourceReader

    ### Class variables

    `ADDITIONAL_PATTERN_RULE`
    :

    `OPTIONAL_PATTERN_RULE`
    :

    `PATTERN_RULE`
    :

    `RESOURCE_PATTERN`
    :

    `SUB_RESOURCE_TYPE_RULE`
    :

    `account_id: str`
    :

    `additional_rule`
    :

    `all_: str | None`
    :

    `identifier: str`
    :

    `optional_rule`
    :

    `partition: str`
    :

    `resource_id: str | None`
    :

    `resource_type: str`
    :

    `rule`
    :

    `service: str`
    :

    `sub_rule`
    :

    `sub_type: str`
    :

    `xrn: str`
    :

    ### Static methods

    `parse(s: str) ‑> ~RL`
    :

    ### Instance variables

    `urn: str`
    :

`ResourceReader(all_: str | None = None, xrn: str = 'urn', partition: str = '', service: str = '', identifier: str = '', account_id: str = '', resource_type: str = '', sub_type: str = '', resource_id: str | None = None)`
:   ResourceReader(all_: str | None = None, xrn: str = 'urn', partition: str = '', service: str = '', identifier: str = '', account_id: str = '', resource_type: str = '', sub_type: str = '', resource_id: str | None = None)

    ### Ancestors (in MRO)

    * neos_common.base.ResourceLike

    ### Class variables

    `STAR`
    :

    ### Static methods

    `to_root(other: ~RR) ‑> ~RR`
    :

    ### Methods

    `is_any(self) ‑> bool`
    :

    `is_any_resource_id(self) ‑> bool`
    :

    `to_list(self) ‑> list[str]`
    :

`ResourceType(*args, **kwds)`
:   Create a collection of name/value pairs.
    
    Example enumeration:
    
    >>> class Color(Enum):
    ...     RED = 1
    ...     BLUE = 2
    ...     GREEN = 3
    
    Access them by:
    
    - attribute access:
    
      >>> Color.RED
      <Color.RED: 1>
    
    - value lookup:
    
      >>> Color(1)
      <Color.RED: 1>
    
    - name lookup:
    
      >>> Color['RED']
      <Color.RED: 1>
    
    Enumerations can be iterated over, and know how many members they have:
    
    >>> len(Color)
    3
    
    >>> list(Color)
    [<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]
    
    Methods can be added to enumerations, and members can have their own
    attributes -- see the documentation for details.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `account`
    :

    `core`
    :

    `data_product`
    :

    `data_source`
    :

    `data_system`
    :

    `data_unit`
    :

    `dataset`
    :

    `group`
    :

    `journal_note`
    :

    `mesh`
    :

    `minio`
    :

    `notification`
    :

    `output`
    :

    `policy`
    :

    `postgres`
    :

    `principal`
    :

    `product`
    :

    `resource`
    :

    `secret`
    :

    `signature`
    :

    `spark`
    :

    `statement`
    :

    `tag`
    :

    `token`
    :

    `user`
    :

`Service(*args, **kwds)`
:   Create a collection of name/value pairs.
    
    Example enumeration:
    
    >>> class Color(Enum):
    ...     RED = 1
    ...     BLUE = 2
    ...     GREEN = 3
    
    Access them by:
    
    - attribute access:
    
      >>> Color.RED
      <Color.RED: 1>
    
    - value lookup:
    
      >>> Color(1)
      <Color.RED: 1>
    
    - name lookup:
    
      >>> Color['RED']
      <Color.RED: 1>
    
    Enumerations can be iterated over, and know how many members they have:
    
    >>> len(Color)
    3
    
    >>> list(Color)
    [<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]
    
    Methods can be added to enumerations, and members can have their own
    attributes -- see the documentation for details.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `core`
    :

    `iam`
    :

    `registry`
    :