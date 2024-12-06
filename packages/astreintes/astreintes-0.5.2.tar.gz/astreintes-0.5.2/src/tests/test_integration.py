import unittest
import pandas as pd
import astreintes.calculs
import astreintes.models

params = astreintes.models.Parametres(n_iter_shuffle=1000)


class TestGenerePlanning(unittest.TestCase):
    def test_un_seul_site_un_rail(self):
        params = astreintes.models.Parametres(n_iter_shuffle=1000, min_aga=0, min_respi=1)
        df_sites = pd.DataFrame(
            {
                'nom': ['Clermont'],
                'aga': [6],
                'respi': [4],
                'rotations': [1],
            }
        )
        astreintes.calculs.genere_planning(df_sites, mode='raise', params=params)

    def test_un_seul_site_deux_rails(self):
        df_sites = pd.DataFrame(
            {
                'nom': ['Clermont'],
                'aga': [6],
                'respi': [4],
                'rotations': [2],
            }
        )
        astreintes.calculs.genere_planning(df_sites, mode='raise', params=params)

    def test_deux_sites(self):
        df_sites = pd.DataFrame(
            {
                'nom': ['Caen', 'Rouen'],
                'aga': [6, 3],
                'respi': [2, 3],
                'rotations': [1, 1],
            }
        )
        astreintes.calculs.genere_planning(df_sites, mode='raise', params=params)

    def test_deux_sites_un_seul_respi(self):
        df_sites = pd.DataFrame(
            {
                'nom': ['Caen', 'Rouen'],
                'aga': [6, 6],
                'respi': [1, 8],
                'rotations': [1, 1],
            }
        )
        astreintes.calculs.genere_planning(df_sites, mode='raise', params=params)

    def test_trois_sites_juste_2_respis(self):
        df_sites = pd.DataFrame(
            {
                'nom': ['Albi', 'Foix', 'Toulouse'],
                'aga': [3, 5, 9],
                'respi': [4, 2, 7],
                'rotations': [1, 1, 1],
            }
        )
        astreintes.calculs.genere_planning(df_sites, mode='raise', params=params)

    def test_trois_sites_mixed(self):
        df_sites = pd.DataFrame(
            {
                'nom': ['Marseille', 'Toulon', 'Nice'],
                'aga': [8, 3, 4],
                'respi': [4, 3, 3],
                'rotations': [1, 1, 1],
            }
        )
        astreintes.calculs.genere_planning(df_sites, mode='raise', params=params)

    def test_trois_sites_1_aga_2_respis(self):
        params = astreintes.models.Parametres(min_respi=2, min_aga=1, seed=1234, n_iter_shuffle=1000)
        # exemple Pays de la Loire
        df_sites = pd.DataFrame(
            {
                'nom': ['Angers', 'Le Mans', 'Nantes'],
                'aga': [4, 5, 6],
                'respi': [5, 5, 13],
                'rotations': [1, 1, 1],
            }
        )
        astreintes.calculs.genere_planning(df_sites, mode='raise', params=params)

    def test_trois_sites_et_plusieurs_rails(self):
        params = astreintes.models.Parametres(min_respi=4, min_aga=2, seed=1234, n_iter_shuffle=1000)
        df_sites = pd.DataFrame(
            {
                'nom': ['Fleury', 'Nanterre', 'Bobigny'],
                'aga': [6, 9, 10],
                'respi': [14, 16, 19],
                'rotations': [1, 2, 3],
            }
        )
        astreintes.calculs.genere_planning(df_sites, mode='raise', params=params)

    def test_quatre_sites_et_deux_rails(self):
        params = astreintes.models.Parametres(min_respi=2, min_aga=2, seed=1234, n_iter_shuffle=1000)
        df_sites = pd.DataFrame(
            {
                'nom': ['Fleury', 'Nanterre', 'Bobigny', 'Rungis'],
                'aga': [6, 9, 10, 7],
                'respi': [14, 16, 19, 4],
                'rotations': [1, 1, 1, 1],
            }
        )
        astreintes.calculs.genere_planning(df_sites, mode='raise', params=params)
