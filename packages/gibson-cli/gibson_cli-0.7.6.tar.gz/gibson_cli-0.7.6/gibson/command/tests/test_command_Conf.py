from gibson.command.Conf import Conf
from gibson.core.Configuration import Configuration


def test_get_configuration_keys():
    assert Conf(Configuration()).get_configuration_keys() == [
        "id",
        "api::key",
        "code::custom::model::class",
        "code::custom::model::path",
        "code::frameworks::api",
        "code::frameworks::model",
        "code::frameworks::revision",
        "code::frameworks::schema",
        "code::frameworks::test",
        "code::language",
        "datastore::type",
        "datastore::uri",
        "meta::project::description",
    ]
