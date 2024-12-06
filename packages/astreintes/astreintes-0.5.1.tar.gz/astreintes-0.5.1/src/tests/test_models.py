import unittest
from astreintes import models


class TestModeles(unittest.TestCase):
    def test_params(self):
        params = models.Parametres(seed=1234)
        self.assertTrue(params.max_astreintes == 13)
