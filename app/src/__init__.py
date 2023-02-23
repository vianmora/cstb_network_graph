import logging
from importlib.resources import open_text
from pathlib import Path
from typing import Any, Dict

import pandas as pd
import yaml


def get_secrets():
    with open_text(__name__, f"secrets.yml") as f:
        return yaml.safe_load(f)


def get_temps_planifie(equipe:str = 'rgp') -> 'Dict[str, Any]':
    path_tps_planifie = [file for file in Path(f"./{__name__.replace('.', '/')}").iterdir() if f'temps-reel-planifie_{equipe}' in str(file)][0]

    dict_tps_planifie = pd.read_excel(path_tps_planifie, None, header=1)
    dict_agents = pd.read_excel(path_tps_planifie, None, nrows=0)

    dict_return = {'date_maj':str(path_tps_planifie).split('_')[2], 'agents':{}}
    for k in dict_tps_planifie:
        dict_return['agents'][k] = {'info_temps': dict_tps_planifie[k], 'info_agent': dict_agents[k]}

    return dict_return
