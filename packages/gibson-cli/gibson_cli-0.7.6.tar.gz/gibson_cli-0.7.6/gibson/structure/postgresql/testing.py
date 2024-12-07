from gibson.structure.postgresql.Entity import Entity


def structure_testing_get_entity():
    entity = Entity()
    entity.attributes = [
        {
            "check": None,
            "datastore": {
                "specifics": {
                    "references": None,
                }
            },
            "data_type": {"formatted": "bigint", "raw": "bigint"},
            "default": None,
            "key": {"index": None, "primary": True, "unique": None},
            "length": None,
            "name": "id",
            "nullable": False,
            "numeric": {"precision": None, "scale": None},
            "sql": "id bigint not null auto_increment primary key",
        },
        {
            "check": None,
            "datastore": {
                "specifics": {
                    "references": None,
                }
            },
            "data_type": {"formatted": "varchar(36)", "raw": "varchar"},
            "default": None,
            "key": {"index": None, "primary": None, "unique": True},
            "length": 36,
            "name": "uuid",
            "nullable": False,
            "numeric": {"precision": None, "scale": None},
            "sql": "uuid varchar(36) not null unique key",
        },
        {
            "check": None,
            "datastore": {
                "specifics": {
                    "references": None,
                }
            },
            "data_type": {"formatted": "datetime", "raw": "datetime"},
            "default": "current_timestamp",
            "key": {"index": None, "primary": None, "unique": None},
            "length": None,
            "name": "date_created",
            "nullable": False,
            "numeric": {"precision": None, "scale": None},
            "sql": "date_created datetime not null default current_timestamp",
        },
        {
            "check": None,
            "datastore": {
                "specifics": {
                    "references": None,
                }
            },
            "data_type": {"formatted": "datetime", "raw": "datetime"},
            "default": "null",
            "key": {"index": None, "primary": None, "unique": None},
            "length": None,
            "name": "date_updated",
            "nullable": None,
            "numeric": {"precision": None, "scale": None},
            "sql": "date_updated datetime default null on update current_timestamp",
        },
    ]
    entity.constraints = {"check": []}
    entity.keys = {"foreign": [], "index": [], "primary": None, "unique": []}
    entity.name = "abc_def"
    entity.table = None

    return entity


def structure_testing_get_struct_data():
    return {
        "entity": {
            "name": "abc_def",
            "struct": {
                "attributes": [
                    {
                        "check": None,
                        "datastore": {
                            "specifics": {
                                "references": None,
                            }
                        },
                        "data_type": {"formatted": "bigint", "raw": "bigint"},
                        "default": None,
                        "key": {"index": None, "primary": True, "unique": None},
                        "length": None,
                        "name": "id",
                        "nullable": False,
                        "numeric": {"precision": None, "scale": None},
                        "sql": "id bigint not null auto_increment primary key",
                    },
                    {
                        "check": None,
                        "datastore": {
                            "specifics": {
                                "reference": None,
                            }
                        },
                        "data_type": {"formatted": "varchar(36)", "raw": "varchar"},
                        "default": None,
                        "key": {"index": None, "primary": None, "unique": True},
                        "length": 36,
                        "name": "uuid",
                        "nullable": False,
                        "numeric": {"precision": None, "scale": None},
                        "sql": "uuid varchar(36) not null unique key",
                    },
                    {
                        "check": None,
                        "datastore": {
                            "specifics": {
                                "references": None,
                            }
                        },
                        "data_type": {"formatted": "datetime", "raw": "datetime"},
                        "default": "current_timestamp",
                        "key": {"index": None, "primary": None, "unique": None},
                        "length": None,
                        "name": "date_created",
                        "nullable": False,
                        "numeric": {"precision": None, "scale": None},
                        "sql": "date_created datetime not null default current_timestamp",
                    },
                    {
                        "check": None,
                        "datastore": {
                            "specifics": {
                                "references": None,
                            }
                        },
                        "data_type": {"formatted": "datetime", "raw": "datetime"},
                        "default": "null",
                        "key": {"index": None, "primary": None, "unique": None},
                        "length": None,
                        "name": "date_updated",
                        "nullable": None,
                        "numeric": {"precision": None, "scale": None},
                        "sql": "date_updated datetime default null on update "
                        + "current_timestamp",
                    },
                ],
                "constraints": {"check": []},
                "keys": {"foreign": [], "index": [], "primary": None, "unique": []},
                "table": None,
            },
        }
    }
