import numpy as np
import pandas as pd
import logging

import astreintes.models as models
from astreintes.models import N_SEMAINES

_logger = logging.getLogger(__name__)


def _repartition(p, n_semaines=N_SEMAINES, max_astreintes=13):
    """
    Calcule la répartition d'un nombre entier (en général semaines) en len(p) personnes,
    avec un maximum (13 par défaut) et des affinités (vecteur p).
    :param p: préférence pour chaque technicien ou site
    :param n_semaines: nombre de semaines à répartir, 52 semaines par an par default
    :param max_astreintes: 13 semaines maximum par technicien par défault,
    peut-être un scalaire ou un vecteur size(p)
    :return:
    """
    p = p / p.sum()  # on normalise les probabilités à 1
    max_astreintes = np.zeros_like(p) + max_astreintes if np.isscalar(max_astreintes) else max_astreintes
    # pas le droit à plus de n_semaines par an, tout en restant normalisé à un
    i = p > max_astreintes / n_semaines
    if np.sum(i):
        p[i] = max_astreintes[i] / n_semaines
        p[~i] = p[~i] * (1 - p[i]) / np.sum(p[~i])
    # on répartit du mieux possible les arrondis selon les affinités
    f = n_semaines / p.sum()
    n = np.floor(f * p).astype(int)
    decimal = f * p - n
    n_missing = int(n_semaines - n.sum())
    # Indices des plus grandes décimales
    i = np.argsort(-decimal)[:n_missing]  # stable=True on np >= 2.0
    n[i] += 1
    return n


def _assignation(counts, seed=None):
    """
    Assigne les astreintes a partir d'un vecteur ou chaque entrée représente le nombre d'astreintes
    par personne.
    :param counts:
    :param seed:
    :return:
    """
    if seed is not None:
        np.random.seed(seed)
    n_semaines = counts.sum()
    assign = np.zeros(n_semaines, dtype=int)
    remaining = counts.copy()
    last = -1
    for i in np.arange(n_semaines):
        j = np.where(remaining == np.max(remaining))[0]
        if len(j) > 1:
            j = np.random.choice(np.setdiff1d(j, last))
        else:
            j = j[0]
        assign[i] = j
        remaining[j] -= 1
        last = j
    return assign


def _sites2effectifs(df_sites: pd.DataFrame) -> pd.DataFrame:
    """
    Crée une dataframe d'effectifs fictive à partir d'une dataframe sites
    Les techs AGA sont nommés A0 - A1 ... , les techs respi R0 - R1 ...
    :param df_sites:
    :return: df_effectifs
    """
    df_effectifs = []
    for j in range(df_sites.shape[0]):
        df_effectifs.append(
            pd.DataFrame(
                {
                    'specialite': ['aga'] * df_sites.loc[j, 'aga'] + ['respi'] * df_sites.loc[j, 'respi'],
                    'nom': [f'A{i}' for i in np.arange(df_sites.loc[j, 'aga'])]
                    + [f'R{i}' for i in np.arange(df_sites.loc[j, 'respi'])],
                    'site': df_sites.loc[j, 'nom'],
                }
            )
        )
    df_effectifs = pd.concat(df_effectifs)
    df_effectifs['preference'] = 1
    df_effectifs['id_tech'] = np.arange(df_effectifs.shape[0])
    df_effectifs.reset_index(inplace=True)
    return df_effectifs


def _shuffle_techs(itechs, semaines=None, n_iter=10_000):
    semaines = np.arange(itechs) if semaines is None else semaines

    def _varp(itechs, semaines):
        svar, nviol, ndelais = (0, 0, 0)
        for t in np.unique(itechs):
            it = np.where(itechs == t)[0]
            if len(it) == 0:
                continue
            dt = np.diff(semaines[it])
            svar += np.var(dt)
            nviol += np.sum(dt == 1)
            ndelais += np.sum(dt == 2) / 4
        return svar, nviol, ndelais

    var_ref, viol_ref, court_ref = _varp(itechs, semaines)
    _logger.debug(f'permutations, variance initiale: {var_ref}, consecutives:  {viol_ref}')
    # on permute n_iter fois et on ne retient que les permutations qui font baisser la variance
    for _ in np.arange(n_iter):
        tt = itechs.copy()
        ii = np.random.choice(np.arange(itechs.size), 2, replace=False)
        tt[ii] = tt[np.flipud(ii)]
        var, viol, courtes = _varp(tt, semaines)
        # on rejette si on a une astreinte consécutive de plus
        if viol > viol_ref:
            continue
        # on rejette si les astreintes courtes sont plus importantes
        if courtes > court_ref:
            continue
        # la variance a baissé, on accepte la permutation
        if (var < var_ref) or (viol < viol_ref):
            itechs = tt.copy()
            var_ref, viol_ref = (var, viol)
    _logger.debug(f'permutations, variance acceptée: {var_ref}, consécutives: {viol_ref}')
    return itechs, viol_ref


