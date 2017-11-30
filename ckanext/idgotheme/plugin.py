import ckan.plugins as p
import ckan.plugins.toolkit as toolkit
from ckan.common import config
from collections import OrderedDict
import json

#from ckan.common import c
#from ckantoolkit import (
#    DefaultDatasetForm,
#    DefaultGroupForm,
#    DefaultOrganizationForm,
#    get_validator,
#    get_converter,
#    navl_validate,
#    add_template_directory,
#)

#from ckanext.scheming import helpers
#from ckanext.scheming import loader
#from ckanext.scheming.errors import SchemingException
#from ckanext.scheming.validation import (
#    validators_from_string, scheming_choices, scheming_required,
#    scheming_multiple_choice, scheming_multiple_choice_output)
#from ckanext.scheming.logic import (
#    scheming_dataset_schema_list, scheming_dataset_schema_show,
#    scheming_group_schema_list, scheming_group_schema_show,
#    scheming_organization_schema_list, scheming_organization_schema_show,
#    )
#from ckanext.scheming.converters import (
#        convert_from_extras_group, convert_to_json_if_date
#        )
from ckanext.scheming.plugins import _SchemingMixin
#from ckanext.scheming.plugins import DefaultDatasetForm
#from ckan.lib.plugins import DefaultDatasetForm


def get_url_wp():
    url_site_wp = config.get('ckanext.idgotheme.url_site_wp', '')
    return url_site_wp

def get_url_publier():
    url_site_publier = config.get('ckanext.idgotheme.url_site_publier', '')
    return url_site_publier



# Plugin
class IdgothemePlugin(p.SingletonPlugin, _SchemingMixin):
    p.implements(p.IConfigurer)
    p.implements(p.IFacets, inherit=True)
    p.implements(p.IPackageController, inherit=True)
    p.implements(p.ITemplateHelpers)

    SCHEMA_OPTION = 'scheming.dataset_schemas'
    FALLBACK_OPTION = 'scheming.dataset_fallback'
    SCHEMA_TYPE_FIELD = 'dataset_type'

    # ITemplateHelpers : Custom Helpers functions
    def get_helpers(self):
        return {'idgotheme_get_url_wp': get_url_wp,
		'idgotheme_get_url_publier': get_url_publier}

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'idgotheme')

    
    # IFacets
    def dataset_facets(self, facets_dict, package_type):
        
        # Ajouter les filtres, dans l'ordre d'affichage sur la page
 	return OrderedDict([
                             #Default facets
                             ('organization', toolkit._('Organization')),
                             ('groups', toolkit._('Groups')),
                             ('tags', toolkit._('Tags')),
                             ('res_format', toolkit._('Formats')),
                             ('license_id', toolkit._('Licence')),
                             #Add new facets
                             ('support', 'Support'),
                             ('datatype', 'Type'),
                             ('update_frequency', 'Frequence de mise a jour'),
                             ])

    # IPackageController
    def before_index(self, data_dict):
        data_dict['datatype'] = json.loads(data_dict.get('datatype', '[]'))
        return data_dict








    
