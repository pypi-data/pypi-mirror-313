from . import Client as BaseClient


class Client(BaseClient):
    _class_reasoner = "cvc5"
