import os

from gibson.conf.dev.Api import Api
from gibson.conf.dev.Base import Base
from gibson.conf.dev.Model import Model
from gibson.conf.dev.Schema import Schema


class Dev:
    def __init__(self):
        self.active = False
        self.api = Api()
        self.base = Base()
        self.model = Model()
        self.schema = Schema()