def _shuffle_sites(planning, n_iter=10_000):
    """
    :param planning: (nrails, nsemaines)
    :param n_iter
    :return:
    """
    rng = np.random.default_rng()
    planning = planning[:, rng.permutation(planning.shape[1])]

    def _varp(p):
        svar = 0
        for site in np.unique(p):
            for r in np.arange(p.shape[0]):
                dd = np.diff(np.where(site == p[r, :])[0])
                svar += np.var(dd)
        return svar

    svar_ref = _varp(planning)
    _logger.debug(f'sites permutations, variance initiale: {svar_ref}')
    # on permute n_iter fois et on ne retient que les permutations qui font baisser la variance
    for _ in np.arange(n_iter):
        pp = planning.copy()
        ii = np.random.choice(np.arange(52), 2, replace=False)
        pp[:, ii] = pp[:, np.flipud(ii)]
        svar = _varp(pp)
        # la variance a baissé, on accepte la permutation
        if svar <= svar_ref:
            planning = pp.copy()
            svar_ref = svar
    _logger.debug(f'sites permutations, variance acceptee: {svar_ref}')
    return planning


def _planning_sites(counts, n_iter=0):
    """
    Organise le planning par site pour un nombre d'astreintes par site et par spécialité
    :param counts: np.array (nrails, nsites)
    :param shuffle: bool. On cherche les permutations qui minimisent la variance de la diff:
     ce sont celles qui répartissent le mieux les astreintes au long de l'année
    :return: np.array( nsemaines, nrails)
    """
    nr, ns = counts.shape
    planning = np.zeros((N_SEMAINES, nr), dtype=int) - 1
    for week in np.arange(N_SEMAINES):
        counts_ = counts.copy()
        sites_ = np.ones(nr, dtype=bool)
        for ir in np.arange(nr):
            # on cherche le site avec le plus d'astreintes a caser,
            # sauf s'il s'agit du précédent
            imaxs = np.argsort(-counts[ir, sites_])
            imax = imaxs[0]
            for im in imaxs:
                if im == planning[week - 1, ir]:
                    continue
                if counts[ir, im] > 0:
                    imax = im
                    break
            isite = np.where(sites_)[0][imax]
            planning[week, ir] = isite
            counts_[ir, :] = 0
            sites_[isite] = False
            counts[ir, isite] += -1
    planning = _shuffle_sites(planning.T, n_iter=n_iter) if n_iter else planning.T
    return planning


