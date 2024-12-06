import unittest
import numpy as np
import pandas as pd
import astreintes.calculs
import astreintes.models


class TestRepartition(unittest.TestCase):
    def test_n_astreintes(self):
        np.testing.assert_array_equal(np.array([9, 9, 9, 9, 8, 8]), astreintes.calculs._repartition(p=np.ones(6) * 100))

        np.testing.assert_array_equal(
            np.array([8, 9, 9, 9, 8, 9]),
            astreintes.calculs._repartition(p=np.array([0.99, 1, 1, 1, 1, 1.03]) * 100),
        )

        np.testing.assert_array_equal(
            np.array([13, 10, 10, 10, 9]),
            astreintes.calculs._repartition(np.array([4, 1, 1, 1, 1]) * 100),
        )

        np.testing.assert_array_equal(
            np.array([16, 36]),
            astreintes.calculs._repartition(np.array([2, 3]), max_astreintes=np.array([2, 5]) * 8),
        )


class TestAssignation(unittest.TestCase):
    def test_assign(self):
        a = astreintes.calculs._assignation(np.array([26, 26]), seed=1234)
        np.testing.assert_array_equal(a, (np.arange(52) + 1) % 2)


class TestPlanningSites(unittest.TestCase):
    def test_planning_sites(self):
        # colonnes sites, lignes rails

        def validate_planning(planning, n):
            assert np.all(np.bincount(planning.flatten()) == 52)
            for i in range(n):
                np.testing.assert_array_equal(np.sum(planning == i, axis=0), 1)
            assert not np.any(planning == -1)

        counts = np.array([[22, 15, 15], [13, 20, 19], [17, 17, 18]])
        validate_planning(astreintes.calculs._planning_sites(counts), n=3)

        counts = np.array([[39, 13], [13, 39]])
        validate_planning(astreintes.calculs._planning_sites(counts), n=2)


class TestCalendriers(unittest.TestCase):
    def test_partage_calendriers_111(self):
        params = astreintes.models.Parametres(min_aga=1, min_respi=1)
        df_sites = pd.DataFrame(
            {
                'nom': ['Fleury', 'Nanterre', 'Bobigny'],
                'aga': [6, 9, 10],
                'respi': [14, 16, 19],
                'rotations': [1, 1, 1],
            }
        )
        d = astreintes.calculs.separation_calendriers(df_sites, params=params)[0]
        pd.testing.assert_frame_equal(d['sites'], df_sites)

    def test_partage_calendriers_123(self):
        params = astreintes.models.Parametres(min_aga=2, min_respi=4)
        df_sites = pd.DataFrame(
            {
                'nom': ['Fleury', 'Nanterre', 'Bobigny'],
                'aga': [6, 9, 10],
                'respi': [14, 16, 19],
                'rotations': [1, 2, 3],
            }
        )
        d = astreintes.calculs.separation_calendriers(df_sites, params=params)
        for dd in d:
            print(dd['sites'])
        assert [dd['sites'].shape[0] for dd in d] == [3, 2, 1]

    def test_partage_calendriers_124(self):
        params = astreintes.models.Parametres(min_aga=3, min_respi=4)
        df_sites = pd.DataFrame(
            {
                'nom': ['Fleury', 'Nanterre', 'Bobigny'],
                'aga': [6, 9, 10],
                'respi': [14, 16, 19],
                'rotations': [1, 2, 4],
            }
        )
        d = astreintes.calculs.separation_calendriers(df_sites, params=params)
        self.assertEqual([dd['sites'].shape[0] for dd in d], [3, 2, 1, 1])

    def test_partage_calendriers_222(self):
        params = astreintes.models.Parametres(min_aga=3, min_respi=3)
        df_sites = pd.DataFrame(
            {
                'nom': ['Fleury', 'Nanterre', 'Bobigny'],
                'aga': [6, 9, 10],
                'respi': [14, 16, 19],
                'rotations': [2, 2, 2],
            }
        )
        d = astreintes.calculs.separation_calendriers(df_sites, params=params)
        assert [dd['sites'].shape[0] for dd in d] == [3, 3]
