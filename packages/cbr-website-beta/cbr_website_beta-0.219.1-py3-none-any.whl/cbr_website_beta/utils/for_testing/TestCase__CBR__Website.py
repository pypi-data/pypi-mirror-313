from unittest import TestCase

from tests.unit.app__for_tests import fast_api__cbr__client, fast_api__cbr


class TestCase__CBR__Website(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.client       = fast_api__cbr__client
        cls.cbr_fast_api = fast_api__cbr
        cls.cbr_athena   = cls.cbr_fast_api.cbr__athena()



