from importlib.resources import open_text
import yaml
import os
import airtable
import pandas as pd
import numpy as np
from pathlib import Path

from app.src import get_secrets, get_temps_planifie


def get_data_for_network(equipe:str = 'rgp'):
    # get secrets
    secrets = get_secrets()

    # Airtable treatment
    # ------------------

    # Connection to airtable
    at = airtable.Airtable(secrets['rgp_base_id'], secrets['api_key'])

    # DataFrame des agents
    df_agent_at = pd.DataFrame(columns=['prenom', 'nom', 'url_photo'])
    df_agent_at.index.name='agent_id'
    for record in at.get('Agents RGP')['records']:
        df_agent_at.loc[record['id']] = [record['fields']['prenom'].capitalize(), record['fields']['nom'].upper(), record['fields']['photo'][0]['url']]

    # DataFrame des projets
    df_project_at = pd.DataFrame(columns=['nom', 'url_image'])
    df_project_at.index.name='project_id'
    for record in at.get('Projets')['records']:
        df_project_at.loc[record['id']] = [record['fields']['nom'] if 'nom' in record['fields'] else 'projetInconnu',
                                        record['fields']['image_projet'][0]['url'] if 'image_projet' in record['fields'] else './app/src/local-file-not-found.png',
                                       ]

    # DataFrame des relations agent_projet
    df_rel_agent_projet_at = pd.DataFrame(columns=['project_id', 'agent_id'])
    i=0
    for record in at.get('Projets')['records']:
        if 'Membres RGP' in record['fields']:
            df_rel_agent_projet_at.loc[i] = [record['id'], record['fields']['Membres RGP']]
            i+=1
    df_rel_agent_projet_at = df_rel_agent_projet_at.explode('agent_id').set_index(['project_id', 'agent_id']).reset_index()


    # Gestaf treatment
    # -----------------

    dict_gestaf = get_temps_planifie(equipe)

    # DataFrame agents
    df_agent = pd.DataFrame(columns=['prenom', 'nom', 'mail', 'projete_total'])
    df_agent.index.name = 'agent_id'
    for agent_id, agent_dict in dict_gestaf['agents'].items():
        blopblop = list(agent_dict['info_agent'].columns)
        df_agent.loc[agent_id] = [blopblop[1].replace('_', '-').capitalize(), blopblop[0].upper(), blopblop[2],
                               agent_dict['info_temps']['Projetés'].to_list()[-2]]

    # DataFrame projets
    df_project = pd.DataFrame(columns=['project_otp', 'projete_total'])
    df_project.index.name = 'nom'
    df_rel_agent_projet = pd.DataFrame(columns=['agent_id', 'nom_project', 'projete'])
    i = 0
    for agent_id, agent in dict_gestaf['agents'].items():
        for project in agent['info_temps'].itertuples():
            if (project._1 not in ['TOTAL', 'Activités non rémunérées']) \
                    and (project._4 not in ['Planifié']) \
                    and (not np.isnan(project.Projetés)):
                df_rel_agent_projet.loc[i] = [agent_id, project._2, int(project.Projetés)]
                if project._2 not in df_project.index:
                    df_project.loc[project._2] = [project._3, int(project.Projetés)]
                else:
                    df_project.loc[project._2, 'projete_total'] = df_project.loc[
                                                                      project._2, 'projete_total'] + project.Projetés
                i += 1

    # enrichie et nettoie les tables

    # récupère les photos depuis airtable
    df_agent_merge = df_agent_at.merge(df_agent.reset_index(), on=['nom', 'prenom'], how='outer').set_index('agent_id')
    df_agent_merge.loc[df_agent_merge['url_photo'].isna(), 'url_photo'] = './app/src/local-file-not-found.png'

    # filtre les liens qui représentent moins de 3% de la charge des personnes
    df_rel_merge = df_rel_agent_projet.merge(df_agent_merge.reset_index(), on='agent_id', how='left').drop(['url_photo', 'mail'], axis=1)
    df_rel_agent_projet_filtered = df_rel_merge[df_rel_merge['projete']/df_rel_merge['projete_total']>0.03].drop(['prenom', 'nom', 'projete_total'], axis=1)

    # supprime les projets peu prenants
    df_project_filtered = df_project.loc[df_rel_agent_projet_filtered['nom_project'].unique()]

    # jsonify
    nodes = [dict(id    = f"{agent.prenom.capitalize()} {agent.nom.capitalize()[:2]}.",
                  label = f"{agent.prenom.capitalize()} {agent.nom.capitalize()[:2]}.",
                  title = f"{agent.prenom} {agent.nom}",
                  image = agent.url_photo,
                  color = '#15443C',
                  shape = 'circularImage',
                  font = dict(size=12, color='#15443C', face="arial"),
                 )
             for agent in df_agent_merge.itertuples()]

    nodes += [dict(id    = project.Index,
                   label = project.Index,
                   title = f"OTP : {project.project_otp}",
                   size  = project.projete_total/30,
                   color = '#C3443C',
                   shape = 'circularImage',
                   image = '',
                   font = dict(size=9, color='#C3443C', face="arial"),
                 )
              for project in df_project_filtered.itertuples()]

    edges = [{'from': f"{df_agent_merge.loc[t.agent_id]['prenom'].capitalize()} {df_agent_merge.loc[t.agent_id]['nom'].capitalize()[:2]}.",
              'to'  : t.nom_project}
             for t in df_rel_agent_projet_filtered.itertuples()]

    return {"nodes": nodes, "edges": edges}
