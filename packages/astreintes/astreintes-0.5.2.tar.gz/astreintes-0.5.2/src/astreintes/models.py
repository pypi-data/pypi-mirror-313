from typing import Optional
from pydantic import BaseModel, conint, NonNegativeInt, PositiveInt
import pandera
from pandera.typing import Series

N_SEMAINES = 52
MAX_ASTREINTES = 13

# todo test sum(site.n_rotation) >= min_aga + min_respi


class Parametres(BaseModel):
    max_astreintes: conint(ge=0, le=N_SEMAINES) = MAX_ASTREINTES
    min_aga: Optional[NonNegativeInt] = 1
    min_respi: Optional[NonNegativeInt] = 1
    n_iter_shuffle: Optional[PositiveInt] = 10_000
    seed: Optional[int] = None


class Sites(pandera.DataFrameModel):
    nom: Series[str] = pandera.Field(coerce=True)
    aga: Series[int] = pandera.Field(coerce=True, gt=0)
    respi: Series[int] = pandera.Field(coerce=True, gt=0)
    rotations: Series[int] = pandera.Field(coerce=True, ge=0)


class Effectifs(pandera.DataFrameModel):
    nom: Series[str] = pandera.Field(coerce=True)
    specialite: Series[str] = pandera.Field(isin=['aga', 'respi'])
    site: Series[str] = pandera.Field(coerce=True)
    preference: Series[float] = pandera.Field(coerce=True, ge=0, le=200)
    id_tech: Series[int] = pandera.Field(coerce=True, ge=0)