def _calcul_rotations(df_sites: pd.DataFrame, df_effectifs: pd.DataFrame, params: models.Parametres):
    n_sites = df_sites.shape[0]
    # première étape est de trouver la spécialité ayant le moins d'intervenants
    n_mixed = df_sites.rotations.sum() - params.min_aga - params.min_respi
    rails = params.min_aga * ['aga'] + params.min_respi * ['respi'] + n_mixed * ['mixed']
    df_rail = pd.DataFrame(dict(specialite=rails, **{n: 0 for n in df_sites['nom']}))
    if n_sites == 1:
        df_rail.loc[:, df_sites['nom']] = N_SEMAINES
        sites_per_rail = np.zeros((len(rails), N_SEMAINES), dtype=int)
    else:
        # on cherche la spécialité la plus sollicitée
        df_specialites = df_sites.loc[:, ['aga', 'respi']].min() / np.array([params.min_aga, params.min_respi])
        df_specialites = df_specialites.sort_values()
        df_specialites['mixed'] = df_sites.rotations.sum() - params.min_aga - params.min_respi
        df_specialites['aga'] = params.min_aga
        df_specialites['respi'] = params.min_respi
        rails = []
        for s, c in df_specialites.items():
            rails.extend([s] * int(c))
        df_rail = pd.DataFrame(dict(specialite=rails, **{n: 0 for n in df_sites['nom']}))
        site_preference = np.ones(n_sites)
        for ir, rail in df_rail.iterrows():
            if rail['specialite'] == 'mixed':
                npax = df_sites.loc[:, ['aga', 'respi']].values.sum(axis=1)
            else:
                npax = df_sites.loc[:, rail.specialite].values
            df_rail.loc[ir, df_sites['nom']] = _repartition(site_preference, max_astreintes=npax * params.max_astreintes)
            # on essaie de compenser avec les rails suivants pour balancer entre les sites
            site_preference = 1 / ((p := df_rail[df_sites['nom']].sum(axis=0).values) / sum(p))
        assert np.all(
            df_rail.loc[:, df_sites['nom']].sum(axis=1) == N_SEMAINES
        ), f"Certaines rotations n'on pas 52 semaines {df_rail}"
        assert np.all(
            df_rail.loc[:, df_sites['nom']].sum(axis=0) == N_SEMAINES
        ), f"Certains sites n'ont pas 52 semaines {df_rail}"
        sites_per_rail = _planning_sites(df_rail.loc[:, df_sites['nom']].values, n_iter=params.n_iter_shuffle)

    df_planning = []
    for i, rotation in enumerate(df_rail['specialite']):
        for isemaine, isite in enumerate(sites_per_rail[i]):
            df_planning.append(
                {
                    'site': df_sites.loc[isite, 'nom'],
                    'semaine': isemaine + 1,
                    'rotation': rotation,
                    'specialite': rotation,  # pour l'instant les mixed sont séparés
                }
            )
    df_planning = pd.DataFrame(df_planning).sort_values(by='semaine')

    # il faut ventiler les 'mixed' entre les spécialités selon les effectifs, on le fait en fonction de la charge des équipes site par site
    if n_mixed > 0:
        df_cspec = df_rail.groupby(['specialite']).sum()
        for site in df_sites['nom']:
            nr_aga, nr_respi, nr_mixed = (df_cspec.loc['aga', site], df_cspec.loc['respi', site], df_cspec.loc['mixed', site])
            n_aga, n_respi = df_sites.loc[df_sites['nom'] == site, ['aga', 'respi']].values.flatten()
            n_respi_mixed = np.maximum(
                0, int(np.round(((nr_aga + nr_mixed) / n_aga - nr_respi / n_respi) / (1 / n_respi + 1 / n_aga)))
            )
            imixed = np.where(np.logical_and(df_planning['site'] == site, df_planning['rotation'] == 'mixed').values)[0]
            np.random.shuffle(imixed)
            df_planning.iloc[imixed[:n_respi_mixed], df_planning.columns.get_loc('specialite')] = 'respi'
            df_planning.iloc[imixed[n_respi_mixed:], df_planning.columns.get_loc('specialite')] = 'aga'

    for site in df_sites['nom']:
        for specialite in df_planning['specialite'].unique():  # normalement ['aga', 'respi']
            ip = np.logical_and(df_planning['site'] == site, df_planning['specialite'] == specialite)
            semaines = df_planning.loc[ip, 'semaine'].values
            df_techs_ = df_effectifs[
                np.logical_and(
                    df_effectifs['site'] == site,
                    df_effectifs['specialite'] == specialite,
                )
            ]
            n_astreintes_per_tech = _repartition(
                p=df_techs_['preference'].values,
                n_semaines=semaines.size,
                max_astreintes=params.max_astreintes,
            )
            itechs_, n_consecutives = _shuffle_techs(
                _assignation(n_astreintes_per_tech), semaines=semaines, n_iter=params.n_iter_shuffle
            )
            for col in ['nom', 'id_tech', 'preference']:
                df_planning.loc[ip, col] = df_techs_.iloc[itechs_][col].values
            assert n_consecutives == 0
    assert np.isnan(df_planning['id_tech']).sum() == 0
    # ici la dataframe résultante a les colonnes semaine | site | rotation | id_tech | specialite
    return df_planning


def rapport_planning(df_planning: pd.DataFrame):
    """
    Aggrégations du planning d'un regroupement de sites:
    par technicien
    par site
    par spécialité
    :param df_planning:
    :return:
    """
    df_report_effectifs = (
        df_planning.groupby(['site', 'specialite', 'id_tech'])
        .agg(
            n_astreintes=pd.NamedAgg(column='semaine', aggfunc='count'),
            nom=pd.NamedAgg(column='nom', aggfunc='first'),
            delai_min=pd.NamedAgg(column='semaine', aggfunc=lambda x: np.min(np.diff(x)) if x.size > 1 else N_SEMAINES),
        )
        .reset_index()
    )
    df_report_sites = (
        df_planning.groupby(['site', 'rotation']).agg(n_semaines=pd.NamedAgg(column='semaine', aggfunc='nunique')).reset_index()
    )
    df_report_specialite = (
        df_planning.groupby(['specialite']).agg(n_semaines=pd.NamedAgg(column='semaine', aggfunc='nunique')).reset_index()
    )
    return df_report_effectifs, df_report_sites, df_report_specialite


def validation_planning(df_planning, params: models.Parametres):
    """
    :param df_planning:
    :param params:
    :return:
    """
    df_report_effectifs, df_report_sites, df_report_specialite = rapport_planning(df_planning)
    validation = {
        'astreintes_consecutives': np.all(df_report_effectifs.delai_min > 1),
        'quota employe depasse': np.all(df_report_effectifs.n_astreintes <= params.max_astreintes),
        'quota sites rempli': np.all(df_planning.groupby('site').nunique()['semaine'] == N_SEMAINES),
        'quota specialites rempli': np.all(df_report_specialite.n_semaines == N_SEMAINES),
    }
    return df_report_effectifs, df_report_sites, df_report_specialite, validation


