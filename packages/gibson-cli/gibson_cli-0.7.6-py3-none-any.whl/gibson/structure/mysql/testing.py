from gibson.structure.mysql.Entity import Entity


def structure_testing_get_entity():
    entity = Entity()
    entity.attributes = [
        {
            "check": None,
            "datastore": {
                "specifics": {
                    "as_": None,
                    "bytes_": None,
                    "comment": None,
                    "extra": {"increment": {"auto": True}},
                    "on": None,
                    "reference": None,
                    "unsigned": None,
                    "values": None,
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
                    "as_": None,
                    "bytes_": None,
                    "comment": None,
                    "extra": {"increment": {"auto": None}},
                    "on": None,
                    "reference": None,
                    "unsigned": None,
                    "values": None,
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
                    "as_": None,
                    "bytes_": None,
                    "comment": None,
                    "extra": {"increment": {"auto": None}},
                    "on": None,
                    "reference": None,
                    "unsigned": None,
                    "values": None,
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
                    "as_": None,
                    "bytes_": None,
                    "comment": None,
                    "extra": {"increment": {"auto": None}},
                    "on": "update current_timestamp",
                    "reference": None,
                    "unsigned": None,
                    "values": None,
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
    entity.table = {
        "parameters": {
            "auto": None,
            "charset": None,
            "collate": None,
            "default": None,
            "engine": None,
            "sql": None,
        }
    }

    return entity


def structure_testing_get_struct_data():
    return {
        "entity": {
            "name": "abc_def",
            "struct": {
                "attributes": [
                    {
                        "check": None,
                        "datstore": {
                            "specifics": {
                                "as_": None,
                                "bytes_": None,
                                "comment": None,
                                "extra": {"increment": {"auto": True}},
                                "on": None,
                                "reference": None,
                                "unsigned": None,
                                "values": None,
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
                                "as_": None,
                                "bytes_": None,
                                "comment": None,
                                "extra": {"increment": {"auto": None}},
                                "on": None,
                                "reference": None,
                                "unsigned": None,
                                "values": None,
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
                                "as_": None,
                                "bytes_": None,
                                "comment": None,
                                "extra": {"increment": {"auto": None}},
                                "on": None,
                                "reference": None,
                                "unsigned": None,
                                "values": None,
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
                                "as_": None,
                                "bytes_": None,
                                "comment": None,
                                "extra": {"increment": {"auto": None}},
                                "on": "update current_timestamp",
                                "reference": None,
                                "unsigned": None,
                                "values": None,
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
                "table": {
                    "parameters": {
                        "auto": None,
                        "charset": None,
                        "collate": None,
                        "default": None,
                        "engine": None,
                        "sql": None,
                    },
                },
            },
        }
    }
