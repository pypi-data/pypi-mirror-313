import gspread
import pandas as pd
import traceback

import astreintes.models
import astreintes.calculs

FOLDER_ID = '18iaecTVG9ZDjGRDHsErAUJthK5ij6myV'


def _df_to_wks(df: pd.DataFrame, wks: gspread.Worksheet, cell: str = 'A2') -> None:
    """
    Met à jour une feuille Google Sheet avec un DataFrame, à partir d'une cellule de départ.
    """
    nr, nc = df.shape
    r0, c0 = gspread.utils.a1_to_rowcol(cell)
    range_str = f'{cell}:{gspread.utils.rowcol_to_a1(nr + r0 - 1, nc + c0 - 1)}'
    wks.update(range_name=range_str, values=df.values.tolist(), value_input_option='USER_ENTERED')


def create_or_get_sheet(
    wkb: gspread.spreadsheet.Spreadsheet, title: str, clear: bool = False, rows: int = 128, cols: int = 32
) -> gspread.Worksheet:
    """
    :param wkb:
    :param clear:
    :param rows:
    :param cols:
    :return:
    """
    wks = next((wk for wk in wkb.worksheets() if wk.title == title), None)
    if wks is None:
        wks = wkb.add_worksheet(title=title, rows=rows, cols=cols)
    else:
        if clear:
            wks.clear()
    return wks


class FeuilleAstreinte:
    def __init__(self, gc: gspread.Client, nom_feuille: str, folder_id: str = FOLDER_ID):
        self.gc: gspread.Client = gc
        self.nom_feuille: str = nom_feuille
        self.folder_id: str = folder_id
        self.wkb = self.gc.open(nom_feuille)

    def get_parametres(self) -> astreintes.models.Parametres:
        """
        Lit les paramètres depuis un range défini et valide/convertit dans le schéma de paramètres
        :return:
        """
        wks = self.wkb.worksheet('Paramètres')
        params = wks.get_values('C3:C7')
        params = {k: p[0] for k, p in zip(astreintes.models.Parametres.model_fields, params)}
        params = astreintes.models.Parametres(**params)
        return params

    def get_sites(self) -> pd.DataFrame:
        """
        Lit la liste des sites et leurs attributs depuis le range défini et valide
        :return:
        """
        wks = self.wkb.worksheet('Paramètres')
        sites = wks.get_values('E3:H8')
        df_sites = pd.DataFrame(sites, columns=['nom', 'aga', 'respi', 'rotations'])
        df_sites = astreintes.models.Sites.validate(df_sites)
        return df_sites

    def get_effectifs(self) -> pd.DataFrame:
        """
        Lit la liste des effectifs depuis le range défini et applique la validation
        :return:
        """
        wks = self.wkb.worksheet('Effectifs')
        effectifs = wks.get_values('A2:E146')
        df_effectifs = pd.DataFrame(effectifs, columns=['id_tech', 'nom', 'site', 'specialite', 'preference'])
        df_effectifs = astreintes.models.Effectifs.validate(df_effectifs)
        return df_effectifs

    def calcul(self):
        self.wkb.worksheet('Paramètres').batch_clear(['E12:E13'])
        params = self.get_parametres()
        df_sites = self.get_sites()
        df_effectifs = self.get_effectifs()
        try:
            r = astreintes.calculs.genere_planning(df_sites, params=params, df_effectifs=df_effectifs)
            df_planning, df_report_effectifs, df_report_sites, df_report_specialite, validation = r
        except Exception as e:
            traceback_str = traceback.format_exc()
            error_str = f'Erreur lors du calcul: {e.__class__.__name__}: {str(e)}'
            self.wkb.worksheet('Paramètres').update_cell(row=12, col=5, value=error_str)
            self.wkb.worksheet('Paramètres').update_cell(row=13, col=5, value=traceback_str)
            raise e

        # on classe le planning et on enlève la colonne de préférences
        _df_to_wks(
            df=df_planning.loc[:, ['site', 'semaine', 'specialite', 'id_tech']].sort_values(by=['site', 'semaine', 'specialite']),
            wks=self.wkb.worksheet('Planning'),
            cell='A2',
        )
        # on exporte le nombre d'astreintes par tech et le délai minimum
        # on fait un merge de façon à s'assurer que les colonnes correspondent à la feuille excel
        effectifs_data = df_effectifs.merge(
            df_report_effectifs.loc[:, ['id_tech', 'n_astreintes', 'delai_min']],
            right_on='id_tech',
            left_on='id_tech',
            how='left',
        )
        effectifs_data.fillna(0, inplace=True)
        _df_to_wks(df=effectifs_data.loc[:, ['n_astreintes', 'delai_min']], wks=self.wkb.worksheet('Effectifs'), cell='G2')
        _df_to_wks(df=df_report_sites, wks=self.wkb.worksheet('Rapports'), cell='A2')
        _df_to_wks(df=df_report_specialite, wks=self.wkb.worksheet('Rapports'), cell='E2')
        print(f'résultats écrit dans le fichier: {self.wkb.url}')
