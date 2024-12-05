from .testcase import TestCase
from heaserver.service.testcase.mixin import GetAllMixin


class TestGetAll(TestCase, GetAllMixin):
    pass
