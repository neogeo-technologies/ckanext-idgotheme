import ckan.plugins as p
import ckan.plugins.toolkit as toolkit
from collections import OrderedDict
import json

from ckan.common import c
from ckantoolkit import (
    DefaultDatasetForm,
    DefaultGroupForm,
    DefaultOrganizationForm,
    get_validator,
    get_converter,
    navl_validate,
    add_template_directory,
)



from ckanext.scheming import helpers
from ckanext.scheming import loader
from ckanext.scheming.errors import SchemingException
from ckanext.scheming.validation import (
    validators_from_string, scheming_choices, scheming_required,
    scheming_multiple_choice, scheming_multiple_choice_output)
from ckanext.scheming.logic import (
    scheming_dataset_schema_list, scheming_dataset_schema_show,
    scheming_group_schema_list, scheming_group_schema_show,
    scheming_organization_schema_list, scheming_organization_schema_show,
    )
from ckanext.scheming.converters import (
        convert_from_extras_group, convert_to_json_if_date
        )

from ckanext.scheming.plugins import _SchemingMixin
from ckanext.scheming.plugins import DefaultDatasetForm
from ckan.lib.plugins import DefaultDatasetForm


# Plugin
class IdgothemePlugin(p.SingletonPlugin, _SchemingMixin):
    p.implements(p.IConfigurer)
    p.implements(p.IFacets, inherit=True)
    p.implements(p.IPackageController, inherit=True)


# Tests
    p.implements(p.ITemplateHelpers)
#    p.implements(p.IDatasetForm, inherit=True)
#    p.implements(p.IActions)
#    p.implements(p.IValidators)


    SCHEMA_OPTION = 'scheming.dataset_schemas'
    FALLBACK_OPTION = 'scheming.dataset_fallback'
    SCHEMA_TYPE_FIELD = 'dataset_type'


    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'idgotheme')

    
    # IFacets
    def dataset_facets(self, facets_dict, package_type):
        
#        facets_dict['datatype'] = 'Type de donnees'
        
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
#        return facets_dict    
    


    # IPackageController
    def before_index(self, data_dict):
        data_dict['datatype'] = json.loads(data_dict.get('datatype', '[]'))

        return data_dict








    
