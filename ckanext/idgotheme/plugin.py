# coding: utf-8

import ckan.plugins as p
import ckan.plugins.toolkit as toolkit
from ckan.common import config
from collections import OrderedDict
import json

from ckanext.scheming.plugins import _SchemingMixin

import ckan.authz as authz




def get_url_wp():
    url_site_wp = config.get('ckanext.idgotheme.url_site_wp', '')
    return url_site_wp

def get_url_publier():
    url_site_publier = config.get('ckanext.idgotheme.url_site_publier', '')
    return url_site_publier



# Traduction "Groupes" en "Thématiques"
THEMATIQUE_MIN = u'thématique'
THEMATIQUE_MAJ = u'Thématique'
THEMATIQUES_MIN = u'thématiques'
THEMATIQUES_MAJ= u'Thématiques'


def trad_thematique_min():
    return THEMATIQUE_MIN

def trad_thematique_maj():
    return THEMATIQUE_MAJ

def trad_thematiques_min():
    return THEMATIQUES_MIN

def trad_thematiques_maj():
    return THEMATIQUES_MAJ



# Plugin
class IdgothemePlugin(p.SingletonPlugin, _SchemingMixin):
    p.implements(p.IConfigurer)
    p.implements(p.IFacets, inherit=True)
    p.implements(p.IPackageController, inherit=True)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IAuthFunctions)

    SCHEMA_OPTION = 'scheming.dataset_schemas'
    FALLBACK_OPTION = 'scheming.dataset_fallback'
    SCHEMA_TYPE_FIELD = 'dataset_type'

    # ITemplateHelpers : Custom Helpers functions
    def get_helpers(self):
        return {'idgotheme_get_url_wp': get_url_wp,
		'idgotheme_get_url_publier': get_url_publier,
                'trad_thematique_min' : trad_thematique_min,
                'trad_thematique_maj' : trad_thematique_maj,
                'trad_thematiques_min' : trad_thematiques_min,
                'trad_thematiques_maj' : trad_thematiques_maj}

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'idgotheme')

    
    # IFacets
    def dataset_facets(self, facets_dict, package_type):
        
        # Ajouter les filtres, dans l'ordre d'affichage sur la page
 	return OrderedDict([
                             ('organization', u'Organisations'),
                             ('groups', u'Thématiques'),
                             ('datatype', u'Types'),
                             ('support', u'Supports'),
                             ('res_format', u'Formats'),
                             ('license_id', u'Licences'),
                             ('tags', u'Mots-clés'),
                             ('update_frequency', u'Fréquence de mise à jour'),
                             ])

    # IPackageController
    def before_index(self, data_dict):
        data_dict['datatype'] = json.loads(data_dict.get('datatype', '[]'))
        return data_dict








    