def separation_calendriers(df_sites, df_effectifs=None, params=None):
    """
    Pour les regroupements de site complexes, il est plus facile de séparer le problème
    :param df_sites:
    :param df_effectifs
    :return:
    """
    assert params is not None
    df_effectifs = _sites2effectifs(df_sites) if df_effectifs is None else df_effectifs
    # le but est d'arriver à une seule rotation par site et/ou un seul site
    if np.all(df_sites['rotations'] == 1) or df_sites.shape[0] == 1:
        return [{'sites': df_sites, 'effectifs': df_effectifs, 'params': params}]
    # le premier passage est pour assigner les spécialités aux regroupements, en fonction du nombre minimum de chaque
    # specialite requis
    rotations = df_sites['rotations'].values.copy()
    rails = {'aga': params.min_aga, 'respi': params.min_respi}
    all_sites, all_groups = ([], [])
    for ig in np.arange(np.max(rotations)):
        ir = rotations > 0
        rotations[ir] = rotations[ir] - 1
        ns = np.sum(ir)
        # ici on donne 50/50 si il n'y a pas de préférence pour la spécialité
        ispe = np.mod(
            np.arange(ns) + (params.min_respi > params.min_aga) + (params.min_respi == params.min_aga) * np.random.choice([1, 0]),
            2,
        )
        min_aga, min_respi = (np.sum(ispe == 0), np.sum(ispe == 1))
        rails['aga'] -= min_aga
        rails['respi'] -= min_respi
        all_groups.append({'min_aga': min_aga, 'min_respi': min_respi, 'n_sites': ns})
        all_sites.append(pd.DataFrame({'nom': df_sites['nom'][ir], 'respi': -1, 'aga': -1, 'rotations': 1, 'groupe': ig}))
    all_sites = pd.concat(all_sites)
    all_groups = pd.DataFrame(all_groups)
    # le deuxieme passage permet de répartir les effectifs en fonction des spécialités ci-dessus
    df_effectifs['groupe'] = -1
    for _, site in df_sites.iterrows():
        isites = all_sites['nom'] == site.nom
        ig = all_sites.loc[isites, 'groupe'].unique()
        ratios = all_groups.loc[ig, ['min_aga', 'min_respi']].values / all_groups.loc[ig, 'n_sites'].values[:, np.newaxis]
        for ispe, specialite in enumerate(['aga', 'respi']):
            rep = _repartition(ratios[:, ispe], n_semaines=site[specialite], max_astreintes=999)
            all_sites.loc[isites, specialite] = rep
            ie = np.where((df_effectifs['site'] == site.nom) & (df_effectifs['specialite'] == specialite))[0]
            np.random.shuffle(ie)
            for igg, iee in zip(ig, np.split(ie, np.cumsum(rep[:-1]))):
                df_effectifs.loc[iee, 'groupe'] = igg
    # au final, on crée les dataframes sites, dataframe effectif et params pour chaque groupe dans une liste de dictionaires
    dse = []
    for ig, df_sites_ in all_sites.groupby('groupe'):
        params_ = params.model_dump() | {f: all_groups.loc[ig, f] for f in ['min_aga', 'min_respi']}
        dse.append(
            {
                'sites': df_sites_.copy().drop(columns='groupe').reset_index(drop=True),
                'effectifs': df_effectifs[df_effectifs['groupe'] == ig].copy().drop(columns='groupe').reset_index(drop=True),
                'params': models.Parametres(**params_),
            }
        )
    return dse


def genere_planning(
    df_sites: pd.DataFrame,
    params: models.Parametres = None,
    df_effectifs: pd.DataFrame = None,
    mode='raise',
):
    params = models.Parametres() if params is None else params
    models.Parametres.model_validate(params)
    # specialite  id_tech nom   site
    df_effectifs = _sites2effectifs(df_sites) if df_effectifs is None else df_effectifs

    liste_sites_effectifs = separation_calendriers(df_sites, df_effectifs, params=params)
    df_planning = []
    for dse in liste_sites_effectifs:
        # semaine   site  rotation  id_tech specialite
        df_planning.append(_calcul_rotations(dse['sites'], dse['effectifs'], params=dse['params']))
    df_planning = pd.concat(df_planning).sort_values(['site', 'specialite', 'semaine'])
    # validation du planning
    df_report_effectifs, df_report_sites, df_report_specialite, validation = validation_planning(df_planning, params=params)

    for k, v in validation.items():
        if not v:
            _logger.warning(f'{k} failed for site {df_sites}')
        if mode == 'raise':
            assert v, f'{k}'
    return (df_planning, df_report_effectifs, df_report_sites, df_report_specialite, validation)
